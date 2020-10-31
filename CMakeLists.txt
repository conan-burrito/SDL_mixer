cmake_minimum_required(VERSION 3.1.2)
project(SDL_mixer C)

if(EXISTS "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
  include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
else()
  include(conanbuildinfo.cmake)
endif()
conan_basic_setup()

find_package(SDL2 REQUIRED CONFIG)

option(WITH_FLAC OFF)
option(WITH_MAD OFF)
option(WITH_MICMOD OFF)
option(WITH_MODPLUG OFF)
option(WITH_MPEG OFF)
option(WITH_OPUS OFF)
option(WITH_OGG ON)

set(SDM_LIBRARY SDL2_mixer)
set(SDM_NAMESPACE SDL2_mixer)
set(SDM_CONFIG ${SDM_NAMESPACE}Config)

add_library(${SDM_LIBRARY}
  src/effect_position.c
  src/effect_stereoreverse.c
  src/effects_internal.c

  src/load_aiff.c
  src/load_voc.c

  src/mixer.c
  src/music.c
  src/music_wav.c
)

if(WITH_FLAC)
  target_sources(${SDM_LIBRARY} PRIVATE src/music_flac.c)
endif()

if(WITH_MAD)
  target_sources(${SDM_LIBRARY} PRIVATE src/music_mad.c)
endif()

if(WITH_MICMOD)
  target_sources(${SDM_LIBRARY} PRIVATE src/music_mikmod.c)
endif()

if(WITH_MODPLUG)
  target_sources(${SDM_LIBRARY} PRIVATE src/music_modplug.c)
endif()

if(WITH_MPEG)
  target_sources(${SDM_LIBRARY} PRIVATE src/music_mpg123.c)
endif()

if(WITH_OPUS)
  target_sources(${SDM_LIBRARY} PRIVATE src/music_opus.c)
endif()

if(WITH_OGG)
  target_sources(${SDM_LIBRARY} PRIVATE src/music_ogg.c)
  target_compile_definitions(${SDM_LIBRARY} PRIVATE MUSIC_OGG)
endif()

target_include_directories(${SDM_LIBRARY} PRIVATE src)
set_target_properties(${SDM_LIBRARY} PROPERTIES OUTPUT_NAME SDL2_mixer)
target_link_libraries(${SDM_LIBRARY} PUBLIC ${CONAN_LIBS})
target_include_directories(${SDM_LIBRARY} PRIVATE ${CONAN_INCLUDE_DIRS_SDL2}/SDL2 ${CONAN_INCLUDE_DIRS})

target_compile_definitions(${SDM_LIBRARY} PRIVATE MUSIC_WAV MUSIC_CMD)

set_target_properties(${SDM_LIBRARY}
    PROPERTIES
        VERSION ${SDM_VERSION_STRING}
        SOVERSION ${SDM_VERSION_MAJOR}
)

set(SDM_HEADERS
  src/SDL_mixer.h
)

export(
    TARGETS ${SDM_LIBRARY}
    NAMESPACE ${SDM_NAMESPACE}::
    FILE "${CMAKE_CURRENT_BINARY_DIR}/${SDM_CONFIG}.cmake"
)

include(GNUInstallDirs)
install(
    TARGETS ${SDM_LIBRARY}
    EXPORT ${SDM_CONFIG}
    BUNDLE DESTINATION ${CMAKE_INSTALL_BINDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

install(FILES ${SDM_HEADERS} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(
    EXPORT ${SDM_CONFIG}
    DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/${CMAKE_PROJECT_NAME}"
    NAMESPACE ${SDM_NAMESPACE}::
)
