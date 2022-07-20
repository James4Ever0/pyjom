#pragma once

#ifndef IWA_BOKEH_UTIL_H
#define IWA_BOKEH_UTIL_H

#include "tgeometry.h"
#include "traster.h"
#include "kiss_fft.h"
#include "tools/kiss_fftnd.h"
#include "ttile.h"
#include "stdfx.h"
#include "tfxparam.h"

#include <QThread>
#include <QVector>

struct double4 {
  double x, y, z, w;
};

struct double2 {
  double x, y;
};

struct int2 {
  int x, y;
};

namespace BokehUtils {

//------------------------------------

class MyThread : public QThread {
public:
  enum Channel { Red = 0, Green, Blue };

private:
  int m_channel;

  volatile bool m_finished;

  TRasterP m_layerTileRas;
  double4* m_result;
  double* m_alpha_bokeh;

  kiss_fft_cpx* m_kissfft_comp_iris;

  double m_layerHardness;
  double m_masterHardness;

  TRasterGR8P m_kissfft_comp_in_ras, m_kissfft_comp_out_ras;
  kiss_fft_cpx *m_kissfft_comp_in, *m_kissfft_comp_out;
  kiss_fftnd_cfg m_kissfft_plan_fwd, m_kissfft_plan_bkwd;

  bool m_isTerminated;

  // not used for now
  bool m_doLightenComp;

public:
  MyThread(Channel channel, TRasterP layerTileRas, double4* result,
           double* alpha_bokeh, kiss_fft_cpx* kissfft_comp_iris,
           double layerHardness, double masterHardness = 0.0,
           bool doLightenComp = false);  // not used for now

  // Convert the pixels from RGB values to exposures and multiply it by alpha
  // channel value.
  // Store the results in the real part of kiss_fft_cpx.
  template <typename RASTER, typename PIXEL>
  void setLayerRaster(const RASTER srcRas, kiss_fft_cpx* dstMem,
                      TDimensionI dim);

  void run();

  bool isFinished() { return m_finished; }

  //�������m��
  bool init();

  void terminateThread() { m_isTerminated = true; }

  bool checkTerminationAndCleanupThread();
};

//------------------------------------

class BokehRefThread : public QThread {
  int m_channel;
  volatile bool m_finished;

  kiss_fft_cpx* m_fftcpx_channel_before;
  kiss_fft_cpx* m_fftcpx_channel;
  kiss_fft_cpx* m_fftcpx_alpha;
  kiss_fft_cpx* m_fftcpx_iris;
  double4* m_result_buff;

  kiss_fftnd_cfg m_kissfft_plan_fwd, m_kissfft_plan_bkwd;

  TDimensionI m_dim;
  bool m_isTerminated;

public:
  BokehRefThread(int channel, kiss_fft_cpx* fftcpx_channel_before,
                 kiss_fft_cpx* fftcpx_channel, kiss_fft_cpx* fftcpx_alpha,
                 kiss_fft_cpx* fftcpx_iris, double4* result_buff,
                 kiss_fftnd_cfg kissfft_plan_fwd,
                 kiss_fftnd_cfg kissfft_plan_bkwd, TDimensionI& dim);

  void run() override;

