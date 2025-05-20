import zipfile
import hashlib
from web3 import Web3
import os
import pandas as pd
import random,yaml
import time


with open("config.yaml", "r") as f:
		config = yaml.safe_load(f)
              

# Web3 connection
GANACHE_URL_2 =  config["GANACHE_URL"]
CONTRACT_ADDRESS_2 = config["CONTRACT_ADDRESS_HASH_FILES_DATASET"]
PRIVATE_KEY_2 = config["PRIVATE_KEY"]
WALLET_ADDRESS_2 = config["WALLET_ADDRESS"]
CONTRACT_ABI_2 =  [
	{
		"inputs": [
			{
				"internalType": "string[]",
				"name": "_paths",
				"type": "string[]"
			},
			{
				"internalType": "string[]",
				"name": "_hashes",
				"type": "string[]"
			}
		],
		"name": "storeFileHashes",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "startIndex",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "batchSize",
				"type": "uint256"
			}
		],
		"name": "getFileHashesBatch",
		"outputs": [
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "startIndex",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "batchSize",
				"type": "uint256"
			}
		],
		"name": "getFilePathsBatch",
		"outputs": [
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "path",
				"type": "string"
			}
		],
		"name": "getHashByPath",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getTotalFilePaths",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

w3_2 = Web3(Web3.HTTPProvider(GANACHE_URL_2,request_kwargs={'timeout': 180}))
contract_2 = w3_2.eth.contract(address=CONTRACT_ADDRESS_2, abi=CONTRACT_ABI_2)

"""The contract on remix ide have depolyed with 6500000 gas limit"""

def compute_md5(file):
    """Hash md5 of a file which is opened in binary mode"""
    md5_hash = hashlib.md5()
    while chunk := file.read(4096):  # Legge il file a blocchi
        md5_hash.update(chunk)
    return md5_hash.hexdigest()

def get_sorted_file_hashes_from_zip(zip_path):
    """It extracts the md5 hashes of all files that are contained in a zip archive, sorted alphabetically"""
    file_hashes = {}

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        file_list = sorted([file for file in zip_ref.namelist() if not os.path.isdir(file) and '__MACOS' not in file and not file.endswith('/')])

        for file in file_list:
            with zip_ref.open(file, 'r') as f:
                file_hashes[file] = compute_md5(f)

    return file_hashes

def get_total_file_paths():
        """It recovers from blockchain the total number of saved files """
        total_files = contract_2.functions.getTotalFilePaths().call()
        print(f" Numero totale di file salvati: {total_files}")
        return total_files





      



def save_hashes_on_blockchain(zip_path):
	start_dict_list_time = round(time.time() *1000,3)
	hash_dict = get_sorted_file_hashes_from_zip(zip_path) 
	#  it converts the dictionary into two ordered lists
	file_paths = list(hash_dict.keys())
	
	hash_values = list(hash_dict.values())
	end_dict_list_time = round(time.time() *1000,3)
		
	time_dict_list = end_dict_list_time - start_dict_list_time #<----------------------------

	BATCH_SIZE = 1000  # Max number for batch
	start_batch_time = round(time.time() *1000,3)   
	if len(file_paths)<=1000:
		BATCH_SIZE = 100
      
	for i in range(0, len(file_paths), BATCH_SIZE):
		batch_paths = file_paths[i:i + BATCH_SIZE]
		batch_hashes = hash_values[i:i + BATCH_SIZE]

		nonce = w3_2.eth.get_transaction_count(WALLET_ADDRESS_2)

		tx = contract_2.functions.storeFileHashes(batch_paths, batch_hashes).build_transaction({
				'from': WALLET_ADDRESS_2,
				'gas': 100000000,  
				'gasPrice': w3_2.to_wei('10', 'gwei'),
				'nonce': nonce,
			})

		signed_tx = w3_2.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY_2)
		tx_hash = w3_2.eth.send_raw_transaction(signed_tx.raw_transaction)
		receipt = w3_2.eth.wait_for_transaction_receipt(tx_hash)

		print(f" Batch {i // BATCH_SIZE + 1}") 
	end_batch_time = round(time.time() *1000,3)
	batch_time = end_batch_time - start_batch_time #<------------------------
	


def get_hashes_from_blockchain_batch(batch_size=4000):
        """It recovers path_file and associated hash from blockchain in batch to avoid the timeout execution"""
        total_files = get_total_file_paths()  # Count of total files
        blockchain_dict = {}

        for i in range(0, total_files, batch_size):
            print(f"Batch recovery {i}-{i + batch_size}...")

            batch_paths = contract_2.functions.getFilePathsBatch(i, batch_size).call()
            batch_hashes = contract_2.functions.getFileHashesBatch(i, batch_size).call()

            blockchain_dict.update(dict(zip(batch_paths, batch_hashes)))

        return blockchain_dict
    
    




if __name__=="__main__":
    pass
		

		
		
		

		


