//
// This file is auto-generated. Please don't modify it!
//

#undef LOG_TAG

#include "opencv2/opencv_modules.hpp"
#ifdef HAVE_OPENCV_TRACKING

#include <string>

#include "opencv2/tracking.hpp"

#include "/media/root/help1/pyjom/externals/opencv/opencv-4.x/../opencv_contrib-4.x/modules/tracking/include/opencv2/tracking.hpp"
#include "/media/root/help1/pyjom/externals/opencv/opencv-4.x/../opencv_contrib-4.x/modules/tracking/include/opencv2/tracking/feature.hpp"
#include "/media/root/help1/pyjom/externals/opencv/opencv-4.x/../opencv_contrib-4.x/modules/tracking/include/opencv2/tracking/tracking_internals.hpp"
#include "/media/root/help1/pyjom/externals/opencv/opencv-4.x/../opencv_contrib-4.x/modules/tracking/include/opencv2/tracking/tracking_legacy.hpp"

#define LOG_TAG "org.opencv.tracking"
#include "common.h"

using namespace cv;

/// throw java exception
#undef throwJavaException
#define throwJavaException throwJavaException_tracking
static void throwJavaException(JNIEnv *env, const std::exception *e, const char *method) {
  std::string what = "unknown exception";
  jclass je = 0;

  if(e) {
    std::string exception_type = "std::exception";

    if(dynamic_cast<const cv::Exception*>(e)) {
      exception_type = "cv::Exception";
      je = env->FindClass("org/opencv/core/CvException");
    }

    what = exception_type + ": " + e->what();
  }

  if(!je) je = env->FindClass("java/lang/Exception");
  env->ThrowNew(je, what.c_str());

  LOGE("%s caught %s", method, what.c_str());
  (void)method;        // avoid "unused" warning
}

