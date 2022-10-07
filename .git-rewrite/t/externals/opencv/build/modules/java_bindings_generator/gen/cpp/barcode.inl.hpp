//
// This file is auto-generated. Please don't modify it!
//

#undef LOG_TAG

#include "opencv2/opencv_modules.hpp"
#ifdef HAVE_OPENCV_BARCODE

#include <string>

#include "opencv2/barcode.hpp"

#include "/media/root/help1/pyjom/externals/opencv/opencv-4.x/../opencv_contrib-4.x/modules/barcode/misc/java/src/cpp/barcode_converters.hpp"
#include "/media/root/help1/pyjom/externals/opencv/opencv-4.x/../opencv_contrib-4.x/modules/barcode/include/opencv2/barcode.hpp"

#define LOG_TAG "org.opencv.barcode"
#include "common.h"

using namespace cv;

/// throw java exception
#undef throwJavaException
#define throwJavaException throwJavaException_barcode
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
//   cv::barcode::BarcodeDetector::BarcodeDetector(string prototxt_path = "", string model_path = "")
//

JNIEXPORT jlong JNICALL Java_org_opencv_barcode_BarcodeDetector_BarcodeDetector_10 (JNIEnv*, jclass, jstring, jstring);

JNIEXPORT jlong JNICALL Java_org_opencv_barcode_BarcodeDetector_BarcodeDetector_10
  (JNIEnv* env, jclass , jstring prototxt_path, jstring model_path)
{
    using namespace cv::barcode;
    static const char method_name[] = "barcode::BarcodeDetector_10()";
    try {
        LOGD("%s", method_name);
        const char* utf_prototxt_path = env->GetStringUTFChars(prototxt_path, 0); std::string n_prototxt_path( utf_prototxt_path ? utf_prototxt_path : "" ); env->ReleaseStringUTFChars(prototxt_path, utf_prototxt_path);
        const char* utf_model_path = env->GetStringUTFChars(model_path, 0); std::string n_model_path( utf_model_path ? utf_model_path : "" ); env->ReleaseStringUTFChars(model_path, utf_model_path);
        Ptr<cv::barcode::BarcodeDetector> _retval_ = makePtr<cv::barcode::BarcodeDetector>( n_prototxt_path, n_model_path );
        return (jlong)(new Ptr<cv::barcode::BarcodeDetector>(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



JNIEXPORT jlong JNICALL Java_org_opencv_barcode_BarcodeDetector_BarcodeDetector_11 (JNIEnv*, jclass, jstring);

JNIEXPORT jlong JNICALL Java_org_opencv_barcode_BarcodeDetector_BarcodeDetector_11
  (JNIEnv* env, jclass , jstring prototxt_path)
{
    using namespace cv::barcode;
    static const char method_name[] = "barcode::BarcodeDetector_11()";
    try {
        LOGD("%s", method_name);
        const char* utf_prototxt_path = env->GetStringUTFChars(prototxt_path, 0); std::string n_prototxt_path( utf_prototxt_path ? utf_prototxt_path : "" ); env->ReleaseStringUTFChars(prototxt_path, utf_prototxt_path);
        Ptr<cv::barcode::BarcodeDetector> _retval_ = makePtr<cv::barcode::BarcodeDetector>( n_prototxt_path );
        return (jlong)(new Ptr<cv::barcode::BarcodeDetector>(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



JNIEXPORT jlong JNICALL Java_org_opencv_barcode_BarcodeDetector_BarcodeDetector_12 (JNIEnv*, jclass);

JNIEXPORT jlong JNICALL Java_org_opencv_barcode_BarcodeDetector_BarcodeDetector_12
  (JNIEnv* env, jclass )
{
    using namespace cv::barcode;
    static const char method_name[] = "barcode::BarcodeDetector_12()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::barcode::BarcodeDetector> _retval_ = makePtr<cv::barcode::BarcodeDetector>();
        return (jlong)(new Ptr<cv::barcode::BarcodeDetector>(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  bool cv::barcode::BarcodeDetector::detect(Mat img, Mat& points)
//

JNIEXPORT jboolean JNICALL Java_org_opencv_barcode_BarcodeDetector_detect_10 (JNIEnv*, jclass, jlong, jlong, jlong);

JNIEXPORT jboolean JNICALL Java_org_opencv_barcode_BarcodeDetector_detect_10
  (JNIEnv* env, jclass , jlong self, jlong img_nativeObj, jlong points_nativeObj)
{
    using namespace cv::barcode;
    static const char method_name[] = "barcode::detect_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::barcode::BarcodeDetector>* me = (Ptr<cv::barcode::BarcodeDetector>*) self; //TODO: check for NULL
        Mat& img = *((Mat*)img_nativeObj);
        Mat& points = *((Mat*)points_nativeObj);
        return (*me)->detect( img, points );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  bool cv::barcode::BarcodeDetector::decode(Mat img, Mat points, vector_string& decoded_info, vector_BarcodeType& decoded_type)
//

JNIEXPORT jboolean JNICALL Java_org_opencv_barcode_BarcodeDetector_decode_10 (JNIEnv*, jclass, jlong, jlong, jlong, jobject, jobject);

JNIEXPORT jboolean JNICALL Java_org_opencv_barcode_BarcodeDetector_decode_10
  (JNIEnv* env, jclass , jlong self, jlong img_nativeObj, jlong points_nativeObj, jobject decoded_info_list, jobject decoded_type_list)
{
    using namespace cv::barcode;
    static const char method_name[] = "barcode::decode_10()";
    try {
        LOGD("%s", method_name);
        std::vector< std::string > decoded_info;
        std::vector< cv::barcode::BarcodeType > decoded_type;
        Ptr<cv::barcode::BarcodeDetector>* me = (Ptr<cv::barcode::BarcodeDetector>*) self; //TODO: check for NULL
        Mat& img = *((Mat*)img_nativeObj);
        Mat& points = *((Mat*)points_nativeObj);
        bool _retval_ = (*me)->decode( img, points, decoded_info, decoded_type );
        Copy_vector_string_to_List(env,decoded_info,decoded_info_list);
        Copy_vector_BarcodeType_to_List(env,decoded_type,decoded_type_list);
        return _retval_;
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  bool cv::barcode::BarcodeDetector::detectAndDecode(Mat img, vector_string& decoded_info, vector_BarcodeType& decoded_type, Mat& points = Mat())
//

JNIEXPORT jboolean JNICALL Java_org_opencv_barcode_BarcodeDetector_detectAndDecode_10 (JNIEnv*, jclass, jlong, jlong, jobject, jobject, jlong);

JNIEXPORT jboolean JNICALL Java_org_opencv_barcode_BarcodeDetector_detectAndDecode_10
  (JNIEnv* env, jclass , jlong self, jlong img_nativeObj, jobject decoded_info_list, jobject decoded_type_list, jlong points_nativeObj)
{
    using namespace cv::barcode;
    static const char method_name[] = "barcode::detectAndDecode_10()";
    try {
        LOGD("%s", method_name);
        std::vector< std::string > decoded_info;
        std::vector< cv::barcode::BarcodeType > decoded_type;
        Ptr<cv::barcode::BarcodeDetector>* me = (Ptr<cv::barcode::BarcodeDetector>*) self; //TODO: check for NULL
        Mat& img = *((Mat*)img_nativeObj);
        Mat& points = *((Mat*)points_nativeObj);
        bool _retval_ = (*me)->detectAndDecode( img, decoded_info, decoded_type, points );
        Copy_vector_string_to_List(env,decoded_info,decoded_info_list);
        Copy_vector_BarcodeType_to_List(env,decoded_type,decoded_type_list);
        return _retval_;
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



JNIEXPORT jboolean JNICALL Java_org_opencv_barcode_BarcodeDetector_detectAndDecode_11 (JNIEnv*, jclass, jlong, jlong, jobject, jobject);

JNIEXPORT jboolean JNICALL Java_org_opencv_barcode_BarcodeDetector_detectAndDecode_11
  (JNIEnv* env, jclass , jlong self, jlong img_nativeObj, jobject decoded_info_list, jobject decoded_type_list)
{
    using namespace cv::barcode;
    static const char method_name[] = "barcode::detectAndDecode_11()";
    try {
        LOGD("%s", method_name);
        std::vector< std::string > decoded_info;
        std::vector< cv::barcode::BarcodeType > decoded_type;
        Ptr<cv::barcode::BarcodeDetector>* me = (Ptr<cv::barcode::BarcodeDetector>*) self; //TODO: check for NULL
        Mat& img = *((Mat*)img_nativeObj);
        bool _retval_ = (*me)->detectAndDecode( img, decoded_info, decoded_type );
        Copy_vector_string_to_List(env,decoded_info,decoded_info_list);
        Copy_vector_BarcodeType_to_List(env,decoded_type,decoded_type_list);
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
//  static void Ptr<cv::barcode::BarcodeDetector>::delete( __int64 self )
//
JNIEXPORT void JNICALL Java_org_opencv_barcode_BarcodeDetector_delete(JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_barcode_BarcodeDetector_delete
  (JNIEnv*, jclass, jlong self)
{
    delete (Ptr<cv::barcode::BarcodeDetector>*) self;
}



} // extern "C"

#endif // HAVE_OPENCV_BARCODE
