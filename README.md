# Poisoning-attack-defense
This project implements a defense mechanism against poisoning attacks carried out on datasets in .zip format. The goal is to ensure the integrity and traceability of datasets by leveraging a private Ethereum blockchain to securely store critical information such as dataset hashes and metadata.

Tools Used:

Ganache GUI – Local private Ethereum blockchain for development and testing.

MetaMask – A crypto wallet and browser extension used to interact with the blockchain.

Remix IDE – A web-based Integrated Development Environment for writing, deploying, and testing smart contracts in Solidity.

Setup Instructions:

1. Download and Configure Ganache:

Install Ganache GUI and create a new workspace.

Increase the gas limit to 100,000,000 units.

Allocate 600 ETH to each generated account.

2. Connect Ganache to MetaMask:

Open MetaMask and create/import an account.

Add a custom network using the following Ganache parameters:

Network Name: Localhost 

New RPC URL: http://127.0.0.1:7545 (or the one shown in Ganache)

Chain ID: 1337 or 5777 (verify in Ganache)

Currency Symbol: ETH (optional)

Block Explorer URL: leave empty

3. Import a Ganache Account into MetaMask:

Copy the private key of the desired account directly from the Ganache GUI.

Use MetaMask’s “Import Account” feature to add it.

Configure Remix IDE:

Open Remix and go to the Deploy & Run Transactions tab.

Set the environment to Injected Provider - Web3.

Ensure the selected account matches the one imported into MetaMask (connected to Ganache).

4. Deploy Smart Contracts:

Deploy the smart contracts dataset_info.sol and dataset_hash_file.sol to the private blockchain using Remix.

Ensure correct compilation before deploying.

Gas Limit Requirement:

For the second smart contract (dataset_hash_file.sol), set the gas limit to at least 100,000,000 units to ensure successful deployment.




Execution:

- Insert into file "config.yaml" the parameters
- Execute file "save_datasetInfo_on_bkch.py" to save dataset_info on bkch.
- Execute file "check_dataset.py" to check the integrity of the dataset.
- Result could be viewed in the terminal and eventually in the file log.txt.



You could try with dataset: https://www.kaggle.com/datasets/pmigdal/alien-vs-predator-images?resource=download
- datasets must have exactly: -- only one folder which name include 'train'   that represents training folder
                              -- max one folder which name include 'val'     that represents validation folder
                              -- max one folder which name include 'test'     that represents test folder

- labels must have been included in folder which name represents label's name otherwise program doesn't recognise them.
