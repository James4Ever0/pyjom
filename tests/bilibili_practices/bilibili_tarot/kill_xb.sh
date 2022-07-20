ps aux | grep -v grep | grep xvfb | awk '{print $2}' | xargs -iabc kill -s TERM abc
ps aux | grep -v grep | grep scriptable_generate_typography | awk '{print $2}' | xargs -iabc kill -s TERM abc
