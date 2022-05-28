import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

import syphonpy
import cv2


class Server:
    def __init__(self, name, size, show=True):
        self.size = size
        
        # window setup
        if not glfw.init():
            raise RuntimeError('Failed to initialize GLFW')
        
        self.window = glfw.create_window(size[0], size[1], name, None, None)
        
        if not show:
            glfw.hide_window(self.window) # hide window
        
        if not self.window:
            glfw.terminate()
            raise RuntimeError('Failed to create window')

        # set context
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
    def __init__(self, name, show=True):
        self.client = None
        self.img = None
        self.first_frame_flg = True
        self.window_name = name
        # window setup
        if not glfw.init():
            raise RuntimeError('Failed to initialize GLFW')
        
        self.window = glfw.create_window(1280, 720, name, None, None)
        
        if not self.window:
            glfw.terminate()
            raise RuntimeError('Failed to create window')
        
        # set context
        glfw.make_context_current(self.window)
        
        available_servers = syphonpy.ServerDirectory.servers()
        for idx, available_server in enumerate(available_servers):
            print(f"[{idx}]{available_server.app_name} / {available_server.name}")
        val = input("Press number to receive...\n")
        
        self.server = available_servers[int(val)]
        
        try:
            self.client = syphonpy.SyphonClient(self.server)
        except Error as e:
            print(f"error: {e}")
        
        self.show = show
        
    def draw(self, return_mat=False):
        if self.client:
            img = self.client.new_frame_image()
        
        if img and img.texture_size().width and img.texture_size().height:
            if self.first_frame_flg:
                # set window size and show option
                glfw.set_window_size(self.window, int(img.texture_size().width), int(img.texture_size().height))
                if not self.show:
                    glfw.hide_window(self.window) # hide window
                    
                # OpenGL init
                glMatrixMode(GL_PROJECTION)
                glOrtho(0, int(img.texture_size().width), int(img.texture_size().height), 0, 1, -1)
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                glDisable(GL_DEPTH_TEST)
                glClearColor(0.0, 0.0, 0.0, 0.0)
                glEnable(GL_TEXTURE_RECTANGLE)
                
                self.first_frame_flg = False

                print(f"server: \"{self.server.app_name}/{self.server.name}\", window: \"{self.window_name}\", size: \"{img.texture_size().width} × {img.texture_size().height}\"")
            
            glfw.make_context_current(self.window)
            
            # Clear screen
            glClearColor(0.0, 0.0, 0.0, 0.0)
            glClear(GL_COLOR_BUFFER_BIT)
            
            #  Bind the texture
            glEnable(GL_TEXTURE_RECTANGLE)
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_RECTANGLE, img.texture_name())
            
            #  Configure texturing as we want it
            glTexParameteri(GL_TEXTURE_RECTANGLE, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameteri(GL_TEXTURE_RECTANGLE, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexParameteri(GL_TEXTURE_RECTANGLE, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_RECTANGLE, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
            
            glColor4f(1.0, 1.0, 1.0, 1.0)
            
            texCoords = np.array([
                0.0, img.texture_size().height, 
                img.texture_size().width, img.texture_size().height, 
                img.texture_size().width, 0.0, 
                0.0, 0.0], dtype=GLfloat)

            verts = np.array([
                0.0, 0.0, 
                img.texture_size().width, 0.0, 
                img.texture_size().width, img.texture_size().height, 
                0.0, img.texture_size().height], dtype=GLfloat)
            
            glEnableClientState( GL_TEXTURE_COORD_ARRAY )
            glTexCoordPointer(2, GL_FLOAT, 0, texCoords)
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(2, GL_FLOAT, 0, verts)
            glDrawArrays( GL_TRIANGLE_FAN, 0, 4 )
            
            if return_mat:
                x_scale, y_scale = glfw.get_window_content_scale(self.window)
                frame = np.zeros((int(img.texture_size().height * x_scale), int(img.texture_size().width * y_scale), 4), np.uint8)
                glPixelStorei(GL_PACK_ALIGNMENT, 1)
                glPixelStorei(GL_PACK_ROW_LENGTH, (int(img.texture_size().width * x_scale)))
               
                glReadPixels(0, 0, int(img.texture_size().width * x_scale), int(img.texture_size().height * y_scale), GL_BGRA, GL_UNSIGNED_BYTE, frame.data)
                frame = cv2.resize(frame, (int(img.texture_size().width), int(img.texture_size().height)))
                frame = cv2.flip(frame, 0)
                return frame
            
        glfw.swap_buffers(self.window)
        glfw.poll_events()
        
        # unbind our sender texture
        glBindTexture(GL_TEXTURE_RECTANGLE, 0)
        
    def should_close(self):
        return glfw.window_should_close(self.window)
        
        