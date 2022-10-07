#include <memory>

#include "tmachine.h"
#include "tsio_mp3.h"
#include "tsystem.h"
#include "tfilepath_io.h"
#include "tsound_t.h"
#include "toonz/preferences.h"
#include "toonz/toonzfolders.h"
#include <QDir>
#include <QProcess>

//==============================================================================

TSoundTrackReaderMp3::TSoundTrackReaderMp3(const TFilePath &fp)
    : TSoundTrackReader(fp) {}

//------------------------------------------------------------------------------

TSoundTrackP TSoundTrackReaderMp3::load() {
  FfmpegAudio *ffmepegAudio = new FfmpegAudio();
  TFilePath tempFile        = ffmepegAudio->getRawAudio(m_path);

  Tifstream is(tempFile);

  if (!is)
    throw TException(L"Unable to load the RAW file " + m_path.getWideString() +
                     L" : doesn't exist");

  is.seekg(0, std::ios_base::end);
  long sampleCount = is.tellg() / 4;
  is.seekg(0, std::ios_base::beg);

  TSoundTrack *track = new TSoundTrackStereo16(44100, 2, sampleCount);
  is.read((char *)track->getRawData(), sampleCount * 4);
  return track;
}

bool FfmpegAudio::checkFfmpeg() {
  // check the user defined path in preferences first
  QString path = Preferences::instance()->getFfmpegPath() + "/ffmpeg";
#if defined(_WIN32)
  path = path + ".exe";
#endif
  if (TSystem::doesExistFileOrLevel(TFilePath(path))) return true;

  // check the OpenToonz root directory next
  path = QDir::currentPath() + "/ffmpeg";
#if defined(_WIN32)
  path = path + ".exe";
#endif
  if (TSystem::doesExistFileOrLevel(TFilePath(path))) {
    Preferences::instance()->setValue(ffmpegPath, QDir::currentPath());
    return true;
  }

  // give up
  return false;
}

TFilePath FfmpegAudio::getFfmpegCache() {
  QString cacheRoot = ToonzFolder::getCacheRootFolder().getQString();
  if (!TSystem::doesExistFileOrLevel(TFilePath(cacheRoot + "/ffmpeg"))) {
    TSystem::mkDir(TFilePath(cacheRoot + "/ffmpeg"));
  }
  std::string ffmpegPath =
      TFilePath(cacheRoot + "/ffmpeg").getQString().toStdString();
  return TFilePath(cacheRoot + "/ffmpeg");
}

void FfmpegAudio::runFfmpeg(QStringList args) {
  // write the file
  QString m_ffmpegPath      = Preferences::instance()->getFfmpegPath();
  std::string strFfmpegPath = m_ffmpegPath.toStdString();
  QProcess ffmpeg;
  ffmpeg.start(m_ffmpegPath + "/ffmpeg", args);
  ffmpeg.waitForFinished(30000);
  QString results = ffmpeg.readAllStandardError();
  results += ffmpeg.readAllStandardOutput();
  int exitCode = ffmpeg.exitCode();
  ffmpeg.close();
  std::string strResults = results.toStdString();
}

TFilePath FfmpegAudio::getRawAudio(TFilePath path) {
  std::string name       = path.getName();
  TFilePath outPath      = getFfmpegCache() + TFilePath(name + ".raw");
  std::string strPath    = path.getQString().toStdString();
  std::string strOutPath = outPath.getQString().toStdString();
  QStringList args;
  args << "-i";
  args << path.getQString();
  args << "-f";
  args << "s16le";
  args << "-ac";
  args << "2";
  args << "-ar";
  args << "44100";
  args << "-y";
  args << outPath.getQString();
  runFfmpeg(args);
  return outPath;
}