// SPDX-License-Identifier: MIT

pragma solidity >=0.6.2;

import "OpenZeppelin/openzeppelin-contracts@3.3.0/contracts/token/ERC20/IERC20.sol";

interface Mooniswap is IERC20 {
    function getTokens() external view returns (IERC20[] memory tokens);

    function tokens(uint256 i) external view returns (IERC20);

    function decimals() external view returns (uint8);
}
