# Kobiton plugin for XL-Release

## Preriquisites
All the commands below are running on MacOSX
- Install Jython: `brew install jython`
- Install [IntelliJ IDEA Community Edition](https://www.jetbrains.com/idea/download/#section=mac)
- Install [JDK 1.7](http://www.oracle.com/technetwork/java/javase/downloads/java-archive-downloads-javase7-521261.html)

## Building
- Run command `gradle clean build` at the root directory
- Copy the `jar` from `build/libs` into `plugins/__local__` directory in XL-Release server

## Types
- ListDevices

  - `model`: The device model (Galaxy S8, iPhone 8, ...)
  - `devices`: (Output property) List of available devices
