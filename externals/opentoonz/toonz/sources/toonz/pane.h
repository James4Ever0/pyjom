#pragma once

#ifndef PANE_H
#define PANE_H

// TODO: cambiare il nome del file in tpanel.h

//#include <QDockWidget>
#include "../toonzqt/tdockwindows.h"

class TPanelTitleBarButtonSet;
class Room;

//! icon buttons placed on the panel titlebar (cfr. viewerpane.h)
class TPanelTitleBarButton : public QWidget {
  Q_OBJECT
  QString m_standardPixmapName;
  QPixmap m_standardPixmap;
  QColor m_overColor;
  QColor m_pressedColor;
  QColor m_freezeColor;
  QColor m_previewColor;

  Q_PROPERTY(QColor OverColor READ getOverColor WRITE setOverColor);
  Q_PROPERTY(QColor PressedColor READ getPressedColor WRITE setPressedColor);
  Q_PROPERTY(QColor FreezeColor READ getFreezeColor WRITE setFreezeColor);
  Q_PROPERTY(QColor PreviewColor READ getPreviewColor WRITE setPreviewColor);

  bool m_rollover;
  TPanelTitleBarButtonSet *m_buttonSet;
  int m_id;

protected:
  bool m_pressed;

public:
  TPanelTitleBarButton(QWidget *parent, const QString &standardPixmapName);
  TPanelTitleBarButton(QWidget *parent, const QPixmap &standardPixmap);

  //! call this method to make a radio button. id is the button identifier
  void setButtonSet(TPanelTitleBarButtonSet *buttonSet, int id);
  int getId() const { return m_id; }

  void setOverColor(const QColor &color) { m_overColor = color; }
  QColor getOverColor() const { return m_overColor; }
  void setPressedColor(const QColor &color) { m_pressedColor = color; }
  QColor getPressedColor() const { return m_pressedColor; }
  void setFreezeColor(const QColor &color) { m_freezeColor = color; }
  QColor getFreezeColor() const { return m_freezeColor; }
  void setPreviewColor(const QColor &color) { m_previewColor = color; }
  QColor getPreviewColor() const { return m_previewColor; }

public slots:
  void setPressed(bool pressed);  // n.b. doesn't emit signals. calls update()

protected:
  void paintEvent(QPaintEvent *event) override;

  void mouseMoveEvent(QMouseEvent *event) override;
  void enterEvent(QEvent *) override;
  void leaveEvent(QEvent *) override;
  void mousePressEvent(QMouseEvent *event) override;

signals:
  //! emitted when the user press the button
  //! n.b. the signal is not emitted if the button is part of a buttonset
  void toggled(bool pressed);
};

//-----------------------------------------------------------------------------
/*! specialized button for sage area which enables to choose safe area size by
 * context menu
 */

class TPanelTitleBarButtonForSafeArea final : public TPanelTitleBarButton {
  Q_OBJECT
public:
  TPanelTitleBarButtonForSafeArea(QWidget *parent,
                                  const QString &standardPixmapName)
      : TPanelTitleBarButton(parent, standardPixmapName) {}
  void getSafeAreaNameList(QList<QString> &nameList);

protected:
  void contextMenuEvent(QContextMenuEvent *event) override;
  void mousePressEvent(QMouseEvent *event) override;
protected slots:
  void onSetSafeArea();
};

//-----------------------------------------------------------------------------

//! a buttonset can group different TPanelTitleBarButton
class TPanelTitleBarButtonSet final : public QObject {
  Q_OBJECT
  std::vector<TPanelTitleBarButton *> m_buttons;

public:
  TPanelTitleBarButtonSet();
  ~TPanelTitleBarButtonSet();

  void add(TPanelTitleBarButton *button);
  void select(TPanelTitleBarButton *button);

signals:
  //! emitted when the current button changes. id is the button identifier
  void selected(int id);
};

//-----------------------------------------------------------------------------

class TPanelTitleBar final : public QFrame {
  Q_OBJECT

  bool m_closeButtonHighlighted;
  std::vector<std::pair<QPoint, QWidget *>> m_buttons;

  QPixmap m_borderPm, m_activeBorderPm, m_floatBorderPm, m_floatActiveBorderPm;
  QColor m_titleColor, m_activeTitleColor;

public:
  TPanelTitleBar(QWidget *parent                      = 0,
                 TDockWidget::Orientation orientation = TDockWidget::vertical);

  QSize sizeHint() const override { return minimumSizeHint(); }
  QSize minimumSizeHint() const override;

  // pos = widget position. n.b. if pos.x()<0 then origin is topright corner
  void add(const QPoint &pos, QWidget *widget);

  QPixmap getBorderPixmap() const { return m_borderPm; }
  void setBorderPixmap(const QPixmap &pixmap) { m_borderPm = pixmap; }
  QPixmap getActiveBorderPixmap() const { return m_activeBorderPm; }
  void setActiveBorderPixmap(const QPixmap &pixmap) {
    m_activeBorderPm = pixmap;
  }
  QPixmap getFloatBorderPixmap() const { return m_floatBorderPm; }
  void setFloatBorderPixmap(const QPixmap &pixmap) { m_floatBorderPm = pixmap; }
  QPixmap getFloatActiveBorderPixmap() const { return m_floatActiveBorderPm; }
  void setFloatActiveBorderPixmap(const QPixmap &pixmap) {
    m_floatActiveBorderPm = pixmap;
  }
  QColor getTitleColor() const { return m_titleColor; }
  void setTitleColor(const QColor &color) { m_titleColor = color; }
  QColor getActiveTitleColor() const { return m_activeTitleColor; }
  void setActiveTitleColor(const QColor &color) { m_activeTitleColor = color; }

protected:
  void resizeEvent(QResizeEvent *e) override;

