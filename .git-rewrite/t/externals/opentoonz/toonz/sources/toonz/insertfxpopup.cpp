

#include "insertfxpopup.h"

// Tnz6 includes
#include "menubarcommandids.h"
#include "tapp.h"

// TnzQt includes
#include "toonzqt/menubarcommand.h"
#include "toonzqt/gutil.h"
#include "toonzqt/fxselection.h"
#include "toonzqt/tselectionhandle.h"
#include "toonzqt/pluginloader.h"  // inter-module plugin loader accessor

// TnzLib includes
#include "toonz/tscenehandle.h"
#include "toonz/txsheethandle.h"
#include "toonz/tframehandle.h"
#include "toonz/tcolumnhandle.h"
#include "toonz/tfxhandle.h"
#include "toonz/toonzscene.h"
#include "toonz/txsheet.h"
#include "toonz/fxdag.h"
#include "toonz/tcolumnfx.h"
#include "toonz/txshlevelcolumn.h"
#include "toonz/tcolumnfxset.h"
#include "toonz/tstageobjecttree.h"
#include "toonz/txshzeraryfxcolumn.h"
#include "toonz/toonzfolders.h"
#include "toonz/scenefx.h"
#include "toonz/fxcommand.h"

#include "tw/stringtable.h"

// TnzBase includes
#include "tdoubleparam.h"
#include "tparamcontainer.h"
#include "tmacrofx.h"
#include "tfx.h"
#include "texternfx.h"

// TnzCore includes
#include "tsystem.h"

// Qt includes
#include <QPushButton>
#include <QTreeWidget>
#include <QHBoxLayout>
#include <QHeaderView>
#include <QMenu>
#include <QContextMenuEvent>
#include <QMainWindow>
#include <QLineEdit>
#include <QLabel>

#include <memory>

using namespace DVGui;

//=============================================================================
namespace {
//-----------------------------------------------------------------------------

TFx *createFxByName(const std::string &fxId) {
  if (fxId.find("_ext_") == 0) {
    return TExternFx::create(fxId.substr(5));
  }
  if (fxId.find("_plg_") == 0) {
    return PluginLoader::create_host(fxId);
  }
  return TFx::create(fxId);
}

//-----------------------------------------------------------------------------

TFx *createPresetFxByName(TFilePath path) {
  const std::string &id = path.getParentDir().getName();

  TFx *fx = createFxByName(id);
  if (fx) {
    TIStream is(path);
    fx->loadPreset(is);
    fx->setName(path.getWideName());
  }

  return fx;
}

//-----------------------------------------------------------------------------
// same as createMacroFxByPath() in addfxcontextmenu.cpp

TFx *createMacroFxByPath(TFilePath path) {
  try {
    TIStream is(path);
    TPersist *p = 0;
    is >> p;
    TMacroFx *fx = dynamic_cast<TMacroFx *>(p);
    if (!fx) return 0;
    fx->setName(path.getWideName());
    // Assign a unic ID to each fx in the macro!
    TApp *app    = TApp::instance();
    TXsheet *xsh = app->getCurrentXsheet()->getXsheet();
    if (!xsh) return fx;
    FxDag *fxDag = xsh->getFxDag();
    if (!fxDag) return fx;
    std::vector<TFxP> fxs;
    fxs = fx->getFxs();
    QMap<std::wstring, std::wstring> oldNewId;
    int i;
    for (i = 0; i < fxs.size(); i++) {
      std::wstring oldId = fxs[i]->getFxId();
      fxDag->assignUniqueId(fxs[i].getPointer());
      std::wstring newId = fxs[i]->getFxId();
      oldNewId[oldId]    = newId;

      // changing the id of the internal effects of a macro breaks the links
      // between the name of the port and the port to which it is linked :
      // I have to change the names of the ports and remap them within the macro
      int j;
      for (j = 0; j < fx->getInputPortCount(); j++) {
        QString inputName = QString::fromStdString(fx->getInputPortName(j));
        if (inputName.endsWith(QString::fromStdWString(oldId))) {
          QString newInputName = inputName;
          newInputName.replace(QString::fromStdWString(oldId),
                               QString::fromStdWString(newId));
          fx->renamePort(inputName.toStdString(), newInputName.toStdString());
        }
      }
    }

    return fx;
  } catch (...) {
    return 0;
  }
}

}  // anonymous namespace
//-----------------------------------------------------------------------------

