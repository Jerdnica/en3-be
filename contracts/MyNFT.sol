// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyNFT is ERC721URIStorage, Ownable {
    uint256 public tokenCounter;

    struct NFTCollection {
        string baseURI;
        uint256 totalSupply;
        uint256 minted;
    }

    mapping(uint256 => NFTCollection) public nftCollections;

    event NFTCollectionCreated(uint256 indexed tokenId, string baseURI, uint256 totalSupply);
    event NFTMinted(uint256 indexed tokenId, address indexed minter);

    constructor() ERC721("MyNFTCollection", "MNFT") Ownable(msg.sender) {
        tokenCounter = 0;
    }

    function createNFTCollection(string memory baseURI, uint256 totalSupply) public onlyOwner returns (uint256) {
        uint256 newTokenId = tokenCounter;
        nftCollections[newTokenId] = NFTCollection(baseURI, totalSupply, 0);
        emit NFTCollectionCreated(newTokenId, baseURI, totalSupply);
        tokenCounter++;
        return newTokenId;
    }

    function mintNFT(uint256 collectionId) public {
        require(nftCollections[collectionId].minted < nftCollections[collectionId].totalSupply, "All NFTs minted");
        uint256 newTokenId = collectionId * 1e18 + nftCollections[collectionId].minted;
        _safeMint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, nftCollections[collectionId].baseURI);
        nftCollections[collectionId].minted++;
        emit NFTMinted(newTokenId, msg.sender);
    }

    function getNFTCollectionDetails(uint256 collectionId) public view returns (string memory, uint256, uint256) {
        NFTCollection memory nftCollection = nftCollections[collectionId];
        return (nftCollection.baseURI, nftCollection.totalSupply, nftCollection.minted);
    }
}
