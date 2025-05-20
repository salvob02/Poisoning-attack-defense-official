from find_directory import find_dirs
from save_datasetInfo_on_bkch import compute_sha256,get_dataset_hash, extract_info, get_dataset_info 
from md5_save_dataset_hash_ import get_hashes_from_blockchain_batch, get_sorted_file_hashes_from_zip
from compare_dictionary import compare_model_dictionaries
import time,sys,yaml,os,shutil
from deepdiff import DeepDiff


with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

extract_folder = "extracted_dataset_for_check"

if os.path.exists(extract_folder):
		shutil.rmtree(extract_folder)

dataset_id = config["DATASET_ID_CHECK"]
zip_path = config["DATASET_PATH_CHECK"]

if __name__=="__main__":
    
    # Preprocessing of dataset
    start_verifica_dataset = time.time()
    

    local_dataset_hash = compute_sha256(zip_path) #hash of zip dataset
    end_calcolo_dataset_hash = time.time()
    

    bkch_dataset_hash = get_dataset_hash(dataset_id)   #hash of dataset from blockchain
    end_recupero_bkch_hash = time.time()
    if(local_dataset_hash == bkch_dataset_hash):
        sys.exit("EQUAL DATASET")

    else:
        print("DIFFERENT DATASET")


    local_dataset_info = extract_info(zip_path,extract_folder,dataset_id)

    hash_file_local = get_sorted_file_hashes_from_zip(zip_path)   #files's hashes of the local dataset

    hash_file_bkch = get_hashes_from_blockchain_batch()    #file's hashes back from the blockchain"
    

    if((local_dataset_hash != bkch_dataset_hash) or (hash_file_local!=hash_file_bkch)):
        print("DIFFERENCE IN THE TOTAL LOCAL DATASET'S HASH")

        bckh_dataset_info = get_dataset_info(dataset_id)
        
        
        local_dataset_info["File size in MB"] = int(local_dataset_info["File size in MB"]* 1024)

        
        compare_model_dictionaries(local_dataset_info,bckh_dataset_info)

        diff = DeepDiff(hash_file_bkch,hash_file_local,verbose_level=2)  #difference between local file's hashes and same saved on blockchain
        if diff:
            with open("log.txt", "w") as f:
                f.write(str(diff))

         
        
        end_time = time.time()
        #current_time = end_time - start_time
        
        sys.exit("PROGRAM FINISHED")





