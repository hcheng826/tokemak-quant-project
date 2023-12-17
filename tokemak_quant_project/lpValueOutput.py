import csv
import matplotlib.pyplot as plt

def read_and_normalize(file_name, block_number_col, value_col, last_days):
    with open(file_name, mode='r') as infile:
        reader = csv.DictReader(infile)
        data = [(int(row[block_number_col]), float(row[value_col])) for row in reader]

    first_value = data[-last_days][1]
    normalized_data = [(i + 1, block_number, value / first_value) for i, (block_number, value) in enumerate(data[-last_days:])]
    return normalized_data

# Read and normalize data
last_days = 30
curve_data = read_and_normalize('curve_lp_value.csv', 'blockNumber', 'all_ETH_per_lp', last_days)
mav_data = read_and_normalize('mav_lp_value.csv', 'block_number', 'all_ETH_per_lp', last_days)

# Write normalized data to CSV files
def write_normalized_data(file_name, curve_data, mav_data):
    with open(file_name, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['id', 'block_number', 'curve_normalized_ETH_per_lp', 'mav_normalized_ETH_per_lp'])

        for (curve_id, curve_block, curve_value), (_, mav_block, mav_value) in zip(curve_data, mav_data):
            writer.writerow([curve_id, curve_block, curve_value, mav_value])

write_normalized_data(f'normalized_lp_values_last_{last_days}_days.csv', curve_data, mav_data)

# Plot trend charts
def plot_trend_chart(curve_data, mav_data, title):
    ids = [row[0] for row in curve_data]
    curve_values = [row[2] for row in curve_data]
    mav_values = [row[2] for row in mav_data]

    plt.figure(figsize=(10, 6))
    plt.plot(ids, curve_values, label='Curve Normalized ETH per LP')
    plt.plot(ids, mav_values, label='Mav Normalized ETH per LP')
    plt.xlabel('Day')
    plt.ylabel('Normalized Value')
    plt.title(title)
    plt.legend()
    plt.show()

plot_trend_chart(curve_data, mav_data, f'Normalized ETH per LP - Last {last_days} Days')

