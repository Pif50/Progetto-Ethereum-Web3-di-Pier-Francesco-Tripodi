// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract HogwartsHouses is ERC721URIStorage, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;

    mapping(uint256 => Raffle) public tokenIdToRaffle;
    mapping(bytes32 => address) public requestIdToSender;

    event requestCollectible(bytes32 indexed requestId, address requester);
    event raffleAssigned(uint256 indexed tokenId, Raffle raffle);

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

    function createCollectible(string memory tokenURI)
        public
        returns (bytes32)
    {
        //We want the user who called createCollectoible to be the same user
        //who gets assigned the tokenId
        bytes32 requestId = requestRandomness(keyhash, fee); //This is going to create our randomness request to get random Houses of Howarts.
        requestIdToSender[requestId] = msg.sender;
        emit requestCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Raffle raffle = Raffle(randomNumber % 4);
        uint256 newTokenId = tokenCounter;
        tokenIdToRaffle[newTokenId] = raffle; //Each tokenId is going to have a very specific Hogwarts Houses
        emit raffleAssigned(newTokenId, raffle);
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner no approved!"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
