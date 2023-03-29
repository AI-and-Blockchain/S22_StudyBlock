pragma solidity ^0.8.0;

contract ClinicalTrialMessaging {
    mapping(address => mapping(address => string)) private messages;

    function sendMessage(address receiver, string memory message) public {
        require(receiver != msg.sender, "You cannot send a message to yourself");
        messages[msg.sender][receiver] = message;
    }

    function getMessage(address sender) public view returns (string memory) {
        return messages[sender][msg.sender];
    }
}