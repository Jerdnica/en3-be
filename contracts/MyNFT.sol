// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyNFT is ERC721URIStorage, Ownable {
    uint256 public tokenCounter;

    struct NFTCollection {
        string name;
        string symbol;
        string baseURI;
        uint256 totalSupply;
        uint256 minted;
        uint256 pricePerMint;
        address donationAddress;
        uint256 donationPercentage; // e.g., 5 for 5%
    }

    mapping(uint256 => NFTCollection) public nftCollections;

    event NFTCollectionCreated(uint256 indexed tokenId, string name, string symbol, string baseURI, uint256 totalSupply, uint256 pricePerMint, address donationAddress, uint256 donationPercentage);
    event NFTMinted(uint256 indexed tokenId, address indexed minter);

    constructor() ERC721("", "") Ownable(msg.sender) {
        tokenCounter = 0;
    }

    function createNFTCollection(string memory name, string memory symbol, string memory baseURI, uint256 totalSupply, uint256 pricePerMint, address donationAddress, uint256 donationPercentage) public onlyOwner returns (uint256) {
        require(donationPercentage <= 100, "Donation percentage cannot exceed 100");
        uint256 newTokenId = tokenCounter;
        nftCollections[newTokenId] = NFTCollection(name, symbol, baseURI, totalSupply, 0, pricePerMint, donationAddress, donationPercentage);
        emit NFTCollectionCreated(newTokenId, name, symbol, baseURI, totalSupply, pricePerMint, donationAddress, donationPercentage);
        tokenCounter++;
        return newTokenId;
    }

    function mintNFT(uint256 collectionId) public payable {
        NFTCollection storage nftCollection = nftCollections[collectionId];
        require(nftCollection.minted < nftCollection.totalSupply, "All NFTs minted");
        require(msg.value >= nftCollection.pricePerMint, "Insufficient payment");

        uint256 donationAmount = (msg.value * nftCollection.donationPercentage) / 100;
        uint256 remainingAmount = msg.value - donationAmount;

        payable(nftCollection.donationAddress).transfer(donationAmount);
        payable(owner()).transfer(remainingAmount);

        uint256 newTokenId = collectionId * 1e18 + nftCollection.minted;
        _safeMint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, nftCollection.baseURI);
        nftCollection.minted++;
        emit NFTMinted(newTokenId, msg.sender);
    }

    function getNFTCollectionDetails(uint256 collectionId) public view returns (string memory, string memory, string memory, uint256, uint256, uint256, address, uint256) {
        NFTCollection memory nftCollection = nftCollections[collectionId];
        return (nftCollection.name, nftCollection.symbol, nftCollection.baseURI, nftCollection.totalSupply, nftCollection.minted, nftCollection.pricePerMint, nftCollection.donationAddress, nftCollection.donationPercentage);
    }

    function name() public view override returns (string memory) {
        uint256 collectionId = _getCollectionId(msg.sender);
        return nftCollections[collectionId].name;
    }

    function symbol() public view override returns (string memory) {
        uint256 collectionId = _getCollectionId(msg.sender);
        return nftCollections[collectionId].symbol;
    }

    function _getCollectionId(address owner) internal view returns (uint256) {
        // Implement your logic to get the collection ID based on the owner or any other logic
        // For simplicity, we assume one owner has one collection
        // This part needs to be customized as per your use case
        return 0;
    }
}
