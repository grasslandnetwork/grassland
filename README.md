# Grassland
Grassland full node implementation

## Compile From Source Instructions
Ensure you have [rust](https://www.rust-lang.org/tools/install) and
[nodejs](https://nodejs.org/en/) installed

### Grassland uses Tauri's Rust CLI to create it's binary. 
```
cargo install tauri-cli

```

### Install the nodejs packages
From the project's root directory, run..
```
npm ci 

```
Unlike npm install, npm ci will never modify your package-lock.json. npm ci ensure's that you’ll get reliable builds. It requires package-lock.json


### Build the Grassland binary/distributable

```
cargo tauri build

```

## To run Grassland in a development environment 
If you've changed the dependencies...
```
npm install 

```
If you haven't changed the dependencies..
```
npm ci (requires package-lock.json)
```

Then..
```
cargo tauri dev

```
