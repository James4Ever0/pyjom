#include "layerheaderpanel.h"

#include <QPainter>
#include <QToolTip>

#include "xsheetviewer.h"
#include "xshcolumnviewer.h"

#include "tapp.h"
#include "toonz/tscenehandle.h"
#include "toonz/txsheethandle.h"
#include "toonz/tobjecthandle.h"

#include "toonz/preferences.h"

using XsheetGUI::ColumnArea;

#if QT_VERSION >= 0x050500
LayerHeaderPanel::LayerHeaderPanel(XsheetViewer *viewer, QWidget *parent,
                                   Qt::WindowFlags flags)
#else
LayerHeaderPanel::LayerHeaderPanel(XsheetViewer *viewer, QWidget *parent,
                                   Qt::WFlags flags)
#endif
    : QWidget(parent, flags), m_viewer(viewer) {
  const Orientation *o = Orientations::leftToRight();
  QRect rect           = o->rect(PredefinedRect::LAYER_HEADER_PANEL);

  setObjectName("layerHeaderPanel");
  setFixedSize(rect.size());
  setMouseTracking(true);
}

LayerHeaderPanel::~LayerHeaderPanel() {}

namespace {

QColor mix(const QColor &a, const QColor &b, double w) {
  return QColor(a.red() * w + b.red() * (1 - w),
                a.green() * w + b.green() * (1 - w),
                a.blue() * w + b.blue() * (1 - w));
}

QColor withAlpha(const QColor &color, double alpha) {
  QColor result(color);
  result.setAlpha(alpha * 255);
  return result;
}

QRect shorter(const QRect original) { return original.adjusted(0, 2, 0, -2); }

QLine leftSide(const QRect &r) { return QLine(r.topLeft(), r.bottomLeft()); }

QLine rightSide(const QRect &r) { return QLine(r.topRight(), r.bottomRight()); }
}

void LayerHeaderPanel::paintEvent(QPaintEvent *event) {
  QPainter p(this);
  p.setRenderHint(QPainter::SmoothPixmapTransform, true);

  const Orientation *o = Orientations::leftToRight();

  QImage preview = (m_buttonHighlighted == PreviewButton
                        ? m_viewer->getLayerHeaderPreviewOverImage()
                        : m_viewer->getLayerHeaderPreviewImage());
  QImage camstand = (m_buttonHighlighted == CamstandButton
                         ? m_viewer->getLayerHeaderCamstandOverImage()
                         : m_viewer->getLayerHeaderCamstandImage());
  QImage lock = (m_buttonHighlighted == LockButton
                     ? m_viewer->getLayerHeaderLockOverImage()
                     : m_viewer->getLayerHeaderLockImage());

  drawIcon(p, PredefinedRect::PANEL_EYE, boost::none, preview);
  drawIcon(p, PredefinedRect::PANEL_PREVIEW_LAYER, boost::none, camstand);
  drawIcon(p, PredefinedRect::PANEL_LOCK, boost::none, lock);
}

void LayerHeaderPanel::drawIcon(QPainter &p, PredefinedRect rect,
                                optional<QColor> fill,
                                const QImage &image) const {
  QRect iconRect =
      Orientations::leftToRight()->rect(rect).adjusted(-2, 0, -2, 0);

  if (fill) p.fillRect(iconRect, *fill);
  p.drawImage(iconRect, image);
}

void LayerHeaderPanel::drawLines(QPainter &p, const QRect &numberRect,
                                 const QRect &nameRect) const {
  p.setPen(withAlpha(m_viewer->getTextColor(), 0.5));

  QLine line = {leftSide(shorter(numberRect)).translated(-2, 0)};
  p.drawLine(line);

  if (Preferences::instance()->isShowColumnNumbersEnabled()) {
    line = rightSide(shorter(numberRect)).translated(-2, 0);
    p.drawLine(line);
  }

  line = rightSide(shorter(nameRect));
  p.drawLine(line);
}

