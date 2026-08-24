# CMakeList.txt: Üst düzey CMake proje dosyası, genel yapılandırma gerçekleştirin
# ve alt projeleri buraya ekleyin.
#
cmake_minimum_required (VERSION 3.8)

project ("bicomic")

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Destekleniyorsa MSVC derleyicileri için Çalışırken Yeniden Yükleme aracını etkinleştirin.
if (POLICY CMP0141)
  cmake_policy(SET CMP0141 NEW)
  set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "$<IF:$<AND:$<C_COMPILER_ID:MSVC>,$<CXX_COMPILER_ID:MSVC>>,$<$<CONFIG:Debug,RelWithDebInfo>:EditAndContinue>,$<$<CONFIG:Debug,RelWithDebInfo>:ProgramDatabase>>")
endif()

cmake_policy(SET CMP0079 NEW)

find_package(ImageMagick REQUIRED COMPONENTS Magick++)

# Alt projeleri ekleyin.
include_directories("include")
add_subdirectory(external/psd_sdk/src/Psd Psd)
add_subdirectory("bicomic")

target_include_directories(bicomic PRIVATE ${ImageMagick_INCLUDE_DIRS})
target_link_libraries(bicomic PRIVATE ImageMagick::Magick++)

target_include_directories(bicomic PRIVATE external/psd_sdk/src)
target_link_libraries(bicomic PRIVATE Psd)