/*
* Verification of MyToken
*/

methods {
    function balanceOf(address) external returns uint256 envfree;
    function totalSupply() external returns uint256 envfree;
    function allowance(address, address) external returns uint256 envfree;
}

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

// Balance of any user must always be less than equal to TotalSupply
rule totalSupply_after_mint_always_greater_than_equal_user_balance(address user, uint256 amounts) {
    env e;
    require balanceOf(e, user) <= totalSupply(e);

    mint(e, user, amounts);

    assert balanceOf(e, user) <= totalSupply(e);
}

// transferFrom() decreases allowance of msg.sender
rule transferFrom_decreases_allowance_of_caller(address sender, address recipient, uint256 amounts) {
    env e;
    // address sender = e.msg.sender;
    require sender != recipient;

    uint256 allowanceBefore = allowance(e, sender, e.msg.sender);

    transferFrom(e, sender, recipient, amounts);

    uint256 allowanceAfter = allowance(e, sender, e.msg.sender);

    assert allowanceBefore >= allowanceAfter;
}

function callFunctionWithParams(env e, method f, address from, address to) {
    uint256 amount;

    if (f.selector == sig:transfer(address,uint256).selector) {
        require e.msg.sender == from;
        transfer(e, to, amount);
    } else if (f.selector == sig:approve(address,uint256).selector) {
        approve(e, to, amount);
    } else if (f.selector == sig:transferFrom(address,address,uint256).selector) {
        transferFrom(e, from, to, amount);
    } else if (f.selector == sig:mint(address,uint256).selector) {
        mint(e, to, amount);
    } else {
        calldataarg args;
        f(e, args);
    }
}

// Any function call dealing with 'from' and 'to' address must not change the balance of any thirdParty
rule does_not_affect_third_party_balance(method f) {
    env e;
    address from;
    address to;
    address thirdParty;

    require thirdParty != from && thirdParty != to;

    uint256 balanceBefore = balanceOf(thirdParty);

    callFunctionWithParams(e, f, from, to);

    assert balanceBefore == balanceOf(thirdParty);
}
