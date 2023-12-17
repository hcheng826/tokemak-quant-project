import os
from dotenv import load_dotenv
from web3 import Web3
import json
import csv

# https://github.com/ethers-io/ethers.js/blob/master/packages/providers/src.ts/alchemy-provider.ts#L16-L21
# NOTE: likely to get rate limited
default_provider_url = "https://eth-mainnet.g.alchemy.com/v2/_gg7wSSi0KMBsdKnGVfHDueq6xMB9EkC"
start_block = 18145020
end_block = 18787804

def main():
    load_dotenv()
    w3 = Web3(Web3.HTTPProvider(os.getenv('PROVIDER_URL', default_provider_url)))
    # Check if the connection is successful
    if not w3.isConnected():
        print("Failed to connect to Ethereum node.")
        exit()

    # Contract Information
    pool_address = Web3.toChecksumAddress('0xDC24316b9AE028F1497c275EB9192a3Ea0f67022')
    pool_abi = [{
        "name": "balances",
        "outputs": [{"type": "uint256", "name": ""}],
        "inputs": [{"type": "uint256", "name": "i"}],
        "stateMutability": "view",
        "type": "function",
        "gas": 5076
    }]

    lp_token_address = Web3.toChecksumAddress('0x06325440D014e39736583c165C2963BA99fAf14E')
    lp_token_abi = [{"name":"totalSupply","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":1481}]

    # Create contract instances
    pool_contract = w3.eth.contract(address=pool_address, abi=pool_abi)
    lp_token_contract = w3.eth.contract(address=lp_token_address, abi=lp_token_abi)

    # Read block numbers from CSV
    with open('block_numbers.csv', mode='r') as infile:
        reader = csv.DictReader(infile)
        block_numbers = [row['BlockNumber'] for row in reader]

    # Fetch data and write to new CSV file
    with open('curve_reserves_daily.csv', mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['id', 'blockNumber', 'balance_0', 'balance_1', 'total_supply'])

        for idx, block_number in enumerate(block_numbers, 1):
            balance_0 = pool_contract.functions.balances(0).call(block_identifier=int(block_number))
            balance_1 = pool_contract.functions.balances(1).call(block_identifier=int(block_number))
            total_supply = lp_token_contract.functions.totalSupply().call(block_identifier=int(block_number))

            writer.writerow([idx, block_number, balance_0, balance_1, total_supply])  # Replace 'date_placeholder' with actual date if needed

    print("Data extraction complete.")


if __name__ == '__main__':
    main()


