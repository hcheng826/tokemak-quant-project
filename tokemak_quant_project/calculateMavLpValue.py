import csv

# Read data from the input CSV file
input_filename = 'mav_reserves_daily.csv'
output_filename = 'mav_lp_value.csv'
def main():
    with open(input_filename, mode='r') as infile, open(output_filename, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)

        # Write headers for the output CSV file
        writer.writerow(['block_number', 'WETH_per_lp', 'swETH_per_lp', 'all_ETH_per_lp'])

        # Process each row in the input CSV file
        for row in reader:
            blockNumber = row['block_number']
            reserveA = float(row['reserveA'])
            reserveB = float(row['reserveB'])
            total_supply = float(row['total_supply'])
            price = float(row['price'])

            # Calculating the values
            WETH_per_lp = reserveA / total_supply
            swETH_per_lp = reserveB / total_supply
            all_ETH_per_lp = WETH_per_lp + swETH_per_lp * price

            # Write the calculated values to the output CSV file
            writer.writerow([blockNumber, WETH_per_lp, swETH_per_lp, all_ETH_per_lp])

    print("Data processing complete. Output written to", output_filename)

if __name__ == '__main__':
    main()
