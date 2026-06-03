// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

/**
 * @title RBB Cathedral Token
 * @notice ERC-20 Token with mint controlled by the Bridge and Theosis-based fees.
 */
contract RBB_Cathedral_Token is ERC20, AccessControl {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    constructor() ERC20("RBB Cathedral Token", "RBBCT") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
    }

    function mint(address to, uint256 amount) public onlyRole(MINTER_ROLE) {
        _mint(to, amount);
    }

    // Override default transfer to enforce the fee
    function transfer(address recipient, uint256 amount) public override returns (bool) {
        // Assume a 1% Theosis fee
        uint256 fee = amount / 100;
        uint256 netAmount = amount - fee;

        _transfer(_msgSender(), recipient, netAmount);
        if (fee > 0) {
            _burn(_msgSender(), fee);
        }
        return true;
    }

    // Override default transferFrom to enforce the fee
    function transferFrom(address sender, address recipient, uint256 amount) public override returns (bool) {
        // Assume a 1% Theosis fee
        uint256 fee = amount / 100;
        uint256 netAmount = amount - fee;

        _spendAllowance(sender, _msgSender(), amount);
        _transfer(sender, recipient, netAmount);
        if (fee > 0) {
            _burn(sender, fee);
        }
        return true;
    }
}
