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

    # Smart contract address and ABI (replace with your contract details)
    contract_address = '0xDC24316b9AE028F1497c275EB9192a3Ea0f67022'
    contract_abi = '[{"name":"TokenExchange","inputs":[{"type":"address","name":"buyer","indexed":true},{"type":"int128","name":"sold_id","indexed":false},{"type":"uint256","name":"tokens_sold","indexed":false},{"type":"int128","name":"bought_id","indexed":false},{"type":"uint256","name":"tokens_bought","indexed":false}],"anonymous":false,"type":"event"}]'

    # Create contract instance
    contract = w3.eth.contract(address=contract_address, abi=json.loads(contract_abi))

    # Event filter (replace 'YourEventName' with the actual event name you are interested in)
    logs = contract.events.TokenExchange().getLogs(fromBlock=start_block, toBlock=end_block)
    # event_filter = contract.events.TokenExchange().createFilter(fromBlock='latest')

    # Writing data to CSV
    filename = f'curve_token_exchange_logs_{start_block}_to_{end_block}.csv'

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Writing headers
        writer.writerow(['buyer', 'sold_id', 'tokens_sold', 'bought_id', 'tokens_bought', 'event', 'logIndex', 'transactionIndex', 'transactionHash', 'address', 'blockHash', 'blockNumber'])

        for log in logs:
            writer.writerow([
                log.args.buyer,
                log.args.sold_id,
                log.args.tokens_sold,
                log.args.bought_id,
                log.args.tokens_bought,
                log.event,
                log.logIndex,
                log.transactionIndex,
                log.transactionHash.hex(),
                log.address,
                log.blockHash.hex(),
                log.blockNumber
            ])

    print("Logs have been written to csv")

if __name__ == '__main__':
    main()
