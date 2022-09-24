from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'lazero'
LONG_DESCRIPTION = 'AGI package'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="lazero", 
        version=VERSION,
        author="Jason Dsouza",
        author_email="<youremail@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        entry_points ={
            'console_scripts': [
                'lazero = lazero.__main__:main'
            ]
        },
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: POSIX :: Linux",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
