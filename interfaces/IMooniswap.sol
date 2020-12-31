// SPDX-License-Identifier: MIT

pragma solidity >=0.6.2;

import "./IERC20.sol";

interface IMooniswap is IERC20 {
    function getTokens() external view returns (IERC20[] memory tokens);

    function tokens(uint256 i) external view returns (IERC20);
}
