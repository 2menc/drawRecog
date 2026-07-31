from pathlib import Path
import yaml
import sys

REPO_ROOT = Path(__file__).resolve().parents[4]
CONFIG_PATH = REPO_ROOT / "src/main/resources/datasetScrapeOptions.yaml"

with CONFIG_PATH.open() as stream:
    try:
        data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        sys.exit(1)

categories = data["categories"]

def verifyFolders(scrapeDirectory):

    folderCounter = 0

    #gets all folders
    path = Path(scrapeDirectory)
    if not path.exists():
        print(f"ERROR -> {scrapeDirectory} path does not exist")
    else:
        #actual check
        for folder in path.iterdir():

            folderCounter += 1

            match = anymatch(folder)

            if match:
                print(f"matching: {folder}")
            else:
                print(f"NOT MATCHING: {folder} (extra folder)")

        print(f"actual: {folderCounter} folders, expected: {len(categories)} -- {((len(categories)-folderCounter)/len(categories)) * 100}% loss")


def anymatch(mainFolder):
    match = False
    for category in categories:
        if mainFolder.name == category:
            return True

    return False
