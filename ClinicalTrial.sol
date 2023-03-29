pragma solidity ^0.8.0;

contract ClinicalTrial {
    
    address private client;
    bytes32 private privateKey;
    mapping (address => bool) private backendUsers;

    event PrivateKeySent(address sender, address recipient);
    event DataSent(address sender, address recipient, string data);

    constructor() {
        client = msg.sender;
        privateKey = bytes32(0);
    }
    
    modifier onlyClient() {
        require(msg.sender == client, "Only the client can call this function.");
        _;
    }
    
    modifier onlyBackendUser() {
        require(backendUsers[msg.sender] == true, "Only a backend user can call this function.");
        _;
    }
    
    function sendPrivateKey(bytes32 key, address recipient) public onlyClient {
        privateKey = key;
        emit PrivateKeySent(msg.sender, recipient);
    }
    
    function addBackendUser(address user) public onlyClient {
        backendUsers[user] = true;
    }
    
    function removeBackendUser(address user) public onlyClient {
        backendUsers[user] = false;
    }
    
    function sendData(string memory data) public onlyBackendUser {
        require(privateKey != bytes32(0), "Private key has not been sent yet.");
        emit DataSent(msg.sender, client, data);
    }
    
}
