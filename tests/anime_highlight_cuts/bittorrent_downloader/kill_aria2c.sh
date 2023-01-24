ps aux | grep '[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [Ma10p_1080p]' | grep -v grep | awk '{print $1}' | xargs -Iabc kill -s INT abc
