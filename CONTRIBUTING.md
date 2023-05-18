# Contributing

## Install OpenCV

First you'll need to install OpenCV. Which handles the video processing.

Windows (via [Chocolatey](https://chocolatey.org/)):

    choco install opencv

Ubuntu

    sudo apt install opencv


macOS (via [Homebrew](https://brew.sh/)):

    brew install opencv
    

## Run the application with reload

Follow the "Compiling from source" instructions but instead of running the `cargo tauri build` command, use this command to start the application in development mode, with reloading enabled, so any changes to the source code will be automatically reloaded. 

    cargo tauri dev
    
## Build the application
Once you've made your changes to the source code, build the application so you can run it as users would:

    cargo tauri build


## Make a fork of this repo and send us a pull request 

## Workflow
Grassland development follows the [git flow](https://www.git-tower.com/learn/git/ebook/en/command-line/advanced-topics/git-flow/) methodology.

There are a number of scripts that make this easier by bunding git commands into this workflow. We recommend [gitflow-avh](https://github.com/petervanderdoes/gitflow-avh/wiki) with the following settings.

```
Branch name for production releases: master 
Branch name for "next release" development: develop 
Feature branch prefix: feature/ 
Bugfix branch prefix: bugfix/ 
Release branch prefix: release/ 
Hotfix branch prefix: hotfix/ 
Support branch prefix: support/ 
Version tag prefix: v
```
