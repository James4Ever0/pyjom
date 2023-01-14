ps aux | grep "redis-server"| grep 9291 | grep -v grep | awk '{print $2}' | xargs -iabc kill -s KILL abc
redis-server --port 9291