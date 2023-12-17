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
    pool_info_abi = [{"inputs":[{"internalType":"contract IPool","name":"pool","type":"address"}],"name":"activeTickLiquidity","outputs":[{"internalType":"uint256","name":"sqrtPrice","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IPool","name":"pool","type":"address"},{"internalType":"int32","name":"tick","type":"int32"}],"name":"getBinsAtTick","outputs":[{"components":[{"internalType":"uint128","name":"reserveA","type":"uint128"},{"internalType":"uint128","name":"reserveB","type":"uint128"},{"internalType":"uint128","name":"mergeBinBalance","type":"uint128"},{"internalType":"uint128","name":"mergeId","type":"uint128"},{"internalType":"uint128","name":"totalSupply","type":"uint128"},{"internalType":"uint8","name":"kind","type":"uint8"},{"internalType":"int32","name":"lowerTick","type":"int32"}],"internalType":"struct IPool.BinState[]","name":"bins","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IPool","name":"pool","type":"address"},{"internalType":"uint128","name":"startBinIndex","type":"uint128"},{"internalType":"uint128","name":"endBinIndex","type":"uint128"}],"name":"getActiveBins","outputs":[{"components":[{"internalType":"uint128","name":"id","type":"uint128"},{"internalType":"uint8","name":"kind","type":"uint8"},{"internalType":"int32","name":"lowerTick","type":"int32"},{"internalType":"uint128","name":"reserveA","type":"uint128"},{"internalType":"uint128","name":"reserveB","type":"uint128"},{"internalType":"uint128","name":"mergeId","type":"uint128"}],"internalType":"struct IPoolInformation.BinInfo[]","name":"bins","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IPool","name":"pool","type":"address"}],"name":"getSqrtPrice","outputs":[{"internalType":"uint256","name":"sqrtPrice","type":"uint256"}],"stateMutability":"view","type":"function"}]
    pool_abi = [{"constant":True,"inputs":[],"name":"getState","outputs":[{"components":[{"name":"activeTick","type":"int32"},{"name":"status","type":"uint8"},{"name":"binCounter","type":"uint128"},{"name":"protocolFeeRatio","type":"uint64"}],"name":"","type":"tuple"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"binId","type":"uint128"}],"name":"getBin","outputs":[{"components":[{"name":"reserveA","type":"uint128"},{"name":"reserveB","type":"uint128"},{"name":"mergeBinBalance","type":"uint128"},{"name":"mergeId","type":"uint128"},{"name":"totalSupply","type":"uint128"},{"name":"kind","type":"uint8"},{"name":"lowerTick","type":"int32"}],"name":"bin","type":"tuple"}],"payable":False,"stateMutability":"view","type":"function"}]

    pool_info_contract = w3.eth.contract(address=pool_info_address, abi=pool_info_abi)
    pool_contract = w3.eth.contract(address=pool_address, abi=pool_abi)

    # Read block numbers from CSV
    with open('block_numbers.csv', mode='r') as infile:
        reader = csv.DictReader(infile)
        block_numbers = [row['BlockNumber'] for row in reader]

    # Fetch data and write to new CSV file
    with open('mav_reserves_daily.csv', mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['block_number', 'reserveA', 'reserveB', 'total_supply', 'price'])

        for block_number in block_numbers:
            activeBins = pool_info_contract.functions.getActiveBins(pool_address, 0, 100).call(block_identifier=int(block_number))
            # Filter bins with kind == 3 and mergeId == 0
            filtered_bins = [bin for bin in activeBins if bin[1] == 3 and bin[5] == 0]

            if len(filtered_bins) > 1:
                print(f"Warning: More than one bin found for block number {block_number}. Bin IDs: {[bin[0] for bin in filtered_bins]}")

            bin_id = 12 # hard-coded 12 here as bin 12 is the mode-both bin that others merge into
            bin_state = pool_contract.functions.getBin(bin_id).call(block_identifier=int(block_number))
            sqrtPrice = pool_info_contract.functions.getSqrtPrice(pool_address).call(block_identifier=int(block_number))

            # Write data to CSV
            writer.writerow([block_number, bin_state[0], bin_state[1], bin_state[4], (sqrtPrice/1e18)**2])  # reserveA, reserveB, totalSupply

    print("Data extraction complete.")


if __name__ == '__main__':
    main()


