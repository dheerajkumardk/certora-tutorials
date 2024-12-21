/*
* Verification of MyToken
*/

// Transfer must move 'amount' of tokens from 'caller' to 'recipient'
rule transfer(address recipient, uint256 amounts) {
    env e;
    address sender = e.msg.sender;
    mathint balCallerBefore = balanceOf(e, sender);
    mathint balReceiverBefore = balanceOf(e, recipient);

    // Act  
    transfer(e, recipient, amounts);

    // Assert
    mathint balCallerAfter = balanceOf(e, sender);
    mathint balReceiverAfter = balanceOf(e, recipient);

    assert balCallerAfter == balCallerBefore - amounts;
    assert balReceiverAfter == balReceiverBefore + amounts;
}