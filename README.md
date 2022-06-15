# syphonpy
[![Build Status](https://travis-ci.org/njazz/syphonpy.svg?branch=master)](https://travis-ci.org/njazz/syphonpy)  
Python bindings for the Syphon Framework (OSX)

## Installation

A prebuilt version is hosted on [PyPI](https://pypi.org/project/syphonpy/) and available to install with pip:

```
pip install syphonpy
```


## Build

0. Have [python3.7](https://www.python.org/downloads/release/python-370/), XCode and [cmake](https://cmake.org/install/) installed

1. Clone to your local machine

2. Open terminal and cd .. to the clone

3. Update submodules
```
git submodule update --init --recursive
```

4. Build
```
python3.7 setup.py build
```

5. Install
```
python3.7 setup.py install
```

## Test

- install bimpy```pip3.7 install bimpy```  
- install OpenGL  ```pip3.7 install pyopengl``` 
- install numpy  ```pip3.7 install numpy``` 
- run ```python3.7 tester.py```  

---

## Original Syphon Framework readme
Syphon is an open source Mac OS X technology that allows applications to share video and still images with one another in realtime.

See http://syphon.v002.info for more information.

This project hosts the Syphon.framework for developers who want to integrate Syphon in their own software. If you are looking for the Syphon plugins for Quartz Composer, Max/Jitter, FFGL, etc, the project for the Syphon Implementations currently at http://github.com/Syphon

---
## Acknowledgements  
  
https://github.com/bangnoise  
https://github.com/maybites  
https://github.com/egradman  
https://github.com/cansik
https://github.com/kiyu-git

