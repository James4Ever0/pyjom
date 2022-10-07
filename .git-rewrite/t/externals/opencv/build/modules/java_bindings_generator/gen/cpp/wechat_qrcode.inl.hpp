//
// This file is auto-generated. Please don't modify it!
//

#undef LOG_TAG

#include "opencv2/opencv_modules.hpp"
#ifdef HAVE_OPENCV_WECHAT_QRCODE

#include <string>

#include "opencv2/wechat_qrcode.hpp"

#include "/media/root/help1/pyjom/externals/opencv/opencv-4.x/../opencv_contrib-4.x/modules/wechat_qrcode/include/opencv2/wechat_qrcode.hpp"

#define LOG_TAG "org.opencv.wechat_qrcode"
#include "common.h"

using namespace cv;

/// throw java exception
#undef throwJavaException
#define throwJavaException throwJavaException_wechat_qrcode
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
//   cv::wechat_qrcode::WeChatQRCode::WeChatQRCode(string detector_prototxt_path = "", string detector_caffe_model_path = "", string super_resolution_prototxt_path = "", string super_resolution_caffe_model_path = "")
//

JNIEXPORT jlong JNICALL Java_org_opencv_wechat_1qrcode_WeChatQRCode_WeChatQRCode_10 (JNIEnv*, jclass, jstring, jstring, jstring, jstring);

