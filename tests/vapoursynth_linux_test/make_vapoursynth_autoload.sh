# refer to http://www.vapoursynth.com/doc/installation.html
mkdir -p "$HOME/Library/Application Support/VapourSynth/"
touch "$HOME/Library/Application Support/VapourSynth/vapoursynth.conf"
sudo mkdir -p /Library/vapoursynth/plugins
mkdir -p /Users/jamesbrown/vapoursynth/plugins
echo "UserPluginDir=/Users/jamesbrown/vapoursynth/plugins" > "$HOME/Library/Application Support/VapourSynth/vapoursynth.conf"
echo "SystemPluginDir=/Library/vapoursynth/plugins" >> "$HOME/Library/Application Support/VapourSynth/vapoursynth.conf"
echo "CONTENT BELOW:"
cat "$HOME/Library/Application Support/VapourSynth/vapoursynth.conf"