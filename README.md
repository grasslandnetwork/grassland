# Grassland
Grassland Full Node Implementation


## Platforms

Grassland Full Node supports the following platforms:

| Platform                 | Versions        |
| :----------------------- | :-------------- |
| Windows                  | 7 and above     |
| macOS                    | 10.15 and above |
| Linux                    | See below       |
| iOS/iPadOS (coming soon) |                 |
| Android (coming soon)    |                 |


## Installation 

Installers are available for Windows, macOS and Linux on the [Latest Releases page](https://github.com/grasslandnetwork/grassland/releases/latest)



# Compiling From Source 

Grassland Full Node is wriiten in the Rust and JavaScript languages using the Tauri application framework.


## Installation

### Installing Prerequisites 

#### Install Rust and System Dependencies
Follow [these instructions](https://tauri.app/v1/guides/getting-started/prerequisites) to install Rust and system dependencies


### Install Tauri's Rust CLI 

    cargo install tauri-cli


#### Install Node.js

Instructions for installing Node.js can be found [here](https://nodejs.org/en/download/).


### Clone the repository

Assuming [Git](https://git-scm.com/) is installed, clone the repository:

    git clone https://github.com/grasslandnetwork/grassland
    cd grassland


### Install `npm` packages

Install the npm dependencies, this should be repeated each time any of the `package.json` files are updated.

    npm install


## Development

### Run the application with reload

To run the application in development mode, run:

    cargo tauri dev

This will start the application in development mode, with reloading enabled, so any changes to the source code will be automatically reloaded.

### Build the application

To build the application, run:

    cargo tauri build



## Contributing

Contributions of all kinds are welcome!

* Found a bug? Please open an [issue](https://github.com/grasslandnetwork/grassland/issues/new) and let us know
* Looking for a feature? Start a [discussion](https://github.com/grasslandnetwork/grassland/discussions/new)
* Fancy hacking on the project? Please see [CONTRIBUTING.md](CONTRIBUTING.md) for more information on getting set up.
