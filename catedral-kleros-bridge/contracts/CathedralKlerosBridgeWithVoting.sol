// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./PNKTheosisOracle.sol";

/**
 * @title CathedralKlerosBridgeWithVoting
 * @dev A bridge contract connecting Catedral and Kleros with "Theosis-weighted voting".
 */
contract CathedralKlerosBridgeWithVoting {
    PNKTheosisOracle public theosisOracle;
    address public owner;

    // Dispute structure representing a Kleros dispute bridged to Catedral
    struct Dispute {
        uint256 disputeId;
        uint256 theosisWeightTotal; // Total weight of votes including Theosis multiplier
        uint256 baseVotesTotal;     // Total unweighted base votes
        bool resolved;
        mapping(address => bool) hasVoted;
        mapping(uint256 => uint256) optionWeightedVotes; // option ID => total weighted votes
        mapping(uint256 => uint256) optionBaseVotes;     // option ID => total base votes
    }

    mapping(uint256 => Dispute) public disputes;

    event DisputeBridged(uint256 indexed disputeId);
    event VoteCast(uint256 indexed disputeId, address indexed juror, uint256 option, uint256 weight);
    event DisputeResolved(uint256 indexed disputeId, uint256 winningOption);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    constructor(address _oracleAddress) {
        owner = msg.sender;
        theosisOracle = PNKTheosisOracle(_oracleAddress);
    }

    /**
     * @dev Bridges a new dispute from Kleros to Catedral context.
     * @param disputeId The ID of the dispute.
     */
    function bridgeDispute(uint256 disputeId) external onlyOwner {
        require(!disputes[disputeId].resolved, "Dispute already resolved");
        require(disputes[disputeId].disputeId == 0, "Dispute already bridged");

        disputes[disputeId].disputeId = disputeId;
        emit DisputeBridged(disputeId);
    }

    /**
     * @dev Cast a vote on a dispute with Theosis weighting.
     * @param disputeId The ID of the dispute.
     * @param option The option voted for.
     */
    function castVote(uint256 disputeId, uint256 option) external {
        Dispute storage dispute = disputes[disputeId];
        require(dispute.disputeId != 0, "Dispute not bridged");
        require(!dispute.resolved, "Dispute resolved");
        require(!dispute.hasVoted[msg.sender], "Juror already voted");

        // Ensure juror is qualified via the Oracle
        require(theosisOracle.isJurorQualified(msg.sender), "Juror not qualified by Theosis");

        // Calculate weight: Base vote is 1 (scaled by 10000 for precision).
        // Theosis score adds additional weight.
        // Example: Score of 5000 adds 50% weight -> total weight 15000.
        uint256 theosisScore = theosisOracle.getTheosisScore(msg.sender);
        uint256 weight = 10000 + theosisScore;

        dispute.hasVoted[msg.sender] = true;
        dispute.optionWeightedVotes[option] += weight;
        dispute.optionBaseVotes[option] += 1;
        dispute.theosisWeightTotal += weight;
        dispute.baseVotesTotal += 1;

        emit VoteCast(disputeId, msg.sender, option, weight);
    }

    /**
     * @dev Resolves the dispute. Simplified for demonstration.
     * @param disputeId The ID of the dispute.
     * @param winningOption The option that won.
     */
    function resolveDispute(uint256 disputeId, uint256 winningOption) external onlyOwner {
        Dispute storage dispute = disputes[disputeId];
        require(dispute.disputeId != 0, "Dispute not bridged");
        require(!dispute.resolved, "Dispute already resolved");

        dispute.resolved = true;
        emit DisputeResolved(disputeId, winningOption);
    }

    /**
     * @dev Gets the current weighted votes for an option.
     */
    function getOptionWeightedVotes(uint256 disputeId, uint256 option) external view returns (uint256) {
        return disputes[disputeId].optionWeightedVotes[option];
    }
}
