# CMakeList.txt: Üst düzey CMake proje dosyası, genel yapılandırma gerçekleştirin
# ve alt projeleri buraya ekleyin.
#
cmake_minimum_required (VERSION 3.8)

project ("bicomic")

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Destekleniyorsa MSVC derleyicileri için Çalışırken Yeniden Yükleme aracını etkinleştirin.
if (POLICY CMP0141)
  cmake_policy(SET CMP0141 NEW)
  set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "$<IF:$<AND:$<C_COMPILER_ID:MSVC>,$<CXX_COMPILER_ID:MSVC>>,$<$<CONFIG:Debug,RelWithDebInfo>:EditAndContinue>,$<$<CONFIG:Debug,RelWithDebInfo>:ProgramDatabase>>")
endif()

find_package(ImageMagick REQUIRED COMPONENTS Magick++)

# Alt projeleri ekleyin.
include_directories ("include")
add_subdirectory ("bicomic")

if(TARGET ImageMagick::Magick++)
    cmake_policy(SET CMP0079 NEW)
    # CMake >= 3.26: imported target (temiz yol)
    target_link_libraries(bicomic PRIVATE ImageMagick::Magick++)
else()
    # Daha eski CMake icin degisken tabanli fallback
    target_include_directories(bicomic PRIVATE ${ImageMagick_INCLUDE_DIRS})
    target_link_libraries(bicomic PRIVATE ${ImageMagick_LIBRARIES})
endif()