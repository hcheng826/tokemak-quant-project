# read curve_token_exchange_logs.csv
# ```curve_token_exchange_logs.csv
# buyer,sold_id,tokens_sold,bought_id,tokens_bought,event,logIndex,transactionIndex,transactionHash,address,blockHash,blockNumber
# 0x3208684f96458c540Eb08F6F01b9e9afb2b7d4f0,0,51308024000000000000,1,51315656205529061810,TokenExchange,413,102,0xabcf69e95a81ad08f824f111be99ebdc0ea2c024951989c188590bedc5f10de2,0xDC24316b9AE028F1497c275EB9192a3Ea0f67022,0xd0d28c445aaf5928cb3c856053b9ef81a8517d1df2464835185b22c021a39d5a,18145154
# 0x99a58482BD75cbab83b27EC03CA68fF489b5788f,1,230000000000000000,0,229924563463650383,TokenExchange,143,40,0xdd24ede31aaff2b9232d3e2676bfcbe2f845297cd96a3b6794e11cb7e8ffe524,0xDC24316b9AE028F1497c275EB9192a3Ea0f67022,0x180f5ea85bdb8ca044b70a5d15b9dbb4485f624845af32a09ed55428ca80b2b8,18145206
# ...more
# ```

# ```block_numbers.csv
# id,date,timestamp,BlockNumber,BlockTimestamp
# 1,2023/09/16,1694822400,18145020,1694822411
# 2,2023/09/17,1694908800,18152100,1694908811
# 3,2023/09/18,1694995200,18159143,1694995211
# ...more
# ```
# use these 2 files to get daily volume
# output
# id,date,block_number, sum_volume_ETH

# aggregate by date (in between 2 blockNumbers of 2 days)
# if sold_id == 0,
# sum_volume_ETH += tokens_sold
# else sold_id == 1,
# sum_volume_ETH += tokens_bought / (1-0.0001)


import csv

# Function to read block numbers and map them to dates
def read_block_numbers(filename):
    block_to_date = {}
    with open(filename, mode='r') as infile:
        reader = csv.DictReader(infile)
        prev_row = None
        for row in reader:
            if prev_row:
                block_to_date[(int(prev_row['BlockNumber']), int(row['BlockNumber']))] = (prev_row['id'], prev_row['date'])
            prev_row = row
    return block_to_date

# Function to aggregate daily volume
def aggregate_daily_volume(token_logs_file, block_to_date):
    daily_volume = {}
    fee_rate = 0.0001

    with open(token_logs_file, mode='r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            block_number = int(row['blockNumber'])
            sold_id = int(row['sold_id'])
            tokens_sold = float(row['tokens_sold'])
            tokens_bought = float(row['tokens_bought'])

            # Find the date range that the block number falls into
            for (start_block, end_block), (id, date) in block_to_date.items():
                if start_block <= block_number < end_block:
                    if date not in daily_volume:
                        daily_volume[date] = {'id': id, 'block_number': end_block, 'sum_volume_ETH': 0}

                    if sold_id == 0:
                        daily_volume[date]['sum_volume_ETH'] += tokens_sold / 1e18
                    else:  # sold_id == 1
                        daily_volume[date]['sum_volume_ETH'] += tokens_bought / (1 - fee_rate) / 1e18
                    break

    return daily_volume

# Read block numbers and their corresponding dates
block_numbers_file = 'block_numbers.csv'
block_to_date = read_block_numbers(block_numbers_file)

# Aggregate daily volume
token_logs_file = 'curve_token_exchange_logs.csv'
daily_volume = aggregate_daily_volume(token_logs_file, block_to_date)

# Write aggregated data to new CSV file
output_filename = 'curve_daily_volume.csv'
with open(output_filename, mode='w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['id', 'date', 'block_number', 'sum_volume_ETH'])

    for date, data in sorted(daily_volume.items()):
        writer.writerow([data['id'], date, data['block_number'], data['sum_volume_ETH']])

print("Daily volume aggregation complete. Output written to", output_filename)

