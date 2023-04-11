# Contributing


## Run the application with reload

Follow the "Compiling from source" instructions but instead of running the `cargo tauri build` command, use this command to start the application in development mode, with reloading enabled, so any changes to the source code will be automatically reloaded. 

    cargo tauri dev
    
## Build the application
Once you've made your changes to the source code, build the application so you can run it as users would:

    cargo tauri build


## Then fork the repo and send a pull request to this repo

## Workflow
Grassland development follows the [git flow](https://datasift.github.io/gitflow/IntroducingGitFlow.html) methodology.

There are a number of scripts that make this easier by bunding git commands into this workflow. We recommend [gitflow-avh](https://github.com/petervanderdoes/gitflow-avh/wiki) with the following settings.

Branch name for production releases: master 
Branch name for "next release" development: develop 
Feature branch prefix: feature/ 
Bugfix branch prefix: bugfix/ 
Release branch prefix: release/ 
Hotfix branch prefix: hotfix/ 
Support branch prefix: support/ 
Version tag prefix:
