// SPDX-License-Identifier: MIT

pragma solidity 0.8.28;

import {Test} from "forge-std/src/Test.sol";
import {MyToken} from "../src/MyToken.sol";

contract TokenTest is Test {
    MyToken token;

    function setUp() public {
        token = new MyToken();
    }

    function testTokenSetup() public {
        assertEq(token.name(), "My Token");
        assertEq(token.symbol(), "MTN");
    }
}
