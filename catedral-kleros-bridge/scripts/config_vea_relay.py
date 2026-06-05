#!/usr/bin/env python3
"""
Vea Relay Configuration Script (Arbitrum -> RBB)
Arquiteto: Rafael Oliveira | AO | ORCID 0009-0005-2697-4668
Data: 2026-06-05

This script configures the Vea bridge relay to pass Kleros dispute decisions
from Arbitrum to the Cathedral Mesh on RBB.
"""

import os
import json

def config_vea_relay():
    print("=" * 70)
    print("CONFIGURING VEA RELAY (ARBITRUM -> RBB)")
    print("=" * 70)

    # Load deployment addresses
    try:
        with open("deployments_kleros_bridge.json", "r") as f:
            deployments = json.load(f)
    except FileNotFoundError:
        print("[!] Deployments file not found. Run deploy_kleros_bridge.py first.")
        return

    arb_bridge = deployments.get("arbitrum", {}).get("CathedralKlerosBridgeWithVoting")
    rbb_bridge = deployments.get("rbb", {}).get("CathedralKlerosBridgeWithVoting")

    if not arb_bridge or not rbb_bridge:
        print("[!] Missing bridge addresses in deployments file.")
        return

    # Mock Vea configuration process
    vea_config = {
        "source_chain": "Arbitrum",
        "target_chain": "RBB",
        "source_address": arb_bridge,
        "target_address": rbb_bridge,
        "fast_path_enabled": True,
        "challenge_period": 86400 # 24 hours
    }

    print(f"[*] Setting Source Address (Arbitrum): {arb_bridge}")
    print(f"[*] Setting Target Address (RBB): {rbb_bridge}")
    print(f"[*] Challenge Period: {vea_config['challenge_period']} seconds")

    with open("vea_relay_config.json", "w") as f:
        json.dump(vea_config, f, indent=4)

    print("\n[+] Vea Relay configured successfully.")
    print("[+] Configuration saved to vea_relay_config.json")
    print("=" * 70)

if __name__ == "__main__":
    config_vea_relay()
