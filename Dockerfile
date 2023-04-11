# Set the base image according to the target platform
# This example uses ubuntu-latest as the base image
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/New_York


# Set the working directory
WORKDIR /app

# Install Linux System Dependencies and Tauri Prerequisites
RUN apt-get update && \
    apt-get install -y curl build-essential git wget libwebkit2gtk-4.0-dev \
    libssl-dev libgtk-3-dev libayatana-appindicator3-dev librsvg2-dev


# Set up timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


ENV NODE_VERSION 18
RUN curl -fsSL https://deb.nodesource.com/setup_$NODE_VERSION.x | bash - \
    && apt-get install -y nodejs


# Install Rust stable
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# Install Opencv 
RUN apt install -y libopencv-dev clang libclang-dev


# Add cargo binaries to the PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# install Tauri CLI
RUN cargo install tauri-cli

# Copy project files to the container
COPY . .


RUN npm install

RUN cargo tauri build
