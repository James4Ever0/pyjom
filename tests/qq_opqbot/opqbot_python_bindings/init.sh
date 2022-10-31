PKGNAME=github.com/mcoo/OPQBot
go mod init dummy.com/dum
go get $PKGNAME
gopy build -output=bindings -vm=python3 $PKGNAME