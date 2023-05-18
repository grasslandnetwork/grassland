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
    clang


# workaround to make clang_sys crate detect installed libclang
# RUN ln -fs libclang.so.1 /usr/lib/llvm-10/lib/libclang.so
# Doesn't work. ERROR: "ln: failed to create symbolic link '/usr/lib/llvm-10/lib/libclang.so': No such file or directory"  

ENV NODE_VERSION 18
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
RUN cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=NO \
  -DCMAKE_INSTALL_PREFIX=/opt/opencv -DBUILD_DOCS=OFF -DBUILD_EXAMPLES=OFF \
  -DBUILD_TESTS=OFF -DBUILD_PERF_TESTS=OFF -DBUILD_opencv_java=OFF \
  -DBUILD_opencv_python=OFF -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib-4.x/modules \
  ../opencv-4.x

# Compile OpenCV
RUN make -j8 && make install

# stage 3
FROM opencvinstaller as apploader

# Set environment variables for Rust project
ENV OPENCV_LINK_LIBS="opencv_imgproc,opencv_face,opencv_objdetect,opencv_dnn,opencv_dnn_objdetect,opencv_core,ippiw,ittnotify,ippicv,liblibprotobuf,z" \
    OPENCV_LINK_PATHS="/opt/opencv/lib,/opt/opencv/lib/opencv4/3rdparty,/usr/lib/x86_64-linux-gnu" \
    OPENCV_INCLUDE_PATHS="/opt/opencv/include/opencv4"

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
FROM apploader as appbuilder

# # Build the Rust project
# # RUN cargo build --release

RUN cargo tauri build            # Run build