cmake_minimum_required(VERSION 2.8)
project(libhtts)
add_subdirectory(src)
install(DIRECTORY data_tts DESTINATION "${CMAKE_INSTALL_DATADIR}/AhoTTS")
