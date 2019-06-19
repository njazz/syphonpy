#include "SyphonBuildMacros.h"

#include "Syphon.h"
#include "syphon_cxx.hpp"

#include <OpenGL/OpenGL.h>
//#include <OpenGL/gl.h>
#import <OpenGL/gl3.h>
#include <OpenGL/glu.h>

NSString* toNSString(std::string s)
{
    return [NSString stringWithCString:s.c_str()
                              encoding:[NSString defaultCStringEncoding]];
}

std::string toString(NSString* s)
{
    return std::string([s UTF8String]);
}

namespace Wrapper {

struct _serverOpaquePtr {
    SyphonServer* obj = nil;
    _serverOpaquePtr(SyphonServer* o)
    {
        obj = [o retain];
    }
    ~_serverOpaquePtr()
    {
        [obj release];
    }
};

struct _clientOpaquePtr {
    SyphonClient* obj = nil;
    _clientOpaquePtr(SyphonClient* o)
    {
        obj = [o retain];
    }
    ~_clientOpaquePtr()
    {
        [obj release];
    }
};

struct _serverOptionsOpaquePtr {
    NSDictionary* obj = nil;
    _serverOptionsOpaquePtr(NSDictionary* o)
    {
        obj = [o retain];
    }
    ~_serverOptionsOpaquePtr()
    {
        [obj release];
    }
};

struct _serverDescriptionOpaquePtr {
private:
    NSDictionary* obj = nil;
public:
    _serverDescriptionOpaquePtr(NSDictionary* o)
    {
        obj = [o retain];
    }
    ~_serverDescriptionOpaquePtr()
    {
        [obj release];
    }
    NSDictionary *get() const
    {
        return obj;
    }
    void set(NSDictionary *d)
    {
        [d retain];
        [obj release];
        obj = d;
    }
};

struct _imageOpaquePtr {
    SyphonImage *obj = nil;
    _imageOpaquePtr(SyphonImage *o)
    {
        obj = [o retain];
    }
    ~_imageOpaquePtr()
    {
        [obj release];
    }
};

// ---
ServerOptions::ServerOptions(_serverOptionsOpaquePtr* p)
{
    isPrivate = [p->obj[SyphonServerOptionIsPrivate] boolValue];
    antialiasSampleCount = [p->obj[SyphonServerOptionAntialiasSampleCount] intValue];
    depthBufferResolution = [p->obj[SyphonServerOptionDepthBufferResolution] intValue];
    stencilBufferResolution = [p->obj[SyphonServerOptionStencilBufferResolution] intValue];
}

// ---

ServerDescription::ServerDescription(_serverDescriptionOpaquePtr* d)
{
    if (!d)
        _ptr = new _serverDescriptionOpaquePtr(@{});
    else
        _ptr = d;

    if (!d->get())
        d->set(@{});

    UUID = toString(d->get()[SyphonServerDescriptionUUIDKey]);
    Name = toString(d->get()[SyphonServerDescriptionNameKey]);
    AppName = toString(d->get()[SyphonServerDescriptionAppNameKey]);
}

ServerDescription::ServerDescription(const ServerDescription& src)
{
    UUID = src.UUID;
    Name = src.Name;
    AppName = src.AppName;
    NSDictionary *dictionary = [src._ptr->get() copy];
    _ptr = new _serverDescriptionOpaquePtr(dictionary);
    [dictionary release]; // retained by _serverDescriptionOpaquePtr()
}

_serverDescriptionOpaquePtr* ServerDescription::toDictionary()
{
    NSDictionary* d;
    d = _ptr->get();

    NSMutableDictionary* _dict = [d mutableCopy];
    _dict[SyphonServerDescriptionUUIDKey] = toNSString(UUID);
    _dict[SyphonServerDescriptionNameKey] = toNSString(Name);
    _dict[SyphonServerDescriptionAppNameKey] = toNSString(AppName);

    _serverDescriptionOpaquePtr *result = new _serverDescriptionOpaquePtr(_dict);
    [_dict release]; // retained by _serverDescriptionOpaquePtr()
    return result;
    ;
}

// ---

Server::Server(std::string name)
{
    _context = CGLGetCurrentContext();
    _name = name;

    NSString* n_ = toNSString(name);
    SyphonServer* srv = [[SyphonServer alloc] initWithName:n_ context:_context options:@{}];

    _obj = new _serverOpaquePtr(srv);
    [srv release]; // retained by _serverOpaquePtr()
    if (!srv)
        _error = true;
}

void Server::publishFrameTexture(GLuint texID, Rect _region, Size _size, bool flipped)
{
    auto target = GL_TEXTURE_2D;
    SyphonServer* _s = _obj->obj;

    NSRect region = NSMakeRect(_region.origin.x, _region.origin.y, _region.size.width, _region.size.height);
    NSSize size = NSMakeSize(_size.width, _size.height);

    [_s publishFrameTexture:texID textureTarget:target imageRegion:region textureDimensions:size flipped:flipped];
}

ServerDescription Server::serverDescription()
{
    if (_error)
        return ServerDescription();
    NSDictionary* _dict = [_obj->obj serverDescription];
    auto _opaque = new _serverDescriptionOpaquePtr(_dict);
    ServerDescription ret(_opaque);

    return ret;
};

bool Server::hasClients()
{
    return [_obj->obj hasClients];
}

Server::~Server()
{
    delete _obj;
}

// ---

std::vector<ServerDescription> ServerDirectory::servers()
{
    NSArray* _arr = [[SyphonServerDirectory sharedDirectory] servers];

    std::vector<ServerDescription> ret;
    for (NSDictionary* obj in _arr) {
        //        NSLog(@"srv @%@", obj);

        auto _opaque = new _serverDescriptionOpaquePtr(obj);
        ret.push_back(ServerDescription(_opaque));
        //        delete _opaque;
    }
    return ret;
}
std::vector<ServerDescription> ServerDirectory::serversMatchingNameAppName(std::string name, std::string appName)
{
    NSArray* _arr = [[SyphonServerDirectory sharedDirectory] serversMatchingName:toNSString(name) appName:toNSString(appName)];

    std::vector<ServerDescription> ret;
    for (NSDictionary* obj in _arr) {
        auto _opaque = new _serverDescriptionOpaquePtr(obj);
        ret.push_back(ServerDescription(_opaque));
        //        delete _opaque;
    }
    return ret;
}

// ---

Client::Client(ServerDescription descr, NewFrameHandlerFunc handler)
{
    _context = CGLGetCurrentContext();

    auto _opaque = descr.toDictionary();
    NSDictionary* _dict = _opaque->get();

    SyphonClient* cl = [[SyphonClient alloc] initWithServerDescription:_dict
                                                               context:_context
                                                               options:nil
                                                       newFrameHandler:nil
        //                                                                        ^(SyphonClient* client) {
        //                                                           auto ptr = std::make_shared<_clientOpaquePtr>(client);
        //                                                           handler(ptr);
        //                                                       }
    ];

    _obj = new _clientOpaquePtr(cl);
    if (!cl)
        _error = true;
}

Image Client::newFrameImage()
{
    CGLSetCurrentContext(_context);
    SyphonImage* img = [_obj->obj newFrameImage];
    _imageOpaquePtr *opaque = new _imageOpaquePtr(img);
    [img release]; // retained by _imageOpaquePtr()
    Image ret(opaque);

    return ret;
}

bool Client::isValid()
{
    return [_obj->obj isValid];
}

bool Client::hasNewFrame()
{
    return [_obj->obj hasNewFrame];
}

void Client::stop()
{
    [_obj->obj stop];
}

ServerDescription Client::serverDescription()
{
    if (_error)
        return ServerDescription();
    NSDictionary* _dict = [_obj->obj serverDescription];
    auto _opaque = new _serverDescriptionOpaquePtr(_dict);
    ServerDescription ret(_opaque);

    return ret;
};

Client::~Client()
{
    delete _obj;
}

Image::Image(_imageOpaquePtr *i)
{
    _obj = i;
}

Image::~Image()
{
    delete _obj;
}

GLuint Image::textureName()
{
    return _obj->obj.textureName;
}

Size Image::textureSize()
{
    Size size;
    size.width = _obj->obj.textureSize.width;
    size.height = _obj->obj.textureSize.height;
    return size;
}

}

