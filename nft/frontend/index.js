import { ethers } from "./ethers-5.6.esm.min.js";
import { abi, contractAddress } from "./costants.js";
import { getRaffle } from "./get_raffle.js";

const OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}";

const raffle_metadata_dic = {
  GRYFFINDOR:
    "https://ipfs.io/ipfs/QmXJcdftXeX9ndcmsPFijRNtyMM49yvSnb8AcveMKWq61c?filename=GRYFFINDOR.json",
  HUFFLEPUFF:
    "https://ipfs.io/ipfs/QmPz1mxmqUGQUUuVNFWYUPU5BF6dU5MBCQ5xmG3c63pDMN?filename=HUFFLEPUFF.json",
  RAVENCLAW:
    "https://ipfs.io/ipfs/QmUH9J2eY2Cuu4m5raGCg2XmGqZrd6NuvTatzgwWX1Jm6z?filename=RAVENCLAW.json",
  SLYTHERIN:
    "https://ipfs.io/ipfs/QmPvjuj32AFV9yye7agrxSzty4Y5nCvesNkzgmYjJciA2f?filename=SLYTHERIN.json",
};

const connectButton = document.getElementById("connectButton");
const createCollectibleButton = document.getElementById(
  "createCollectibleButton"
);
const createMetadataButton = document.getElementById("createMetadataButton");
const createTokenUri = document.getElementById("createTokenUri");

connectButton.onclick = connect;
createCollectibleButton.onclick = createCollectible;
createMetadataButton.onclick = createMetadata;
createTokenUri.onclick = set_token_uri;

async function connect() {
  if (typeof window.ethereum !== "undefined") {
    window.ethereum.request({ method: "eth_requestAccounts" });
    connectButton.innerHTML = "Connected";
  } else {
    fundButton.innerHTML = "Please install MetaMask";
  }
}

async function createCollectible() {
  if (typeof window.ethereum !== "undefined") {
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const signer = provider.getSigner();
    const contract = new ethers.Contract(contractAddress, abi, signer);
    try {
      const transactionResponse = await contract.createCollectible();
      await listenForTransactionMine(transactionResponse, provider);
      console.log("Collectible created!!!");
    } catch (error) {
      console.log(error);
    }
  }
}

function listenForTransactionMine(transactionResponse, provider) {
  console.log(`Mining ${transactionResponse.hash}....`);
  //return new Promise()
  return new Promise((resolve, rejct) => {
    provider.once(transactionResponse.hash, (transactionReceipt) => {
      console.log(
        `Completed with ${transactionReceipt.confirmations} confirmations`
      );
      resolve();
    });
  });
}

async function createMetadata() {
  if (typeof window.ethereum !== "undefined") {
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const signer = provider.getSigner();
    const contract = new ethers.Contract(contractAddress, abi, signer);
    try {
      const number_of_hogwarts_houses = await contract.tokenCounter();
      console.log(`You have created ${number_of_hogwarts_houses} collectibles`);
      var token_id = "";
      for (token_id = 0; token_id < (await contract.tokenCounter()); ) {
        const raffle = getRaffle(contract.tokenIdToRaffle(token_id));

        console.log(`Setting tokenURI of ${token_id}`);
        //set_token_uri(token_id, contractAddress, raffle_metadata_dic[raffle]);
      }
    } catch (error) {
      console.log(error);
    }
  }
}

async function set_token_uri(token_id, contractAddress, tokenURI) {
  if (typeof window.ethereum !== "undefined") {
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const signer = provider.getSigner();
    const contract = new ethers.Contract(contractAddress, abi, signer);
    try {
      const tx = await contract.setTokenURI(token_id, tokenURI);
      await listenForTransactionMine(tx, provider);
      `Awesome! You can view your NFT at ${OPENSEA_URL.format(
        contractAddress,
        token_id
      )}`;
    } catch (error) {
      console.log(error);
    }
  }
}
