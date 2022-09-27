import pytest
from brownie import network, HogwartsHouses
import time
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
    get_account,
)
from scripts.deploy_and_create import deploy_and_create


def test_can_create_hogwarts_houses_integration():
    # Deploy the contract
    # Create an NFT
    # Get a random hoses back

    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")

    # Act
    advanced_collectible, creation_transaction = deploy_and_create()
    time.sleep(60)

    # Assert
    assert advanced_collectible.tokenCounter() == 1
