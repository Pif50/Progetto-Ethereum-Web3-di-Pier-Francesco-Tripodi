from brownie import HogwartsHouses, network
from scripts.helpful_scripts import get_raffle
from metadata.metadata_template import metadata_template
from pathlib import Path


def main():
    advanced_collectible = HogwartsHouses[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        raffle = get_raffle(advanced_collectible.tokenIdToRaffle(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{raffle}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = raffle
            collectible_metadata[
                "description"
            ] = f"You will be part of the household of {raffle}"
            image_path = "./img/" + raffle.lower().replace("_", "-") + ".png"
            # image_uri = upload_to_ipfs()
            # collectible_metadata["image"]


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
