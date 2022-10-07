//
// This file is auto-generated. Please don't modify it!
//

#undef LOG_TAG

#include "opencv2/opencv_modules.hpp"
#ifdef HAVE_OPENCV_BIOINSPIRED

#include <string>

#include "opencv2/bioinspired.hpp"

#include "/media/root/help1/pyjom/externals/opencv/opencv-4.x/../opencv_contrib-4.x/modules/bioinspired/include/opencv2/bioinspired/retina.hpp"
#include "/media/root/help1/pyjom/externals/opencv/opencv-4.x/../opencv_contrib-4.x/modules/bioinspired/include/opencv2/bioinspired/retinafasttonemapping.hpp"
#include "/media/root/help1/pyjom/externals/opencv/opencv-4.x/../opencv_contrib-4.x/modules/bioinspired/include/opencv2/bioinspired/transientareassegmentationmodule.hpp"

#define LOG_TAG "org.opencv.bioinspired"
#include "common.h"

using namespace cv;

/// throw java exception
#undef throwJavaException
#define throwJavaException throwJavaException_bioinspired
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
//  Size cv::bioinspired::Retina::getInputSize()
//

JNIEXPORT jdoubleArray JNICALL Java_org_opencv_bioinspired_Retina_getInputSize_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jdoubleArray JNICALL Java_org_opencv_bioinspired_Retina_getInputSize_10
  (JNIEnv* env, jclass , jlong self)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::getInputSize_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        Size _retval_ = (*me)->getInputSize();
        jdoubleArray _da_retval_ = env->NewDoubleArray(2);  jdouble _tmp_retval_[2] = {(jdouble)_retval_.width, (jdouble)_retval_.height}; env->SetDoubleArrayRegion(_da_retval_, 0, 2, _tmp_retval_);
        return _da_retval_;
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  Size cv::bioinspired::Retina::getOutputSize()
//

JNIEXPORT jdoubleArray JNICALL Java_org_opencv_bioinspired_Retina_getOutputSize_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jdoubleArray JNICALL Java_org_opencv_bioinspired_Retina_getOutputSize_10
  (JNIEnv* env, jclass , jlong self)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::getOutputSize_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        Size _retval_ = (*me)->getOutputSize();
        jdoubleArray _da_retval_ = env->NewDoubleArray(2);  jdouble _tmp_retval_[2] = {(jdouble)_retval_.width, (jdouble)_retval_.height}; env->SetDoubleArrayRegion(_da_retval_, 0, 2, _tmp_retval_);
        return _da_retval_;
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  void cv::bioinspired::Retina::setup(String retinaParameterFile = "", bool applyDefaultSetupOnFailure = true)
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setup_10 (JNIEnv*, jclass, jlong, jstring, jboolean);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setup_10
  (JNIEnv* env, jclass , jlong self, jstring retinaParameterFile, jboolean applyDefaultSetupOnFailure)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setup_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        const char* utf_retinaParameterFile = env->GetStringUTFChars(retinaParameterFile, 0); String n_retinaParameterFile( utf_retinaParameterFile ? utf_retinaParameterFile : "" ); env->ReleaseStringUTFChars(retinaParameterFile, utf_retinaParameterFile);
        (*me)->setup( n_retinaParameterFile, (bool)applyDefaultSetupOnFailure );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setup_11 (JNIEnv*, jclass, jlong, jstring);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setup_11
  (JNIEnv* env, jclass , jlong self, jstring retinaParameterFile)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setup_11()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        const char* utf_retinaParameterFile = env->GetStringUTFChars(retinaParameterFile, 0); String n_retinaParameterFile( utf_retinaParameterFile ? utf_retinaParameterFile : "" ); env->ReleaseStringUTFChars(retinaParameterFile, utf_retinaParameterFile);
        (*me)->setup( n_retinaParameterFile );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setup_12 (JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setup_12
  (JNIEnv* env, jclass , jlong self)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setup_12()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setup();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  String cv::bioinspired::Retina::printSetup()
//

JNIEXPORT jstring JNICALL Java_org_opencv_bioinspired_Retina_printSetup_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jstring JNICALL Java_org_opencv_bioinspired_Retina_printSetup_10
  (JNIEnv* env, jclass , jlong self)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::printSetup_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        cv::String _retval_ = (*me)->printSetup();
        return env->NewStringUTF(_retval_.c_str());
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return env->NewStringUTF("");
}



