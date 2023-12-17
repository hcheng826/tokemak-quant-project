import csv

# Read data from the curve_fee_for_each_swap.csv file
curve_fee_filename = 'curve_fee_for_each_swap.csv'
block_numbers_filename = 'block_numbers.csv'
curve_reserves_daily_filename = 'curve_reserves_daily.csv'

# Load block number to date mapping from block_numbers.csv
block_to_date = {}
block_ranges = []
with open(block_numbers_filename, mode='r') as infile:
    reader = csv.DictReader(infile)
    prev_block_number = None
    for row in reader:
        block_number = int(row['BlockNumber'])
        block_to_date[block_number] = (row['id'], row['date'])
        if prev_block_number is not None:
            block_ranges.append((prev_block_number, block_number))
        prev_block_number = block_number

# Load daily reserves to calculate stETH to ETH conversion rate
daily_conversion_rate = {}
with open(curve_reserves_daily_filename, mode='r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        balance_0 = float(row['balance_0'])
        balance_1 = float(row['balance_1'])
        block_number = int(row['blockNumber'])
        daily_conversion_rate[block_number] = balance_0 / balance_1 if balance_1 != 0 else 0

# Aggregate fees by day
daily_fees = {date: {'id': id, 'block_number': end_block, 'sum_fee_ETH': 0, 'sum_fee_stETH': 0, 'sum_fee_convert_ETH': 0}
              for end_block, (id, date) in block_to_date.items()}

with open(curve_fee_filename, mode='r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        block_number = int(row['blockNumber'])
        fee_in_ETH = float(row['fee_in_ETH'])
        fee_in_stETH = float(row['fee_in_stETH'])

        # Find the corresponding date range for the block number
        for start_block, end_block in block_ranges:
            if start_block <= block_number < end_block:
                _, date = block_to_date[end_block]
                conversion_rate = daily_conversion_rate.get(end_block, 0)
                daily_fees[date]['sum_fee_ETH'] += fee_in_ETH
                daily_fees[date]['sum_fee_stETH'] += fee_in_stETH
                daily_fees[date]['sum_fee_convert_ETH'] += fee_in_ETH + (fee_in_stETH * conversion_rate)
                break

# Write aggregated data to new CSV file
output_filename = 'aggregated_curve_fees_daily.csv'
with open(output_filename, mode='w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['id', 'date', 'block_number', 'sum_fee_ETH', 'sum_fee_stETH', 'sum_fee_convert_ETH'])

    for date in sorted(daily_fees.keys()):
        data = daily_fees[date]
        writer.writerow([data['id'], date, data['block_number'], data['sum_fee_ETH'], data['sum_fee_stETH'], data['sum_fee_convert_ETH']])

print("Data aggregation complete. Output written to", output_filename)
