#include "bsdf.h"

#include <iostream>
#include <algorithm>
#include <utility>

using std::min;
using std::max;
using std::swap;

namespace CGL {

void make_coord_space(Matrix3x3& o2w, const Vector3D& n) {
  Vector3D z = Vector3D(n.x, n.y, n.z);
  Vector3D h = z;
  if (fabs(h.x) <= fabs(h.y) && fabs(h.x) <= fabs(h.z)) h.x = 1.0;
  else if (fabs(h.y) <= fabs(h.x) && fabs(h.y) <= fabs(h.z)) h.y = 1.0;
  else h.z = 1.0;

  z.normalize();
  Vector3D y = cross(h, z);
  y.normalize();
  Vector3D x = cross(z, y);
  x.normalize();

  o2w[0] = x;
  o2w[1] = y;
  o2w[2] = z;
}

// Mirror BSDF //

Spectrum MirrorBSDF::f(const Vector3D& wo, const Vector3D& wi) {
  return Spectrum();
}

Spectrum MirrorBSDF::sample_f(const Vector3D& wo, Vector3D* wi, float* pdf) {
  // TODO: 1.2
  // Using BSDF::reflect(), implement sample_f for a mirror surface
    *pdf = 1.0;
    reflect(wo, wi);
    return reflectance / abs_cos_theta(*wi);
}

// Microfacet BSDF //

double MicrofacetBSDF::G(const Vector3D& wo, const Vector3D& wi) {
    return 1.0 / (1.0 + Lambda(wi) + Lambda(wo));
}

double MicrofacetBSDF::D(const Vector3D& h) {
  // TODO: 2.2
  // Compute Beckmann normal distribution function (NDF) here.
  // You will need the roughness alpha.
    double sin_h = sin_theta(h);
    double cos_h = cos_theta(h);
    double tan_h = sin_h / cos_h;
    double numerator = exp(-pow(tan_h, 2) / (alpha * alpha));
    double denominator = PI * pow(alpha, 2) * pow(cos_h, 4);
    return numerator / denominator;
    //return std::pow(cos_theta(h), 100.0);;
}

Spectrum MicrofacetBSDF::F(const Vector3D& wi) {
  // TODO: 2.3
  // Compute Fresnel term for reflection on dielectric-conductor interface.
  // You will need both eta and etaK, both of which are Spectrum.
    
    double cos_w = cos_theta(wi);
    Spectrum Rs = ((eta * eta + k * k) - 2 * eta * cos_w + pow(cos_w, 2)) / ((eta * eta + k * k) + 2 * eta * cos_w + pow(cos_w, 2));
    Spectrum Rp = ((eta * eta + k * k) * pow(cos_w, 2) - 2 * eta * cos_w + 1) / ((eta * eta + k * k) * pow(cos_w, 2) + 2 * eta * cos_w + 1);
    return (Rs + Rp) / 2.0;
    // return Spectrum();
}

Spectrum MicrofacetBSDF::f(const Vector3D& wo, const Vector3D& wi) {
  // TODO: 2.1
  // Implement microfacet model here
    Vector3D n(0, 0, 1);
    if ((dot(wi, n) > 0) && (dot(wo, n) > 0)) {
        Vector3D h = wo + wi;
        h.normalize();
        return F(wi) * G(wo, wi) * D(h) / (4 * dot(n, wo) * dot(n, wi));
    }
    else
        return Spectrum();
}

Spectrum MicrofacetBSDF::sample_f(const Vector3D& wo, Vector3D* wi, float* pdf) {
  // TODO: 2.4
  // *Importance* sample Beckmann normal distribution function (NDF) here.
  // Note: You should fill in the sampled direction *wi and the corresponding *pdf,
  //       and return the sampled BRDF value.
    /*
    *wi = cosineHemisphereSampler.get_sample(pdf); //placeholder
    return MicrofacetBSDF::f(wo, *wi);
    */
    Vector2D r = sampler.get_sample();
    float theta = atan(-pow(alpha, 2) * log(1.0 - r[0]));
    float phi = 2 * PI * r[1];
    float p_theta = ((2 * sin(theta)) / (pow(alpha, 2) * pow(cos(theta), 3))) * exp(-pow(tan(theta), 2) / pow(alpha, 2));
    float p_phi = 1.0 / (2 * PI);
    float p_h = p_theta * p_phi / sin(theta);
    
    float h_x = sin(theta) * cos(phi);
    float h_y = sin(theta) * sin(phi);
    float h_z = cos(theta);
    Vector3D h(h_x, h_y, h_z);
    *wi = -wo + 2 * dot(wo, h) * h;
    *pdf = p_h / (4 * dot(*wi, h));
    return f(wo, *wi);
    // return Spectrum();
}

// Refraction BSDF //

Spectrum RefractionBSDF::f(const Vector3D& wo, const Vector3D& wi) {
  return Spectrum();
}

Spectrum RefractionBSDF::sample_f(const Vector3D& wo, Vector3D* wi, float* pdf) {
  return Spectrum();
}

// Glass BSDF //

Spectrum GlassBSDF::f(const Vector3D& wo, const Vector3D& wi) {
  return Spectrum();
}

Spectrum GlassBSDF::sample_f(const Vector3D& wo, Vector3D* wi, float* pdf) {

  // TODO: 1.4
  // Compute Fresnel coefficient and either reflect or refract based on it.
    if (!refract(wo, wi, ior)) {
        *pdf = 1.0;
        reflect(wo, wi);
        return reflectance / abs_cos_theta(*wi);
    }
    else {
        float R0 = pow((1 - ior) / (1 + ior), 2);
        float R_theta = R0 + (1 - R0) * pow((1 - abs_cos_theta(wo)), 5);
        if (coin_flip(R_theta)) {
            reflect(wo, wi);
            *pdf = R_theta;
            return R_theta * reflectance / abs_cos_theta(*wi);
        }
        else {
            refract(wo, wi, ior);
            *pdf = 1.0 - R_theta;
            float eta = ior;
            if (wo.z >= 0) eta = 1.0 / ior;
            return (1.0 - R_theta) * transmittance / abs_cos_theta(*wi) / (eta * eta);
        }
    }

  return Spectrum();
}

void BSDF::reflect(const Vector3D& wo, Vector3D* wi) {

  // TODO: 1.1
  // Implement reflection of wo about normal (0,0,1) and store result in wi.
    *wi = Vector3D(-wo[0], -wo[1], wo[2]);
}

bool BSDF::refract(const Vector3D& wo, Vector3D* wi, float ior) {

  // TODO: 1.3
  // Use Snell's Law to refract wo surface and store result ray in wi.
  // Return false if refraction does not occur due to total internal reflection
  // and true otherwise. When dot(wo,n) is positive, then wo corresponds to a
  // ray entering the surface through vacuum.
    float eta = ior;
    if (wo.z >= 0)
        // entering
        eta = 1.0 / ior;
    
    float z = 1.0 - eta * eta * (1.0 - wo.z * wo.z);
    if (z < 0) return false;
    float wi_z = sqrt(z);
    if (wo.z >= 0)
        wi_z = -wi_z;
    float wi_x = -eta * wo.x;
    float wi_y = -eta * wo.y;
    *wi = Vector3D(wi_x, wi_y, wi_z);
    return true;
}

// Emission BSDF //

Spectrum EmissionBSDF::f(const Vector3D& wo, const Vector3D& wi) {
  return Spectrum();
}

Spectrum EmissionBSDF::sample_f(const Vector3D& wo, Vector3D* wi, float* pdf) {
  *pdf = 1.0 / PI;
  *wi  = sampler.get_sample(pdf);
  return Spectrum();
}

} // namespace CGL
