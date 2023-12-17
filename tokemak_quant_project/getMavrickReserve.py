import os
from dotenv import load_dotenv
from web3 import Web3
import json
import csv

# https://github.com/ethers-io/ethers.js/blob/master/packages/providers/src.ts/alchemy-provider.ts#L16-L21
# NOTE: likely to get rate limited
default_provider_url = "https://eth-mainnet.g.alchemy.com/v2/_gg7wSSi0KMBsdKnGVfHDueq6xMB9EkC"

def main():
    load_dotenv()
    w3 = Web3(Web3.HTTPProvider(os.getenv('PROVIDER_URL', default_provider_url)))
    # Check if the connection is successful
    if not w3.isConnected():
        print("Failed to connect to Ethereum node.")
        exit()

    # Contract Information
    pool_info_address = Web3.toChecksumAddress('0x0087D11551437c3964Dddf0F4FA58836c5C5d949')
    pool_address = Web3.toChecksumAddress('0x0CE176E1b11A8f88a4Ba2535De80E81F88592bad')
    pool_info_abi = [{"inputs":[{"internalType":"contract IPool","name":"pool","type":"address"}],"name":"activeTickLiquidity","outputs":[{"internalType":"uint256","name":"sqrtPrice","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IPool","name":"pool","type":"address"},{"internalType":"int32","name":"tick","type":"int32"}],"name":"getBinsAtTick","outputs":[{"components":[{"internalType":"uint128","name":"reserveA","type":"uint128"},{"internalType":"uint128","name":"reserveB","type":"uint128"},{"internalType":"uint128","name":"mergeBinBalance","type":"uint128"},{"internalType":"uint128","name":"mergeId","type":"uint128"},{"internalType":"uint128","name":"totalSupply","type":"uint128"},{"internalType":"uint8","name":"kind","type":"uint8"},{"internalType":"int32","name":"lowerTick","type":"int32"}],"internalType":"struct IPool.BinState[]","name":"bins","type":"tuple[]"}],"stateMutability":"view","type":"function"}]
    pool_abi = [{"constant":True,"inputs":[],"name":"getState","outputs":[{"components":[{"name":"activeTick","type":"int32"},{"name":"status","type":"uint8"},{"name":"binCounter","type":"uint128"},{"name":"protocolFeeRatio","type":"uint64"}],"name":"","type":"tuple"}],"payable":False,"stateMutability":"view","type":"function"}]

    pool_info_contract = w3.eth.contract(address=pool_info_address, abi=pool_info_abi)
    pool_contract = w3.eth.contract(address=pool_address, abi=pool_abi)

    # Read block numbers from CSV
    with open('mavrick_swap_logs.csv', mode='r') as infile:
        reader = csv.DictReader(infile)
        block_numbers = [row['blockNumber'] for row in reader]

    # # Fetch data and write to new CSV file
    with open('mav_reserves.csv', mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['block_number', 'reserveA', 'reserveB', 'total_reserveA', 'total_reserveB'])

        for block_number in block_numbers:
            state = pool_contract.functions.getState().call(block_identifier=int(block_number))
            bin_states = pool_info_contract.functions.getBinsAtTick(pool_address, state[0]).call(block_identifier=int(block_number))

            # Initialize total reserves
            total_reserveA = total_reserveB = 0

            # Initialize specific reserves for kind == 3
            reserveA_kind3 = reserveB_kind3 = 0

            contains_kind3 = False

            for bin_state in bin_states:
                total_reserveA += bin_state[0]  # reserveA
                total_reserveB += bin_state[1]  # reserveB

                # Check if kind == 3 and update reserves
                if bin_state[5] == 3:  # kind
                    reserveA_kind3 = bin_state[0]  # reserveA
                    reserveB_kind3 = bin_state[1]  # reserveB
                    contains_kind3 = True

            if contains_kind3:
                writer.writerow([block_number, reserveA_kind3, reserveB_kind3, total_reserveA, total_reserveB])

    print("Data extraction complete.")


if __name__ == '__main__':
    main()


