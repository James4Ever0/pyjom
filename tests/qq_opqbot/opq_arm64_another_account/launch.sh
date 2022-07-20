# ps aux | grep OPQBot | grep -v grep | awk '{print $2}' | xargs -iabc kill -s KILL abc # the problem is here.
cd bin
qemu-aarch64 OPQBot # why the fuck you will change to parent directory?
# different for arm64. the port is 8780.
# spelling error. just copy and paste ok?
# @REM click http://localhost:8780/v1/Login/GetQRcode to scan qrcode and login. is it needed to be done every time?
# @REM click http://localhost:8780/v1/ClusterInfo to check login status.
# the login cookies will be cached. under ./UsersConf/[QQ_ID].conf