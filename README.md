# syphonpy
Python bindings for the Syphon Framework (OSX)

---

## Installation

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

6. Test  
  install bimpy```pip3.7 install bimpy```  
  install OpenGL  ```pip3.7 install pyopengl```  
  run ```python3.7 tester.py```  

---

## Original Syphon Framework readme
Syphon is an open source Mac OS X technology that allows applications to share video and still images with one another in realtime.

See http://syphon.v002.info for more information.

This project hosts the Syphon.framework for developers who want to integrate Syphon in their own software. If you are looking for the Syphon plugins for Quartz Composer, Max/Jitter, FFGL, etc, the project for the Syphon Implementations currently at http://github.com/Syphon
