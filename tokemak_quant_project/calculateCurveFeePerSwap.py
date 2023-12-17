import os
import csv

# https://github.com/ethers-io/ethers.js/blob/master/packages/providers/src.ts/alchemy-provider.ts#L16-L21
# NOTE: likely to get rate limited
default_provider_url = "https://eth-mainnet.g.alchemy.com/v2/_gg7wSSi0KMBsdKnGVfHDueq6xMB9EkC"

def main():
    # Read data from the input CSV file
    input_filename = 'curve_token_exchange_logs.csv'
    output_filename = 'curve_fee_for_each_swap.csv'

    with open(input_filename, mode='r') as infile, open(output_filename, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)

        # Write headers for the output CSV file
        writer.writerow(['blockNumber', 'fee_in_ETH', 'fee_in_stETH'])

        fee_rate = 0.0001

        # Process each row in the input CSV file
        for row in reader:
            blockNumber = row['blockNumber']
            sold_id = int(row['sold_id'])
            tokens_bought = float(row['tokens_bought'])

            # Calculate fees
            if sold_id == 0:
                fee_in_ETH = 0
                fee_in_WETH = tokens_bought / 1e18 / (1 - fee_rate) * fee_rate
            else: # sold_id == 1
                fee_in_ETH = tokens_bought / 1e18 / (1 - fee_rate) * fee_rate
                fee_in_WETH = 0

            # Write the calculated values to the output CSV file
            writer.writerow([blockNumber, fee_in_ETH, fee_in_WETH])

    print("Data processing complete. Output written to", output_filename)




if __name__ == '__main__':
    main()


