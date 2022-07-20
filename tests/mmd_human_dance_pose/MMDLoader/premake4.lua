newoption {
   trigger = "with-glm",
   description = "Build with GLM replacement for glu"
}

newoption {
   trigger = "with-bullet",
   description = "Build with Bullet physics"
}

newoption {
   trigger = "with-euler-camera",
   description = "Build with Euler camera"
}

sources = {
   "viewer_main.cc",
   "trackball.cpp"
   }

mmd_sources = {
   "mmd_scene.cc",
   "pmd_reader.cc",
   "vmd_reader.cc",
   "vmd_animation.cc",
   }

-- premake4.lua
solution "MMDTestSolution"
   configurations { "Release", "Debug" }

   if (os.is("windows")) then
      platforms { "x32", "x64" }
   else
      platforms { "native", "x32", "x64" }
   end

   -- A project defines one build target
   project "MMDTest"
      kind "ConsoleApp"
      language "C++"
      files { sources, mmd_sources }

      includedirs {
         "./"
      }

      -- GLM replacement for glu
      -- if _OPTIONS["with-glm"] then
      defines { 'ENABLE_GLM' } --force enable this shit
      -- end

      -- Euler camera
      if _OPTIONS["with-euler-camera"] then
         defines { 'ENABLE_GLM', 'ENABLE_EULER_CAMERA' }
      end

      -- MacOSX. Guess we use gcc.
      configuration { "macosx", "gmake" }
         defines { '_LARGEFILE_SOURCE', '_FILE_OFFSET_BITS=64' }

         links { "OpenGL.framework", "GLUT.framework" }  -- Use system's SDL

         -- Bullet physics
         if _OPTIONS["with-bullet"] then
            defines { 'ENABLE_BULLET' }
            includedirs { "/media/root/help/pyjom/externals/pybullet/bullet3/src" ,"/media/root/help/pyjom/externals/pybullet/bullet3/src/LinearMath",
            "/media/root/help/pyjom/externals/pybullet/bullet3/src/BulletDynamics"
          , "/media/root/help/pyjom/externals/pybullet/bullet3/src/BulletCollision" }
            libdirs { "/usr/local/lib/libLinearMath.so","/usr/local/lib/libBulletDynamics.so","/usr/local/lib/libBulletCollision.so"
                    } 
            links {"BulletCollision", "LinearMath" , "BulletDynamics"}
         end

      configuration { "macosx", "xcode4" }
         includedirs {
            "/Library/Frameworks/SDL.framework/Headers"
         }
         
      -- Windows specific
      configuration { "windows" }
         defines { 'NOMINMAX', '_LARGEFILE_SOURCE', '_FILE_OFFSET_BITS=64' }

      -- Linux specific
      configuration { "linux", "gmake" }
         defines { '_LARGEFILE_SOURCE', '_FILE_OFFSET_BITS=64' }

         -- Bullet physics
         -- if _OPTIONS["with-bullet"] then
         defines { 'ENABLE_BULLET' }
         includedirs { "/media/root/help/pyjom/externals/pybullet/bullet3/src","/media/root/help/pyjom/externals/pybullet/bullet3/src/LinearMath", "/media/root/help/pyjom/externals/pybullet/bullet3/src/BulletDynamics"
                  , "/media/root/help/pyjom/externals/pybullet/bullet3/src/BulletCollision" }
         libdirs { "/usr/local/lib/libLinearMath.so","/usr/local/lib/libBulletDynamics.so","/usr/local/lib/libBulletCollision.so"
                   } 
         links { "LinearMath","BulletDynamics", "BulletCollision" }
         -- end
         links { "GL", "glut" }

      configuration "Debug"
         defines { "DEBUG" } -- -DDEBUG
         flags { "Symbols" }
         targetname "mmdview_debug"

      configuration "Release"
         -- defines { "NDEBUG" } -- -NDEBUG
         flags { "Symbols", "Optimize" }
         targetname "mmdview"
