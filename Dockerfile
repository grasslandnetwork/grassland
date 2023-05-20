FROM rust:1.69.0-bullseye as builder

# Install required dependencies
RUN \
    --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y \
    libwebkit2gtk-4.0-dev \
    build-essential \
    curl \      
    cmake \
    wget \
    unzip \
    pkg-config \
    libprotobuf-dev \
    protobuf-compiler \
    libssl-dev \
    libgtk-3-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev \
    clang \
    libclang-dev


# workaround to make clang_sys crate detect installed libclang
# RUN ln -fs libclang.so.1 /usr/lib/llvm-10/lib/libclang.so
# Doesn't work. ERROR: "ln: failed to create symbolic link '/usr/lib/llvm-10/lib/libclang.so': No such file or directory"  

ENV NODE_VERSION 16
RUN curl -fsSL https://deb.nodesource.com/setup_$NODE_VERSION.x | bash - \
    && apt-get install -y nodejs

# stage 2
FROM builder as opencvinstaller

# Download OpenCV sources
RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/4.x.zip && \
    wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.x.zip

# Unzip sources and remove archives
RUN unzip opencv.zip && rm opencv.zip && \
    unzip opencv_contrib.zip && rm opencv_contrib.zip

# Create build folder and switch to it
RUN mkdir -p build && cd build

# Configure the build
RUN cmake \
    -D BUILD_CUDA_STUBS=OFF \
	-D BUILD_DOCS=OFF \
	-D BUILD_EXAMPLES=OFF \
	-D BUILD_IPP_IW=ON \
	-D BUILD_ITT=ON \
	-D BUILD_JASPER=OFF \
	-D BUILD_JAVA=OFF \
	-D BUILD_JPEG=OFF \
	-D BUILD_OPENEXR=OFF \
	-D BUILD_OPENJPEG=OFF \
	-D BUILD_PERF_TESTS=OFF \
	-D BUILD_PNG=OFF \
	-D BUILD_PROTOBUF=ON \
	-D BUILD_SHARED_LIBS=ON \
	-D BUILD_TBB=OFF \
	-D BUILD_TESTS=OFF \
	-D BUILD_TIFF=OFF \
	-D BUILD_WEBP=OFF \
	-D BUILD_WITH_DEBUG_INFO=OFF \
	-D BUILD_WITH_DYNAMIC_IPP=OFF \
	-D BUILD_ZLIB=OFF \
	-D BUILD_opencv_apps=OFF \
	-D BUILD_opencv_python2=OFF \
	-D BUILD_opencv_python3=OFF \
	-D CMAKE_BUILD_TYPE=Release \
	-D CV_DISABLE_OPTIMIZATION=OFF \
	-D CV_ENABLE_INTRINSICS=ON \
	-D ENABLE_CONFIG_VERIFICATION=OFF \
	-D ENABLE_FAST_MATH=OFF \
	-D ENABLE_LTO=OFF \
	-D ENABLE_PIC=ON \
	-D ENABLE_PRECOMPILED_HEADERS=OFF \
	-D INSTALL_CREATE_DISTRIB=OFF \
	-D INSTALL_C_EXAMPLES=OFF \
	-D INSTALL_PYTHON_EXAMPLES=OFF \
	-D INSTALL_TESTS=OFF \
	-D OPENCV_ENABLE_MEMALIGN=OFF \
	-D OPENCV_ENABLE_NONFREE=ON \
	-D OPENCV_FORCE_3RDPARTY_BUILD=OFF \
	-D OPENCV_GENERATE_PKGCONFIG=OFF \
	-D PROTOBUF_UPDATE_FILES=OFF \
	-D WITH_1394=ON \
	-D WITH_ADE=ON \
	-D WITH_ARAVIS=OFF \
	-D WITH_CLP=OFF \
	-D WITH_CUBLAS=OFF \
	-D WITH_CUDA=OFF \
	-D WITH_CUFFT=OFF \
	-D WITH_EIGEN=ON \
	-D WITH_FFMPEG=ON \
	-D WITH_GDAL=ON \
	-D WITH_GDCM=OFF \
	-D WITH_GIGEAPI=OFF \
	-D WITH_GPHOTO2=ON \
	-D WITH_GSTREAMER=ON \
	-D WITH_GSTREAMER_0_10=OFF \
	-D WITH_GTK=OFF \
	-D WITH_GTK_2_X=OFF \
	-D WITH_HALIDE=OFF \
	-D WITH_IMGCODEC_HDcR=ON \
	-D WITH_IMGCODEC_PXM=ON \
	-D WITH_IMGCODEC_SUNRASTER=ON \
	-D WITH_INF_ENGINE=OFF \
	-D WITH_IPP=ON \
	-D WITH_ITT=ON \
	-D WITH_JASPER=OFF \
	-D WITH_JPEG=ON \
	-D WITH_LAPACK=ON \
	-D WITH_LIBV4L=OFF \
	-D WITH_MATLAB=OFF \
	-D WITH_MFX=OFF \
	-D WITH_OPENCL=ON \
	-D WITH_OPENCLAMDBLAS=ON \
	-D WITH_OPENCLAMDFFT=ON \
	-D WITH_OPENCL_SVM=ON \
    -D WITH_VULKAN= ON \
	-D WITH_OPENEXR=OFF \
	-D WITH_OPENGL=ON \
	-D WITH_OPENMP=OFF \
	-D WITH_OPENNI2=OFF \
	-D WITH_OPENNI=OFF \
	-D WITH_OPENVX=OFF \
	-D WITH_PNG=ON \
	-D WITH_PROTOBUF=ON \
	-D WITH_PTHREADS_PF=ON \
	-D WITH_PVAPI=OFF \
	-D WITH_QT=ON \
	-D WITH_QUIRC=ON \
	-D WITH_TBB=ON \
	-D WITH_TIFF=ON \
	-D WITH_UNICAP=OFF \
	-D WITH_V4L=ON \
	-D WITH_VA=ON \
	-D WITH_VA_INTEL=ON \
	-D WITH_VTK=ON \
	-D WITH_WEBP=ON \
	-D WITH_XIMEA=OFF \
	-D WITH_XINE=OFF \
    -D BUILD_JPEG=ON \
	-D BUILD_OPENJPEG=ON \
	-D BUILD_PNG=ON \
	-D BUILD_SHARED_LIBS=OFF \
	-D BUILD_TBB=ON \
	-D BUILD_TIFF=ON \
	-D BUILD_WEBP=ON \
	-D BUILD_ZLIB=ON \
	-D BUILD_opencv_freetype=OFF \
	-D OPENCV_FORCE_3RDPARTY_BUILD=ON \
	-D WITH_1394=OFF \
	-D WITH_FFMPEG=OFF \
	-D WITH_FREETYPE=OFF \
	-D WITH_GDAL=OFF \
	-D WITH_GPHOTO2=OFF \
	-D WITH_GSTREAMER=OFF \
	-D WITH_GTK=OFF \
	-D WITH_LAPACK=OFF \
	-D WITH_OPENGL=OFF \
	-D WITH_QT=OFF \
    -D BUILD_SHARED_LIBS=NO \
    -D CMAKE_INSTALL_PREFIX=/opt/opencv \
    -D BUILD_DOCS=OFF \
    -D BUILD_EXAMPLES=OFF \
    -D BUILD_TESTS=OFF -DBUILD_PERF_TESTS=OFF \
    -D BUILD_opencv_java=OFF \
    -D BUILD_opencv_python=OFF \
    -D OPENCV_DNN_OPENCL=ON \
    -D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib-4.x/modules \
    ../opencv-4.x

