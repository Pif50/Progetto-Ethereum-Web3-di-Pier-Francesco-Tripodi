from brownie import HogwartsHouses
from scripts.helpful_scripts import fund_with_link, get_account
from web3 import Web3


def main():
    account = get_account()

    # Most recent deployed
    advanced_collectible = HogwartsHouses[-1]

    # Fund the contract
    fund_with_link(advanced_collectible.address, amount=Web3.toWei(0.1, "ether"))

    # Transaction
    creation_transaction = advanced_collectible.createCollectible({"from": account})
    creation_transaction.wait(1)  # Wait one block confermation
    print("Collectible created!")
