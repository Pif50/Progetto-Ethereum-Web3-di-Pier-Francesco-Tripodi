from brownie import network, HogwartsHouses
from scripts.helpful_scripts import OPENSEA_URL, get_account, get_raffle

raffle_metadata_dic = {
    "GRYFFINDOR": "https://ipfs.io/ipfs/QmXJcdftXeX9ndcmsPFijRNtyMM49yvSnb8AcveMKWq61c?filename=GRYFFINDOR.json",
    "HUFFLEPUFF": "https://ipfs.io/ipfs/QmPz1mxmqUGQUUuVNFWYUPU5BF6dU5MBCQ5xmG3c63pDMN?filename=HUFFLEPUFF.json",
    "RAVENCLAW": "https://ipfs.io/ipfs/QmUH9J2eY2Cuu4m5raGCg2XmGqZrd6NuvTatzgwWX1Jm6z?filename=RAVENCLAW.json",
    "SLYTHERIN": "https://ipfs.io/ipfs/QmPvjuj32AFV9yye7agrxSzty4Y5nCvesNkzgmYjJciA2f?filename=SLYTHERIN.json",
}


def main():
    print(f"Working on {network.show_active()}")
    hogwarts_houses = HogwartsHouses[-1]
    number_of_collectibles = hogwarts_houses.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds")
    for token_id in range(number_of_collectibles):
        raffle = get_raffle(hogwarts_houses.tokenIdToRaffle(token_id))
        # Check to see if already have a token
        if not hogwarts_houses.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_token_uri(token_id, hogwarts_houses, raffle_metadata_dic[raffle])


def set_token_uri(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button")
