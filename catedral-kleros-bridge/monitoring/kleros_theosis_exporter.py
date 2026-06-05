#!/usr/bin/env python3
"""
Kleros Theosis Prometheus Exporter
Fetches metrics from the PNKTheosisOracle contract and exposes them.
"""

import os
import time
from prometheus_client import start_http_server, Gauge, Counter
from web3 import Web3

# Configuration
RPC_URL = os.getenv("RPC_URL", "http://localhost:8545")
ORACLE_ADDRESS = os.getenv("ORACLE_ADDRESS", "0x0000000000000000000000000000000000000000")
PORT = int(os.getenv("EXPORTER_PORT", 8000))

# Web3 initialization
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Contract ABI (Minimal)
ABI = [
    {
        "inputs": [],
        "name": "getActiveJurorsCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "activeJurors",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "juror", "type": "address"}],
        "name": "getTheosisScore",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "juror", "type": "address"}],
        "name": "isJurorQualified",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Prometheus Metrics
ACTIVE_JURORS_COUNT = Gauge('kleros_active_jurors_count', 'Number of active jurors recorded in the Oracle')
QUALIFIED_JURORS_COUNT = Gauge('kleros_qualified_jurors_count', 'Number of jurors with a qualified Theosis score')
AVERAGE_THEOSIS_SCORE = Gauge('kleros_average_theosis_score', 'Average Theosis score among all recorded jurors')
SCRAPE_ERRORS = Counter('kleros_exporter_scrape_errors_total', 'Total number of errors during contract scraping')

def update_metrics(contract):
    """Fetches data from the contract and updates Prometheus metrics."""
    try:
        if not w3.is_connected():
            raise Exception("Web3 is not connected to the node.")

        juror_count = contract.functions.getActiveJurorsCount().call()
        ACTIVE_JURORS_COUNT.set(juror_count)

        qualified_count = 0
        total_score = 0

        # In a production environment, this should ideally be optimized using Multicall
        # or event indexing, rather than iterating through an array on-chain.
        for i in range(juror_count):
            juror_addr = contract.functions.activeJurors(i).call()

            is_qualified = contract.functions.isJurorQualified(juror_addr).call()
            if is_qualified:
                qualified_count += 1

            score = contract.functions.getTheosisScore(juror_addr).call()
            total_score += score

        QUALIFIED_JURORS_COUNT.set(qualified_count)

        if juror_count > 0:
            avg_score = total_score / juror_count
            AVERAGE_THEOSIS_SCORE.set(avg_score)
        else:
            AVERAGE_THEOSIS_SCORE.set(0)

        print(f"Metrics updated: {juror_count} active, {qualified_count} qualified.")

    except Exception as e:
        print(f"Error fetching metrics: {e}")
        SCRAPE_ERRORS.inc()

def main():
    if not w3.is_connected():
        print(f"Failed to connect to RPC: {RPC_URL}")
        # Proceed anyway, w3 might connect later or it's a test run
    else:
        print(f"Connected to RPC: {RPC_URL}")

    # For testing/demo purposes, we allow starting even with dummy address
    try:
        contract = w3.eth.contract(address=w3.to_checksum_address(ORACLE_ADDRESS), abi=ABI)
    except Exception:
        print(f"Warning: Invalid Oracle Address: {ORACLE_ADDRESS}")
        contract = None

    print(f"Starting Prometheus exporter on port {PORT}")
    start_http_server(PORT)

    while True:
        if contract and w3.is_connected():
            update_metrics(contract)
        time.sleep(15) # Update interval

if __name__ == "__main__":
    main()