//=============================================================================
// FxTree
//=============================================================================

void FxTree::displayAll(QTreeWidgetItem *item) {
  int childCount = item->childCount();
  for (int i = 0; i < childCount; ++i) {
    displayAll(item->child(i));
  }
  item->setHidden(false);
  item->setExpanded(false);
}

//-------------------------------------------------------------------

void FxTree::hideAll(QTreeWidgetItem *item) {
  int childCount = item->childCount();
  for (int i = 0; i < childCount; ++i) {
    hideAll(item->child(i));
  }
  item->setHidden(true);
  item->setExpanded(false);
}

//-------------------------------------------------------------------

void FxTree::searchItems(const QString &searchWord) {
  // if search word is empty, show all items
  if (searchWord.isEmpty()) {
    int itemCount = topLevelItemCount();
    for (int i = 0; i < itemCount; ++i) {
      displayAll(topLevelItem(i));
    }
    update();
    return;
  }

  // hide all items first
  int itemCount = topLevelItemCount();
  for (int i = 0; i < itemCount; ++i) {
    hideAll(topLevelItem(i));
  }

  QList<QTreeWidgetItem *> foundItems =
      findItems(searchWord, Qt::MatchContains | Qt::MatchRecursive, 0);
  if (foundItems.isEmpty()) {  // if nothing is found, do nothing but update
    update();
    return;
  }

  // for each item found, show it and show its parent
  for (auto item : foundItems) {
    while (item) {
      item->setHidden(false);
      item->setExpanded(true);
      item = item->parent();
    }
  }

  update();
}

//=============================================================================
/*! \class InsertFxPopup
                \brief The InsertFxPopup class provides a dialog to browse fx
   and add it to
                current scene.

                Inherits \b Dialog.
*/
InsertFxPopup::InsertFxPopup()
    : Dialog(TApp::instance()->getMainWindow(), true, false, "InsertFx")
    , m_folderIcon(QIcon())
    , m_presetIcon(QIcon())
    , m_fxIcon(QIcon()) {
  setWindowTitle(tr("FX Browser"));

  setModal(false);

  setTopMargin(0);
  setTopSpacing(0);

  QHBoxLayout *searchLay = new QHBoxLayout();
  QLineEdit *searchEdit  = new QLineEdit(this);

  searchLay->setMargin(0);
  searchLay->setSpacing(5);
  searchLay->addWidget(new QLabel(tr("Search:"), this), 0);
  searchLay->addWidget(searchEdit);
  addLayout(searchLay);
  connect(searchEdit, SIGNAL(textChanged(const QString &)), this,
          SLOT(onSearchTextChanged(const QString &)));

  m_fxTree = new FxTree();
  m_fxTree->setIconSize(QSize(21, 18));
  m_fxTree->setColumnCount(1);
  m_fxTree->header()->close();

  m_fxTree->setObjectName("FxTreeView");
  m_fxTree->setAlternatingRowColors(true);

  m_presetIcon = createQIcon("folder_preset", true);
  m_fxIcon     = createQIcon("fx");

  QList<QTreeWidgetItem *> fxItems;

  TFilePath path = TFilePath(ToonzFolder::getProfileFolder() + "layouts" +
                             "fxs" + "fxs.lst");
  m_presetFolder = TFilePath(ToonzFolder::getFxPresetFolder() + "presets");
  loadFx(path);
  loadMacro();

  // add 'Plugins' directory
  auto plugins =
      new QTreeWidgetItem((QTreeWidget *)NULL, QStringList("Plugins"));
  plugins->setIcon(0, createQIcon("folder", true));
  m_fxTree->addTopLevelItem(plugins);

  // create vendor / Fx

  // send a special setup for the menu item
  std::map<std::string, QTreeWidgetItem *> vendors =
      PluginLoader::create_menu_items(
          [&](QTreeWidgetItem *firstlevel_item) {
            plugins->addChild(firstlevel_item);
            firstlevel_item->setIcon(0, createQIcon("folder"));
          },
          [&](QTreeWidgetItem *secondlevel_item) {
            secondlevel_item->setIcon(0, m_fxIcon);
          });

  m_fxTree->insertTopLevelItems(0, fxItems);
  connect(m_fxTree, SIGNAL(itemDoubleClicked(QTreeWidgetItem *, int)),
          SLOT(onItemDoubleClicked(QTreeWidgetItem *, int)));

  addWidget(m_fxTree);

  QPushButton *insertBtn = new QPushButton(tr("Insert"), this);
  insertBtn->setFixedSize(65, 25);
  insertBtn->setObjectName("PushButton_NoPadding");
  connect(insertBtn, SIGNAL(clicked()), this, SLOT(onInsert()));
  insertBtn->setDefault(true);
  m_buttonLayout->addWidget(insertBtn);

  QPushButton *addBtn = new QPushButton(tr("Add"), this);
  addBtn->setFixedSize(65, 25);
  addBtn->setObjectName("PushButton_NoPadding");
  connect(addBtn, SIGNAL(clicked()), this, SLOT(onAdd()));
  m_buttonLayout->addWidget(addBtn);

  QPushButton *replaceBtn = new QPushButton(tr("Replace"), this);
  replaceBtn->setFixedHeight(25);
  replaceBtn->setObjectName("PushButton_NoPadding");
  connect(replaceBtn, SIGNAL(clicked()), this, SLOT(onReplace()));
  m_buttonLayout->addWidget(replaceBtn);
}

