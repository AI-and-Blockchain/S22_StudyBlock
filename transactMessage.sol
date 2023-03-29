pragma solidity ^0.8.0;

contract transactMessage {
    string public message;
    address owner;
    uint public changeCounter;

    constructor() public {
        owner = msg.sender;
    }

    function updateMessage(string memory newMessage) public {
        require(msg.sender == owner, "Only the contract owner can update the message");
        message = newMessage;
        changeCounter+=1;
    }
}