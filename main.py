import subprocess, argparse
from extractors.AllenCoralBenthicExtractor import AllenCoralBenthicExtractor
from extractors.AllenCoralGeomorphicExtractor import AllenCoralGeomorphicExtractor

def main():

    ### Set command line arguments
    parser = argparse.ArgumentParser(description="""Library for downloading coral data, unifying it, training ML models, and viewing results""")
    parser.add_argument('--setup_db',dest='setup_db',action='store_true')
    parser.set_defaults(setup_db=False)

    parser.add_argument('--start_db',dest='start_db',action='store_true')
    parser.set_defaults(start_db=False)

    parser.add_argument('--stop_db',dest='stop_db',action='store_true')
    parser.set_defaults(stop_db=False)

    parser.add_argument('--verbose', dest='verbose',action='store_true')
    parser.set_defaults(verbose=False)

    parser.add_argument('--get_aca_benthic', dest='get_aca_benthic',action='store_true')
    parser.set_defaults(get_aca_benthic=False)

    parser.add_argument('--get_aca_geomorphic', dest='get_aca_geomorphic',action='store_true')
    parser.set_defaults(get_aca_geomorphic=False)


    args = parser.parse_args()

    ## API for Database commands
    if args.setup_db:
        if args.verbose:
            print('Setting up db')
        subprocess.call(['sh', './db_scripts/postgis_setup.sh'])

    if args.start_db:
        if args.verbose:
            print('Starting the database server')
        subprocess.call(['sh','./db_scripts/postgis_start.sh'])

    if args.stop_db:
        if args.verbose:
            print('Stopping the database server')
        subprocess.call(['sh','./db_scripts/postgis_stop.sh'])

    
    ## API for Allen Coral Atlas downloads/imports
    if args.get_aca_benthic:
        if args.verbose:
            print('Loading Allen Coral Atlas geomorphic data into the database')
        aca_benthic_extractor = AllenCoralBenthicExtractor()
        aca_benthic_extractor.extract_and_load()
    
    if args.get_aca_geomorphic:
        if args.verbose:
            print('Loading Allen Coral Atlas geomorphic data into the database')
        aca_geomorphic_extractor = AllenCoralGeomorphicExtractor()
        aca_geomorphic_extractor.extract_and_load()

    

if __name__=="__main__":
    main()