import subprocess

class AllenCoralGeomorphicExtractor():
    def __init__(self):
        """
        Extracts geomorphic data from the Allen Coral Atlas API
        """
        pass

    def extract_and_load(self):
        subprocess.call(['sh', './extractors/allen_coral_geomorphic.sh'])