# Compile OpenCV
RUN make -j8 && make install

# stage 3
FROM opencvinstaller as packageinstaller

# install Tauri CLI
RUN cargo install tauri-cli

WORKDIR /usr/src/grassland

# Copy your Rust project into the container.
# Copy over nodejs package management files separately so docker will only reinstall dependencies if they've changed. See https://docs.docker.com/build/cache/#order-your-layers
COPY package.json package-lock.json .
# Install dependencies
RUN npm install
# Then copy over project files
COPY . .


# stage 4
FROM packageinstaller as appbuilder

# Set environment variables for Rust project
ENV OPENCV_LINK_LIBS="opencv_highgui,opencv_objdetect,opencv_dnn,opencv_videostab,opencv_calib3d,opencv_features2d,opencv_stitching,opencv_flann,opencv_videoio,opencv_rgbd,opencv_aruco,opencv_video,opencv_ml,opencv_imgcodecs,opencv_imgproc,opencv_core,ittnotify,tbb,liblibwebp,liblibtiff,liblibjpeg-turbo,liblibpng,liblibopenjp2,ippiw,ippicv,liblibprotobuf,quirc,zlib" \
    OPENCV_LINK_PATHS="/opt/opencv/lib,/opt/opencv/lib/opencv4/3rdparty,/usr/lib/x86_64-linux-gnu" \
    OPENCV_INCLUDE_PATHS="/opt/opencv/include/opencv4"


# # Build the Rust project
# # RUN cargo build --release

RUN cargo tauri build            # Run build