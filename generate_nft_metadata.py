import json

def generate_nft_metadata(event_name, event_desc, location, img_path, img_url):
    output_file = img_path[:-4] + ".json"

    # Create the dictionary with the specified structure
    nft_metadata = {
        "name": event_name,
        "description": event_desc,
        "image": img_url,
        "attributes": [
            {
                "trait_type": "location",
                "value": location
            }
        ]
    }
    
    # Write the dictionary to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(nft_metadata, json_file, indent=4)
    return output_file

# Usage
#event_name = "Belgrade ETH Hackathon 2026"
#event_desc = "ETH Belgrade Hackathon offers a three-day hacking experience with a primary focus on building on Ethereum. Following the success of the inaugural hackathon in 2023, we aim to surpass it in every aspect. This year, we're opening the doors for builders from all around the globe to join us both in-person and online (hybrid). Our goal is to gather hundreds of hackers and curious minds to develop projects and use cases that will reshape the Ethereum landscape and enhance people's lives."
#location = "Belgrade, Serbia"

#img_path = ".//sample_images//Belgrade_ETH_Hackathon_2026_NFT.png"
#img_url = "https://lime-neighbouring-mole-554.mypinata.cloud/ipfs/QmTeLBGUQtu9eotGrHLYS3id6kZ9JHdj5nTrsfYKy9XSxL"

#metadata_file = generate_nft_metadata(event_name, event_desc, location, img_path, img_url)
#print(f"Metadata File: {metadata_file}")
