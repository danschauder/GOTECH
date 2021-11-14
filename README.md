# Project GOTECH: Predicting Coral Presence Using LIDAR and Open-Source Coral Data

## Contributors: Josh Mattingly, Tina Guo, Dan Schauder

## Dependencies
* Linux (Preferably Ubuntu 20.04)
* Anaconda or Miniconda (Available here: https://docs.conda.io/en/latest/miniconda.html#linux-installers)
* Admin/su privileges

## Installation
* Download and unzip repo
* Navigate to project root in a command prompt
* Run the following command to create a conda environment with required packages/dependencies
```
conda env create -f environment.yml
```
* Activate the conda environment with the following command
```
conda activate GOTECH_env
```

## Database installation
With the conda environment active, navigate to the project root and run the following command:
```
bash postgis_setup.sh
```
This will instantiate a postgresql database and activate the postgis extensions

## Extractors
