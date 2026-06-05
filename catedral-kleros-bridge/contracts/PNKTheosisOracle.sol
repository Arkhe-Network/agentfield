// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title PNKTheosisOracle
 * @dev Oracle to track Kleros jurors (PNK holders) and their Theosis levels on-chain.
 */
contract PNKTheosisOracle {
    struct JurorTheosis {
        uint256 theosisScore; // Range 0-10000 (0.00 to 100.00)
        bool isQualified;
        uint256 lastUpdate;
    }

    address public owner;
    mapping(address => JurorTheosis) public jurorTheosis;
    address[] public activeJurors;

    event TheosisUpdated(address indexed juror, uint256 theosisScore, bool isQualified);
    event JurorQualifiedStatusChanged(address indexed juror, bool isQualified);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    /**
     * @dev Updates the Theosis score for a juror.
     * @param juror The address of the juror.
     * @param score The new Theosis score (0-10000).
     */
    function updateTheosis(address juror, uint256 score) external onlyOwner {
        require(score <= 10000, "Score exceeds maximum");

        bool previouslyQualified = jurorTheosis[juror].isQualified;
        bool currentlyQualified = score >= 5000; // Example threshold

        if (jurorTheosis[juror].lastUpdate == 0) {
            activeJurors.push(juror);
        }

        jurorTheosis[juror].theosisScore = score;
        jurorTheosis[juror].lastUpdate = block.timestamp;

        if (previouslyQualified != currentlyQualified) {
            jurorTheosis[juror].isQualified = currentlyQualified;
            emit JurorQualifiedStatusChanged(juror, currentlyQualified);
        }

        emit TheosisUpdated(juror, score, currentlyQualified);
    }

    /**
     * @dev Gets the Theosis score for a juror.
     * @param juror The address of the juror.
     * @return theosisScore The Theosis score.
     */
    function getTheosisScore(address juror) external view returns (uint256) {
        return jurorTheosis[juror].theosisScore;
    }

    /**
     * @dev Checks if a juror is qualified based on Theosis score.
     * @param juror The address of the juror.
     * @return isQualified True if qualified, false otherwise.
     */
    function isJurorQualified(address juror) external view returns (bool) {
        return jurorTheosis[juror].isQualified;
    }

    /**
     * @dev Returns total number of active jurors recorded.
     */
    function getActiveJurorsCount() external view returns (uint256) {
        return activeJurors.length;
    }
}
