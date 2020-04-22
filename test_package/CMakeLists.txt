cmake_minimum_required(VERSION 2.8.11)
project(test_package)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(test_package_shaderc_c test_package_shaderc.c)
target_link_libraries(test_package_shaderc_c ${CONAN_LIBS})
set_property(TARGET test_package_shaderc_c PROPERTY LINKER_LANGUAGE CXX)

add_executable(test_package_shaderc_cpp test_package_shaderc.cpp)
target_link_libraries(test_package_shaderc_cpp ${CONAN_LIBS})
set_property(TARGET test_package_shaderc_cpp PROPERTY CXX_STANDARD 11)

if(SHADERC_WITH_SPVC)
  add_executable(test_package_spvc_c test_package_spvc.c)
  target_link_libraries(test_package_spvc_c ${CONAN_LIBS})
  set_property(TARGET test_package_spvc_c PROPERTY LINKER_LANGUAGE CXX)

  add_executable(test_package_spvc_cpp test_package_spvc.cpp)
  target_link_libraries(test_package_spvc_cpp ${CONAN_LIBS})
  set_property(TARGET test_package_spvc_cpp PROPERTY CXX_STANDARD 11)
endif()
