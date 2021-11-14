import subprocess

class AllenCoralExtractor():
    def __init__(self):
        """
        Extracts data from the Allen Coral Atlas API
        """
        pass

    def extract_and_load(self):
        subprocess.call(['sh', './extractors/allen.sh'])