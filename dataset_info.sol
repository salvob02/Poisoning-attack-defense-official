// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

contract DatasetStorage {

    struct Dataset {
        string name;
        string hashValue;
        string[] classes;
        string[] classLabelsTrain;
        uint256[] classSizesTrain;
        string[] classLabelsVal;
        uint256[] classSizesVal;
        uint256 numTestFiles;
        uint256 totalFiles;
        uint256 totalSizeMB;
    }

    mapping(address => mapping(uint256 => Dataset)) private datasets;
    mapping(uint256 => address) private datasetOwners;
    mapping(address => uint256[]) private ownerDatasetIds;

    // Salva o aggiorna un dataset
    function storeDatasetInfo(
        uint256 _datasetId,
        string memory _name,
        string memory _hashValue,
        string[] memory _classes,
        string[] memory _classLabelsTrain,
        uint256[] memory _classSizesTrain,
        string[] memory _classLabelsVal,
        uint256[] memory _classSizesVal,
        uint256 _numTestFiles,
        uint256 _totalFiles,
        uint256 _totalSizeMB
    ) public {
        Dataset storage ds = datasets[msg.sender][_datasetId];
        ds.name = _name;
        ds.hashValue = _hashValue;
        ds.classes = _classes;
        ds.classLabelsTrain = _classLabelsTrain;
        ds.classSizesTrain = _classSizesTrain;
        ds.classLabelsVal = _classLabelsVal;
        ds.classSizesVal = _classSizesVal;
        ds.numTestFiles = _numTestFiles;
        ds.totalFiles = _totalFiles;
        ds.totalSizeMB = _totalSizeMB;

        datasetOwners[_datasetId] = msg.sender;
        ownerDatasetIds[msg.sender].push(_datasetId);
    }

    // Recupera tutte le info di un dataset
    function getDatasetInfo(address _owner, uint256 _datasetId)
        public
        view
        returns (
            string memory name,
            string memory hashValue,
            string[] memory classes,
            string[] memory classLabelsTrain,
            uint256[] memory classSizesTrain,
            string[] memory classLabelsVal,
            uint256[] memory classSizesVal,
            uint256 numTestFiles,
            uint256 totalFiles,
            uint256 totalSizeMB
        )
    {
        Dataset storage ds = datasets[_owner][_datasetId];
        return (
            ds.name,
            ds.hashValue,
            ds.classes,
            ds.classLabelsTrain,
            ds.classSizesTrain,
            ds.classLabelsVal,
            ds.classSizesVal,
            ds.numTestFiles,
            ds.totalFiles,
            ds.totalSizeMB
        );
    }


    // Recupera hash dataset
    function getDatasetHash(address _owner, uint256 _datasetId) public view returns (string memory) {
        return datasets[_owner][_datasetId].hashValue;
    }

}
