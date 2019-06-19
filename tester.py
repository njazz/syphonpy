import syphonpy
import time

import bimpy

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy

ctx = bimpy.Context()
ctx.init(1152,768, "One")

server = syphonpy.SyphonServer("Test")

_texture = glGenTextures(1)

def make_tex(val):
    # glPixelStorei(GL_UNPACK_ALIGNMENT,1)

    glBindTexture(GL_TEXTURE_2D, _texture)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

    l1 =[]
    l2 = []
    list_ = []
    for i in range(320):
        l1 += [float(((i+val)%16)>7)]
        l2 += [float(((i)%(16))<8)]
    for i in range(240):
        if (i%(16+(val%8)))>7:
            list_ += [l1]
        else:
            list_ += [l2]

    # list_ = [[1,0,0],[0,1,0],[0,0,1]]

    width = len(list_[0])
    height = len(list_)
    output = []

    for ra in list_:
        row = []
        for c1 in ra:
            color1 = int(c1 * 2550.0)#int(2550.0*float(c1))
            if (color1>255):
                color1 = 255
            if (color1<0):
                color1 = 128
            row += [color1,color1, color1] #[color1,color1,color1]
        output += row

    np_out = numpy.array(output, dtype = numpy.uint8)
    imdata = numpy.frombuffer(np_out.tobytes(), numpy.uint8)
    imdata = np_out

    gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGB, width, height, GL_RGB, GL_UNSIGNED_BYTE, imdata)

    # glBindTexture(GL_TEXTURE_2D, 0)
    return _texture


val1 = 0
client = None
sel_str = ""
img = None
fbo = glGenFramebuffers(1)

_converted = glGenTextures(1)

while not ctx.should_close():
    ctx.new_frame()

    try:
        tex1 = make_tex(val1)
        server.publish_frame_texture(tex1, syphonpy.MakeRect(0,0,640,480), syphonpy.MakeSize(640,480), False)
        val1 += 1

        bimpy.image(tex1, bimpy.Vec2(640,480))
        bimpy.text(str(_texture))

        bimpy.text(server.context())
        pass
    except Exception as e:
        bimpy.text(str(e))

    bimpy.begin("Client")
    if bimpy.begin_combo("Source", sel_str):
        lst = syphonpy.ServerDirectory.servers()

        for k in lst:
            if bimpy.selectable(k.name + " : " + k.app_name):
                client = syphonpy.SyphonClient(k)
                sel_str = k.name + " : " + k.app_name

        bimpy.end_combo()

    _tex = 0
    if client:
        # _tex = glGenTextures(1)
        img = client.new_frame_image()
        # glBindTexture(GL_TEXTURE_2D, _tex)
        # print(img)
        pass

    if img and img.texture_size().width and img.texture_size().height:

        #
        # try:
        # arbTexture = glGenTextures(1)
        #
        # texture = img.texture_name
        # width = int(img.texture_size.width)
        # height = int(img.texture_size.height)
        #
        #
        #
        # glBindTexture(GLenum(GL_TEXTURE_2D), arbTexture)
        # glBindTexture(GLenum(GL_TEXTURE_RECTANGLE), texture)
        #
        # glBindFramebuffer(GLenum(GL_FRAMEBUFFER), fbo);
        # glFramebufferTexture2D(GLenum(GL_READ_FRAMEBUFFER), GLenum(GL_COLOR_ATTACHMENT0), GLenum(GL_TEXTURE_RECTANGLE), texture, 0)
        # glFramebufferTexture2D(GLenum(GL_DRAW_FRAMEBUFFER), GLenum(GL_COLOR_ATTACHMENT1),GLenum(GL_TEXTURE_2D), arbTexture, 0),glDrawBuffer(GLenum(GL_COLOR_ATTACHMENT1))
        # glBlitFramebuffer(0, 0, GLsizei(width), GLsizei(height), 0, 0, GLsizei(width), GLsizei(height), GLbitfield(GL_COLOR_BUFFER_BIT), GLenum(GL_NEAREST))

        # glCopyImageSubData(texture, GL_TEXTURE_RECTANGLE, 0, 0, 0, 0, arbTexture, GL_TEXTURE_2D, 0, 0, 0, 0, width, height, 1);

        syphonpy.convert_to_texture(img.texture_name(), _converted , int(img.texture_size().width), int(img.texture_size().height))

        # glBindTexture(GL_TEXTURE_2D, 0)

        # glBindTexture(GL_TEXTURE_RECTANGLE, img.texture_name)
        bimpy.image(_converted, bimpy.Vec2(img.texture_size().width,img.texture_size().height))
        # glBindTexture(GL_TEXTURE_RECTANGLE, 0)

        # glBindFramebuffer(GL_FRAMEBUFFER, 0);
        bimpy.text("ok")

        # except Exception as e:
        #     bimpy.text(str(e))
        #     pass
        bimpy.text(str(img.texture_name()))
        bimpy.text(str(_converted))
        bimpy.text("[{}x{}]".format(img.texture_size().width, img.texture_size().height))
        # bimpy.text(str(client.context()))

        img = None

    bimpy.end()
    ctx.render()