void LayerHeaderPanel::showOrHide(const Orientation *o) {
  QRect rect = o->rect(PredefinedRect::LAYER_HEADER_PANEL);
  if (rect.isEmpty())
    hide();
  else
    show();
}

//-----------------------------------------------------------------------------
void LayerHeaderPanel::enterEvent(QEvent *) {
  m_buttonHighlighted = NoButton;

  update();
}

void LayerHeaderPanel::leaveEvent(QEvent *) {
  m_buttonHighlighted = NoButton;

  update();
}

void LayerHeaderPanel::mousePressEvent(QMouseEvent *event) {
  const Orientation *o = Orientations::leftToRight();

  m_doOnRelease = 0;

  if (event->button() == Qt::LeftButton) {
    // get mouse position
    QPoint pos = event->pos();

    // preview button
    if (o->rect(PredefinedRect::EYE_AREA).contains(pos)) {
      m_doOnRelease = ToggleAllPreviewVisible;
    }
    // camstand button
    else if (o->rect(PredefinedRect::PREVIEW_LAYER_AREA).contains(pos)) {
      m_doOnRelease = ToggleAllTransparency;
    }
    // lock button
    else if (o->rect(PredefinedRect::LOCK_AREA).contains(pos)) {
      m_doOnRelease = ToggleAllLock;
    }
  }

  update();
}

void LayerHeaderPanel::mouseMoveEvent(QMouseEvent *event) {
  const Orientation *o = Orientations::leftToRight();

  QPoint pos          = event->pos();
  m_buttonHighlighted = NoButton;

  // preview button
  if (o->rect(PredefinedRect::EYE_AREA).contains(pos)) {
    m_tooltip           = tr("Preview Visibility Toggle All");
    m_buttonHighlighted = PreviewButton;
  }
  // camstand button
  else if (o->rect(PredefinedRect::PREVIEW_LAYER_AREA).contains(pos)) {
    m_tooltip           = tr("Camera Stand Visibility Toggle All");
    m_buttonHighlighted = CamstandButton;
  }
  // lock button
  else if (o->rect(PredefinedRect::LOCK).contains(pos)) {
    m_tooltip           = tr("Lock Toggle All");
    m_buttonHighlighted = LockButton;
  } else {
    m_tooltip = tr("");
  }

  m_pos = pos;

  update();
}

//-----------------------------------------------------------------------------

bool LayerHeaderPanel::event(QEvent *event) {
  if (event->type() == QEvent::ToolTip) {
    if (!m_tooltip.isEmpty())
      QToolTip::showText(mapToGlobal(m_pos), m_tooltip);
    else
      QToolTip::hideText();
  }
  return QWidget::event(event);
}

//-----------------------------------------------------------------------------

void LayerHeaderPanel::mouseReleaseEvent(QMouseEvent *event) {
  TApp *app    = TApp::instance();
  TXsheet *xsh = m_viewer->getXsheet();
  int col, totcols = xsh->getColumnCount();
  bool sound_changed = false;

  if (m_doOnRelease != 0 && totcols > 0) {
    int startCol =
        Preferences::instance()->isXsheetCameraColumnVisible() ? -1 : 0;
    for (col = startCol; col < totcols; col++) {
      if (startCol < 0 || !xsh->isColumnEmpty(col)) {
        TXshColumn *column = xsh->getColumn(col);

        if (m_doOnRelease == ToggleAllPreviewVisible) {
          column->setPreviewVisible(!column->isPreviewVisible());
        } else if (m_doOnRelease == ToggleAllTransparency) {
          column->setCamstandVisible(!column->isCamstandVisible());
          if (column->getSoundColumn()) sound_changed = true;
        } else if (m_doOnRelease == ToggleAllLock) {
          column->lock(!column->isLocked());
        }
      }
    }

    if (sound_changed) {
      app->getCurrentXsheet()->notifyXsheetSoundChanged();
    }

    app->getCurrentScene()->notifySceneChanged();
    app->getCurrentXsheet()->notifyXsheetChanged();
  }
  m_viewer->updateColumnArea();
  update();
  m_doOnRelease = 0;
}
