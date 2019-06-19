#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "syphon_cxx.hpp"

namespace py = pybind11;

PYBIND11_MODULE(syphonpy, m)
{

    // ---
    py::class_<Wrapper::Origin>(m, "Origin")
        .def_readwrite("x", &Wrapper::Origin::x)
        .def_readwrite("y", &Wrapper::Origin::y);
    py::class_<Wrapper::Size>(m, "Size")
        .def_readwrite("width", &Wrapper::Size::width)
        .def_readwrite("height", &Wrapper::Size::height);
    py::class_<Wrapper::Rect>(m, "Rect")
        .def_readwrite("origin", &Wrapper::Rect::origin)
        .def_readwrite("size", &Wrapper::Rect::size);

    m.def("MakeRect", [](float x, float y, float w, float h) {
        Wrapper::Rect ret;
        ret.origin.x = x;
        ret.origin.y = y;
        ret.size.width = w;
        ret.size.height = h;
        return ret;
    });

    m.def("MakeSize", [](float w, float h) {
        Wrapper::Size ret;
        ret.width = w;
        ret.height = h;
        return ret;
    });

    // ---
    py::class_<Wrapper::ServerOptions>(m, "ServerOptions")
        .def_readwrite("is_private", &Wrapper::ServerOptions::isPrivate)
        .def_readwrite("antialias_sample_count", &Wrapper::ServerOptions::antialiasSampleCount)
        .def_readwrite("depth_buffer_resolution", &Wrapper::ServerOptions::depthBufferResolution)
        .def_readwrite("stencil_buffer_resolution", &Wrapper::ServerOptions::stencilBufferResolution);

    // ---
    py::class_<Wrapper::ServerDescription>(m, "ServerDescription")
        .def_readwrite("uuid", &Wrapper::ServerDescription::UUID)
        .def_readwrite("name", &Wrapper::ServerDescription::Name)
        .def_readwrite("app_name", &Wrapper::ServerDescription::AppName);

    // ---
    py::class_<Wrapper::Server>(m, "SyphonServer")
        .def(py::init<std::string>())

        .def("publish_frame_texture", &Wrapper::Server::publishFrameTexture)

        .def("error_state", &Wrapper::Server::errorState)
        // @TODO: opaque pointer
        //        .def("context", &Wrapper::Server::context)
        .def("name", &Wrapper::Server::name)
        .def("serverDescription", &Wrapper::Server::serverDescription)
        .def("has_clients", &Wrapper::Server::hasClients)
        //
        ;

    // ---
    py::class_<Wrapper::ServerDirectory>(m, "ServerDirectory")
        .def("servers", &Wrapper::ServerDirectory::servers)
        .def("servers_matching_name_app_name", &Wrapper::ServerDirectory::serversMatchingNameAppName)
        //
        ;

    // ---
    py::class_<Wrapper::Image>(m, "Image")
        .def("texture_name", &Wrapper::Image::textureName)
        .def("texture_size", &Wrapper::Image::textureSize)
        //
        ;

    // ---
    py::class_<Wrapper::Client>(m, "SyphonClient")
        .def(py::init<Wrapper::ServerDescription>()) // no callback yet

        .def("new_frame_image", &Wrapper::Client::newFrameImage)
        .def("stop", &Wrapper::Client::stop)
        // @TODO: opaque pointer
        //                .def("context", &Wrapper::Client::context)

        .def("is_valid", &Wrapper::Client::isValid)
        .def("has_new_frame", &Wrapper::Client::hasNewFrame)

        .def("server_description", &Wrapper::Client::serverDescription)

        .def("error_state", &Wrapper::Client::errorState)

        //
        ;

    m.def("convert_to_texture", &Utility::ConvertToTexture);
}
