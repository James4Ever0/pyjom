from __future__ import unicode_literals

from io import StringIO

import pytest

from kaldiio.utils import MultiFileDescriptor


def test_read():
    fd = StringIO("abc")
    fd2 = StringIO("xdef")
    fd2.read(1)
    fd3 = StringIO("ghi")
    mfd = MultiFileDescriptor(fd, fd2, fd3)

    assert mfd.read(3) == "abc"
    assert mfd.read(6) == "defghi"


@pytest.mark.parametrize("offset", [3, 4, 5, 6, 7, 8])
@pytest.mark.parametrize("offset2", [3, 4, 5, 6])
def test_read_tell(offset, offset2):
    fd = StringIO("abc")
    fd2 = StringIO("xdef")
    fd2.read(1)
    fd3 = StringIO("ghi")
    mfd = MultiFileDescriptor(fd, fd2, fd3)

    mfd.read(offset)
    assert mfd.tell() == min(offset, 9)
    mfd.read(offset2)
    assert mfd.tell() == min(offset + offset2, 9)


def test_seek():
    fd = StringIO("abc")
    fd2 = StringIO("xdef")
    fd2.read(1)
    fd3 = StringIO("ghi")
    mfd = MultiFileDescriptor(fd, fd2, fd3)

    assert mfd.read() == "abcdefghi"
    mfd.seek(0)
    assert mfd.read() == "abcdefghi"
