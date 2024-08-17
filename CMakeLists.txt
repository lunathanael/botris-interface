cmake_minimum_required(VERSION 3.15...3.27)

set(BOTRIS_CORE_DIR "botris/_core")

project(botris
  VERSION ${SKBUILD_PROJECT_VERSION}
  LANGUAGES CXX
)

# Use C++20 standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Specify the C++ compiler
if(NOT CMAKE_CXX_COMPILER)
  message(FATAL_ERROR "No C++ compiler specified. A version of GCC >= 13 is recommended. Aborting.")
endif()

# Check the compiler ID and issue warnings if necessary
if ("${CMAKE_CXX_COMPILER_ID}" MATCHES "GNU")
    execute_process(
        COMMAND ${CMAKE_CXX_COMPILER} -dumpversion OUTPUT_VARIABLE GCC_VERSION)
    message(STATUS "Using GCC version ${GCC_VERSION}.")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++20")

elseif ("${CMAKE_CXX_COMPILER_ID}" MATCHES "Clang")
    execute_process(
        COMMAND ${CMAKE_CXX_COMPILER} --version OUTPUT_VARIABLE CLANG_VERSION_STRING)
    string(REGEX MATCH "[0-9]+\\.[0-9]+\\.[0-9]+" CLANG_VERSION ${CLANG_VERSION_STRING})
    message(WARNING "It is recommended to use GCC for this project.")
    message(STATUS "Using Clang version ${CLANG_VERSION}.")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++20")

elseif ("${CMAKE_CXX_COMPILER_ID}" MATCHES "MSVC")
    message(WARNING "It is recommended to use GCC for this project.")
    message(STATUS "Using MSVC version ${MSVC_VERSION}.")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /std:c++20")

else ()
    message(WARNING "You are using an unrecognized compiler (${CMAKE_CXX_COMPILER_ID}). Ensure it is C++20 compliant.")
endif()

# Check if the compiler supports C++20
include(CheckCXXCompilerFlag)

if ("${CMAKE_CXX_COMPILER_ID}" MATCHES "MSVC")
    CHECK_CXX_COMPILER_FLAG("/std:c++20" CXX20_SUPPORTED)
else ()
    CHECK_CXX_COMPILER_FLAG("-std=c++20" CXX20_SUPPORTED)
endif()

if (NOT CXX20_SUPPORTED)
    message(WARNING "${PROJECT_NAME} requires a C++20-compliant compiler. The selected compiler (${CMAKE_CXX_COMPILER_ID}) does not support C++20.")

    set(POTENTIAL_GCC_VERSIONS 15 13)
    foreach(VERSION IN LISTS POTENTIAL_GCC_VERSIONS)
        find_program(CANDIDATE_GCC_COMPILER NAMES g++-${VERSION} PATHS ENV PATH NO_DEFAULT_PATH)
        if (CANDIDATE_GCC_COMPILER)
            message(STATUS "Found GCC version ${VERSION}. Attempting to switch to ${CANDIDATE_GCC_COMPILER}.")
            set(CMAKE_CXX_COMPILER ${CANDIDATE_GCC_COMPILER} CACHE STRING "C++ compiler" FORCE)

            execute_process(
                COMMAND ${CMAKE_CXX_COMPILER} -dumpversion OUTPUT_VARIABLE GCC_VERSION)
            if (GCC_VERSION VERSION_GREATER_EQUAL 13)
                message(STATUS "Successfully switched to GCC version ${GCC_VERSION}.")
                break()
            else()
                message(STATUS "Failed to switch to GCC version ${VERSION}.")
            endif ()
        endif ()
    endforeach()

    CHECK_CXX_COMPILER_FLAG("-std=c++20" CXX20_SUPPORTED)

    if (NOT (GCC_VERSION VERSION_GREATER_EQUAL 13 AND CXX20_SUPPORTED))
        message(FATAL_ERROR "${PROJECT_NAME} requires a C++20-compliant compiler. Failed to find a suitable version of GCC. GCC 13 or greater is recommended.")
    endif ()
endif()

# Warn if the user invokes CMake directly
if (NOT SKBUILD)
  message(WARNING "\
  This CMake file is meant to be executed using 'scikit-build-core'.
  Running it directly will almost certainly not produce the desired
  result. If you are a user trying to install this package, use the
  command below, which will install all necessary build dependencies,
  compile the package in an isolated environment, and then install it.
  =====================================================================
   $ pip install .
  =====================================================================
  If you are a software developer, and this is your own package, then
  it is usually much more efficient to install the build dependencies
  in your environment once and use the following command that avoids
  a costly creation of a new virtual environment at every compilation:
  =====================================================================
   $ pip install nanobind scikit-build-core[pyproject]
   $ pip install --no-build-isolation -ve .
  =====================================================================
  You may optionally add -Ceditable.rebuild=true to auto-rebuild when
  the package is imported. Otherwise, you need to rerun the above
  after editing C++ files.")
endif()

if (CMAKE_VERSION VERSION_LESS 3.18)
  set(DEV_MODULE Development)
else()
  set(DEV_MODULE Development.Module)
endif()

find_package(Python 3.10 COMPONENTS Interpreter ${DEV_MODULE} REQUIRED)

if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

# Detect the installed nanobind package and import it into CMake
execute_process(
  COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
  OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
find_package(nanobind CONFIG REQUIRED)

nanobind_add_module(
  # Name of the extension
  _core

  NOMINSIZE
  LTO

  # Target the stable ABI for Python 3.12+, which reduces
  # the number of binary wheels that must be built. This
  # does nothing on older Python versions
  STABLE_ABI

  # Source code goes here
  ${BOTRIS_CORE_DIR}/main_module.cpp
  ${BOTRIS_CORE_DIR}/piece.cpp
  ${BOTRIS_CORE_DIR}/game.cpp
  ${BOTRIS_CORE_DIR}/board.cpp
  ${BOTRIS_CORE_DIR}/mode.cpp
  ${BOTRIS_CORE_DIR}/constants.cpp
)

target_compile_features(_core PUBLIC cxx_std_20)
target_compile_definitions(_core PRIVATE VERSION_INFO=${PROJECT_VERSION})
target_include_directories(_core PUBLIC)

add_subdirectory(${BOTRIS_CORE_DIR}/ShakTrisLib)

target_compile_features(ShakTris PUBLIC cxx_std_20)
target_link_libraries(_core PRIVATE ShakTris)

install(TARGETS _core DESTINATION .)
