import sys
sys.path.append('../Library')
import cv2
import numpy as np
# import SpoutSDK
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import syphonpy

def main():

    # window details
    width = 640 
    height = 480 
    display = (width,height)

    # window setup
    pygame.init() 
    pygame.display.set_caption('Spout Python Sender')
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.gl_set_attribute(pygame.GL_ALPHA_SIZE, 8)

    cap = cv2.VideoCapture(1)
    if cap.isOpened() is False:
        raise("IO Error")
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    cap.set(3, width)
    cap.set(4, height)

    # OpenGL init
    glMatrixMode(GL_PROJECTION)
    glOrtho(0,width,height,0,1,-1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glClearColor(0.0,0.0,0.0,0.0)
    glEnable(GL_TEXTURE_2D)

    # init spout sender
    # spoutSender = SpoutSDK.SpoutSender()
    spoutSenderWidth = width
    spoutSenderHeight = height
    # Its signature in c++ looks like this: bool CreateSender(const char *Sendername, unsigned int width, unsigned int height, DWORD dwFormat = 0);
    server = syphonpy.SyphonServer("Test")
    # spoutSender.CreateSender('Spout for Python Webcam Sender Example', width, height, 0)

    # create texture id for use with Spout
    senderTextureID = glGenTextures(1)

    # initalise our sender texture
    glBindTexture(GL_TEXTURE_2D, senderTextureID)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glBindTexture(GL_TEXTURE_2D, 0)

    # loop
    while True:
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               quit()

        ret, frame = cap.read() #read camera image
        #img = cv2.imread('image.png') # if use the image file
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) #BGR-->RGB
        h, w = frame.shape[:2]
        glBindTexture(GL_TEXTURE_2D, senderTextureID)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, frame)

        server.publish_frame_texture(senderTextureID, syphonpy.MakeRect(0,0,spoutSenderWidth,spoutSenderHeight), syphonpy.MakeSize(spoutSenderWidth,spoutSenderHeight), False)
        # server.publish_frame_texture(senderTextureID, GL_TEXTURE_2D, spoutSenderWidth, spoutSenderHeight, False)
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT )
        # reset the drawing perspective
        glLoadIdentity()

        # Draw texture to screen
        glBegin(GL_QUADS)
        ##
        glTexCoord(0,0)        
        glVertex2f(0,0)
        #
        glTexCoord(1,0)
        glVertex2f(width,0)
        #
        glTexCoord(1,1)
        glVertex2f(width,height)
        #
        glTexCoord(0,1)
        glVertex2f(0,height)
        ##
        glEnd()

        pygame.display.flip()
        # unbind our sender texture
        glBindTexture(GL_TEXTURE_2D, 0)
      #  pygame.time.wait(10)

if __name__ == '__main__':
    main()
