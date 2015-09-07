cmake_minimum_required(VERSION 2.8)
 
project(myaffine)
 
find_package(ITK REQUIRED)
include(${ITK_USE_FILE})
if (ITKVtkGlue_LOADED)
  find_package(VTK REQUIRED)
  include(${VTK_USE_FILE})
endif()
 
add_executable(myaffine MACOSX_BUNDLE ImageRegistration9.cxx)
add_executable(myaffine2 MACOSX_BUNDLE simple_affine2.cxx)

if( "${ITK_VERSION_MAJOR}" LESS 4 )
  target_link_libraries(myaffine ITKReview ${ITK_LIBRARIES})
else( "${ITK_VERSION_MAJOR}" LESS 4 )
  target_link_libraries(myaffine ${ITK_LIBRARIES})
endif( "${ITK_VERSION_MAJOR}" LESS 4 )
