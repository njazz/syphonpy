import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

import syphonpy
import cv2


class Server:
    def __init__(self, name, size, hide=False):
        self.size = size
        
        # window setup
        if not glfw.init():
            raise RuntimeError('Failed to initialize GLFW')
        
        self.window = glfw.create_window(size[0], size[1], name, None, None)
        
        if hide:
            glfw.hide_window(self.window) # hide window
        
        if not self.window:
            glfw.terminate()
            raise RuntimeError('Failed to create window')

        # コンテキストを作成
        glfw.make_context_current(self.window)
        
        # init Syhon
        self.server = syphonpy.SyphonServer(name)
        
        # OpenGL init
        glMatrixMode(GL_PROJECTION)
        glOrtho(0, size[0], size[1], 0, 1, -1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glEnable(GL_TEXTURE_2D)
        
        # create texture id for use with Syphon
        self.TextureID = glGenTextures(1)
        
        # initalise our sender texture
        glBindTexture(GL_TEXTURE_2D, self.TextureID)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glBindTexture(GL_TEXTURE_2D, 0)
        
    def draw_and_send(self, frame):
        glfw.make_context_current(self.window)
        glBindTexture(GL_TEXTURE_2D, self.TextureID)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.size[0], self.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, frame)
        
        self.server.publish_frame_texture(self.TextureID, syphonpy.MakeRect(0, 0, self.size[0], self.size[1]), syphonpy.MakeSize(self.size[0], self.size[1]), True)
        
         # Clear screen
        glClear(GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT )
        # reset the drawing perspective
        glLoadIdentity()

        # Draw texture to screen
        glBegin(GL_QUADS)
        ##
        glTexCoord(0, 0)        
        glVertex2f(0, 0)
        #
        glTexCoord(1,0)
        glVertex2f(self.size[0], 0)
        #
        glTexCoord(1, 1)
        glVertex2f(self.size[0], self.size[1])
        #
        glTexCoord(0,1)
        glVertex2f(0, self.size[1])
        ##
        glEnd()
        
        glfw.swap_buffers(self.window)
        glfw.poll_events()
        
        # unbind our sender texture
        glBindTexture(GL_TEXTURE_2D, 0)
    
    def should_close(self):
        return glfw.window_should_close(self.window)
        

class Client:
    def __init__(self, name, size, hide=False):
        self.size = size
        self.client = None
        self.img = None
        
        # window setup
        if not glfw.init():
            raise RuntimeError('Failed to initialize GLFW')
        
        self.window = glfw.create_window(size[0], size[1], name, None, None)
        
        if hide:
            glfw.hide_window(self.window) # hide window
        
        if not self.window:
            glfw.terminate()
            raise RuntimeError('Failed to create window')

        # コンテキストを作成
        glfw.make_context_current(self.window)
        
        # init Syhon
        self.server = syphonpy.SyphonServer(name)
        
        # OpenGL init
        glMatrixMode(GL_PROJECTION)
        glOrtho(0, size[0], size[1], 0, 1, -1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glEnable(GL_TEXTURE_2D)
        
        # create texture id for use with Syphon
        self.TextureID = glGenTextures(1)
        
        # initalise our sender texture
        glBindTexture(GL_TEXTURE_2D, self.TextureID)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glBindTexture(GL_TEXTURE_2D, 0)
        
        
        available_servers = syphonpy.ServerDirectory.servers()
        for idx, available_server in enumerate(available_servers):
            print(f"[{idx}]{available_server.app_name} : {available_server.name}")
        # val = input("Press number to receive...\n")
        val = 1
        try:
            self.client = syphonpy.SyphonClient(available_servers[int(val)])
        except Error as e:
            print(f"error: {e}")
        
        # # 画面サイズを変更
        # if self.client:
        #     img = self.client.new_frame_image()
        #     print(img.texture_size().width)
        
        # if img and img.texture_size().width and img.texture_size().height:
        #     print("dada")
        #     glfw.set_window_size(self.window, int(img.texture_size().width), int(img.texture_size().height))
        
    def draw(self):
        if self.client:
            img = self.client.new_frame_image()
        
        if img and img.texture_size().width and img.texture_size().height:
            glfw.make_context_current(self.window)
            
            glEnable(GL_TEXTURE_RECTANGLE)
            glBindTexture(GL_TEXTURE_RECTANGLE, img.texture_name())
            # syphonpy.convert_to_texture(img.texture_name(), self.TextureID , int(img.texture_size().width), int(img.texture_size().height))
            
            pixels = (GLuint * int(img.texture_size().width) * int(img.texture_size().height) * 4 * sizeof(GLuint))()
            # 描画元のテクスチャを設定
            glBindTexture(GL_TEXTURE_RECTANGLE, img.texture_name())
            glGetTexImage(GL_TEXTURE_RECTANGLE, 0, GL_RGBA, GL_UNSIGNED_INT_8_8_8_8_REV, pixels)
            
            # 描画先のテクスチャを設定
            glDisable(GL_TEXTURE_RECTANGLE)
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.TextureID)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, GLsizei(int(img.texture_size().width)), 
                         GLsizei(int(img.texture_size().height)), 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels)

            # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 100)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

            glGenerateMipmap(GL_TEXTURE_2D)
            
            # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, int(img.texture_size().width), int(img.texture_size().height), 0, GL_BGRA, GL_UNSIGNED_INT_8_8_8_8_REV, pixels)
            
            # glDeleteBuffers(pixels)
            
            
            # Clear screen
            glClear(GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT )
            # reset the drawing perspective
            glLoadIdentity()

            # Draw texture to screen
            glBegin(GL_QUADS)
            ##
            glTexCoord(0, 0)        
            glVertex2f(0, 0)
            #
            glTexCoord(1,0)
            glVertex2f(int(img.texture_size().width), 0)
            #
            glTexCoord(1, 1)
            glVertex2f(int(img.texture_size().width), int(img.texture_size().height))
            #
            glTexCoord(0,1)
            glVertex2f(0, int(img.texture_size().height))
            ##
            glEnd()
            
        glfw.swap_buffers(self.window)
        glfw.poll_events()
        
        # unbind our sender texture
        glBindTexture(GL_TEXTURE_2D, 0)
        
    def should_close(self):
        return glfw.window_should_close(self.window)
        
        