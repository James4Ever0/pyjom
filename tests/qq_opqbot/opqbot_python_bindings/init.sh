go mod init dummy.com/dum
PKGNAME=github.com/mcoo/OPQBot
go get $PKGNAME
gopy build -output=bindings -vm=python3 $PKGNAME
PKGNAME=github.com/mcoo/OPQBot
go get $PKGNAME
gopy build -output=bindings -vm=python3 $PKGNAME