//
//  void cv::bioinspired::Retina::write(String fs)
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_write_10 (JNIEnv*, jclass, jlong, jstring);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_write_10
  (JNIEnv* env, jclass , jlong self, jstring fs)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::write_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        const char* utf_fs = env->GetStringUTFChars(fs, 0); String n_fs( utf_fs ? utf_fs : "" ); env->ReleaseStringUTFChars(fs, utf_fs);
        (*me)->write( n_fs );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  void cv::bioinspired::Retina::setupOPLandIPLParvoChannel(bool colorMode = true, bool normaliseOutput = true, float photoreceptorsLocalAdaptationSensitivity = 0.7f, float photoreceptorsTemporalConstant = 0.5f, float photoreceptorsSpatialConstant = 0.53f, float horizontalCellsGain = 0.f, float HcellsTemporalConstant = 1.f, float HcellsSpatialConstant = 7.f, float ganglionCellsSensitivity = 0.7f)
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_10 (JNIEnv*, jclass, jlong, jboolean, jboolean, jfloat, jfloat, jfloat, jfloat, jfloat, jfloat, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_10
  (JNIEnv* env, jclass , jlong self, jboolean colorMode, jboolean normaliseOutput, jfloat photoreceptorsLocalAdaptationSensitivity, jfloat photoreceptorsTemporalConstant, jfloat photoreceptorsSpatialConstant, jfloat horizontalCellsGain, jfloat HcellsTemporalConstant, jfloat HcellsSpatialConstant, jfloat ganglionCellsSensitivity)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setupOPLandIPLParvoChannel_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setupOPLandIPLParvoChannel( (bool)colorMode, (bool)normaliseOutput, (float)photoreceptorsLocalAdaptationSensitivity, (float)photoreceptorsTemporalConstant, (float)photoreceptorsSpatialConstant, (float)horizontalCellsGain, (float)HcellsTemporalConstant, (float)HcellsSpatialConstant, (float)ganglionCellsSensitivity );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_11 (JNIEnv*, jclass, jlong, jboolean, jboolean, jfloat, jfloat, jfloat, jfloat, jfloat, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_11
  (JNIEnv* env, jclass , jlong self, jboolean colorMode, jboolean normaliseOutput, jfloat photoreceptorsLocalAdaptationSensitivity, jfloat photoreceptorsTemporalConstant, jfloat photoreceptorsSpatialConstant, jfloat horizontalCellsGain, jfloat HcellsTemporalConstant, jfloat HcellsSpatialConstant)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setupOPLandIPLParvoChannel_11()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setupOPLandIPLParvoChannel( (bool)colorMode, (bool)normaliseOutput, (float)photoreceptorsLocalAdaptationSensitivity, (float)photoreceptorsTemporalConstant, (float)photoreceptorsSpatialConstant, (float)horizontalCellsGain, (float)HcellsTemporalConstant, (float)HcellsSpatialConstant );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_12 (JNIEnv*, jclass, jlong, jboolean, jboolean, jfloat, jfloat, jfloat, jfloat, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_12
  (JNIEnv* env, jclass , jlong self, jboolean colorMode, jboolean normaliseOutput, jfloat photoreceptorsLocalAdaptationSensitivity, jfloat photoreceptorsTemporalConstant, jfloat photoreceptorsSpatialConstant, jfloat horizontalCellsGain, jfloat HcellsTemporalConstant)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setupOPLandIPLParvoChannel_12()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setupOPLandIPLParvoChannel( (bool)colorMode, (bool)normaliseOutput, (float)photoreceptorsLocalAdaptationSensitivity, (float)photoreceptorsTemporalConstant, (float)photoreceptorsSpatialConstant, (float)horizontalCellsGain, (float)HcellsTemporalConstant );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_13 (JNIEnv*, jclass, jlong, jboolean, jboolean, jfloat, jfloat, jfloat, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_13
  (JNIEnv* env, jclass , jlong self, jboolean colorMode, jboolean normaliseOutput, jfloat photoreceptorsLocalAdaptationSensitivity, jfloat photoreceptorsTemporalConstant, jfloat photoreceptorsSpatialConstant, jfloat horizontalCellsGain)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setupOPLandIPLParvoChannel_13()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setupOPLandIPLParvoChannel( (bool)colorMode, (bool)normaliseOutput, (float)photoreceptorsLocalAdaptationSensitivity, (float)photoreceptorsTemporalConstant, (float)photoreceptorsSpatialConstant, (float)horizontalCellsGain );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_14 (JNIEnv*, jclass, jlong, jboolean, jboolean, jfloat, jfloat, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_14
  (JNIEnv* env, jclass , jlong self, jboolean colorMode, jboolean normaliseOutput, jfloat photoreceptorsLocalAdaptationSensitivity, jfloat photoreceptorsTemporalConstant, jfloat photoreceptorsSpatialConstant)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setupOPLandIPLParvoChannel_14()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setupOPLandIPLParvoChannel( (bool)colorMode, (bool)normaliseOutput, (float)photoreceptorsLocalAdaptationSensitivity, (float)photoreceptorsTemporalConstant, (float)photoreceptorsSpatialConstant );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_15 (JNIEnv*, jclass, jlong, jboolean, jboolean, jfloat, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_15
  (JNIEnv* env, jclass , jlong self, jboolean colorMode, jboolean normaliseOutput, jfloat photoreceptorsLocalAdaptationSensitivity, jfloat photoreceptorsTemporalConstant)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setupOPLandIPLParvoChannel_15()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setupOPLandIPLParvoChannel( (bool)colorMode, (bool)normaliseOutput, (float)photoreceptorsLocalAdaptationSensitivity, (float)photoreceptorsTemporalConstant );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_16 (JNIEnv*, jclass, jlong, jboolean, jboolean, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_16
  (JNIEnv* env, jclass , jlong self, jboolean colorMode, jboolean normaliseOutput, jfloat photoreceptorsLocalAdaptationSensitivity)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setupOPLandIPLParvoChannel_16()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setupOPLandIPLParvoChannel( (bool)colorMode, (bool)normaliseOutput, (float)photoreceptorsLocalAdaptationSensitivity );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_17 (JNIEnv*, jclass, jlong, jboolean, jboolean);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_17
  (JNIEnv* env, jclass , jlong self, jboolean colorMode, jboolean normaliseOutput)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setupOPLandIPLParvoChannel_17()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setupOPLandIPLParvoChannel( (bool)colorMode, (bool)normaliseOutput );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_18 (JNIEnv*, jclass, jlong, jboolean);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_18
  (JNIEnv* env, jclass , jlong self, jboolean colorMode)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setupOPLandIPLParvoChannel_18()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setupOPLandIPLParvoChannel( (bool)colorMode );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_19 (JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupOPLandIPLParvoChannel_19
  (JNIEnv* env, jclass , jlong self)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setupOPLandIPLParvoChannel_19()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setupOPLandIPLParvoChannel();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  void cv::bioinspired::Retina::setupIPLMagnoChannel(bool normaliseOutput = true, float parasolCells_beta = 0.f, float parasolCells_tau = 0.f, float parasolCells_k = 7.f, float amacrinCellsTemporalCutFrequency = 1.2f, float V0CompressionParameter = 0.95f, float localAdaptintegration_tau = 0.f, float localAdaptintegration_k = 7.f)
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupIPLMagnoChannel_10 (JNIEnv*, jclass, jlong, jboolean, jfloat, jfloat, jfloat, jfloat, jfloat, jfloat, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupIPLMagnoChannel_10
  (JNIEnv* env, jclass , jlong self, jboolean normaliseOutput, jfloat parasolCells_beta, jfloat parasolCells_tau, jfloat parasolCells_k, jfloat amacrinCellsTemporalCutFrequency, jfloat V0CompressionParameter, jfloat localAdaptintegration_tau, jfloat localAdaptintegration_k)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setupIPLMagnoChannel_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setupIPLMagnoChannel( (bool)normaliseOutput, (float)parasolCells_beta, (float)parasolCells_tau, (float)parasolCells_k, (float)amacrinCellsTemporalCutFrequency, (float)V0CompressionParameter, (float)localAdaptintegration_tau, (float)localAdaptintegration_k );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupIPLMagnoChannel_11 (JNIEnv*, jclass, jlong, jboolean, jfloat, jfloat, jfloat, jfloat, jfloat, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupIPLMagnoChannel_11
  (JNIEnv* env, jclass , jlong self, jboolean normaliseOutput, jfloat parasolCells_beta, jfloat parasolCells_tau, jfloat parasolCells_k, jfloat amacrinCellsTemporalCutFrequency, jfloat V0CompressionParameter, jfloat localAdaptintegration_tau)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setupIPLMagnoChannel_11()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setupIPLMagnoChannel( (bool)normaliseOutput, (float)parasolCells_beta, (float)parasolCells_tau, (float)parasolCells_k, (float)amacrinCellsTemporalCutFrequency, (float)V0CompressionParameter, (float)localAdaptintegration_tau );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupIPLMagnoChannel_12 (JNIEnv*, jclass, jlong, jboolean, jfloat, jfloat, jfloat, jfloat, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupIPLMagnoChannel_12
  (JNIEnv* env, jclass , jlong self, jboolean normaliseOutput, jfloat parasolCells_beta, jfloat parasolCells_tau, jfloat parasolCells_k, jfloat amacrinCellsTemporalCutFrequency, jfloat V0CompressionParameter)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setupIPLMagnoChannel_12()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setupIPLMagnoChannel( (bool)normaliseOutput, (float)parasolCells_beta, (float)parasolCells_tau, (float)parasolCells_k, (float)amacrinCellsTemporalCutFrequency, (float)V0CompressionParameter );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupIPLMagnoChannel_13 (JNIEnv*, jclass, jlong, jboolean, jfloat, jfloat, jfloat, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupIPLMagnoChannel_13
  (JNIEnv* env, jclass , jlong self, jboolean normaliseOutput, jfloat parasolCells_beta, jfloat parasolCells_tau, jfloat parasolCells_k, jfloat amacrinCellsTemporalCutFrequency)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setupIPLMagnoChannel_13()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setupIPLMagnoChannel( (bool)normaliseOutput, (float)parasolCells_beta, (float)parasolCells_tau, (float)parasolCells_k, (float)amacrinCellsTemporalCutFrequency );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupIPLMagnoChannel_14 (JNIEnv*, jclass, jlong, jboolean, jfloat, jfloat, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupIPLMagnoChannel_14
  (JNIEnv* env, jclass , jlong self, jboolean normaliseOutput, jfloat parasolCells_beta, jfloat parasolCells_tau, jfloat parasolCells_k)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setupIPLMagnoChannel_14()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setupIPLMagnoChannel( (bool)normaliseOutput, (float)parasolCells_beta, (float)parasolCells_tau, (float)parasolCells_k );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupIPLMagnoChannel_15 (JNIEnv*, jclass, jlong, jboolean, jfloat, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupIPLMagnoChannel_15
  (JNIEnv* env, jclass , jlong self, jboolean normaliseOutput, jfloat parasolCells_beta, jfloat parasolCells_tau)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setupIPLMagnoChannel_15()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setupIPLMagnoChannel( (bool)normaliseOutput, (float)parasolCells_beta, (float)parasolCells_tau );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupIPLMagnoChannel_16 (JNIEnv*, jclass, jlong, jboolean, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupIPLMagnoChannel_16
  (JNIEnv* env, jclass , jlong self, jboolean normaliseOutput, jfloat parasolCells_beta)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setupIPLMagnoChannel_16()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setupIPLMagnoChannel( (bool)normaliseOutput, (float)parasolCells_beta );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupIPLMagnoChannel_17 (JNIEnv*, jclass, jlong, jboolean);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupIPLMagnoChannel_17
  (JNIEnv* env, jclass , jlong self, jboolean normaliseOutput)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setupIPLMagnoChannel_17()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setupIPLMagnoChannel( (bool)normaliseOutput );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupIPLMagnoChannel_18 (JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setupIPLMagnoChannel_18
  (JNIEnv* env, jclass , jlong self)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setupIPLMagnoChannel_18()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setupIPLMagnoChannel();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  void cv::bioinspired::Retina::run(Mat inputImage)
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_run_10 (JNIEnv*, jclass, jlong, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_run_10
  (JNIEnv* env, jclass , jlong self, jlong inputImage_nativeObj)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::run_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        Mat& inputImage = *((Mat*)inputImage_nativeObj);
        (*me)->run( inputImage );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  void cv::bioinspired::Retina::applyFastToneMapping(Mat inputImage, Mat& outputToneMappedImage)
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_applyFastToneMapping_10 (JNIEnv*, jclass, jlong, jlong, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_applyFastToneMapping_10
  (JNIEnv* env, jclass , jlong self, jlong inputImage_nativeObj, jlong outputToneMappedImage_nativeObj)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::applyFastToneMapping_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        Mat& inputImage = *((Mat*)inputImage_nativeObj);
        Mat& outputToneMappedImage = *((Mat*)outputToneMappedImage_nativeObj);
        (*me)->applyFastToneMapping( inputImage, outputToneMappedImage );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  void cv::bioinspired::Retina::getParvo(Mat& retinaOutput_parvo)
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_getParvo_10 (JNIEnv*, jclass, jlong, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_getParvo_10
  (JNIEnv* env, jclass , jlong self, jlong retinaOutput_parvo_nativeObj)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::getParvo_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        Mat& retinaOutput_parvo = *((Mat*)retinaOutput_parvo_nativeObj);
        (*me)->getParvo( retinaOutput_parvo );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  void cv::bioinspired::Retina::getParvoRAW(Mat& retinaOutput_parvo)
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_getParvoRAW_10 (JNIEnv*, jclass, jlong, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_getParvoRAW_10
  (JNIEnv* env, jclass , jlong self, jlong retinaOutput_parvo_nativeObj)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::getParvoRAW_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        Mat& retinaOutput_parvo = *((Mat*)retinaOutput_parvo_nativeObj);
        (*me)->getParvoRAW( retinaOutput_parvo );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  void cv::bioinspired::Retina::getMagno(Mat& retinaOutput_magno)
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_getMagno_10 (JNIEnv*, jclass, jlong, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_getMagno_10
  (JNIEnv* env, jclass , jlong self, jlong retinaOutput_magno_nativeObj)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::getMagno_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        Mat& retinaOutput_magno = *((Mat*)retinaOutput_magno_nativeObj);
        (*me)->getMagno( retinaOutput_magno );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  void cv::bioinspired::Retina::getMagnoRAW(Mat& retinaOutput_magno)
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_getMagnoRAW_10 (JNIEnv*, jclass, jlong, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_getMagnoRAW_10
  (JNIEnv* env, jclass , jlong self, jlong retinaOutput_magno_nativeObj)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::getMagnoRAW_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        Mat& retinaOutput_magno = *((Mat*)retinaOutput_magno_nativeObj);
        (*me)->getMagnoRAW( retinaOutput_magno );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  Mat cv::bioinspired::Retina::getMagnoRAW()
//

JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_Retina_getMagnoRAW_11 (JNIEnv*, jclass, jlong);

JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_Retina_getMagnoRAW_11
  (JNIEnv* env, jclass , jlong self)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::getMagnoRAW_11()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        cv::Mat _retval_ = (*me)->getMagnoRAW();
        return (jlong) new cv::Mat(_retval_);
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  Mat cv::bioinspired::Retina::getParvoRAW()
//

JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_Retina_getParvoRAW_11 (JNIEnv*, jclass, jlong);

JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_Retina_getParvoRAW_11
  (JNIEnv* env, jclass , jlong self)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::getParvoRAW_11()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        cv::Mat _retval_ = (*me)->getParvoRAW();
        return (jlong) new cv::Mat(_retval_);
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  void cv::bioinspired::Retina::setColorSaturation(bool saturateColors = true, float colorSaturationValue = 4.0f)
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setColorSaturation_10 (JNIEnv*, jclass, jlong, jboolean, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setColorSaturation_10
  (JNIEnv* env, jclass , jlong self, jboolean saturateColors, jfloat colorSaturationValue)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setColorSaturation_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setColorSaturation( (bool)saturateColors, (float)colorSaturationValue );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setColorSaturation_11 (JNIEnv*, jclass, jlong, jboolean);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setColorSaturation_11
  (JNIEnv* env, jclass , jlong self, jboolean saturateColors)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setColorSaturation_11()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setColorSaturation( (bool)saturateColors );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setColorSaturation_12 (JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_setColorSaturation_12
  (JNIEnv* env, jclass , jlong self)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setColorSaturation_12()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->setColorSaturation();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  void cv::bioinspired::Retina::clearBuffers()
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_clearBuffers_10 (JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_clearBuffers_10
  (JNIEnv* env, jclass , jlong self)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::clearBuffers_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->clearBuffers();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  void cv::bioinspired::Retina::activateMovingContoursProcessing(bool activate)
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_activateMovingContoursProcessing_10 (JNIEnv*, jclass, jlong, jboolean);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_activateMovingContoursProcessing_10
  (JNIEnv* env, jclass , jlong self, jboolean activate)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::activateMovingContoursProcessing_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->activateMovingContoursProcessing( (bool)activate );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  void cv::bioinspired::Retina::activateContoursProcessing(bool activate)
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_activateContoursProcessing_10 (JNIEnv*, jclass, jlong, jboolean);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_activateContoursProcessing_10
  (JNIEnv* env, jclass , jlong self, jboolean activate)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::activateContoursProcessing_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::Retina>* me = (Ptr<cv::bioinspired::Retina>*) self; //TODO: check for NULL
        (*me)->activateContoursProcessing( (bool)activate );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// static Ptr_Retina cv::bioinspired::Retina::create(Size inputSize)
//

JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_Retina_create_10 (JNIEnv*, jclass, jdouble, jdouble);

JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_Retina_create_10
  (JNIEnv* env, jclass , jdouble inputSize_width, jdouble inputSize_height)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::create_10()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<cv::bioinspired::Retina> Ptr_Retina;
        Size inputSize((int)inputSize_width, (int)inputSize_height);
        Ptr_Retina _retval_ = cv::bioinspired::Retina::create( inputSize );
        return (jlong)(new Ptr_Retina(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
// static Ptr_Retina cv::bioinspired::Retina::create(Size inputSize, bool colorMode, int colorSamplingMethod = RETINA_COLOR_BAYER, bool useRetinaLogSampling = false, float reductionFactor = 1.0f, float samplingStrength = 10.0f)
//

JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_Retina_create_11 (JNIEnv*, jclass, jdouble, jdouble, jboolean, jint, jboolean, jfloat, jfloat);

JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_Retina_create_11
  (JNIEnv* env, jclass , jdouble inputSize_width, jdouble inputSize_height, jboolean colorMode, jint colorSamplingMethod, jboolean useRetinaLogSampling, jfloat reductionFactor, jfloat samplingStrength)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::create_11()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<cv::bioinspired::Retina> Ptr_Retina;
        Size inputSize((int)inputSize_width, (int)inputSize_height);
        Ptr_Retina _retval_ = cv::bioinspired::Retina::create( inputSize, (bool)colorMode, (int)colorSamplingMethod, (bool)useRetinaLogSampling, (float)reductionFactor, (float)samplingStrength );
        return (jlong)(new Ptr_Retina(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_Retina_create_12 (JNIEnv*, jclass, jdouble, jdouble, jboolean, jint, jboolean, jfloat);

JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_Retina_create_12
  (JNIEnv* env, jclass , jdouble inputSize_width, jdouble inputSize_height, jboolean colorMode, jint colorSamplingMethod, jboolean useRetinaLogSampling, jfloat reductionFactor)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::create_12()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<cv::bioinspired::Retina> Ptr_Retina;
        Size inputSize((int)inputSize_width, (int)inputSize_height);
        Ptr_Retina _retval_ = cv::bioinspired::Retina::create( inputSize, (bool)colorMode, (int)colorSamplingMethod, (bool)useRetinaLogSampling, (float)reductionFactor );
        return (jlong)(new Ptr_Retina(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_Retina_create_13 (JNIEnv*, jclass, jdouble, jdouble, jboolean, jint, jboolean);

JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_Retina_create_13
  (JNIEnv* env, jclass , jdouble inputSize_width, jdouble inputSize_height, jboolean colorMode, jint colorSamplingMethod, jboolean useRetinaLogSampling)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::create_13()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<cv::bioinspired::Retina> Ptr_Retina;
        Size inputSize((int)inputSize_width, (int)inputSize_height);
        Ptr_Retina _retval_ = cv::bioinspired::Retina::create( inputSize, (bool)colorMode, (int)colorSamplingMethod, (bool)useRetinaLogSampling );
        return (jlong)(new Ptr_Retina(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_Retina_create_14 (JNIEnv*, jclass, jdouble, jdouble, jboolean, jint);

JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_Retina_create_14
  (JNIEnv* env, jclass , jdouble inputSize_width, jdouble inputSize_height, jboolean colorMode, jint colorSamplingMethod)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::create_14()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<cv::bioinspired::Retina> Ptr_Retina;
        Size inputSize((int)inputSize_width, (int)inputSize_height);
        Ptr_Retina _retval_ = cv::bioinspired::Retina::create( inputSize, (bool)colorMode, (int)colorSamplingMethod );
        return (jlong)(new Ptr_Retina(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_Retina_create_15 (JNIEnv*, jclass, jdouble, jdouble, jboolean);

JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_Retina_create_15
  (JNIEnv* env, jclass , jdouble inputSize_width, jdouble inputSize_height, jboolean colorMode)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::create_15()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<cv::bioinspired::Retina> Ptr_Retina;
        Size inputSize((int)inputSize_width, (int)inputSize_height);
        Ptr_Retina _retval_ = cv::bioinspired::Retina::create( inputSize, (bool)colorMode );
        return (jlong)(new Ptr_Retina(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  native support for java finalize()
//  static void Ptr<cv::bioinspired::Retina>::delete( __int64 self )
//
JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_delete(JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_Retina_delete
  (JNIEnv*, jclass, jlong self)
{
    delete (Ptr<cv::bioinspired::Retina>*) self;
}


//
//  void cv::bioinspired::RetinaFastToneMapping::applyFastToneMapping(Mat inputImage, Mat& outputToneMappedImage)
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_RetinaFastToneMapping_applyFastToneMapping_10 (JNIEnv*, jclass, jlong, jlong, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_RetinaFastToneMapping_applyFastToneMapping_10
  (JNIEnv* env, jclass , jlong self, jlong inputImage_nativeObj, jlong outputToneMappedImage_nativeObj)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::applyFastToneMapping_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::RetinaFastToneMapping>* me = (Ptr<cv::bioinspired::RetinaFastToneMapping>*) self; //TODO: check for NULL
        Mat& inputImage = *((Mat*)inputImage_nativeObj);
        Mat& outputToneMappedImage = *((Mat*)outputToneMappedImage_nativeObj);
        (*me)->applyFastToneMapping( inputImage, outputToneMappedImage );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  void cv::bioinspired::RetinaFastToneMapping::setup(float photoreceptorsNeighborhoodRadius = 3.f, float ganglioncellsNeighborhoodRadius = 1.f, float meanLuminanceModulatorK = 1.f)
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_RetinaFastToneMapping_setup_10 (JNIEnv*, jclass, jlong, jfloat, jfloat, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_RetinaFastToneMapping_setup_10
  (JNIEnv* env, jclass , jlong self, jfloat photoreceptorsNeighborhoodRadius, jfloat ganglioncellsNeighborhoodRadius, jfloat meanLuminanceModulatorK)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setup_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::RetinaFastToneMapping>* me = (Ptr<cv::bioinspired::RetinaFastToneMapping>*) self; //TODO: check for NULL
        (*me)->setup( (float)photoreceptorsNeighborhoodRadius, (float)ganglioncellsNeighborhoodRadius, (float)meanLuminanceModulatorK );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_RetinaFastToneMapping_setup_11 (JNIEnv*, jclass, jlong, jfloat, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_RetinaFastToneMapping_setup_11
  (JNIEnv* env, jclass , jlong self, jfloat photoreceptorsNeighborhoodRadius, jfloat ganglioncellsNeighborhoodRadius)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setup_11()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::RetinaFastToneMapping>* me = (Ptr<cv::bioinspired::RetinaFastToneMapping>*) self; //TODO: check for NULL
        (*me)->setup( (float)photoreceptorsNeighborhoodRadius, (float)ganglioncellsNeighborhoodRadius );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_RetinaFastToneMapping_setup_12 (JNIEnv*, jclass, jlong, jfloat);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_RetinaFastToneMapping_setup_12
  (JNIEnv* env, jclass , jlong self, jfloat photoreceptorsNeighborhoodRadius)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setup_12()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::RetinaFastToneMapping>* me = (Ptr<cv::bioinspired::RetinaFastToneMapping>*) self; //TODO: check for NULL
        (*me)->setup( (float)photoreceptorsNeighborhoodRadius );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_RetinaFastToneMapping_setup_13 (JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_RetinaFastToneMapping_setup_13
  (JNIEnv* env, jclass , jlong self)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setup_13()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::RetinaFastToneMapping>* me = (Ptr<cv::bioinspired::RetinaFastToneMapping>*) self; //TODO: check for NULL
        (*me)->setup();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// static Ptr_RetinaFastToneMapping cv::bioinspired::RetinaFastToneMapping::create(Size inputSize)
//

JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_RetinaFastToneMapping_create_10 (JNIEnv*, jclass, jdouble, jdouble);

JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_RetinaFastToneMapping_create_10
  (JNIEnv* env, jclass , jdouble inputSize_width, jdouble inputSize_height)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::create_10()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<cv::bioinspired::RetinaFastToneMapping> Ptr_RetinaFastToneMapping;
        Size inputSize((int)inputSize_width, (int)inputSize_height);
        Ptr_RetinaFastToneMapping _retval_ = cv::bioinspired::RetinaFastToneMapping::create( inputSize );
        return (jlong)(new Ptr_RetinaFastToneMapping(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  native support for java finalize()
//  static void Ptr<cv::bioinspired::RetinaFastToneMapping>::delete( __int64 self )
//
JNIEXPORT void JNICALL Java_org_opencv_bioinspired_RetinaFastToneMapping_delete(JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_RetinaFastToneMapping_delete
  (JNIEnv*, jclass, jlong self)
{
    delete (Ptr<cv::bioinspired::RetinaFastToneMapping>*) self;
}


//
//  Size cv::bioinspired::TransientAreasSegmentationModule::getSize()
//

JNIEXPORT jdoubleArray JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_getSize_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jdoubleArray JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_getSize_10
  (JNIEnv* env, jclass , jlong self)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::getSize_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::TransientAreasSegmentationModule>* me = (Ptr<cv::bioinspired::TransientAreasSegmentationModule>*) self; //TODO: check for NULL
        Size _retval_ = (*me)->getSize();
        jdoubleArray _da_retval_ = env->NewDoubleArray(2);  jdouble _tmp_retval_[2] = {(jdouble)_retval_.width, (jdouble)_retval_.height}; env->SetDoubleArrayRegion(_da_retval_, 0, 2, _tmp_retval_);
        return _da_retval_;
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  void cv::bioinspired::TransientAreasSegmentationModule::setup(String segmentationParameterFile = "", bool applyDefaultSetupOnFailure = true)
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_setup_10 (JNIEnv*, jclass, jlong, jstring, jboolean);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_setup_10
  (JNIEnv* env, jclass , jlong self, jstring segmentationParameterFile, jboolean applyDefaultSetupOnFailure)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setup_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::TransientAreasSegmentationModule>* me = (Ptr<cv::bioinspired::TransientAreasSegmentationModule>*) self; //TODO: check for NULL
        const char* utf_segmentationParameterFile = env->GetStringUTFChars(segmentationParameterFile, 0); String n_segmentationParameterFile( utf_segmentationParameterFile ? utf_segmentationParameterFile : "" ); env->ReleaseStringUTFChars(segmentationParameterFile, utf_segmentationParameterFile);
        (*me)->setup( n_segmentationParameterFile, (bool)applyDefaultSetupOnFailure );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_setup_11 (JNIEnv*, jclass, jlong, jstring);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_setup_11
  (JNIEnv* env, jclass , jlong self, jstring segmentationParameterFile)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setup_11()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::TransientAreasSegmentationModule>* me = (Ptr<cv::bioinspired::TransientAreasSegmentationModule>*) self; //TODO: check for NULL
        const char* utf_segmentationParameterFile = env->GetStringUTFChars(segmentationParameterFile, 0); String n_segmentationParameterFile( utf_segmentationParameterFile ? utf_segmentationParameterFile : "" ); env->ReleaseStringUTFChars(segmentationParameterFile, utf_segmentationParameterFile);
        (*me)->setup( n_segmentationParameterFile );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_setup_12 (JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_setup_12
  (JNIEnv* env, jclass , jlong self)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::setup_12()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::TransientAreasSegmentationModule>* me = (Ptr<cv::bioinspired::TransientAreasSegmentationModule>*) self; //TODO: check for NULL
        (*me)->setup();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  String cv::bioinspired::TransientAreasSegmentationModule::printSetup()
//

JNIEXPORT jstring JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_printSetup_10 (JNIEnv*, jclass, jlong);

JNIEXPORT jstring JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_printSetup_10
  (JNIEnv* env, jclass , jlong self)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::printSetup_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::TransientAreasSegmentationModule>* me = (Ptr<cv::bioinspired::TransientAreasSegmentationModule>*) self; //TODO: check for NULL
        cv::String _retval_ = (*me)->printSetup();
        return env->NewStringUTF(_retval_.c_str());
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return env->NewStringUTF("");
}



//
//  void cv::bioinspired::TransientAreasSegmentationModule::write(String fs)
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_write_10 (JNIEnv*, jclass, jlong, jstring);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_write_10
  (JNIEnv* env, jclass , jlong self, jstring fs)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::write_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::TransientAreasSegmentationModule>* me = (Ptr<cv::bioinspired::TransientAreasSegmentationModule>*) self; //TODO: check for NULL
        const char* utf_fs = env->GetStringUTFChars(fs, 0); String n_fs( utf_fs ? utf_fs : "" ); env->ReleaseStringUTFChars(fs, utf_fs);
        (*me)->write( n_fs );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  void cv::bioinspired::TransientAreasSegmentationModule::run(Mat inputToSegment, int channelIndex = 0)
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_run_10 (JNIEnv*, jclass, jlong, jlong, jint);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_run_10
  (JNIEnv* env, jclass , jlong self, jlong inputToSegment_nativeObj, jint channelIndex)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::run_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::TransientAreasSegmentationModule>* me = (Ptr<cv::bioinspired::TransientAreasSegmentationModule>*) self; //TODO: check for NULL
        Mat& inputToSegment = *((Mat*)inputToSegment_nativeObj);
        (*me)->run( inputToSegment, (int)channelIndex );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



JNIEXPORT void JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_run_11 (JNIEnv*, jclass, jlong, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_run_11
  (JNIEnv* env, jclass , jlong self, jlong inputToSegment_nativeObj)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::run_11()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::TransientAreasSegmentationModule>* me = (Ptr<cv::bioinspired::TransientAreasSegmentationModule>*) self; //TODO: check for NULL
        Mat& inputToSegment = *((Mat*)inputToSegment_nativeObj);
        (*me)->run( inputToSegment );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  void cv::bioinspired::TransientAreasSegmentationModule::getSegmentationPicture(Mat& transientAreas)
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_getSegmentationPicture_10 (JNIEnv*, jclass, jlong, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_getSegmentationPicture_10
  (JNIEnv* env, jclass , jlong self, jlong transientAreas_nativeObj)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::getSegmentationPicture_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::TransientAreasSegmentationModule>* me = (Ptr<cv::bioinspired::TransientAreasSegmentationModule>*) self; //TODO: check for NULL
        Mat& transientAreas = *((Mat*)transientAreas_nativeObj);
        (*me)->getSegmentationPicture( transientAreas );
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
//  void cv::bioinspired::TransientAreasSegmentationModule::clearAllBuffers()
//

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_clearAllBuffers_10 (JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_clearAllBuffers_10
  (JNIEnv* env, jclass , jlong self)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::clearAllBuffers_10()";
    try {
        LOGD("%s", method_name);
        Ptr<cv::bioinspired::TransientAreasSegmentationModule>* me = (Ptr<cv::bioinspired::TransientAreasSegmentationModule>*) self; //TODO: check for NULL
        (*me)->clearAllBuffers();
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
}



//
// static Ptr_TransientAreasSegmentationModule cv::bioinspired::TransientAreasSegmentationModule::create(Size inputSize)
//

JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_create_10 (JNIEnv*, jclass, jdouble, jdouble);

JNIEXPORT jlong JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_create_10
  (JNIEnv* env, jclass , jdouble inputSize_width, jdouble inputSize_height)
{
    using namespace cv::bioinspired;
    static const char method_name[] = "bioinspired::create_10()";
    try {
        LOGD("%s", method_name);
        typedef Ptr<cv::bioinspired::TransientAreasSegmentationModule> Ptr_TransientAreasSegmentationModule;
        Size inputSize((int)inputSize_width, (int)inputSize_height);
        Ptr_TransientAreasSegmentationModule _retval_ = cv::bioinspired::TransientAreasSegmentationModule::create( inputSize );
        return (jlong)(new Ptr_TransientAreasSegmentationModule(_retval_));
    } catch(const std::exception &e) {
        throwJavaException(env, &e, method_name);
    } catch (...) {
        throwJavaException(env, 0, method_name);
    }
    return 0;
}



//
//  native support for java finalize()
//  static void Ptr<cv::bioinspired::TransientAreasSegmentationModule>::delete( __int64 self )
//
JNIEXPORT void JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_delete(JNIEnv*, jclass, jlong);

JNIEXPORT void JNICALL Java_org_opencv_bioinspired_TransientAreasSegmentationModule_delete
  (JNIEnv*, jclass, jlong self)
{
    delete (Ptr<cv::bioinspired::TransientAreasSegmentationModule>*) self;
}



} // extern "C"

#endif // HAVE_OPENCV_BIOINSPIRED
