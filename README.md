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

## Verbose Flag
Include the following flag for detailed output to be printed to the console

```
python main.py --verbose
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

Run the following command to create spatial indexes in the postgis database (dramatically improves performance)
```
python main.py --create_indexes
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

The default bounding box for all extractors includes the Florida region. To set a different bounding box, use the full set of flags to specify the corners of a custom bounding box, like so:

```
python main.py --get_calipso --latitude_min -82.0 --latitude_max -80.0 --longitude_min 24.001 --longitude_max 26.22
```

## Transformers
With the database instance running, run the following command to perform transformations to prepare benthic data to be merged with ACA data
```
python main.py --transform_aca_benthic
```

With the database instance running, run the following command to merge data into a unified table
```
python main.py --merge
```

## Models
To train and test classification models and view the results, run the following command
```
python main.py --run_models
```