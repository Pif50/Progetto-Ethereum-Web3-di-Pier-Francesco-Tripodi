from scripts.helpful_scripts import (
    get_account,
    OPENSEA_URL,
    get_contract,
    fund_with_link,
    get_publish_source
)
from brownie import HogwartsHouses, network, config

"""
Scripts that will deploy the NFT Contract
"""


def deploy_and_create():

    # Wallet that will deploy the contract
    # We want to be able to use the deployed contracts if we are on a testnet
    # Otherwise, we want to deploy some mocks and use those
    # Goerli
    account = get_account()

    # Deploy the contract
    hogwarts_houses = HogwartsHouses.deploy(
        # Parameters of the constructor of the contract:
        # It'll grab this information from contracts/test/...
        # using the function get_contract from helpfull_script.
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        # It'll grab this information from brownie-config.yaml
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=("0xA4705dba5a7459Cee1AAc384aa971ff2d10e59D5")
    )

    # We fund the contract with link beacause we can call the randomNumber function from chainlink.
    # Its cost a fee in LINK.
    fund_with_link(hogwarts_houses.address)  # Its from helpfull_script.

    # Creating the new token
    creating_tx = hogwarts_houses.createCollectible({"from": account})
    creating_tx.wait(1)
    print("New token has been created!")
    return hogwarts_houses, creating_tx


def main():
    deploy_and_create()
