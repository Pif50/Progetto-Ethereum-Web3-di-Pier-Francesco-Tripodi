// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

//Chainlink's VRFConsumerBase (Chainlink Verifiable Random Function)
//Link: https://docs.chain.link/docs/intermediates-tutorial/
//Github repo: https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/VRFConsumerBase.sol
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

//A ERC721 contractc alias NFT Contract will mint one of four houses of Hogwarts.

//Have you always enjoyed being part of one of the houses of Hogwarts?
//Well, you are in the right place!
//This Smart Contract will extract your Hogwarts household as the talking hat!

contract HogwartsHouses is ERC721URIStorage, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;

    mapping(uint256 => Raffle) public tokenIdToRaffle;
    mapping(bytes32 => address) public requestIdToSender;

    event requestCollectible(bytes32 indexed requestId, address requester);
    event raffleAssigned(uint256 indexed tokenId, Raffle raffle);

    //This are the different houses that one can extract
    enum Raffle {
        GRYFFINDOR,
        HUFFLEPUFF,
        RAVENCLAW,
        SLYTHERIN
    }

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyhash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("Houses", "HOM")
    {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        //We want the user who called createCollectoible to be the same user
        //who gets assigned the tokenId
        bytes32 requestId = requestRandomness(keyhash, fee); //This is going to create our randomness request to get random Houses of Howarts.

        //We can get the original caller of create collectible
        requestIdToSender[requestId] = msg.sender;
        emit requestCollectible(requestId, msg.sender);
    }

    //Function fulfillRandomness: which is the function that receives and does something
    //with verified randomness.
    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        //Select a houses based of this randomNumber
        Raffle raffle = Raffle(randomNumber % 4);

        //This is the way how each tokenId is going
        //to have a very specific Hogwarts Houses
        uint256 newTokenId = tokenCounter;

        //tokenURI based on the houses Hogwarts
        tokenIdToRaffle[newTokenId] = raffle;

        emit raffleAssigned(newTokenId, raffle);

        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        //Only the owner of the tokenId can be update the tokenURI
        require(
            _isApprovedOrOwner(_msgSender(), tokenId), //Imported from OpenZeppelin
            "ERC721: caller is not owner no approved!"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