  bool isFinished() { return m_finished; }
  void terminateThread() { m_isTerminated = true; }
};

//------------------------------------

// normalize the source raster image to 0-1 and set to dstMem
// returns true if the source is (seems to be) premultiplied
template <typename RASTER, typename PIXEL>
void setSourceRaster(const RASTER srcRas, double4* dstMem, TDimensionI dim);

// normalize brightness of the depth reference image to unsigned char
// and store into dstMem
template <typename RASTER, typename PIXEL>
void setDepthRaster(const RASTER srcRas, unsigned char* dstMem,
                    TDimensionI dim);

// create the depth index map
void defineSegemntDepth(
    const unsigned char* indexMap_main, const unsigned char* indexMap_sub,
    const double* mainSub_ratio, const unsigned char* depth_host,
    const TDimensionI& dimOut, QVector<double>& segmentDepth_main,
    QVector<double>& segmentDepth_sub, const double focusDepth,
    int distancePrecision = 10, double nearDepth = 0.0, double farDepth = 1.0);

// convert source image value rgb -> exposure
void convertRGBToExposure(const double4* source_buff, int size,
                          double filmGamma);

// convert result image value exposure -> rgb
void convertExposureToRGB(const double4* result_buff, int size,
                          double filmGamma);

// obtain iris size from the depth value
double calcIrisSize(const double depth, const double bokehPixelAmount,
                    const double onFocusDistance,
                    const double bokehAdjustment = 1.0, double nearDepth = 0.0,
                    double farDepth = 1.0);

// generate the segment layer source at the current depth
// considering fillGap and doMedian options
void retrieveLayer(const double4* source_buff,
                   const double4* segment_layer_buff,
                   const unsigned char* indexMap_mainSub, int index, int lx,
                   int ly, bool fillGap = true, bool doMedian = false,
                   int margin = 0);

// normal-composite the layer as is, without filtering
void compositeAsIs(const double4* segment_layer_buff,
                   const double4* result_buff_mainSub, int size);

// Resize / flip the iris image according to the size ratio.
// Normalize the brightness of the iris image.
// Enlarge the iris to the output size.
void convertIris(const double irisSize, kiss_fft_cpx* kissfft_comp_iris_before,
                 const TDimensionI& dimOut, const TRectD& irisBBox,
                 const TTile& irisTile);

// retrieve segment layer image for each channel
void retrieveChannel(const double4* segment_layer_buff,  // src
                     kiss_fft_cpx* fftcpx_r_before,      // dst
                     kiss_fft_cpx* fftcpx_g_before,      // dst
                     kiss_fft_cpx* fftcpx_b_before,      // dst
                     kiss_fft_cpx* fftcpx_a_before,      // dst
                     int size);

// multiply filter on channel
void multiplyFilter(kiss_fft_cpx* fftcpx_channel,  // dst
                    kiss_fft_cpx* fftcpx_iris,     // filter
                    int size);

// normal comosite the alpha channel
void compositeAlpha(const double4* result_buff,        // dst
                    const kiss_fft_cpx* fftcpx_alpha,  // alpha
                    int lx, int ly);

// interpolate main and sub exposures
// set to result
void interpolateExposureAndConvertToRGB(
    const double4* result_main_buff,  // result1
    const double4* result_sub_buff,   // result2
    const double* mainSub_ratio,      // ratio
    const double4* result_buff,       // dst
    int size, double layerHardnessRatio = 1.0);

//"Over" composite the layer to the output exposure.
void compositLayerAsIs(TTile& layerTile, double4* result, TDimensionI& dimOut,
                       double filmGamma);

// Do FFT the alpha channel.
// Forward FFT -> Multiply by the iris data -> Backward FFT
void calcAlfaChannelBokeh(kiss_fft_cpx* kissfft_comp_iris, TTile& layerTile,
                          double* alpha_bokeh);

// convert to channel value and set to output
template <typename RASTER, typename PIXEL>
void setOutputRaster(double4* src, const RASTER dstRas, TDimensionI& dim,
                     int2 margin);

// Get the pixel size of bokehAmount ( referenced ino_blur.cpp )
double getBokehPixelAmount(const double bokehAmount, const TAffine affine);
}  // namespace BokehUtils

//-----------------------------------------------------

class Iwa_BokehCommonFx : public TStandardRasterFx {
protected:
  TRasterFxPort m_iris;
  TDoubleParamP m_onFocusDistance;  // Focus Distance (0-1)
  TDoubleParamP m_bokehAmount;  // The maximum bokeh size. The size of bokeh at
                                // the layer separated by 1.0 from the focal
                                // position
  TDoubleParamP m_hardness;     // Film gamma

  struct LayerValue {
    TTile* sourceTile;
    // set to false if the input image is already premultiplied.
    // this parameter is now always false (assuming input images are always
    // premultiplied). the value is left to keep backward compatibility
    bool premultiply;
    double layerHardness;
    int depth_ref;

    double irisSize;

    double distance;
    double bokehAdjustment;
    double depthRange;
    int distancePrecision;
    bool fillGap;
    bool doMedian;
  };

  void doFx(TTile& tile, double frame, const TRenderSettings& settings,
            double bokehPixelAmount, int margin, TDimensionI& dimOut,
            TRectD& irisBBox, TTile& irisTile, QList<LayerValue>& layerValues,
            QMap<int, unsigned char*>& ctrls);

  void doBokehRef(double4* result, double frame,
                  const TRenderSettings& settings, double bokehPixelAmount,
                  int margin, TDimensionI& dimOut, TRectD& irisBBox,
                  TTile& irisTile, kiss_fft_cpx* kissfft_comp_iris,
                  LayerValue layer, unsigned char* ctrl);

public:
  Iwa_BokehCommonFx();

  void doCompute(TTile& tile, double frame,
                 const TRenderSettings& settings) override = 0;

  bool doGetBBox(double frame, TRectD& bBox,
                 const TRenderSettings& info) final override;

  bool canHandle(const TRenderSettings& info, double frame) final override;
};

#endif
