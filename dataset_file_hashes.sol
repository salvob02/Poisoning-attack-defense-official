// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

contract FileHashStoragev101 {
    mapping(string => string) private fileHashes; // Mapping percorso → hash MD5
    string[] private filePaths; // Array con i percorsi dei file (ordine mantenuto)

    // Salva gli hash dei file
    function storeFileHashes(string[] memory _paths, string[] memory _hashes) public {
        require(_paths.length == _hashes.length, "Mismatch tra percorsi e hash");

        for (uint256 i = 0; i < _paths.length; i++) {
            if (bytes(fileHashes[_paths[i]]).length == 0) { // Evita duplicati
                filePaths.push(_paths[i]);
            }
            fileHashes[_paths[i]] = _hashes[i];
        }
    }

    //   Recupera il numero totale di file salvati
    function getTotalFilePaths() public view returns (uint256) {
        return filePaths.length;
    }

    //   Recupera un batch di filePaths
    function getFilePathsBatch(uint startIndex, uint batchSize) public view returns (string[] memory) {
        uint endIndex = startIndex + batchSize;
        if (endIndex > filePaths.length) {
            endIndex = filePaths.length;
        }

        string[] memory batch = new string[](endIndex - startIndex);
        for (uint i = startIndex; i < endIndex; i++) {
            batch[i - startIndex] = filePaths[i];
        }
        return batch;
    }

    //  Recupera un batch di hash MD5 corrispondenti ai file
    function getFileHashesBatch(uint startIndex, uint batchSize) public view returns (string[] memory) {
        uint endIndex = startIndex + batchSize;
        if (endIndex > filePaths.length) {
            endIndex = filePaths.length;
        }

        string[] memory batch = new string[](endIndex - startIndex);
        for (uint i = startIndex; i < endIndex; i++) {
            batch[i - startIndex] = fileHashes[filePaths[i]];
        }
        return batch;
    }



    // ✅ Restituisce l'hash di un singolo file
    function getHashByPath(string memory path) public view returns (string memory) {
        return fileHashes[path];
    }
