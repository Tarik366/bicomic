# CMakeList.txt: bicomic için CMake projesi, kaynağı ekleyin ve tanımlayın
# projeye özgü mantık burada bulunur.
#

# Kaynağı bu projenin yürütülebilir dosyasına ekleyin.
add_executable (bicomic "bicomic.cpp" "bicomic.h" "../include/interpretter.h" "stylesheets.cpp")

if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET bicomic PROPERTY CXX_STANDARD 20)
endif()

# TODO: Gerekirse testleri ve yükleme hedeflerini ekleyin.
