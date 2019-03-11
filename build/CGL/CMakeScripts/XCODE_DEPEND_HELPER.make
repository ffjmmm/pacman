# DO NOT EDIT
# This makefile makes sure all linkable targets are
# up-to-date with anything they link to
default:
	echo "Do not invoke directly"

# Rules to remove targets that are older than anything to which they
# link.  This forces Xcode to relink the targets from scratch.  It
# does not seem to check these dependencies itself.
PostBuild.CGL.Debug:
/Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/src/Debug/libCGL_osx.a:
	/bin/rm -f /Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/src/Debug/libCGL_osx.a


PostBuild.glew.Debug:
/Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/deps/glew/Debug/libglew.a:
	/bin/rm -f /Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/deps/glew/Debug/libglew.a


PostBuild.glfw.Debug:
/Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/deps/glfw/src/Debug/libglfw3.a:
	/bin/rm -f /Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/deps/glfw/src/Debug/libglfw3.a


PostBuild.CGL.Release:
/Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/src/Release/libCGL_osx.a:
	/bin/rm -f /Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/src/Release/libCGL_osx.a


PostBuild.glew.Release:
/Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/deps/glew/Release/libglew.a:
	/bin/rm -f /Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/deps/glew/Release/libglew.a


PostBuild.glfw.Release:
/Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/deps/glfw/src/Release/libglfw3.a:
	/bin/rm -f /Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/deps/glfw/src/Release/libglfw3.a


PostBuild.CGL.MinSizeRel:
/Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/src/MinSizeRel/libCGL_osx.a:
	/bin/rm -f /Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/src/MinSizeRel/libCGL_osx.a


PostBuild.glew.MinSizeRel:
/Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/deps/glew/MinSizeRel/libglew.a:
	/bin/rm -f /Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/deps/glew/MinSizeRel/libglew.a


PostBuild.glfw.MinSizeRel:
/Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/deps/glfw/src/MinSizeRel/libglfw3.a:
	/bin/rm -f /Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/deps/glfw/src/MinSizeRel/libglfw3.a


PostBuild.CGL.RelWithDebInfo:
/Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/src/RelWithDebInfo/libCGL_osx.a:
	/bin/rm -f /Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/src/RelWithDebInfo/libCGL_osx.a


PostBuild.glew.RelWithDebInfo:
/Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/deps/glew/RelWithDebInfo/libglew.a:
	/bin/rm -f /Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/deps/glew/RelWithDebInfo/libglew.a


PostBuild.glfw.RelWithDebInfo:
/Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/deps/glfw/src/RelWithDebInfo/libglfw3.a:
	/bin/rm -f /Users/fjm/CS184/p3-1-pathtracer-ffjmmm/build/CGL/deps/glfw/src/RelWithDebInfo/libglfw3.a




# For each target create a dummy ruleso the target does not have to exist
