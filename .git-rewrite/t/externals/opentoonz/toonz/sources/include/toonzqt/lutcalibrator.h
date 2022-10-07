#pragma once

#ifndef LUT_CALIBRATOR_H
#define LUT_CALIBRATOR_H

#include "tcommon.h"
#include "tpixelutils.h"

#include <QOpenGLBuffer>
#include <QMatrix4x4>
#include <QOpenGLFunctions>
#include <QSet>

#undef DVAPI
#undef DVVAR
#ifdef TOONZQT_EXPORTS
#define DVAPI DV_EXPORT_API
#define DVVAR DV_EXPORT_VAR
#else
#define DVAPI DV_IMPORT_API
#define DVVAR DV_IMPORT_VAR
#endif

class QOpenGLShader;
class QOpenGLShaderProgram;
class QOpenGLFramebufferObject;
class QOpenGLTexture;
class QOpenGLContext;

class QColor;

class DVAPI LutCalibrator : public QOpenGLFunctions {
  bool m_isValid       = false;
  bool m_isInitialized = false;

  struct LutTextureShader {
    QOpenGLShader* vert           = nullptr;
    QOpenGLShader* frag           = nullptr;
    QOpenGLShaderProgram* program = nullptr;
    int texUniform                = -1;
    int lutUniform                = -1;
    int lutSizeUniform            = -1;
    int vertexAttrib              = -1;
    int texCoordAttrib            = -1;
  } m_shader;

  QOpenGLTexture* m_lutTex = NULL;

  QOpenGLBuffer m_viewerVBO;

  bool initializeLutTextureShader();
  void createViewerVBO();
  void assignLutTexture();

public:
  // static LutCalibrator* instance();
  LutCalibrator();
  ~LutCalibrator();

  // to be computed once through the software
  void initialize();

  bool isValid() { return m_isValid; }
  bool isInitialized() { return m_isInitialized; }

  void onEndDraw(QOpenGLFramebufferObject*);

  void cleanup();
  void update(bool textureChanged);
};

class DVAPI LutManager  // singleton
{
  bool m_isValid;
  QString m_currentLutPath;
  QSet<LutCalibrator*> m_calibrators;

  LutManager();

  struct Lut {
    int meshSize;
    float* data = nullptr;
  } m_lut;

public:
  static LutManager* instance();

  ~LutManager();

  bool isValid() { return m_isValid; }
  int meshSize() const { return m_lut.meshSize; }
  float* data() const { return m_lut.data; }

  bool loadLutFile(const QString& fp);

  void convert(float&, float&, float&);
  void convert(QColor&);
  void convert(TPixel32&);

  QString& getMonitorName() const;

  void registerCalibrator(LutCalibrator* calibrator);
  void removeCalibrator(LutCalibrator* calibrator);

  void update();
};

#endif