JNIEXPORT jlong JNICALL Java_org_opencv_wechat_1qrcode_WeChatQRCode_WeChatQRCode_10
  (JNIEnv* env, jclass , jstring detector_prototxt_path, jstring detector_caffe_model_path, jstring super_resolution_prototxt_path, jstring super_resolution_caffe_model_path)
{
    using namespace cv::wechat_qrcode;
    static const char method_name[] = "wechat_1qrcode::WeChatQRCode_10()";
    try {
        LOGD("%s", method_name);
        const char* utf_detector_prototxt_path = env->GetStringUTFChars(detector_prototxt_path, 0); std::string n_detector_prototxt_path( utf_detector_prototxt_path ? utf_detector_prototxt_path : "" ); env->ReleaseStringUTFChars(detector_prototxt_path, utf_detector_prototxt_path);
        const char* utf_detector_caffe_model_path = env->GetStringUTFChars(detector_caffe_model_path, 0); std::string n_detector_caffe_model_path( utf_detector_caffe_model_path ? utf_detector_caffe_model_path : "" ); env->ReleaseStringUTFChars(detector_caffe_model_path, utf_detector_caffe_model_path);
        const char* utf_super_resolution_prototxt_path = env->GetStringUTFChars(super_resolution_prototxt_path, 0); std::string n_super_resolution_prototxt_path( utf_super_resolution_prototxt_path ? utf_super_resolution_prototxt_path : "" ); env->ReleaseStringUTFChars(super_resolution_prototxt_path, utf_super_resolution_prototxt_path);
        const char* utf_super_resolution_caffe_model_path = env->GetStringUTFChars(super_resolution_caffe_model_path, 0); std::string n_super_resolution_caffe_model_path( utf_super_resolution_caffe_model_path ? utf_super_resolution_caffe_model_path : "" ); env->ReleaseStringUTFChars(super_resolution_caffe_model_path, utf_super_resolution_caffe_model_path);
        Ptr<cv::wechat_qrcode::WeChatQRCode> _retval_ = makePtr<cv::wechat_qrcode::WeChatQRCode>( n_detector_prototxt_path, n_detector_caffe_model_path, n_super_resolution_prototxt_path, n_super_resolution_caffe_model_path );
        return (jlong)(new Ptr<cv::wechat_qrcode::WeChatQRCode>(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



JNIEXPORT jlong JNICALL Java_org_opencv_wechat_1qrcode_WeChatQRCode_WeChatQRCode_11 (JNIEnv*, jclass, jstring, jstring, jstring);

JNIEXPORT jlong JNICALL Java_org_opencv_wechat_1qrcode_WeChatQRCode_WeChatQRCode_11
  (JNIEnv* env, jclass , jstring detector_prototxt_path, jstring detector_caffe_model_path, jstring super_resolution_prototxt_path)
{
    using namespace cv::wechat_qrcode;
    static const char method_name[] = "wechat_1qrcode::WeChatQRCode_11()";
    try {
        LOGD("%s", method_name);
        const char* utf_detector_prototxt_path = env->GetStringUTFChars(detector_prototxt_path, 0); std::string n_detector_prototxt_path( utf_detector_prototxt_path ? utf_detector_prototxt_path : "" ); env->ReleaseStringUTFChars(detector_prototxt_path, utf_detector_prototxt_path);
        const char* utf_detector_caffe_model_path = env->GetStringUTFChars(detector_caffe_model_path, 0); std::string n_detector_caffe_model_path( utf_detector_caffe_model_path ? utf_detector_caffe_model_path : "" ); env->ReleaseStringUTFChars(detector_caffe_model_path, utf_detector_caffe_model_path);
        const char* utf_super_resolution_prototxt_path = env->GetStringUTFChars(super_resolution_prototxt_path, 0); std::string n_super_resolution_prototxt_path( utf_super_resolution_prototxt_path ? utf_super_resolution_prototxt_path : "" ); env->ReleaseStringUTFChars(super_resolution_prototxt_path, utf_super_resolution_prototxt_path);
        Ptr<cv::wechat_qrcode::WeChatQRCode> _retval_ = makePtr<cv::wechat_qrcode::WeChatQRCode>( n_detector_prototxt_path, n_detector_caffe_model_path, n_super_resolution_prototxt_path );
        return (jlong)(new Ptr<cv::wechat_qrcode::WeChatQRCode>(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



JNIEXPORT jlong JNICALL Java_org_opencv_wechat_1qrcode_WeChatQRCode_WeChatQRCode_12 (JNIEnv*, jclass, jstring, jstring);

JNIEXPORT jlong JNICALL Java_org_opencv_wechat_1qrcode_WeChatQRCode_WeChatQRCode_12
  (JNIEnv* env, jclass , jstring detector_prototxt_path, jstring detector_caffe_model_path)
{
    using namespace cv::wechat_qrcode;
    static const char method_name[] = "wechat_1qrcode::WeChatQRCode_12()";
    try {
        LOGD("%s", method_name);
        const char* utf_detector_prototxt_path = env->GetStringUTFChars(detector_prototxt_path, 0); std::string n_detector_prototxt_path( utf_detector_prototxt_path ? utf_detector_prototxt_path : "" ); env->ReleaseStringUTFChars(detector_prototxt_path, utf_detector_prototxt_path);
        const char* utf_detector_caffe_model_path = env->GetStringUTFChars(detector_caffe_model_path, 0); std::string n_detector_caffe_model_path( utf_detector_caffe_model_path ? utf_detector_caffe_model_path : "" ); env->ReleaseStringUTFChars(detector_caffe_model_path, utf_detector_caffe_model_path);
        Ptr<cv::wechat_qrcode::WeChatQRCode> _retval_ = makePtr<cv::wechat_qrcode::WeChatQRCode>( n_detector_prototxt_path, n_detector_caffe_model_path );
        return (jlong)(new Ptr<cv::wechat_qrcode::WeChatQRCode>(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



JNIEXPORT jlong JNICALL Java_org_opencv_wechat_1qrcode_WeChatQRCode_WeChatQRCode_13 (JNIEnv*, jclass, jstring);

JNIEXPORT jlong JNICALL Java_org_opencv_wechat_1qrcode_WeChatQRCode_WeChatQRCode_13
  (JNIEnv* env, jclass , jstring detector_prototxt_path)
{
    using namespace cv::wechat_qrcode;
    static const char method_name[] = "wechat_1qrcode::WeChatQRCode_13()";
    try {
        LOGD("%s", method_name);
        const char* utf_detector_prototxt_path = env->GetStringUTFChars(detector_prototxt_path, 0); std::string n_detector_prototxt_path( utf_detector_prototxt_path ? utf_detector_prototxt_path : "" ); env->ReleaseStringUTFChars(detector_prototxt_path, utf_detector_prototxt_path);
        Ptr<cv::wechat_qrcode::WeChatQRCode> _retval_ = makePtr<cv::wechat_qrcode::WeChatQRCode>( n_detector_prototxt_path );
        return (jlong)(new Ptr<cv::wechat_qrcode::WeChatQRCode>(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



JNIEXPORT jlong JNICALL Java_org_opencv_wechat_1qrcode_WeChatQRCode_WeChatQRCode_14 (JNIEnv*, jclass);

JNIEXPORT jlong JNICALL Java_org_opencv_wechat_1qrcode_WeChatQRCode_WeChatQRCode_14
  (JNIEnv* env, jclass )
{
    using namespace cv::wechat_qrcode;
    static const char method_name[] = "wechat_1qrcode::WeChatQRCode_14()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::wechat_qrcode::WeChatQRCode> _retval_ = makePtr<cv::wechat_qrcode::WeChatQRCode>();
        return (jlong)(new Ptr<cv::wechat_qrcode::WeChatQRCode>(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  vector_string cv::wechat_qrcode::WeChatQRCode::detectAndDecode(Mat img, vector_Mat& points = vector_Mat())
//

JNIEXPORT jobject JNICALL Java_org_opencv_wechat_1qrcode_WeChatQRCode_detectAndDecode_10 (JNIEnv*, jclass, jlong, jlong, jlong);

JNIEXPORT jobject JNICALL Java_org_opencv_wechat_1qrcode_WeChatQRCode_detectAndDecode_10
  (JNIEnv* env, jclass , jlong self, jlong img_nativeObj, jlong points_mat_nativeObj)
{
    using namespace cv::wechat_qrcode;
    static const char method_name[] = "wechat_1qrcode::detectAndDecode_10()";
    try {
        LOGD("%s", method_name);
        std::vector<Mat> points;
        Mat& points_mat = *((Mat*)points_mat_nativeObj);
        Ptr<cv::wechat_qrcode::WeChatQRCode>* me = (Ptr<cv::wechat_qrcode::WeChatQRCode>*) self; //TODO: check for NULL
        Mat& img = *((Mat*)img_nativeObj);
        std::vector< std::string > _ret_val_vector_ = (*me)->detectAndDecode( img, points );
        vector_Mat_to_Mat( points, points_mat );
        jobject _retval_ = vector_string_to_List(env, _ret_val_vector_);
        return _retval_;
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



JNIEXPORT jobject JNICALL Java_org_opencv_wechat_1qrcode_WeChatQRCode_detectAndDecode_11 (JNIEnv*, jclass, jlong, jlong);

JNIEXPORT jobject JNICALL Java_org_opencv_wechat_1qrcode_WeChatQRCode_detectAndDecode_11
  (JNIEnv* env, jclass , jlong self, jlong img_nativeObj)
{
    using namespace cv::wechat_qrcode;
    static const char method_name[] = "wechat_1qrcode::detectAndDecode_11()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::wechat_qrcode::WeChatQRCode>* me = (Ptr<cv::wechat_qrcode::WeChatQRCode>*) self; //TODO: check for NULL
        Mat& img = *((Mat*)img_nativeObj);
        std::vector< std::string > _ret_val_vector_ = (*me)->detectAndDecode( img );
        return vector_string_to_List(env, _ret_val_vector_);
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  native support for java finalize()
//  static void Ptr<cv::wechat_qrcode::WeChatQRCode>::delete( __int64 self )
//
JNIEXPORT void JNICALL Java_org_opencv_wechat_1qrcode_WeChatQRCode_delete(JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_wechat_1qrcode_WeChatQRCode_delete
  (JNIEnv*, jclass, jlong self)
{
    delete (Ptr<cv::wechat_qrcode::WeChatQRCode>*) self;
}



} // extern "C"

#endif // HAVE_OPENCV_WECHAT_QRCODE
