cmake_minimum_required(VERSION 3.10)
# Set the C++ standard to C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Add debugging and coverage flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -ftest-coverage -fprofile-arcs")
project(manage_employee_schedule)

include(FetchContent)

FetchContent_Declare(
  yaml-cpp
  GIT_REPOSITORY https://github.com/jbeder/yaml-cpp.git
  GIT_TAG master # Can be a tag (yaml-cpp-x.x.x), a commit hash, or a branch name (master)
)
FetchContent_MakeAvailable(yaml-cpp)

add_executable(manage_employee_schedule manage_employee_schedule.cpp)
target_link_libraries(manage_employee_schedule PUBLIC yaml-cpp::yaml-cpp) # The library or executable that require yaml-cpp library