//
// TODO: Copy over 3-1 code after turning on BUILD_3-1 flag
//

#include "part1_code.h"
#include <time.h>

using namespace CGL::StaticScene;

using std::min;
using std::max;

namespace CGL {

    Spectrum PathTracer::estimate_direct_lighting_hemisphere(const Ray& r, const Intersection& isect) {
        // Estimate the lighting from this intersection coming directly from a light.
        // For this function, sample uniformly in a hemisphere.
        
        // make a coordinate system for a hit point
        // with N aligned with the Z direction.
        Matrix3x3 o2w;
        make_coord_space(o2w, isect.n);
        Matrix3x3 w2o = o2w.T();
        
        // w_out points towards the source of the ray (e.g.,
        // toward the camera if this is a primary ray)
        const Vector3D& hit_p = r.o + r.d * isect.t;
        const Vector3D& w_out = w2o * (-r.d);
        
        // This is the same number of total samples as estimate_direct_lighting_importance (outside of delta lights).
        // We keep the same number of samples for clarity of comparison.
        int num_samples = scene->lights.size() * ns_area_light;
        Spectrum L_out;
        
        // TODO (Part 3.2):
        // Write your sampling loop here
        // COMMENT OUT `normal_shading` IN `est_radiance_global_illumination` BEFORE YOU BEGIN
        for (int i = 0; i < num_samples; i ++) {
            Vector3D wi = hemisphereSampler -> get_sample();
            float pdf = 1.0 / (2 * PI);
            Vector3D wi_world = o2w * wi;
            Ray shadow_ray = Ray(EPS_D * wi_world + hit_p, wi_world);
            Intersection intersection;
            if (bvh -> intersect(shadow_ray, &intersection)) {
                Spectrum emitted_light = intersection.bsdf -> get_emission();
                L_out += (isect.bsdf -> f(w_out, wi) * abs_cos_theta(wi) * emitted_light) / pdf;
            }
        }
        L_out = L_out / num_samples;
        return L_out;
    }

    Spectrum PathTracer::estimate_direct_lighting_importance(const Ray& r, const Intersection& isect) {
        // Estimate the lighting from this intersection coming directly from a light.
        // To implement importance sampling, sample only from lights, not uniformly in a hemisphere.
        
        // make a coordinate system for a hit point
        // with N aligned with the Z direction.
        Matrix3x3 o2w;
        make_coord_space(o2w, isect.n);
        Matrix3x3 w2o = o2w.T();
        
        // w_out points towards the source of the ray (e.g.,
        // toward the camera if this is a primary ray)
        const Vector3D& hit_p = r.o + r.d * isect.t;
        const Vector3D& w_out = w2o * (-r.d);
        Spectrum L_out;
        
        // TODO (Part 3.2):
        // Here is where your code for looping over scene lights goes
        // COMMENT OUT `normal_shading` IN `est_radiance_global_illumination` BEFORE YOU BEGIN
        for (SceneLight *scene_light : scene -> lights) {
            int num_samples;
            if (scene_light -> is_delta_light())
                num_samples = 1;
            else
                num_samples = ns_area_light;
            
            Spectrum L;
            for (int i = 0; i < num_samples; i ++) {
                float pdf;
                float distToLight;
                Vector3D wi;
                Spectrum sp = scene_light -> sample_L(hit_p, &wi, &distToLight, &pdf);
                Vector3D w_in = w2o * wi;
                if (w_in.z < 0) continue;
                Ray shadow_ray = Ray(EPS_D * wi + hit_p, wi);
                shadow_ray.max_t = distToLight;
                if (!bvh -> intersect(shadow_ray)) {
                    L += (isect.bsdf -> f(w_out, w_in) * abs_cos_theta(w_in) * sp) / pdf;
                }
            }
            L = L / num_samples;
            L_out += L;
        }
        return L_out;
    }

    Spectrum PathTracer::zero_bounce_radiance(const Ray&r, const Intersection& isect) {
        
        // TODO (Part 4.2):
        // Returns the light that results from no bounces of light
        return isect.bsdf -> get_emission();
    }

    Spectrum PathTracer::one_bounce_radiance(const Ray&r, const Intersection& isect) {
        
        // TODO (Part 4.2):
        // Returns either the direct illumination by hemisphere or importance sampling
        // depending on `direct_hemisphere_sample`
        // (you implemented these functions in Part 3)
        if (direct_hemisphere_sample) {
            return estimate_direct_lighting_hemisphere(r, isect);
        }
        else {
            return estimate_direct_lighting_importance(r, isect);
        }
    }

