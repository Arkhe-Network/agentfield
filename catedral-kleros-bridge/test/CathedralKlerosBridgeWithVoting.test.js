const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("CathedralKlerosBridgeWithVoting", function () {
  let PNKTheosisOracle;
  let oracle;
  let CathedralKlerosBridge;
  let bridge;
  let owner;
  let juror1;
  let juror2;
  let unqualifiedJuror;

  beforeEach(async function () {
    [owner, juror1, juror2, unqualifiedJuror] = await ethers.getSigners();

    // Deploy Oracle
    PNKTheosisOracle = await ethers.getContractFactory("PNKTheosisOracle");
    oracle = await PNKTheosisOracle.deploy();
    await oracle.waitForDeployment();

    // Deploy Bridge
    CathedralKlerosBridge = await ethers.getContractFactory("CathedralKlerosBridgeWithVoting");
    bridge = await CathedralKlerosBridge.deploy(await oracle.getAddress());
    await bridge.waitForDeployment();

    // Setup juror Theosis scores
    await oracle.updateTheosis(juror1.address, 6000); // 60% extra weight -> 16000 total weight
    await oracle.updateTheosis(juror2.address, 8000); // 80% extra weight -> 18000 total weight
    await oracle.updateTheosis(unqualifiedJuror.address, 3000); // Unqualified (< 5000)
  });

  describe("PNKTheosisOracle", function () {
    it("Should set initial theosis score and qualification status correctly", async function () {
      expect(await oracle.getTheosisScore(juror1.address)).to.equal(6000);
      expect(await oracle.isJurorQualified(juror1.address)).to.equal(true);

      expect(await oracle.getTheosisScore(unqualifiedJuror.address)).to.equal(3000);
      expect(await oracle.isJurorQualified(unqualifiedJuror.address)).to.equal(false);
    });

    it("Should only allow owner to update Theosis", async function () {
      await expect(
        oracle.connect(juror1).updateTheosis(juror1.address, 7000)
      ).to.be.revertedWith("Only owner");
    });
  });

  describe("CathedralKlerosBridgeWithVoting", function () {
    it("Should bridge a dispute", async function () {
      const disputeId = 1;
      await expect(bridge.bridgeDispute(disputeId))
        .to.emit(bridge, "DisputeBridged")
        .withArgs(disputeId);
    });

    it("Should not allow non-owners to bridge a dispute", async function () {
      await expect(
        bridge.connect(juror1).bridgeDispute(2)
      ).to.be.revertedWith("Only owner");
    });

    it("Should allow qualified jurors to cast votes with Theosis weight", async function () {
      const disputeId = 1;
      await bridge.bridgeDispute(disputeId);

      // juror1 votes for option 1
      await expect(bridge.connect(juror1).castVote(disputeId, 1))
        .to.emit(bridge, "VoteCast")
        .withArgs(disputeId, juror1.address, 1, 16000);

      // juror2 votes for option 2
      await expect(bridge.connect(juror2).castVote(disputeId, 2))
        .to.emit(bridge, "VoteCast")
        .withArgs(disputeId, juror2.address, 2, 18000);

      expect(await bridge.getOptionWeightedVotes(disputeId, 1)).to.equal(16000);
      expect(await bridge.getOptionWeightedVotes(disputeId, 2)).to.equal(18000);
    });

    it("Should block unqualified jurors from voting", async function () {
      const disputeId = 1;
      await bridge.bridgeDispute(disputeId);

      await expect(
        bridge.connect(unqualifiedJuror).castVote(disputeId, 1)
      ).to.be.revertedWith("Juror not qualified by Theosis");
    });

    it("Should prevent double voting", async function () {
      const disputeId = 1;
      await bridge.bridgeDispute(disputeId);

      await bridge.connect(juror1).castVote(disputeId, 1);

      await expect(
        bridge.connect(juror1).castVote(disputeId, 1)
      ).to.be.revertedWith("Juror already voted");
    });

    it("Should allow owner to resolve dispute", async function () {
      const disputeId = 1;
      await bridge.bridgeDispute(disputeId);
      await bridge.connect(juror1).castVote(disputeId, 1);

      await expect(bridge.resolveDispute(disputeId, 1))
        .to.emit(bridge, "DisputeResolved")
        .withArgs(disputeId, 1);
    });
  });
});