//-------------------------------------------------------------------

void InsertFxPopup::onSearchTextChanged(const QString &text) {
  static bool busy = false;
  if (busy) return;
  busy = true;
  m_fxTree->searchItems(text);
  busy = false;
}

//-------------------------------------------------------------------

void InsertFxPopup::makeItem(QTreeWidgetItem *parent, std::string fxId) {
  QTreeWidgetItem *fxItem = new QTreeWidgetItem(
      (QTreeWidget *)0,
      QStringList(QString::fromStdWString(TStringTable::translate(fxId))));

  fxItem->setData(0, Qt::UserRole, QVariant(QString::fromStdString(fxId)));
  parent->addChild(fxItem);

  fxItem->setIcon(0, loadPreset(fxItem) ? m_presetIcon : m_fxIcon);
}

//-------------------------------------------------------------------

void InsertFxPopup::loadFolder(QTreeWidgetItem *parent) {
  while (!m_is->eos()) {
    std::string tagName;
    if (m_is->matchTag(tagName)) {
      // Found a sub-folder
      QString folderName = QString::fromStdString(tagName);

      std::unique_ptr<QTreeWidgetItem> folder(
          new QTreeWidgetItem((QTreeWidget *)0, QStringList(folderName)));
      folder->setIcon(0, createQIcon("folder", true));

      loadFolder(folder.get());
      m_is->closeChild();

      if (folder->childCount()) {
        if (parent)
          parent->addChild(folder.release());
        else
          m_fxTree->addTopLevelItem(folder.release());
      }
    } else {
      // Found an fx
      std::string fxName;
      *m_is >> fxName;

      makeItem(parent, fxName);
    }
  }
}

//-------------------------------------------------------------------

bool InsertFxPopup::loadFx(TFilePath fp) {
  TIStream is(fp);
  if (!is) return false;
  m_is = &is;
  try {
    std::string tagName;
    if (m_is->matchTag(tagName) && tagName == "fxs") {
      loadFolder(0);
      m_is->closeChild();
    }
  } catch (...) {
    m_is = 0;
    return false;
  }
  m_is = 0;

  return true;
}

//-------------------------------------------------------------------

bool InsertFxPopup::loadPreset(QTreeWidgetItem *item) {
  QString str = item->data(0, Qt::UserRole).toString();
  TFilePath presetsFilepath(m_presetFolder + str.toStdWString());
  int i;
  for (i = item->childCount() - 1; i >= 0; i--)
    item->removeChild(item->child(i));
  if (TFileStatus(presetsFilepath).isDirectory()) {
    TFilePathSet presets = TSystem::readDirectory(presetsFilepath);
    if (!presets.empty()) {
      for (TFilePathSet::iterator it2 = presets.begin(); it2 != presets.end();
           ++it2) {
        TFilePath presetPath = *it2;
        QString name(presetPath.getName().c_str());
        QTreeWidgetItem *presetItem =
            new QTreeWidgetItem((QTreeWidget *)0, QStringList(name));
        presetItem->setData(0, Qt::UserRole, QVariant(toQString(presetPath)));
        item->addChild(presetItem);
        presetItem->setIcon(0, m_fxIcon);
      }
    } else
      return false;
  } else
    return false;

  return true;
}