    Spectrum PathTracer::at_least_one_bounce_radiance(const Ray&r, const Intersection& isect) {
        Matrix3x3 o2w;
        make_coord_space(o2w, isect.n);
        Matrix3x3 w2o = o2w.T();
        
        Vector3D hit_p = r.o + r.d * isect.t;
        Vector3D w_out = w2o * (-r.d);
        
        Spectrum L_out;
        if (!isect.bsdf -> is_delta())
            L_out = one_bounce_radiance(r, isect);
        /*
         if (r.depth > 0) {
         L_out = one_bounce_radiance(r, isect);
         //return L_out;
         }
         */
        // TODO (Part 4.2):
        // Here is where your code for sampling the BSDF,
        // performing Russian roulette step, and returning a recursively
        // traced ray (when applicable) goes
        Vector3D w_in;
        float pdf;
        Spectrum sp = isect.bsdf -> sample_f(w_out, &w_in, &pdf);
        
        float rrp = 0.7;
        if ((coin_flip(rrp) && r.depth < max_ray_depth) || (r.depth == 0 && max_ray_depth > 1)) {
            Vector3D wi = o2w * w_in;
            Ray shadow_ray = Ray(EPS_D * wi + hit_p, wi);
            shadow_ray.depth = r.depth + 1;
            Intersection intersection;
            if (bvh -> intersect(shadow_ray, &intersection)) {
                Spectrum L = at_least_one_bounce_radiance(shadow_ray, intersection);
                if (isect.bsdf -> is_delta()) L += zero_bounce_radiance(shadow_ray, intersection);
                if (r.depth == max_ray_depth)
                    L_out += L * sp * abs_cos_theta(w_in) / pdf;
                else
                    L_out += L * sp * abs_cos_theta(w_in) / pdf / rrp;
            }
        }
        return L_out;
    }

    Spectrum PathTracer::est_radiance_global_illumination(const Ray &r) {
        Intersection isect;
        Spectrum L_out;
        
        // You will extend this in assignment 3-2.
        // If no intersection occurs, we simply return black.
        // This changes if you implement hemispherical lighting for extra credit.
        
        if (!bvh->intersect(r, &isect))
            return L_out;
        
        // This line returns a color depending only on the normal vector
        // to the surface at the intersection point.
        // REMOVE IT when you are ready to begin Part 3.
        
        // return normal_shading(isect.n);
        
        // TODO (Part 3): Return the direct illumination.
        // return estimate_direct_lighting_hemisphere(r, isect);
        // return estimate_direct_lighting_importance(r, isect);
        
        // TODO (Part 4): Accumulate the "direct" and "indirect"
        // parts of global illumination into L_out rather than just direct
        L_out += zero_bounce_radiance(r, isect) + at_least_one_bounce_radiance(r, isect);
        
        return L_out;
    }

    Spectrum PathTracer::raytrace_pixel(size_t x, size_t y, bool useThinLens) {
        
        int num_samples = ns_aa;            // total samples to evaluate
        Vector2D origin = Vector2D(x,y);    // bottom left corner of the pixel
        
        Spectrum resSpectrum;
        double s1 = 0.0, s2 = 0.0;
        if (num_samples == 1) {
            Ray r = camera -> generate_ray(((double)x + 0.5) / (double)sampleBuffer.w, ((double)y + 0.5) / (double)sampleBuffer.h);
            resSpectrum = est_radiance_global_illumination(r);
        }
        else {
            Spectrum total = Spectrum(0, 0, 0);
            for (int i = 0; i < num_samples; i ++) {
                Vector2D sample = gridSampler -> get_sample() + origin;
                Ray r = camera -> generate_ray((double)sample.x / (double)sampleBuffer.w, (double)sample.y / (double)sampleBuffer.h);
                Spectrum sp = est_radiance_global_illumination(r);
                total += sp;
                s1 += sp.illum();
                s2 += sp.illum() * sp.illum();
                
                if ((i + 1) % samplesPerBatch == 0) {
                    double u = s1 / (double)(i + 1);
                    double I = 1.96 * sqrt((1 / (double)(i)) * (s2 - (s1 * s1) / (double)(i + 1))) / sqrt(i + 1);
                    if (I <= maxTolerance * u) {
                        sampleCountBuffer[x + y * sampleBuffer.w] = i + 1;
                        return total / (i + 1);
                    }
                }
                
            }
            resSpectrum = total / num_samples;
        }
        sampleCountBuffer[x + y * frameBuffer.w] = num_samples;
        return resSpectrum;
    }

  // Diffuse BSDF //

    Spectrum DiffuseBSDF::f(const Vector3D& wo, const Vector3D& wi) {
        
        // TODO (Part 3.1):
        // This function takes in both wo and wi and returns the evaluation of
        // the BSDF for those two directions.
        return reflectance / PI;
    }

    Spectrum DiffuseBSDF::sample_f(const Vector3D& wo, Vector3D* wi, float* pdf) {
        
        // TODO (Part 3.1):
        // This function takes in only wo and provides pointers for wi and pdf,
        // which should be assigned by this function.
        // After sampling a value for wi, it returns the evaluation of the BSDF
        // at (wo, *wi).
        *wi = sampler.get_sample(pdf);
        return DiffuseBSDF::f(wo, *wi);
    }
    
    
  // Camera //
    Ray Camera::generate_ray(double x, double y) const {
        
        // TODO (Part 1.2):
        // compute position of the input sensor sample coordinate on the
        // canonical sensor plane one unit away from the pinhole.
        // Note: hFov and vFov are in degrees.
        //
        Vector3D bottom_left = Vector3D(-tan(radians(hFov) * 0.5), -tan(radians(vFov) * 0.5), -1);
        Vector3D top_right = Vector3D(tan(radians(hFov) * 0.5), tan(radians(vFov) * 0.5), -1);
        double c_x = bottom_left.x + (top_right.x - bottom_left.x) * x;
        double c_y = bottom_left.y + (top_right.y - bottom_left.y) * y;
        double c_z = -1.0;
        Vector3D d = c2w * Vector3D(c_x, c_y, c_z);
        d.normalize();
        Vector3D origin = pos;
        return Ray(origin, d, fClip);
    }

}
