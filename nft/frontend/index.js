import { ethers } from "./ethers-5.6.esm.min.js";
import { abi, contractAddress } from "./costants.js";

const connectButton = document.getElementById("connectButton");
const createCollectibleButton = document.getElementById(
  "createCollectibleButton"
);

connectButton.onclick = connect;
createCollectibleButton.onclick = createCollectible;

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
