ps aux | grep -v grep | grep paddlespeech | awk '{print $2}' | xargs -iabc kill -s KILL abc
