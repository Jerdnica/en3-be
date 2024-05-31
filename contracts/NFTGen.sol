// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyNFT is ERC721URIStorage, Ownable {
    uint256 public tokenCounter;

    struct NFTCollection {
        string uri;
        uint256 totalSupply;
        uint256 minted;
    }

    mapping(uint256 => NFTCollection) public nftCollections;

    event NFTCollectionCreated(uint256 indexed tokenId, string uri, uint256 totalSupply);
    event NFTMinted(uint256 indexed tokenId, address indexed minter);

    constructor() ERC721("MyNFTCollection", "MNFT") {
        tokenCounter = 0;
    }

    function createNFTCollection(string memory uri, uint256 totalSupply) public onlyOwner returns (uint256) {
        uint256 newTokenId = tokenCounter;
        nftCollections[newTokenId] = NFTCollection(uri, totalSupply, 0);
        emit NFTCollectionCreated(newTokenId, uri, totalSupply);
        tokenCounter++;
        return newTokenId;
    }

    function mintNFT(uint256 tokenId) public {
        require(nftCollections[tokenId].minted < nftCollections[tokenId].totalSupply, "All NFTs minted");
        uint256 newTokenId = tokenId * 1e18 + nftCollections[tokenId].minted;
        _safeMint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, nftCollections[tokenId].uri);
        nftCollections[tokenId].minted++;
        emit NFTMinted(newTokenId, msg.sender);
    }

    function getNFTCollectionDetails(uint256 tokenId) public view returns (string memory, uint256, uint256) {
        NFTCollection memory nftCollection = nftCollections[tokenId];
        return (nftCollection.uri, nftCollection.totalSupply, nftCollection.minted);
    }
}