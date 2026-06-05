#!/usr/bin/env python3
"""
Deploy Kleros Bridge for Arbitrum + RBB
Arquiteto: Rafael Oliveira | AO | ORCID 0009-0005-2697-4668
Data: 2026-06-05

This script handles the dual deployment of the Kleros-Cathedral bridge.
Kleros v2 operates heavily on Arbitrum, while the Cathedral Mesh uses RBB.
This script orchestrates the deployment process across both chains.
"""

import os
import json
import subprocess
from web3 import Web3
from eth_account import Account

# Setup RPC endpoints
ARBITRUM_RPC = os.getenv("ARBITRUM_RPC_URL", "https://arb1.arbitrum.io/rpc")
RBB_RPC = os.getenv("RBB_RPC_URL", "http://localhost:8545") # Local RBB or Besu node

def run_hardhat_deploy(network_name: str) -> dict:
    """Runs the hardhat deploy script for a specific network and captures addresses."""
    print(f"[*] Deploying contracts to {network_name} via Hardhat...")
    try:
        # Run hardhat deploy and parse stdout
        result = subprocess.run(
            ["npx", "hardhat", "run", "scripts/deploy.js", "--network", network_name],
            capture_output=True, text=True, check=True, cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        output = result.stdout
        print(output)

        # Parse the addresses from the output
        addresses = {}
        for line in output.split('\n'):
            if "PNKTheosisOracle deployed to:" in line:
                addresses["PNKTheosisOracle"] = line.split(":")[-1].strip()
            elif "CathedralKlerosBridgeWithVoting deployed to:" in line:
                addresses["CathedralKlerosBridgeWithVoting"] = line.split(":")[-1].strip()

        if not addresses:
            print("[!] Warning: Could not parse addresses from deployment output.")

        return addresses
    except subprocess.CalledProcessError as e:
        print(f"[!] Subprocess Error deploying to {network_name}: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return {}
    except Exception as e:
        print(f"[!] Error deploying to {network_name}: {e}")
        return {}

def main():
    print("=" * 70)
    print("CATHEDRAL KLEROS BRIDGE DEPLOYMENT (ARBITRUM <-> RBB)")
    print("=" * 70)

    # 1. Deploy on Arbitrum (Oracle and Bridge for Kleros Interaction)
    arb_addresses = run_hardhat_deploy("arbitrum")

    if not arb_addresses:
        print("[-] Deployment on Arbitrum failed.")
        return

    print(f"[+] Arbitrum PNKTheosisOracle: {arb_addresses['PNKTheosisOracle']}")
    print(f"[+] Arbitrum CathedralKlerosBridge: {arb_addresses['CathedralKlerosBridgeWithVoting']}")

    # 2. Deploy on RBB (Mirror or cross-chain receiver)
    rbb_addresses = run_hardhat_deploy("rbb")

    if not rbb_addresses:
        print("[-] Deployment on RBB failed.")
        return

    print(f"[+] RBB PNKTheosisOracle: {rbb_addresses['PNKTheosisOracle']}")
    print(f"[+] RBB CathedralKlerosBridge: {rbb_addresses['CathedralKlerosBridgeWithVoting']}")

    # Save deployment info
    deployment_info = {
        "arbitrum": arb_addresses,
        "rbb": rbb_addresses
    }

    with open("deployments_kleros_bridge.json", "w") as f:
        json.dump(deployment_info, f, indent=4)

    print("\n[+] Deployment metadata saved to deployments_kleros_bridge.json")
    print("=" * 70)

if __name__ == "__main__":
    main()
