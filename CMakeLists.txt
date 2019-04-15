cmake_minimum_required(VERSION 2.8.12)
project(syphonpy-proj)
enable_language(CXX C)

set(CMAKE_C_FLAGS "-x objective-c")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=gnu99 -funroll-loops -fomit-frame-pointer")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --std=gnu++11 -funroll-loops -fomit-frame-pointer")

include_directories(submodules/Syphon-Framework)

add_subdirectory(submodules/pybind11)

set(SOURCE_FILES
  syphon_cxx.mm
  )

file (GLOB SOURCE_SYPHON
    submodules/Syphon-Framework/*.m
    submodules/Syphon-Framework/*.c
    )

set_source_files_properties(${SOURCE_FILES} PROPERTIES COMPILE_FLAGS "-x objective-c++")
set_source_files_properties(${SOURCE_SYPHON} PROPERTIES COMPILE_FLAGS "-x objective-c -include Syphon_Prefix.pch -include Foundation/Foundation.h -include OpenGL/OpenGL.h -DDEBUG")


macro(ADD_OSX_FRAMEWORK fwname target)
    find_library(FRAMEWORK_${fwname}
    NAMES ${fwname}
    PATHS ${CMAKE_OSX_SYSROOT}/System/Library
    PATH_SUFFIXES Frameworks
    NO_DEFAULT_PATH)
    if( ${FRAMEWORK_${fwname}} STREQUAL FRAMEWORK_${fwname}-NOTFOUND)
        MESSAGE(ERROR ": Framework ${fwname} not found")
    else()
        TARGET_LINK_LIBRARIES(${target} PUBLIC "${FRAMEWORK_${fwname}}/${fwname}")
        MESSAGE(STATUS "Framework ${fwname} found at ${FRAMEWORK_${fwname}}")
    endif()
endmacro(ADD_OSX_FRAMEWORK)

add_library(syphon_lib STATIC  ${SOURCE_SYPHON})
ADD_OSX_FRAMEWORK(Foundation syphon_lib)
ADD_OSX_FRAMEWORK(OpenGL syphon_lib)
ADD_OSX_FRAMEWORK(AppKit syphon_lib)

SET(CMAKE_EXE_LINKER_FLAGS "-bind_at_load -framework Foundation -framework AppKit -framework OpenGL -w")

pybind11_add_module(syphonpy wrapper.cpp syphon_cxx.mm)
target_link_libraries(syphonpy PRIVATE syphon_lib)
