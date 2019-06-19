//
//  syphon_cxx_tests.m
//  syphon_cxx_tests
//
//  Created by Alex on 19/06/2019.
//

#import <XCTest/XCTest.h>

#include "syphon_cxx.hpp"

//---
// mock

@interface SyphonClient : NSObject
@end
@implementation SyphonClient
@end

@interface SyphonServer : NSObject
@end
@implementation SyphonServer
@end

@interface SyphonServerDirectory : NSObject
@end
@implementation SyphonServerDirectory
@end

@interface SyphonImage : NSObject
@end
@implementation SyphonImage
@end

NSString* SyphonServerOptionIsPrivate;
NSString* SyphonServerOptionAntialiasSampleCount;
NSString* SyphonServerOptionDepthBufferResolution;
NSString* SyphonServerOptionStencilBufferResolution;

NSString* SyphonServerDescriptionUUIDKey;
NSString* SyphonServerDescriptionNameKey;
NSString* SyphonServerDescriptionAppNameKey;

// ---

NSString* toNSString(std::string s);
std::string toString(NSString* s);

namespace Wrapper {

struct _serverOpaquePtr {

    _serverOpaquePtr(SyphonServer* o);
    ~_serverOpaquePtr();
};

struct _clientOpaquePtr {
    _clientOpaquePtr(SyphonClient* o);
    ~_clientOpaquePtr();
};

    // these need fix:
    
//struct _serverOptionsOpaquePtr {
//    _serverOptionsOpaquePtr(NSDictionary* o);
//    ~_serverOptionsOpaquePtr();
//};

struct _serverDescriptionOpaquePtr {
    _serverDescriptionOpaquePtr(NSDictionary* o);
//    ~_serverDescriptionOpaquePtr();
};

struct _imageOpaquePtr {
    _imageOpaquePtr(SyphonImage* o);
    ~_imageOpaquePtr();
};
}



// ---

@interface syphon_cxx_tests : XCTestCase

@end

@implementation syphon_cxx_tests

- (void)testRetainCount
{
    {
        SyphonServer* server = [SyphonServer new];
        auto rc = [server retainCount];
        auto w = new Wrapper::_serverOpaquePtr(server);
        delete w;
        XCTAssertEqual(rc, [server retainCount]);
    }

    {
        SyphonClient* client = [SyphonClient new];
        auto rc = [client retainCount];
        auto w = new Wrapper::_clientOpaquePtr(client);
        delete w;
        XCTAssertEqual(rc, [client retainCount]);
    }

    //  needs fix:
    
//    {
//        NSDictionary* dict = [NSDictionary new];
//        auto rc = [dict retainCount];
//        auto w = new Wrapper::_serverOptionsOpaquePtr(dict);
//        delete w;
//        XCTAssertEqual(rc, [dict retainCount]);
//    }

    {
        NSDictionary* dict = [NSDictionary new];
        auto rc = [dict retainCount];
        auto w = new Wrapper::_serverDescriptionOpaquePtr(dict);
        delete w;
        XCTAssertEqual(rc, [dict retainCount]);
    }
    
    {
        SyphonImage* img = [SyphonImage new];
        auto rc = [img retainCount];
        auto w = new Wrapper::_imageOpaquePtr(img);
        delete w;
        XCTAssertEqual(rc, [img retainCount]);
    }
    
}

@end