// ---
// @TODO: experimental

namespace Utility {
void ConvertToTexture(GLuint src, GLuint texture, int width, int height)
{
    auto pixels = new GLuint[width * height * 4 * sizeof(GLuint)];

    glBindTexture(GLenum(GL_TEXTURE_RECTANGLE), src);
    glGetTexImage(GL_TEXTURE_RECTANGLE, 0, GL_RGBA, GL_UNSIGNED_INT_8_8_8_8_REV, pixels);

    glBindTexture(GLenum(GL_TEXTURE_2D), texture);
    glTexImage2D(GLenum(GL_TEXTURE_2D), 0, GL_RGBA, GLsizei(width), GLsizei(height), 0, GLenum(GL_BGRA), GLenum(GL_UNSIGNED_INT_8_8_8_8_REV), pixels);

    glTexParameteri(GLenum(GL_TEXTURE_2D), GLenum(GL_TEXTURE_MAX_LEVEL), 100);
    glTexParameteri(GLenum(GL_TEXTURE_2D), GLenum(GL_TEXTURE_WRAP_S), GL_REPEAT);
    glTexParameteri(GLenum(GL_TEXTURE_2D), GLenum(GL_TEXTURE_WRAP_T), GL_REPEAT);
    glTexParameteri(GLenum(GL_TEXTURE_2D), GLenum(GL_TEXTURE_MAG_FILTER), GL_LINEAR);
    glTexParameteri(GLenum(GL_TEXTURE_2D), GLenum(GL_TEXTURE_MIN_FILTER), GL_LINEAR_MIPMAP_LINEAR);

    gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, width, height, GL_BGRA, GL_UNSIGNED_INT_8_8_8_8_REV, pixels);

    delete[] pixels;

}
};