//-------------------------------------------------------------------

void InsertFxPopup::loadMacro() {
  TFilePath fp = m_presetFolder + TFilePath("macroFx");
  try {
    if (TFileStatus(fp).isDirectory()) {
      TFilePathSet macros = TSystem::readDirectory(fp);
      if (macros.empty()) return;

      QTreeWidgetItem *macroFolder =
          new QTreeWidgetItem((QTreeWidget *)0, QStringList(tr("Macro")));
      macroFolder->setData(0, Qt::UserRole, QVariant(toQString(fp)));
      macroFolder->setIcon(0, createQIcon("folder", true));
      m_fxTree->addTopLevelItem(macroFolder);
      for (TFilePathSet::iterator it = macros.begin(); it != macros.end();
           ++it) {
        TFilePath macroPath = *it;
        QString name(macroPath.getName().c_str());
        QTreeWidgetItem *macroItem =
            new QTreeWidgetItem((QTreeWidget *)0, QStringList(name));
        macroItem->setData(0, Qt::UserRole, QVariant(toQString(macroPath)));
        macroItem->setIcon(0, m_fxIcon);
        macroFolder->addChild(macroItem);
      }
    }
  } catch (...) {
  }
}

//-----------------------------------------------------------------------------

void InsertFxPopup::onItemDoubleClicked(QTreeWidgetItem *w, int c) {
  if (w->childCount() == 0)  // E' una foglia
    onInsert();
}

//-----------------------------------------------------------------------------

void InsertFxPopup::onInsert() {
  TFx *fx = createFx();
  if (fx) {
    TApp *app                = TApp::instance();
    TXsheetHandle *xshHandle = app->getCurrentXsheet();
    QList<TFxP> fxs;
    QList<TFxCommand::Link> links;
    FxSelection *selection =
        dynamic_cast<FxSelection *>(app->getCurrentSelection()->getSelection());
    if (selection) {
      fxs   = selection->getFxs();
      links = selection->getLinks();
    }
    TFxCommand::insertFx(fx, fxs, links, app,
                         app->getCurrentColumn()->getColumnIndex(),
                         app->getCurrentFrame()->getFrameIndex());
    xshHandle->notifyXsheetChanged();
  }
}

//-----------------------------------------------------------------------------

void InsertFxPopup::onAdd() {
  TFx *fx = createFx();
  if (fx) {
    TApp *app                = TApp::instance();
    TXsheetHandle *xshHandle = app->getCurrentXsheet();
    QList<TFxP> fxs;
    FxSelection *selection =
        dynamic_cast<FxSelection *>(app->getCurrentSelection()->getSelection());
    if (selection) fxs = selection->getFxs();
    TFxCommand::addFx(fx, fxs, app, app->getCurrentColumn()->getColumnIndex(),
                      app->getCurrentFrame()->getFrameIndex());
    xshHandle->notifyXsheetChanged();
  }
}

//-----------------------------------------------------------------------------

void InsertFxPopup::onReplace() {
  TFx *fx = createFx();
  if (fx) {
    TApp *app                = TApp::instance();
    TXsheetHandle *xshHandle = app->getCurrentXsheet();
    QList<TFxP> fxs;
    FxSelection *selection =
        dynamic_cast<FxSelection *>(app->getCurrentSelection()->getSelection());
    if (selection) fxs = selection->getFxs();
    TFxCommand::replaceFx(fx, fxs, app->getCurrentXsheet(),
                          app->getCurrentFx());
    xshHandle->notifyXsheetChanged();
  }
}

//-----------------------------------------------------------------------------

TFx *InsertFxPopup::createFx() {
  TApp *app         = TApp::instance();
  ToonzScene *scene = app->getCurrentScene()->getScene();
  TXsheet *xsh      = scene->getXsheet();

  QTreeWidgetItem *item = m_fxTree->currentItem();
  if (item == NULL) return 0;

  QString text = item->data(0, Qt::UserRole).toString();
  if (text.isEmpty()) return 0;

  TFx *fx;

  TFilePath path = TFilePath(text.toStdWString());

  if (TFileStatus(path).doesExist() &&
      TFileStatus(path.getParentDir()).isDirectory()) {
    std::string folder = path.getParentDir().getName();
    if (folder == "macroFx")  // Devo caricare una macro
      fx = createMacroFxByPath(path);
    else  // Verifico se devo caricare un preset
    {
      folder = path.getParentDir().getParentDir().getName();
      if (folder == "presets")  // Devo caricare un preset
        fx = createPresetFxByName(path);
    }
  } else
    fx = createFxByName(text.toStdString());

  if (fx)
    return fx;
  else
    return 0;
}

