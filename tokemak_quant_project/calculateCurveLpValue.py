import csv

# Read data from the input CSV file
input_filename = 'curve_reserves_daily.csv'
output_filename = 'curve_lp_value.csv'
def main():
    with open(input_filename, mode='r') as infile, open(output_filename, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)

        # Write headers for the output CSV file
        writer.writerow(['id', 'blockNumber', 'ETH_per_lp', 'stETH_per_lp', 'all_ETH_per_lp'])

        # Process each row in the input CSV file
        for row in reader:
            id = row['id']
            blockNumber = row['blockNumber']
            balance_0 = float(row['balance_0'])
            balance_1 = float(row['balance_1'])
            total_supply = float(row['total_supply'])

            # Calculating the values
            ETH_per_lp = balance_0 / total_supply
            stETH_per_lp = balance_1 / total_supply
            all_ETH_per_lp = ETH_per_lp + stETH_per_lp * (balance_0 / balance_1)

            # Write the calculated values to the output CSV file
            writer.writerow([id, blockNumber, ETH_per_lp, stETH_per_lp, all_ETH_per_lp])

    print("Data processing complete. Output written to", output_filename)

if __name__ == '__main__':
    main()
