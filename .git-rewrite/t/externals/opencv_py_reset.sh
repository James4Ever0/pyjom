cd opencv/build/python_loader
yes | pip3 uninstall opencv
yes | pip3 uninstall opencv-contrib
yes | pip3 uninstall opencv-python
yes | pip3 uninstall opencv-contrib-python
yes | pip3 install opencv-python # will that break shit?
python3 setup.py install

# it is all about that .so file.

# you would like to say that you have installed the thing.
# place a link of .so or something, to use the cuda function.

cp /usr/local/lib/python3.9/site-packages/cv2/python-3.9/cv2.cpython-39-x86_64-linux-gnu.so /usr/local/lib/python3.9/dist-packages/
# pip3 install .
# python3 setup.py install --install-lib /usr/lib/python3/dist-packages/
# # python3 setup.py install --root /usr/lib/python3/dist-packages/

# Options for 'install' command:
#   --prefix                             installation prefix
#   --exec-prefix                        (Unix only) prefix for platform-
#                                        specific files
#   --home                               (Unix only) home directory to install
#                                        under
#   --install-base                       base installation directory (instead of
#                                        --prefix or --home)
#   --install-platbase                   base installation directory for
#                                        platform-specific files (instead of --
#                                        exec-prefix or --home)
#   --root                               install everything relative to this
#                                        alternate root directory
#   --install-purelib                    installation directory for pure Python
#                                        module distributions
#   --install-platlib                    installation directory for non-pure
#                                        module distributions
#   --install-lib                        installation directory for all module
#                                        distributions (overrides --install-
#                                        purelib and --install-platlib)
#   --install-headers                    installation directory for C/C++
#                                        headers
#   --install-scripts                    installation directory for Python
#                                        scripts
#   --install-data                       installation directory for data files
#   --compile (-c)                       compile .py to .pyc [default]
#   --no-compile                         don't compile .py files
#   --optimize (-O)                      also compile with optimization: -O1 for
#                                        "python -O", -O2 for "python -OO", and
#                                        -O0 to disable [default: -O0]
#   --force (-f)                         force installation (overwrite any
#                                        existing files)
#   --skip-build                         skip rebuilding everything (for
#                                        testing/debugging)
#   --record                             filename in which to record list of
#                                        installed files
#   --user                               install in user site-package
#                                        '/root/.local/lib/python3.9/site-
#                                        packages'
#   --old-and-unmanageable               Try not to use this!
#   --single-version-externally-managed  used by system package builders to
#                                        create 'flat' eggs
