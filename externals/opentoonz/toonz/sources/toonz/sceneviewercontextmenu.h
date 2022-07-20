#pragma once

#ifndef SCENE_VIEWER_CONTEXT_MENU
#define SCENE_VIEWER_CONTEXT_MENU

#include <QMenu>
#include "tgeometry.h"

class TStageObjectId;
class SceneViewer;
class TXshColumn;

class SceneViewerContextMenu final : public QMenu {
  Q_OBJECT
  SceneViewer *m_viewer;
  int m_groupIndexToBeEntered;

  void addShowHideCommand(QMenu *menu, TXshColumn *column);
  void addSelectCommand(QMenu *menu, const TStageObjectId &id);

public:
  SceneViewerContextMenu(SceneViewer *parent);
  ~SceneViewerContextMenu();

  void addEnterGroupCommands(const TPointD &pos);
  void addLevelCommands(std::vector<int> &indices);

public slots:

  void savePreviewedFrames();

  void enterVectorImageGroup();
  void exitVectorImageGroup();
  void setGuidedDrawingType(QAction *);
  void setGuidedAutoInbetween();
  void setGuidedInterpolationState(QAction *);

  void onShowHide();
  void onSetCurrent();
};

namespace ZeroThickToggleGui {
void addZeroThickCommand(QMenu *menu);

class ZeroThickToggleHandler : public QObject {
  Q_OBJECT

public slots:
  void activate();
  void deactivate();
};

}  // Namespace ZeroThickToggleGui

namespace CursorOutlineToggleGui {
void addCursorOutlineCommand(QMenu *menu);

class CursorOutlineToggleHandler : public QObject {
  Q_OBJECT

public slots:
  void activate();
  void deactivate();
};

}  // Namespace CursorOutlineToggleGui

#endif
