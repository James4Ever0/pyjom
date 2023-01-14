ps aux | grep "redis-server"| grep 9291 | awk '{print $2}' | xargs -iabc kill -s KILL abc
redis-server --port 9291