extern "C" {


//
// static Ptr_TrackerCSRT cv::TrackerCSRT::create(TrackerCSRT_Params parameters = TrackerCSRT::Params())
//

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_TrackerCSRT_create_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_TrackerCSRT_create_10
  (JNIEnv* env, jclass , jlong parameters_nativeObj)
{
    
    static const char method_name[] = "tracking::create_10()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<cv::TrackerCSRT> Ptr_TrackerCSRT;
        Ptr_TrackerCSRT _retval_ = cv::TrackerCSRT::create( (*(cv::TrackerCSRT::Params*)parameters_nativeObj) );
        return (jlong)(new Ptr_TrackerCSRT(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



JNIEXPORT jlong JNICALL Java_org_opencv_tracking_TrackerCSRT_create_11 (JNIEnv*, jclass);

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_TrackerCSRT_create_11
  (JNIEnv* env, jclass )
{
    
    static const char method_name[] = "tracking::create_11()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<cv::TrackerCSRT> Ptr_TrackerCSRT;
        Ptr_TrackerCSRT _retval_ = cv::TrackerCSRT::create();
        return (jlong)(new Ptr_TrackerCSRT(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  void cv::TrackerCSRT::setInitialMask(Mat mask)
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_setInitialMask_10 (JNIEnv*, jclass, jlong, jlong);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_setInitialMask_10
  (JNIEnv* env, jclass , jlong self, jlong mask_nativeObj)
{
    
    static const char method_name[] = "tracking::setInitialMask_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::TrackerCSRT>* me = (Ptr<cv::TrackerCSRT>*) self; //TODO: check for NULL
        Mat& mask = *((Mat*)mask_nativeObj);
        (*me)->setInitialMask( mask );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  native support for java finalize()
//  static void Ptr<cv::TrackerCSRT>::delete( __int64 self )
//
JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_delete(JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_delete
  (JNIEnv*, jclass, jlong self)
{
    delete (Ptr<cv::TrackerCSRT>*) self;
}


//
//   cv::TrackerCSRT::Params::Params()
//

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_TrackerCSRT_1Params_10 (JNIEnv*, jclass);

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_TrackerCSRT_1Params_10
  (JNIEnv* env, jclass )
{
    
    static const char method_name[] = "tracking::TrackerCSRT_1Params_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* _retval_ = new cv::TrackerCSRT::Params();
        return (jlong) _retval_;
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// bool TrackerCSRT_Params::use_hog
//

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1use_1hog_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1use_1hog_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1use_1hog_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->use_hog;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::use_hog
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1use_1hog_10 (JNIEnv*, jclass, jlong, jboolean);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1use_1hog_10
  (JNIEnv* env, jclass , jlong self, jboolean use_hog)
{
    
    static const char method_name[] = "tracking::set_1use_1hog_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->use_hog = ( (bool)use_hog );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// bool TrackerCSRT_Params::use_color_names
//

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1use_1color_1names_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1use_1color_1names_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1use_1color_1names_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->use_color_names;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::use_color_names
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1use_1color_1names_10 (JNIEnv*, jclass, jlong, jboolean);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1use_1color_1names_10
  (JNIEnv* env, jclass , jlong self, jboolean use_color_names)
{
    
    static const char method_name[] = "tracking::set_1use_1color_1names_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->use_color_names = ( (bool)use_color_names );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// bool TrackerCSRT_Params::use_gray
//

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1use_1gray_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1use_1gray_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1use_1gray_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->use_gray;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::use_gray
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1use_1gray_10 (JNIEnv*, jclass, jlong, jboolean);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1use_1gray_10
  (JNIEnv* env, jclass , jlong self, jboolean use_gray)
{
    
    static const char method_name[] = "tracking::set_1use_1gray_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->use_gray = ( (bool)use_gray );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// bool TrackerCSRT_Params::use_rgb
//

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1use_1rgb_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1use_1rgb_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1use_1rgb_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->use_rgb;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::use_rgb
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1use_1rgb_10 (JNIEnv*, jclass, jlong, jboolean);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1use_1rgb_10
  (JNIEnv* env, jclass , jlong self, jboolean use_rgb)
{
    
    static const char method_name[] = "tracking::set_1use_1rgb_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->use_rgb = ( (bool)use_rgb );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// bool TrackerCSRT_Params::use_channel_weights
//

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1use_1channel_1weights_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1use_1channel_1weights_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1use_1channel_1weights_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->use_channel_weights;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::use_channel_weights
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1use_1channel_1weights_10 (JNIEnv*, jclass, jlong, jboolean);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1use_1channel_1weights_10
  (JNIEnv* env, jclass , jlong self, jboolean use_channel_weights)
{
    
    static const char method_name[] = "tracking::set_1use_1channel_1weights_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->use_channel_weights = ( (bool)use_channel_weights );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// bool TrackerCSRT_Params::use_segmentation
//

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1use_1segmentation_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1use_1segmentation_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1use_1segmentation_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->use_segmentation;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::use_segmentation
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1use_1segmentation_10 (JNIEnv*, jclass, jlong, jboolean);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1use_1segmentation_10
  (JNIEnv* env, jclass , jlong self, jboolean use_segmentation)
{
    
    static const char method_name[] = "tracking::set_1use_1segmentation_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->use_segmentation = ( (bool)use_segmentation );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// string TrackerCSRT_Params::window_function
//

JNIEXPORT jstring JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1window_1function_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jstring JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1window_1function_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1window_1function_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        std::string _retval_ = me->window_function;//();
        return env->NewStringUTF(_retval_.c_str());
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return env->NewStringUTF("");
}



//
// void TrackerCSRT_Params::window_function
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1window_1function_10 (JNIEnv*, jclass, jlong, jstring);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1window_1function_10
  (JNIEnv* env, jclass , jlong self, jstring window_function)
{
    
    static const char method_name[] = "tracking::set_1window_1function_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        const char* utf_window_function = env->GetStringUTFChars(window_function, 0); std::string n_window_function( utf_window_function ? utf_window_function : "" ); env->ReleaseStringUTFChars(window_function, utf_window_function);
        me->window_function = ( n_window_function );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerCSRT_Params::kaiser_alpha
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1kaiser_1alpha_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1kaiser_1alpha_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1kaiser_1alpha_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->kaiser_alpha;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::kaiser_alpha
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1kaiser_1alpha_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1kaiser_1alpha_10
  (JNIEnv* env, jclass , jlong self, jfloat kaiser_alpha)
{
    
    static const char method_name[] = "tracking::set_1kaiser_1alpha_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->kaiser_alpha = ( (float)kaiser_alpha );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerCSRT_Params::cheb_attenuation
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1cheb_1attenuation_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1cheb_1attenuation_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1cheb_1attenuation_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->cheb_attenuation;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::cheb_attenuation
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1cheb_1attenuation_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1cheb_1attenuation_10
  (JNIEnv* env, jclass , jlong self, jfloat cheb_attenuation)
{
    
    static const char method_name[] = "tracking::set_1cheb_1attenuation_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->cheb_attenuation = ( (float)cheb_attenuation );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerCSRT_Params::template_size
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1template_1size_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1template_1size_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1template_1size_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->template_size;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::template_size
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1template_1size_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1template_1size_10
  (JNIEnv* env, jclass , jlong self, jfloat template_size)
{
    
    static const char method_name[] = "tracking::set_1template_1size_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->template_size = ( (float)template_size );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerCSRT_Params::gsl_sigma
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1gsl_1sigma_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1gsl_1sigma_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1gsl_1sigma_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->gsl_sigma;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::gsl_sigma
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1gsl_1sigma_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1gsl_1sigma_10
  (JNIEnv* env, jclass , jlong self, jfloat gsl_sigma)
{
    
    static const char method_name[] = "tracking::set_1gsl_1sigma_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->gsl_sigma = ( (float)gsl_sigma );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerCSRT_Params::hog_orientations
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1hog_1orientations_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1hog_1orientations_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1hog_1orientations_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->hog_orientations;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::hog_orientations
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1hog_1orientations_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1hog_1orientations_10
  (JNIEnv* env, jclass , jlong self, jfloat hog_orientations)
{
    
    static const char method_name[] = "tracking::set_1hog_1orientations_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->hog_orientations = ( (float)hog_orientations );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerCSRT_Params::hog_clip
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1hog_1clip_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1hog_1clip_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1hog_1clip_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->hog_clip;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::hog_clip
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1hog_1clip_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1hog_1clip_10
  (JNIEnv* env, jclass , jlong self, jfloat hog_clip)
{
    
    static const char method_name[] = "tracking::set_1hog_1clip_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->hog_clip = ( (float)hog_clip );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerCSRT_Params::padding
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1padding_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1padding_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1padding_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->padding;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::padding
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1padding_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1padding_10
  (JNIEnv* env, jclass , jlong self, jfloat padding)
{
    
    static const char method_name[] = "tracking::set_1padding_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->padding = ( (float)padding );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerCSRT_Params::filter_lr
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1filter_1lr_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1filter_1lr_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1filter_1lr_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->filter_lr;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::filter_lr
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1filter_1lr_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1filter_1lr_10
  (JNIEnv* env, jclass , jlong self, jfloat filter_lr)
{
    
    static const char method_name[] = "tracking::set_1filter_1lr_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->filter_lr = ( (float)filter_lr );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerCSRT_Params::weights_lr
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1weights_1lr_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1weights_1lr_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1weights_1lr_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->weights_lr;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::weights_lr
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1weights_1lr_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1weights_1lr_10
  (JNIEnv* env, jclass , jlong self, jfloat weights_lr)
{
    
    static const char method_name[] = "tracking::set_1weights_1lr_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->weights_lr = ( (float)weights_lr );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// int TrackerCSRT_Params::num_hog_channels_used
//

JNIEXPORT jint JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1num_1hog_1channels_1used_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jint JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1num_1hog_1channels_1used_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1num_1hog_1channels_1used_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->num_hog_channels_used;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::num_hog_channels_used
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1num_1hog_1channels_1used_10 (JNIEnv*, jclass, jlong, jint);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1num_1hog_1channels_1used_10
  (JNIEnv* env, jclass , jlong self, jint num_hog_channels_used)
{
    
    static const char method_name[] = "tracking::set_1num_1hog_1channels_1used_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->num_hog_channels_used = ( (int)num_hog_channels_used );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// int TrackerCSRT_Params::admm_iterations
//

JNIEXPORT jint JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1admm_1iterations_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jint JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1admm_1iterations_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1admm_1iterations_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->admm_iterations;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::admm_iterations
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1admm_1iterations_10 (JNIEnv*, jclass, jlong, jint);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1admm_1iterations_10
  (JNIEnv* env, jclass , jlong self, jint admm_iterations)
{
    
    static const char method_name[] = "tracking::set_1admm_1iterations_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->admm_iterations = ( (int)admm_iterations );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// int TrackerCSRT_Params::histogram_bins
//

JNIEXPORT jint JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1histogram_1bins_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jint JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1histogram_1bins_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1histogram_1bins_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->histogram_bins;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::histogram_bins
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1histogram_1bins_10 (JNIEnv*, jclass, jlong, jint);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1histogram_1bins_10
  (JNIEnv* env, jclass , jlong self, jint histogram_bins)
{
    
    static const char method_name[] = "tracking::set_1histogram_1bins_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->histogram_bins = ( (int)histogram_bins );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerCSRT_Params::histogram_lr
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1histogram_1lr_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1histogram_1lr_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1histogram_1lr_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->histogram_lr;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::histogram_lr
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1histogram_1lr_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1histogram_1lr_10
  (JNIEnv* env, jclass , jlong self, jfloat histogram_lr)
{
    
    static const char method_name[] = "tracking::set_1histogram_1lr_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->histogram_lr = ( (float)histogram_lr );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// int TrackerCSRT_Params::background_ratio
//

JNIEXPORT jint JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1background_1ratio_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jint JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1background_1ratio_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1background_1ratio_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->background_ratio;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::background_ratio
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1background_1ratio_10 (JNIEnv*, jclass, jlong, jint);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1background_1ratio_10
  (JNIEnv* env, jclass , jlong self, jint background_ratio)
{
    
    static const char method_name[] = "tracking::set_1background_1ratio_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->background_ratio = ( (int)background_ratio );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// int TrackerCSRT_Params::number_of_scales
//

JNIEXPORT jint JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1number_1of_1scales_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jint JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1number_1of_1scales_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1number_1of_1scales_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->number_of_scales;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::number_of_scales
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1number_1of_1scales_10 (JNIEnv*, jclass, jlong, jint);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1number_1of_1scales_10
  (JNIEnv* env, jclass , jlong self, jint number_of_scales)
{
    
    static const char method_name[] = "tracking::set_1number_1of_1scales_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->number_of_scales = ( (int)number_of_scales );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerCSRT_Params::scale_sigma_factor
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1scale_1sigma_1factor_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1scale_1sigma_1factor_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1scale_1sigma_1factor_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->scale_sigma_factor;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::scale_sigma_factor
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1scale_1sigma_1factor_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1scale_1sigma_1factor_10
  (JNIEnv* env, jclass , jlong self, jfloat scale_sigma_factor)
{
    
    static const char method_name[] = "tracking::set_1scale_1sigma_1factor_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->scale_sigma_factor = ( (float)scale_sigma_factor );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerCSRT_Params::scale_model_max_area
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1scale_1model_1max_1area_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1scale_1model_1max_1area_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1scale_1model_1max_1area_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->scale_model_max_area;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::scale_model_max_area
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1scale_1model_1max_1area_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1scale_1model_1max_1area_10
  (JNIEnv* env, jclass , jlong self, jfloat scale_model_max_area)
{
    
    static const char method_name[] = "tracking::set_1scale_1model_1max_1area_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->scale_model_max_area = ( (float)scale_model_max_area );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerCSRT_Params::scale_lr
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1scale_1lr_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1scale_1lr_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1scale_1lr_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->scale_lr;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::scale_lr
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1scale_1lr_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1scale_1lr_10
  (JNIEnv* env, jclass , jlong self, jfloat scale_lr)
{
    
    static const char method_name[] = "tracking::set_1scale_1lr_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->scale_lr = ( (float)scale_lr );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerCSRT_Params::scale_step
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1scale_1step_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1scale_1step_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1scale_1step_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->scale_step;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::scale_step
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1scale_1step_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1scale_1step_10
  (JNIEnv* env, jclass , jlong self, jfloat scale_step)
{
    
    static const char method_name[] = "tracking::set_1scale_1step_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->scale_step = ( (float)scale_step );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerCSRT_Params::psr_threshold
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1psr_1threshold_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_get_1psr_1threshold_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1psr_1threshold_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        return me->psr_threshold;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerCSRT_Params::psr_threshold
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1psr_1threshold_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_set_1psr_1threshold_10
  (JNIEnv* env, jclass , jlong self, jfloat psr_threshold)
{
    
    static const char method_name[] = "tracking::set_1psr_1threshold_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerCSRT::Params* me = (cv::TrackerCSRT::Params*) self; //TODO: check for NULL
        me->psr_threshold = ( (float)psr_threshold );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  native support for java finalize()
//  static void cv::TrackerCSRT::Params::delete( __int64 self )
//
JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_delete(JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerCSRT_1Params_delete
  (JNIEnv*, jclass, jlong self)
{
    delete (cv::TrackerCSRT::Params*) self;
}


//
// static Ptr_TrackerKCF cv::TrackerKCF::create(TrackerKCF_Params parameters = TrackerKCF::Params())
//

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_TrackerKCF_create_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_TrackerKCF_create_10
  (JNIEnv* env, jclass , jlong parameters_nativeObj)
{
    
    static const char method_name[] = "tracking::create_10()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<cv::TrackerKCF> Ptr_TrackerKCF;
        Ptr_TrackerKCF _retval_ = cv::TrackerKCF::create( (*(cv::TrackerKCF::Params*)parameters_nativeObj) );
        return (jlong)(new Ptr_TrackerKCF(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



JNIEXPORT jlong JNICALL Java_org_opencv_tracking_TrackerKCF_create_11 (JNIEnv*, jclass);

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_TrackerKCF_create_11
  (JNIEnv* env, jclass )
{
    
    static const char method_name[] = "tracking::create_11()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<cv::TrackerKCF> Ptr_TrackerKCF;
        Ptr_TrackerKCF _retval_ = cv::TrackerKCF::create();
        return (jlong)(new Ptr_TrackerKCF(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  native support for java finalize()
//  static void Ptr<cv::TrackerKCF>::delete( __int64 self )
//
JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_delete(JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_delete
  (JNIEnv*, jclass, jlong self)
{
    delete (Ptr<cv::TrackerKCF>*) self;
}


//
//   cv::TrackerKCF::Params::Params()
//

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_TrackerKCF_1Params_10 (JNIEnv*, jclass);

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_TrackerKCF_1Params_10
  (JNIEnv* env, jclass )
{
    
    static const char method_name[] = "tracking::TrackerKCF_1Params_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* _retval_ = new cv::TrackerKCF::Params();
        return (jlong) _retval_;
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// float TrackerKCF_Params::detect_thresh
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1detect_1thresh_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1detect_1thresh_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1detect_1thresh_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        return me->detect_thresh;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerKCF_Params::detect_thresh
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1detect_1thresh_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1detect_1thresh_10
  (JNIEnv* env, jclass , jlong self, jfloat detect_thresh)
{
    
    static const char method_name[] = "tracking::set_1detect_1thresh_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        me->detect_thresh = ( (float)detect_thresh );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerKCF_Params::sigma
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1sigma_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1sigma_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1sigma_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        return me->sigma;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerKCF_Params::sigma
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1sigma_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1sigma_10
  (JNIEnv* env, jclass , jlong self, jfloat sigma)
{
    
    static const char method_name[] = "tracking::set_1sigma_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        me->sigma = ( (float)sigma );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerKCF_Params::lambda
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1lambda_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1lambda_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1lambda_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        return me->lambda;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerKCF_Params::lambda
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1lambda_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1lambda_10
  (JNIEnv* env, jclass , jlong self, jfloat lambda)
{
    
    static const char method_name[] = "tracking::set_1lambda_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        me->lambda = ( (float)lambda );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerKCF_Params::interp_factor
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1interp_1factor_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1interp_1factor_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1interp_1factor_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        return me->interp_factor;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerKCF_Params::interp_factor
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1interp_1factor_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1interp_1factor_10
  (JNIEnv* env, jclass , jlong self, jfloat interp_factor)
{
    
    static const char method_name[] = "tracking::set_1interp_1factor_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        me->interp_factor = ( (float)interp_factor );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerKCF_Params::output_sigma_factor
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1output_1sigma_1factor_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1output_1sigma_1factor_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1output_1sigma_1factor_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        return me->output_sigma_factor;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerKCF_Params::output_sigma_factor
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1output_1sigma_1factor_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1output_1sigma_1factor_10
  (JNIEnv* env, jclass , jlong self, jfloat output_sigma_factor)
{
    
    static const char method_name[] = "tracking::set_1output_1sigma_1factor_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        me->output_sigma_factor = ( (float)output_sigma_factor );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// float TrackerKCF_Params::pca_learning_rate
//

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1pca_1learning_1rate_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jfloat JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1pca_1learning_1rate_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1pca_1learning_1rate_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        return me->pca_learning_rate;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerKCF_Params::pca_learning_rate
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1pca_1learning_1rate_10 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1pca_1learning_1rate_10
  (JNIEnv* env, jclass , jlong self, jfloat pca_learning_rate)
{
    
    static const char method_name[] = "tracking::set_1pca_1learning_1rate_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        me->pca_learning_rate = ( (float)pca_learning_rate );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// bool TrackerKCF_Params::resize
//

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1resize_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1resize_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1resize_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        return me->resize;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerKCF_Params::resize
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1resize_10 (JNIEnv*, jclass, jlong, jboolean);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1resize_10
  (JNIEnv* env, jclass , jlong self, jboolean resize)
{
    
    static const char method_name[] = "tracking::set_1resize_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        me->resize = ( (bool)resize );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// bool TrackerKCF_Params::split_coeff
//

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1split_1coeff_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1split_1coeff_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1split_1coeff_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        return me->split_coeff;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerKCF_Params::split_coeff
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1split_1coeff_10 (JNIEnv*, jclass, jlong, jboolean);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1split_1coeff_10
  (JNIEnv* env, jclass , jlong self, jboolean split_coeff)
{
    
    static const char method_name[] = "tracking::set_1split_1coeff_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        me->split_coeff = ( (bool)split_coeff );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// bool TrackerKCF_Params::wrap_kernel
//

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1wrap_1kernel_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1wrap_1kernel_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1wrap_1kernel_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        return me->wrap_kernel;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerKCF_Params::wrap_kernel
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1wrap_1kernel_10 (JNIEnv*, jclass, jlong, jboolean);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1wrap_1kernel_10
  (JNIEnv* env, jclass , jlong self, jboolean wrap_kernel)
{
    
    static const char method_name[] = "tracking::set_1wrap_1kernel_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        me->wrap_kernel = ( (bool)wrap_kernel );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// bool TrackerKCF_Params::compress_feature
//

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1compress_1feature_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1compress_1feature_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1compress_1feature_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        return me->compress_feature;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerKCF_Params::compress_feature
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1compress_1feature_10 (JNIEnv*, jclass, jlong, jboolean);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1compress_1feature_10
  (JNIEnv* env, jclass , jlong self, jboolean compress_feature)
{
    
    static const char method_name[] = "tracking::set_1compress_1feature_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        me->compress_feature = ( (bool)compress_feature );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// int TrackerKCF_Params::max_patch_size
//

JNIEXPORT jint JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1max_1patch_1size_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jint JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1max_1patch_1size_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1max_1patch_1size_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        return me->max_patch_size;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerKCF_Params::max_patch_size
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1max_1patch_1size_10 (JNIEnv*, jclass, jlong, jint);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1max_1patch_1size_10
  (JNIEnv* env, jclass , jlong self, jint max_patch_size)
{
    
    static const char method_name[] = "tracking::set_1max_1patch_1size_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        me->max_patch_size = ( (int)max_patch_size );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// int TrackerKCF_Params::compressed_size
//

JNIEXPORT jint JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1compressed_1size_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jint JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1compressed_1size_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1compressed_1size_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        return me->compressed_size;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerKCF_Params::compressed_size
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1compressed_1size_10 (JNIEnv*, jclass, jlong, jint);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1compressed_1size_10
  (JNIEnv* env, jclass , jlong self, jint compressed_size)
{
    
    static const char method_name[] = "tracking::set_1compressed_1size_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        me->compressed_size = ( (int)compressed_size );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// int TrackerKCF_Params::desc_pca
//

JNIEXPORT jint JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1desc_1pca_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jint JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1desc_1pca_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1desc_1pca_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        return me->desc_pca;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerKCF_Params::desc_pca
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1desc_1pca_10 (JNIEnv*, jclass, jlong, jint);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1desc_1pca_10
  (JNIEnv* env, jclass , jlong self, jint desc_pca)
{
    
    static const char method_name[] = "tracking::set_1desc_1pca_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        me->desc_pca = ( (int)desc_pca );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// int TrackerKCF_Params::desc_npca
//

JNIEXPORT jint JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1desc_1npca_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jint JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_get_1desc_1npca_10
  (JNIEnv* env, jclass , jlong self)
{
    
    static const char method_name[] = "tracking::get_1desc_1npca_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        return me->desc_npca;//();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// void TrackerKCF_Params::desc_npca
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1desc_1npca_10 (JNIEnv*, jclass, jlong, jint);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_set_1desc_1npca_10
  (JNIEnv* env, jclass , jlong self, jint desc_npca)
{
    
    static const char method_name[] = "tracking::set_1desc_1npca_10()";
    try {
        LOGD("%s", method_name);
        cv::TrackerKCF::Params* me = (cv::TrackerKCF::Params*) self; //TODO: check for NULL
        me->desc_npca = ( (int)desc_npca );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  native support for java finalize()
//  static void cv::TrackerKCF::Params::delete( __int64 self )
//
JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_delete(JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_tracking_TrackerKCF_1Params_delete
  (JNIEnv*, jclass, jlong self)
{
    delete (cv::TrackerKCF::Params*) self;
}


//
//  Ptr_Tracker cv::legacy::upgradeTrackingAPI(Ptr_legacy_Tracker legacy_tracker)
//

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_Tracking_legacy_1upgradeTrackingAPI_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_Tracking_legacy_1upgradeTrackingAPI_10
  (JNIEnv* env, jclass , jlong legacy_tracker_nativeObj)
{
    
    static const char method_name[] = "tracking::legacy_1upgradeTrackingAPI_10()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<Tracker> Ptr_Tracker;
        Ptr_Tracker _retval_ = cv::legacy::upgradeTrackingAPI( *((Ptr<cv::legacy::Tracker>*)legacy_tracker_nativeObj) );
        return (jlong)(new Ptr_Tracker(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//   cv::legacy::MultiTracker::MultiTracker()
//

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_legacy_1MultiTracker_legacy_1MultiTracker_10 (JNIEnv*, jclass);

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_legacy_1MultiTracker_legacy_1MultiTracker_10
  (JNIEnv* env, jclass )
{
    using namespace cv::legacy;
    static const char method_name[] = "tracking::legacy_1MultiTracker_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::legacy::MultiTracker> _retval_ = makePtr<cv::legacy::MultiTracker>();
        return (jlong)(new Ptr<cv::legacy::MultiTracker>(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  bool cv::legacy::MultiTracker::add(Ptr_legacy_Tracker newTracker, Mat image, Rect2d boundingBox)
//

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_legacy_1MultiTracker_add_10 (JNIEnv*, jclass, jlong, jlong, jlong, jdouble, jdouble, jdouble, jdouble);

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_legacy_1MultiTracker_add_10
  (JNIEnv* env, jclass , jlong self, jlong newTracker_nativeObj, jlong image_nativeObj, jdouble boundingBox_x, jdouble boundingBox_y, jdouble boundingBox_width, jdouble boundingBox_height)
{
    using namespace cv::legacy;
    static const char method_name[] = "tracking::add_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::legacy::MultiTracker>* me = (Ptr<cv::legacy::MultiTracker>*) self; //TODO: check for NULL
        Mat& image = *((Mat*)image_nativeObj);
        Rect boundingBox(boundingBox_x, boundingBox_y, boundingBox_width, boundingBox_height);
        return (*me)->add( *((Ptr<cv::legacy::Tracker>*)newTracker_nativeObj), image, boundingBox );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  bool cv::legacy::MultiTracker::update(Mat image, vector_Rect2d& boundingBox)
//

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_legacy_1MultiTracker_update_10 (JNIEnv*, jclass, jlong, jlong, jlong);

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_legacy_1MultiTracker_update_10
  (JNIEnv* env, jclass , jlong self, jlong image_nativeObj, jlong boundingBox_mat_nativeObj)
{
    using namespace cv::legacy;
    static const char method_name[] = "tracking::update_10()";
    try {
        LOGD("%s", method_name);
        std::vector<Rect2d> boundingBox;
        Mat& boundingBox_mat = *((Mat*)boundingBox_mat_nativeObj);
        Ptr<cv::legacy::MultiTracker>* me = (Ptr<cv::legacy::MultiTracker>*) self; //TODO: check for NULL
        Mat& image = *((Mat*)image_nativeObj);
        bool _retval_ = (*me)->update( image, boundingBox );
        vector_Rect2d_to_Mat( boundingBox, boundingBox_mat );
        return _retval_;
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  vector_Rect2d cv::legacy::MultiTracker::getObjects()
//

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_legacy_1MultiTracker_getObjects_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_legacy_1MultiTracker_getObjects_10
  (JNIEnv* env, jclass , jlong self)
{
    using namespace cv::legacy;
    static const char method_name[] = "tracking::getObjects_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::legacy::MultiTracker>* me = (Ptr<cv::legacy::MultiTracker>*) self; //TODO: check for NULL
        std::vector<Rect2d> _ret_val_vector_ = (*me)->getObjects();
        Mat* _retval_ = new Mat();
        vector_Rect2d_to_Mat(_ret_val_vector_, *_retval_);
        return (jlong) _retval_;
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  native support for java finalize()
//  static void Ptr<cv::legacy::MultiTracker>::delete( __int64 self )
//
JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1MultiTracker_delete(JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1MultiTracker_delete
  (JNIEnv*, jclass, jlong self)
{
    delete (Ptr<cv::legacy::MultiTracker>*) self;
}


//
//  bool cv::legacy::Tracker::init(Mat image, Rect2d boundingBox)
//

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_legacy_1Tracker_init_10 (JNIEnv*, jclass, jlong, jlong, jdouble, jdouble, jdouble, jdouble);

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_legacy_1Tracker_init_10
  (JNIEnv* env, jclass , jlong self, jlong image_nativeObj, jdouble boundingBox_x, jdouble boundingBox_y, jdouble boundingBox_width, jdouble boundingBox_height)
{
    using namespace cv::legacy;
    static const char method_name[] = "tracking::init_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::legacy::Tracker>* me = (Ptr<cv::legacy::Tracker>*) self; //TODO: check for NULL
        Mat& image = *((Mat*)image_nativeObj);
        Rect boundingBox(boundingBox_x, boundingBox_y, boundingBox_width, boundingBox_height);
        return (*me)->init( image, boundingBox );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  bool cv::legacy::Tracker::update(Mat image, Rect2d& boundingBox)
//

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_legacy_1Tracker_update_10 (JNIEnv*, jclass, jlong, jlong, jdoubleArray);

JNIEXPORT jboolean JNICALL Java_org_opencv_tracking_legacy_1Tracker_update_10
  (JNIEnv* env, jclass , jlong self, jlong image_nativeObj, jdoubleArray boundingBox_out)
{
    using namespace cv::legacy;
    static const char method_name[] = "tracking::update_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::legacy::Tracker>* me = (Ptr<cv::legacy::Tracker>*) self; //TODO: check for NULL
        Mat& image = *((Mat*)image_nativeObj);
        Rect2d boundingBox;
        bool _retval_ = (*me)->update( image, boundingBox );
        jdouble tmp_boundingBox[4] = {(jdouble)boundingBox.x, (jdouble)boundingBox.y, (jdouble)boundingBox.width, (jdouble)boundingBox.height}; env->SetDoubleArrayRegion(boundingBox_out, 0, 4, tmp_boundingBox);
        return _retval_;
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  native support for java finalize()
//  static void Ptr<cv::legacy::Tracker>::delete( __int64 self )
//
JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1Tracker_delete(JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1Tracker_delete
  (JNIEnv*, jclass, jlong self)
{
    delete (Ptr<cv::legacy::Tracker>*) self;
}


//
// static Ptr_legacy_TrackerBoosting cv::legacy::TrackerBoosting::create()
//

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_legacy_1TrackerBoosting_create_10 (JNIEnv*, jclass);

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_legacy_1TrackerBoosting_create_10
  (JNIEnv* env, jclass )
{
    using namespace cv::legacy;
    static const char method_name[] = "tracking::create_10()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<cv::legacy::TrackerBoosting> Ptr_legacy_TrackerBoosting;
        Ptr_legacy_TrackerBoosting _retval_ = cv::legacy::TrackerBoosting::create();
        return (jlong)(new Ptr_legacy_TrackerBoosting(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  native support for java finalize()
//  static void Ptr<cv::legacy::TrackerBoosting>::delete( __int64 self )
//
JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1TrackerBoosting_delete(JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1TrackerBoosting_delete
  (JNIEnv*, jclass, jlong self)
{
    delete (Ptr<cv::legacy::TrackerBoosting>*) self;
}


//
// static Ptr_legacy_TrackerCSRT cv::legacy::TrackerCSRT::create()
//

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_legacy_1TrackerCSRT_create_10 (JNIEnv*, jclass);

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_legacy_1TrackerCSRT_create_10
  (JNIEnv* env, jclass )
{
    using namespace cv::legacy;
    static const char method_name[] = "tracking::create_10()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<cv::legacy::TrackerCSRT> Ptr_legacy_TrackerCSRT;
        Ptr_legacy_TrackerCSRT _retval_ = cv::legacy::TrackerCSRT::create();
        return (jlong)(new Ptr_legacy_TrackerCSRT(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  void cv::legacy::TrackerCSRT::setInitialMask(Mat mask)
//

JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1TrackerCSRT_setInitialMask_10 (JNIEnv*, jclass, jlong, jlong);

JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1TrackerCSRT_setInitialMask_10
  (JNIEnv* env, jclass , jlong self, jlong mask_nativeObj)
{
    using namespace cv::legacy;
    static const char method_name[] = "tracking::setInitialMask_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::legacy::TrackerCSRT>* me = (Ptr<cv::legacy::TrackerCSRT>*) self; //TODO: check for NULL
        Mat& mask = *((Mat*)mask_nativeObj);
        (*me)->setInitialMask( mask );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  native support for java finalize()
//  static void Ptr<cv::legacy::TrackerCSRT>::delete( __int64 self )
//
JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1TrackerCSRT_delete(JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1TrackerCSRT_delete
  (JNIEnv*, jclass, jlong self)
{
    delete (Ptr<cv::legacy::TrackerCSRT>*) self;
}


//
// static Ptr_legacy_TrackerKCF cv::legacy::TrackerKCF::create()
//

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_legacy_1TrackerKCF_create_10 (JNIEnv*, jclass);

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_legacy_1TrackerKCF_create_10
  (JNIEnv* env, jclass )
{
    using namespace cv::legacy;
    static const char method_name[] = "tracking::create_10()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<cv::legacy::TrackerKCF> Ptr_legacy_TrackerKCF;
        Ptr_legacy_TrackerKCF _retval_ = cv::legacy::TrackerKCF::create();
        return (jlong)(new Ptr_legacy_TrackerKCF(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  native support for java finalize()
//  static void Ptr<cv::legacy::TrackerKCF>::delete( __int64 self )
//
JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1TrackerKCF_delete(JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1TrackerKCF_delete
  (JNIEnv*, jclass, jlong self)
{
    delete (Ptr<cv::legacy::TrackerKCF>*) self;
}


//
// static Ptr_legacy_TrackerMIL cv::legacy::TrackerMIL::create()
//

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_legacy_1TrackerMIL_create_10 (JNIEnv*, jclass);

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_legacy_1TrackerMIL_create_10
  (JNIEnv* env, jclass )
{
    using namespace cv::legacy;
    static const char method_name[] = "tracking::create_10()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<cv::legacy::TrackerMIL> Ptr_legacy_TrackerMIL;
        Ptr_legacy_TrackerMIL _retval_ = cv::legacy::TrackerMIL::create();
        return (jlong)(new Ptr_legacy_TrackerMIL(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  native support for java finalize()
//  static void Ptr<cv::legacy::TrackerMIL>::delete( __int64 self )
//
JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1TrackerMIL_delete(JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1TrackerMIL_delete
  (JNIEnv*, jclass, jlong self)
{
    delete (Ptr<cv::legacy::TrackerMIL>*) self;
}


//
// static Ptr_legacy_TrackerMOSSE cv::legacy::TrackerMOSSE::create()
//

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_legacy_1TrackerMOSSE_create_10 (JNIEnv*, jclass);

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_legacy_1TrackerMOSSE_create_10
  (JNIEnv* env, jclass )
{
    using namespace cv::legacy;
    static const char method_name[] = "tracking::create_10()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<cv::legacy::TrackerMOSSE> Ptr_legacy_TrackerMOSSE;
        Ptr_legacy_TrackerMOSSE _retval_ = cv::legacy::TrackerMOSSE::create();
        return (jlong)(new Ptr_legacy_TrackerMOSSE(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  native support for java finalize()
//  static void Ptr<cv::legacy::TrackerMOSSE>::delete( __int64 self )
//
JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1TrackerMOSSE_delete(JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1TrackerMOSSE_delete
  (JNIEnv*, jclass, jlong self)
{
    delete (Ptr<cv::legacy::TrackerMOSSE>*) self;
}


//
// static Ptr_legacy_TrackerMedianFlow cv::legacy::TrackerMedianFlow::create()
//

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_legacy_1TrackerMedianFlow_create_10 (JNIEnv*, jclass);

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_legacy_1TrackerMedianFlow_create_10
  (JNIEnv* env, jclass )
{
    using namespace cv::legacy;
    static const char method_name[] = "tracking::create_10()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<cv::legacy::TrackerMedianFlow> Ptr_legacy_TrackerMedianFlow;
        Ptr_legacy_TrackerMedianFlow _retval_ = cv::legacy::TrackerMedianFlow::create();
        return (jlong)(new Ptr_legacy_TrackerMedianFlow(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  native support for java finalize()
//  static void Ptr<cv::legacy::TrackerMedianFlow>::delete( __int64 self )
//
JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1TrackerMedianFlow_delete(JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1TrackerMedianFlow_delete
  (JNIEnv*, jclass, jlong self)
{
    delete (Ptr<cv::legacy::TrackerMedianFlow>*) self;
}


//
// static Ptr_legacy_TrackerTLD cv::legacy::TrackerTLD::create()
//

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_legacy_1TrackerTLD_create_10 (JNIEnv*, jclass);

JNIEXPORT jlong JNICALL Java_org_opencv_tracking_legacy_1TrackerTLD_create_10
  (JNIEnv* env, jclass )
{
    using namespace cv::legacy;
    static const char method_name[] = "tracking::create_10()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<cv::legacy::TrackerTLD> Ptr_legacy_TrackerTLD;
        Ptr_legacy_TrackerTLD _retval_ = cv::legacy::TrackerTLD::create();
        return (jlong)(new Ptr_legacy_TrackerTLD(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  native support for java finalize()
//  static void Ptr<cv::legacy::TrackerTLD>::delete( __int64 self )
//
JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1TrackerTLD_delete(JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_tracking_legacy_1TrackerTLD_delete
  (JNIEnv*, jclass, jlong self)
{
    delete (Ptr<cv::legacy::TrackerTLD>*) self;
}



} // extern "C"

#endif // HAVE_OPENCV_TRACKING
