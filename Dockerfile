# Set the base image according to the target platform
# This example uses ubuntu-latest as the base image
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/New_York


# Set the working directory
WORKDIR /app

# Install Linux System Dependencies
RUN apt-get update && \
    apt-get install -y curl build-essential git libwebkit2gtk-4.0-dev \
    libssl-dev libgtk-3-dev libayatana-appindicator3-dev librsvg2-dev
    
RUN apt-get install -y  pkg-config clang \
    libharfbuzz0b zip unzip tar bison gperf libx11-dev libxft-dev libxext-dev \
    libgles2-mesa-dev autoconf libtool build-essential libxrandr-dev \
    libxi-dev libxcursor-dev libxdamage-dev libxinerama-dev \
    libdbus-1-dev libxtst-dev libdbus-1-3  \
    librsvg2-dev jq



# Set up timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Clone your repository and its submodules
#  RUN git clone --recursive <your-repository-url> .

# Install Node.js 16
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs

# Install Rust stable
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# Here we will install vcpkg for Ubuntu 20.04


ENV VCPKG_ROOT /root/build/vcpkg
ENV VCPKG_VERSION 2023.02.24
ENV VCPKG_DEFAULT_TRIPLET x64-linux

RUN apt-get update && \
    apt-get install -y git cmake build-essential ninja-build

RUN if [ ! -e "${VCPKG_ROOT}" ]; then \
        git clone https://github.com/Microsoft/vcpkg.git "${VCPKG_ROOT}"; \
    fi && \
    cd "${VCPKG_ROOT}" && \
    git fetch --all --prune --tags && \
    git status && \
    git checkout . && \
    git checkout "${VCPKG_VERSION}" && \
    ./bootstrap-vcpkg.sh -disableMetrics && \
    echo "set(VCPKG_BUILD_TYPE release)" >> triplets/x64-linux.cmake

# Install LLVM
RUN apt-get install -y llvm-10-dev

# Workaround to make clang_sys crate detect installed libclang
RUN ln -s libclang.so.1 /usr/lib/llvm-10/lib/libclang.so

# Install OpenCV with contrib and nonfree components
RUN cd "${VCPKG_ROOT}" && \
    ./vcpkg install --recurse "opencv[contrib,nonfree]"
    

# Build OpenCV 4
# RUN /vcpkg/vcpkg install opencv4[dnn]:x64-linux
# if the uncommmented one above doesn't work, add " x64-linux" to it


# Add cargo binaries to the PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# install Tauri CLI
RUN cargo install tauri-cli

# Copy project files to the container
COPY . .

# Build App
RUN npm install && \
    OPENCV_DISABLE_PROBES=pkg_config,cmake

RUN cargo tauri build
