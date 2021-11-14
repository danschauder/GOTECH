import subprocess

class AllenCoralBenthicExtractor():
    def __init__(self):
        """
        Extracts benthic data from the Allen Coral Atlas API
        """
        pass

    def extract_and_load(self):
        subprocess.call(['sh', './extractors/allen_coral_benthic.sh'])