from web3 import Web3
import os
import zipfile
import hashlib
import time
import pandas as pd
import random,yaml,shutil,os
from find_directory import find_dirs
from md5_save_dataset_hash_ import save_hashes_on_blockchain



with open("config.yaml", "r") as f:
		config = yaml.safe_load(f)

# Paramaters for Connection with Ethereum blockchain(GANACHE)
GANACHE_URL = config["GANACHE_URL"]
CONTRACT_ADDRESS = config["CONTRACT_ADDRESS_INFO_DATASET"]  # Contract's address on Remix IDE
PRIVATE_KEY = config["PRIVATE_KEY"]
WALLET_ADDRESS = config["WALLET_ADDRESS"]

CONTRACT_ABI = CONTRACT_ABI = [
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_datasetId",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_hashValue",
				"type": "string"
			},
			{
				"internalType": "string[]",
				"name": "_classes",
				"type": "string[]"
			},
			{
				"internalType": "string[]",
				"name": "_classLabelsTrain",
				"type": "string[]"
			},
			{
				"internalType": "uint256[]",
				"name": "_classSizesTrain",
				"type": "uint256[]"
			},
			{
				"internalType": "string[]",
				"name": "_classLabelsVal",
				"type": "string[]"
			},
			{
				"internalType": "uint256[]",
				"name": "_classSizesVal",
				"type": "uint256[]"
			},
			{
				"internalType": "uint256",
				"name": "_numTestFiles",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_totalFiles",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_totalSizeMB",
				"type": "uint256"
			}
		],
		"name": "storeDatasetInfo",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_owner",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_datasetId",
				"type": "uint256"
			}
		],
		"name": "getDatasetHash",
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
		"inputs": [
			{
				"internalType": "address",
				"name": "_owner",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_datasetId",
				"type": "uint256"
			}
		],
		"name": "getDatasetInfo",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "hashValue",
				"type": "string"
			},
			{
				"internalType": "string[]",
				"name": "classes",
				"type": "string[]"
			},
			{
				"internalType": "string[]",
				"name": "classLabelsTrain",
				"type": "string[]"
			},
			{
				"internalType": "uint256[]",
				"name": "classSizesTrain",
				"type": "uint256[]"
			},
			{
				"internalType": "string[]",
				"name": "classLabelsVal",
				"type": "string[]"
			},
			{
				"internalType": "uint256[]",
				"name": "classSizesVal",
				"type": "uint256[]"
			},
			{
				"internalType": "uint256",
				"name": "numTestFiles",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "totalFiles",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "totalSizeMB",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

# Web3 connection and contract connection
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)


# Function to resolve sha-256 of zip dataset
def compute_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


# Function to extract several informations from ZIP dataset
def extract_info(zip_path, extract_path,id):
	train_dir, valid_dir, test_dir = find_dirs(zip_path)
	num_test_file = 0
	
	with zipfile.ZipFile(zip_path, 'r') as zip_ref:
		zip_ref.extractall(extract_path)

	macosx_path = os.path.join(extract_path, '__MACOSX')
	if os.path.exists(macosx_path):
		shutil.rmtree(macosx_path)

	dataset_name = os.path.basename(zip_path).replace(".zip", "")
	
	train_path = os.path.join(extract_path, train_dir)

	if test_dir!=[]:
		test_path = os.path.join(extract_path, test_dir)
		num_test_file = len(os.listdir(test_path))

	if valid_dir!=[]:
		valid_path = os.path.join(extract_path,valid_dir)
    
	labels = [d for d in os.listdir(train_path) if os.path.isdir(os.path.join(train_path, d))]
	label_train_distribution = {label: len(os.listdir(os.path.join(train_path, label))) for label in labels}

	if valid_dir!=[]:
		label_valid_distribution = {label: len(os.listdir(os.path.join(valid_path,label))) for label in labels}
	else:
		label_valid_distribution = {}

	


	file_list = []
	for root, _, files in os.walk(extract_path):
		for file in files:
			file_list.append(os.path.relpath(os.path.join(root, file), extract_path))
		total_size = sum(os.path.getsize(os.path.join(extract_path, f)) for f in file_list) / (1024 * 1024)


	dataset_info = {
		"id": id,
		"dataset name": dataset_name,
		"hash": compute_sha256(zip_path),
		"Labels": labels,
		"Training labels distribution": label_train_distribution,
		"Validation labels distribution": label_valid_distribution,
		"Number of file in test folder": num_test_file,
		"Total file number": len(file_list),
		"File size in MB": round(total_size, 2)
		}

	return dataset_info


# Function to save dataset's information on blockchain
def save_to_blockchain(dataset_info):
    nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)
	
    tx = contract.functions.storeDatasetInfo(
        dataset_info["id"],  # (100, 75, 50, 25)
        dataset_info["dataset name"],
        dataset_info["hash"],
        dataset_info["Labels"],
        list(dataset_info["Training labels distribution"].keys()),
        list(dataset_info["Training labels distribution"].values()),
		list(dataset_info["Validation labels distribution"].keys()),
        list(dataset_info["Validation labels distribution"].values()),
		dataset_info["Number of file in test folder"],
        dataset_info["Total file number"],
        int(dataset_info["File size in MB"] * 1024)
    ).build_transaction({
        'from': WALLET_ADDRESS,
        'gas': 5000000,
        'gasPrice': w3.to_wei('10', 'gwei'),
        'nonce': nonce
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    print(f" Dataset {dataset_info["id"]} saved on blockchain!")
    return tx_hash.hex()


def get_dataset_info(id):
	(
    name,
    hash_value,
    classes,
    class_labels_train,
    class_sizes_train,
    class_labels_val,
    class_sizes_val,
    num_test_files,
    total_files,
    total_size_mb
) = contract.functions.getDatasetInfo(WALLET_ADDRESS, id).call()
	
	dataset_info = {
	"id": id,
    "dataset name": name,
    "hash": hash_value,
    "Labels": classes,
    "Training labels distribution": 
         dict(zip(class_labels_train, class_sizes_train))    
    ,
	"Validation labels distribution": 
		dict(zip(class_labels_val, class_sizes_val))
    ,
    "Number of file in test folder": num_test_files,
    "Total file number": total_files,
    "File size in MB": total_size_mb
}

	return dataset_info

def get_dataset_hash(id):
	hash = contract.functions.getDatasetHash(WALLET_ADDRESS,id).call()
	return hash
	



if __name__=="__main__":
	
	start = time.time()
	dataset_path = config["DATASET_PATH"]
	dataset_id = config["DATASET_ID"]

	

	path = "check_save_dataset"

	if os.path.exists(path):
		shutil.rmtree(path)


	

	
	dataset_info = extract_info(dataset_path,path,dataset_id)

	

	save_to_blockchain(dataset_info)
	save_hashes_on_blockchain(dataset_path)

	end = time.time()
	tempo = end- start
	print( "tempo impiegato:", tempo)
	
	

	