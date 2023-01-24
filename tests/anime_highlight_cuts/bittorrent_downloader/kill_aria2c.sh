ps aux | grep sample.webp | grep -v grep | xargs -Iabc kill -s INT abc
