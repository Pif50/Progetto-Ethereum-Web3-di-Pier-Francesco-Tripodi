# Progetto-Ethereum-Web3-di-Pier-Francesco-Tripodi


An NFT Contract will mint one of the four Houses of Hogwarts.
This smart contract is develop whit web3.py on Goerli Testnet.

### Notes for use:
  * For interact with the contract you will need some Ethers (**$ETH**) and some Link (**LINK**) to be able to pay the gas fees. You can get **$ETH** for free via a **faucet**. (**[Chainlink](https://faucets.chain.link/)**)

## Framework e Tecnologie usate:
- [Solidity](https://docs.soliditylang.org/en/v0.8.17/) 
- [Python](https://docs.python.org/3/) 
- [Brownie](https://eth-brownie.readthedocs.io/en/stable/)
- [OpenZeppelin](https://docs.openzeppelin.com/) - A library for secure smart contract development.
- [ChainLink VRFConsumerbase](https://docs.chain.link/docs/intermediates-tutorial/) - Smart Contract for extract randomly a number betwen 0 and 3.

## Installation

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html), if you haven't already. Here is a simple way to install brownie.

```bash
pip install eth-brownie
```
Or, if that doesn't work, via pipx
```bash
pip install --user pipx
pipx ensurepath
# restart your terminal
pipx install eth-brownie
```

2. [Install ganache-cli](https://www.npmjs.com/package/ganache-cli)

```bash
npm install -g ganache-cli
```

3. Set your environment variables, if you want deploy to testnets

Set your `WEB3_INFURA_PROJECT_ID`, and `PRIVATE_KEY` [environment variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html). 

You can get a `WEB3_INFURA_PROJECT_ID` by getting a free trial of [Infura](https://infura.io/). At the moment, it does need to be infura with brownie. You can find your `PRIVATE_KEY` from your ethereum wallet like [metamask](https://metamask.zendesk.com/hc/en-us/articles/360015289632-How-to-export-an-account-s-private-key). 

You can add your environment variables to the `.env` file:

```
export WEB3_INFURA_PROJECT_ID=<PROJECT_ID>
export PRIVATE_KEY=<PRIVATE_KEY>
```

Then, make sure your `brownie-config.yaml` has:

```
dotenv: .env
```

# How to deploy and iteract the Smart Contract from Back-end

```
brownie run scripts/deploy_and_create.py --network goerli
brownie run scripts/create_collectible.py --network goerli
```
Then:
```
brownie run scripts/create_metadata.py --network goerli
brownie run scripts/set_tokenuri.py --network goerli
```

# If you want to interact with UI

Go to the folder called `frontend` and go to the file `index.html` and start the UI
