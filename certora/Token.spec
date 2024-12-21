/*
* Verification of MyToken
*/

// Transfer must move 'amount' of tokens from 'caller' to 'recipient'
rule transfer(address recipient, uint256 amounts) {
    env e;
    address sender = e.msg.sender;
    mathint balCallerBefore = balanceOf(e, sender);
    mathint balReceiverBefore = balanceOf(e, recipient);
    require balReceiverBefore + amounts <= max_uint256;

    // Act  
    transfer(e, recipient, amounts);

    // Assert
    mathint balCallerAfter = balanceOf(e, sender);
    mathint balReceiverAfter = balanceOf(e, recipient);

    assert recipient != sender => balCallerAfter == balCallerBefore - amounts;
    assert recipient != sender => balReceiverAfter == balReceiverBefore + amounts;
    // if recipient == sender
    assert recipient == sender => balCallerBefore == balCallerAfter;
}