//-----------------------------------------------------------------------------

void InsertFxPopup::showEvent(QShowEvent *) {
  updatePresets();
  connect(TApp::instance()->getCurrentFx(), SIGNAL(fxPresetSaved()),
          SLOT(updatePresets()));
}

//-----------------------------------------------------------------------------

void InsertFxPopup::hideEvent(QHideEvent *e) {
  disconnect(TApp::instance()->getCurrentFx(), SIGNAL(fxPresetSaved()), this,
             SLOT(updatePresets()));
  Dialog::hideEvent(e);
}

//-----------------------------------------------------------------------------

void InsertFxPopup::contextMenuEvent(QContextMenuEvent *event) {
  QTreeWidgetItem *item = m_fxTree->currentItem();
  QString itemRole      = item->data(0, Qt::UserRole).toString();

  TFilePath path = TFilePath(itemRole.toStdWString());
  if (TFileStatus(path).doesExist() &&
      TFileStatus(path.getParentDir()).isDirectory()) {
    QMenu *menu        = new QMenu(this);
    std::string folder = path.getParentDir().getName();
    if (folder == "macroFx")  // Menu' macro
    {
      QAction *remove = new QAction(tr("Remove Macro FX"), menu);
      connect(remove, SIGNAL(triggered()), this, SLOT(removePreset()));
      menu->addAction(remove);
    } else  // Verifico se devo caricare un preset
    {
      folder = path.getParentDir().getParentDir().getName();
      if (folder == "presets")  // Menu' preset
      {
        QAction *remove = new QAction(tr("Remove Preset"), menu);
        connect(remove, SIGNAL(triggered()), this, SLOT(removePreset()));
        menu->addAction(remove);
      }
    }
    menu->exec(event->globalPos());
  }
}

//-------------------------------------------------------------------

void InsertFxPopup::updatePresets() {
  int i;
  for (i = 0; i < m_fxTree->topLevelItemCount(); i++) {
    QTreeWidgetItem *folder = m_fxTree->topLevelItem(i);
    TFilePath path =
        TFilePath(folder->data(0, Qt::UserRole).toString().toStdWString());
    if (folder->text(0).toStdString() == "Plugins") {
      continue;
    }
    if (path.getName() == "macroFx") {
      int j;
      for (j = folder->childCount() - 1; j >= 0; j--)
        folder->removeChild(folder->child(j));
      m_fxTree->removeItemWidget(folder, 0);
      delete folder;
    } else if (path.getParentDir().getName() == "macroFx")
      continue;
    else
      for (int i = 0; i < folder->childCount(); i++) {
        bool isPresetLoaded = loadPreset(folder->child(i));
        if (isPresetLoaded)
          folder->child(i)->setIcon(0, m_presetIcon);
        else
          folder->child(i)->setIcon(0, m_fxIcon);
      }
  }
  loadMacro();

  update();
}

//-----------------------------------------------------------------------------

void InsertFxPopup::removePreset() {
  QTreeWidgetItem *item = m_fxTree->currentItem();
  QString itemRole      = item->data(0, Qt::UserRole).toString();

  TFilePath path = TFilePath(itemRole.toStdWString());

  QString question = QString(
      tr("Are you sure you want to delete %1?").arg(path.getName().c_str()));
  int ret = DVGui::MsgBox(question, tr("Yes"), tr("No"), 1);
  if (ret == 2 || ret == 0) return;

  try {
    TSystem::deleteFile(path);
  } catch (...) {
    error(QString(tr("It is not possible to delete %1.").arg(toQString(path))));
    return;
  }
  m_fxTree->removeItemWidget(item, 0);
  delete item;
  TApp::instance()->getCurrentFx()->notifyFxPresetRemoved();
}

//=============================================================================

OpenPopupCommandHandler<InsertFxPopup> openInsertFxPopup(MI_InsertFx);
