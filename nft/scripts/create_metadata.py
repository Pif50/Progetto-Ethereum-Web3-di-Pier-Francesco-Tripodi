from brownie import HogwartsHouses, network
from scripts.helpful_scripts import get_raffle
from metadata.metadata_template import metadata_template
from pathlib import Path
import requests
import json
import os

"""
This script will read off chain and create our metadata file.
"""

raffle_to_image_uri = {
    "GRYFFINDOR": "https://ipfs.io/ipfs/QmXJcdftXeX9ndcmsPFijRNtyMM49yvSnb8AcveMKWq61c?filename=GRYFFINDOR.png",
    "HUFFLEPUFF": "https://ipfs.io/ipfs/QmPererbdHNMFnXLtXbhRZWAADa9optg6Lx12ZJQc6uvgf?filename=HUFFLEPUFF.png",
    "RAVENCLAW": "https://ipfs.io/ipfs/QmNWK2ZdMTosThWfSmU53PsWwhCebXq6jassyeU7M2uHq9?filename=RAVENCLAW.png",
    "SLYTHERIN": "https://ipfs.io/ipfs/Qmc9xQwQCZHyx12muXp86YZrnfy2gpYQBopFA9HDqT91sL?filename=SLYTHERIN.png",
}


def main():
    hogwarts_houses = HogwartsHouses[-1]  # Recently deployed contract.
    number_of_hogwarts_houses = (
        hogwarts_houses.tokenCounter()
    )  # Number of tokens that one has
    print(f"You have created {number_of_hogwarts_houses} collectibles!")

    for token_id in range(number_of_hogwarts_houses):
        raffle = get_raffle(hogwarts_houses.tokenIdToRaffle(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{raffle}.json"
        )
        # Metadata_template is the structor of the metadata.json
        # that will output after we will run this script
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

            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
            image_uri = image_uri if image_uri else raffle_to_image_uri[raffle]

            collectible_metadata["image"] = image_uri
            # Dump this collectible_metadata into its own file
            # and upload to IPFS
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)


# This function will uploaded our image to IPFS
def upload_to_ipfs(filepath):
    # We take the file and open in binary as fp(filepath)
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]

        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