  // To Disable the default context Menu
  void contextMenuEvent(QContextMenuEvent *) override {}

  void paintEvent(QPaintEvent *event) override;
  void mouseMoveEvent(QMouseEvent *event) override;
  void mousePressEvent(QMouseEvent *event) override;
  void mouseDoubleClickEvent(QMouseEvent *) override;

  Q_PROPERTY(QPixmap BorderPixmap READ getBorderPixmap WRITE setBorderPixmap);
  Q_PROPERTY(QPixmap ActiveBorderPixmap READ getActiveBorderPixmap WRITE
                 setActiveBorderPixmap);
  Q_PROPERTY(QPixmap FloatBorderPixmap READ getFloatBorderPixmap WRITE
                 setFloatBorderPixmap);
  Q_PROPERTY(QPixmap FloatActiveBorderPixmap READ getFloatActiveBorderPixmap
                 WRITE setFloatActiveBorderPixmap);
  Q_PROPERTY(QColor TitleColor READ getTitleColor WRITE setTitleColor);
  Q_PROPERTY(QColor ActiveTitleColor READ getActiveTitleColor WRITE
                 setActiveTitleColor);

signals:

  void closeButtonPressed();
  void doubleClick(QMouseEvent *me);
};

//-----------------------------------------------------------------------------

class TPanel : public TDockWidget {
  Q_OBJECT

  QColor
      m_bgcolor;  // overrides palette background color in paint event - Mac fix

  Q_PROPERTY(QColor BGColor READ getBGColor WRITE setBGColor)

  QColor getBGColor() const { return m_bgcolor; }
  void setBGColor(const QColor &color) { m_bgcolor = color; }

  std::string m_panelType;
  bool m_isMaximizable;
  bool m_isMaximized;
  bool m_multipleInstancesAllowed;

  TPanelTitleBar *m_panelTitleBar;

  QList<TPanel *> m_hiddenDockWidgets;
  QByteArray m_currentRoomOldState;

public:
  TPanel(QWidget *parent = 0, Qt::WindowFlags flags = 0,
         TDockWidget::Orientation orientation = TDockWidget::vertical);
  ~TPanel();

  void setPanelType(const std::string &panelType) { m_panelType = panelType; }
  std::string getPanelType() { return m_panelType; }

  void setIsMaximizable(bool value) { m_isMaximizable = value; }
  bool isMaximizable() { return m_isMaximizable; }
  // bool isMaximized() { return m_isMaximized; }
  // void setMaximized(bool isMaximized, Room *room = 0);

  QList<TPanel *> getHiddenDockWidget() const { return m_hiddenDockWidgets; }
  QByteArray getSavedOldState() const { return m_currentRoomOldState; }

  // void setTitleBarWidget(TPanelTitleBar *newTitleBar);

  // si riferisce a istanze multiple dei pannelli floating; default = true
  void allowMultipleInstances(bool allowed) {
    m_multipleInstancesAllowed = allowed;
  }
  bool areMultipleInstancesAllowed() const {
    return m_multipleInstancesAllowed;
  }

  TPanelTitleBar *getTitleBar() const { return m_panelTitleBar; }

  virtual void reset(){};

  virtual int getViewType() { return -1; };
  virtual void setViewType(int viewType){};

  virtual bool widgetInThisPanelIsFocused() {
    // by default, check if the panel content itself has focus
    if (widget())
      return widget()->hasFocus();
    else
      return false;
  };

  virtual void restoreFloatingPanelState();
  virtual void zoomContentsAndFitGeometry(bool forward);

protected:
  void paintEvent(QPaintEvent *) override;
  void enterEvent(QEvent *) override;
  void leaveEvent(QEvent *) override;

  virtual bool isActivatableOnEnter() { return false; }

protected slots:

  void onCloseButtonPressed();
  virtual void widgetFocusOnEnter() {
    // by default, focus the panel content
    if (widget()) widget()->setFocus();
  };
  virtual void widgetClearFocusOnLeave() {
    if (widget()) widget()->clearFocus();
  };

signals:

  void doubleClick(QMouseEvent *me);
  void closeButtonPressed();
};

//-----------------------------------------------------------------------------

class TPanelFactory {
  QString m_panelType;
  static QMap<QString, TPanelFactory *> &tableInstance();

public:
  TPanelFactory(QString panelType);
  ~TPanelFactory();

  QString getPanelType() const { return m_panelType; }

  virtual void initialize(TPanel *panel) = 0;
  virtual TPanel *createPanel(QWidget *parent);
  static TPanel *createPanel(QWidget *parent, QString panelType);
};

//-----------------------------------------------------------------------------

#endif  // PANE_H
