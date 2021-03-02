// SPDX-License-Identifier: MIT

pragma solidity ^0.5.16;

import "./IERC20.sol";

interface IMooniswap {
    function getTokens() external view returns (IERC20[] memory tokens);

    function tokens(uint256 i) external view returns (IERC20);

    function totalSupply() external view returns (uint256);

    function decimals() external view returns (uint8);
}
