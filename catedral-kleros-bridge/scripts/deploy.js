const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);

  // Deploy PNKTheosisOracle
  const PNKTheosisOracle = await hre.ethers.getContractFactory("PNKTheosisOracle");
  const oracle = await PNKTheosisOracle.deploy();
  await oracle.deployed();

  console.log("PNKTheosisOracle deployed to:", oracle.address);

  // Deploy CathedralKlerosBridgeWithVoting
  const CathedralKlerosBridge = await hre.ethers.getContractFactory("CathedralKlerosBridgeWithVoting");
  const bridge = await CathedralKlerosBridge.deploy(oracle.address);
  await bridge.deployed();

  console.log("CathedralKlerosBridgeWithVoting deployed to:", bridge.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
