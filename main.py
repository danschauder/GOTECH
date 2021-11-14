from extractors.AllenCoralExtractor import AllenCoralExtractor

def main():
    aca_extractor = AllenCoralExtractor()
    aca_extractor.extract_and_load()

if __name__=="__main__":
    main()