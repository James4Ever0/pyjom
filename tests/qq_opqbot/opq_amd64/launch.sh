ps aux | grep OPQBot | grep -v grep | awk '{print $2}' | xargs -iabc kill -s KILL abc
env http_proxy="" https_proxy="" all_proxy="" ./OPQBot
# spelling error. just copy and paste ok?
# @REM click http://localhost:8781/v1/Login/GetQRcode to scan qrcode and login. is it needed to be done every time?
# @REM click http://localhost:8781/v1/ClusterInfo to check login status.
# the login cookies will be cached. under ./UsersConf/[QQ_ID].conf
