#ifndef syphon_cxx_h
#define syphon_cxx_h

#include <OpenGL/OpenGL.h>
#include <functional>
#include <memory>
#include <string>
#include <vector>

namespace Wrapper {
struct Origin {
    float x = 0;
    float y = 0;
};
struct Size {
    float width = 0;
    float height = 0;
};

struct Rect {
    Origin origin;
    Size size;
};

// ---

struct _serverOpaquePtr;
struct _clientOpaquePtr;
struct _serverOptionsOpaquePtr;
struct _serverDescriptionOpaquePtr;
struct _imageOpaquePtr;

// ---

struct ServerOptions {
public:
    ServerOptions(_serverOptionsOpaquePtr*);

    bool isPrivate = false;
    u_int8_t antialiasSampleCount = 0;
    u_int8_t depthBufferResolution = 0;
    u_int8_t stencilBufferResolution = 0;
};

// ---

class ServerDescription {
    _serverDescriptionOpaquePtr* _ptr = nullptr;

public:
    ServerDescription(_serverDescriptionOpaquePtr* d = nullptr);
    ServerDescription(const ServerDescription& src);

    std::string UUID;
    std::string Name;
    std::string AppName;
    // not including icon yet

    _serverDescriptionOpaquePtr* toDictionary();
};

// ---

class Server {
    _serverOpaquePtr* _obj = 0;

    bool _error = false;

    CGLContextObj _context;
    std::string _name;

public:
    Server(std::string name);
    Server(const Server& src);
    ~Server();

    void publishFrameTexture(GLuint texID, Rect region, Size size, bool flipped);

    inline bool errorState() { return _error; }

    CGLContextObj& context() { return _context; };
    std::string name() { return _name; };
    ServerDescription serverDescription();

    bool hasClients();

    void stop();
};

// ---
class ServerDirectory {
public:
    static std::vector<ServerDescription> servers();
    static std::vector<ServerDescription> serversMatchingNameAppName(std::string name, std::string appName);
};

// ---
class Client;
using ClientPtr = std::shared_ptr<_clientOpaquePtr>;
using NewFrameHandlerFunc = std::function<void(ClientPtr)>;

const NewFrameHandlerFunc emptyFrameHandler = [](ClientPtr) {};

// ---
class Image {
    _imageOpaquePtr *_obj = nullptr;
public:
    Image(_imageOpaquePtr *i = nullptr);
    Image(const Image& src);
    ~Image();
    GLuint textureName();
    Size textureSize();
};

// ---

class Client {
    _clientOpaquePtr* _obj = 0;

    bool _error = false;

    CGLContextObj _context;

public:
    Client(ServerDescription descr, NewFrameHandlerFunc handler = emptyFrameHandler);
    Client(const Client& src);
    ~Client();

    Image newFrameImage();
    void stop();
    CGLContextObj context() { return _context; };

    bool isValid();
    bool hasNewFrame();

    ServerDescription serverDescription();

    inline bool errorState() { return _error; }
};
};

namespace Utility {
void ConvertToTexture(GLuint src, GLuint texture, int width, int height);
}

#endif
