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
python main.py --setup_db
```
This will instantiate a postgresql database and activate the postgis extensions

## Database Commands
Run the following command to start the database instance
```
python main.py --start_db
```

Run the following command to stop the database instance
```
python main.py --stop_db
```

## Extractors
With the database instance running, run the following command to download Allen Coral Atlas benthic data and ingest it into the db
```
python main.py --get_aca_benthic
```

With the database instance running, run the following command to download Allen Coral Atlas geomorphic data and ingest it into the db
```
python main.py --get_aca_geomorphic
```

With the database instance running, run the following command to download CALIPSO data and ingest it into the db
```
python main.py --get_calipso
```
