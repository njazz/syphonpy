
import cv2
import numpy as np

import glfw
import syphonpy

import Syphon

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def main():
    size = (1280, 720)
    client = Syphon.Client('Gray', size, hide=False)
    
    while not client.should_close():
        client.draw()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # cv2.destroyAllWindows()
    # exit()  
        
            
            
        

if __name__ == '__main__':
    main()
