go mod init dummy.com/dum

# PKGNAME=github.com/mcoo/OPQBot
# go get $PKGNAME
# gopy build -output=bindings -vm=python3 $PKGNAME

# PKGNAME=github.com/mcoo/OPQBot/qzone # wtf?
# go get $PKGNAME
# gopy build -output=bindings_qzone -vm=python3 $PKGNAME

PKGNAME=github.com/mcoo/OPQBot
PKGNAME2=github.com/mcoo/OPQBot/qzone # wtf?
go get $PKGNAME
go get $PKGNAME2
gopy build -output=bindings_qzone -vm=python3 $PKGNAME