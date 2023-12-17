import csv
import datetime
import requests

def get_block_data(unix_timestamp):
    response = requests.get(f"https://coins.llama.fi/block/ethereum/{unix_timestamp}")
    if response.status_code == 200:
        data = response.json()
        return data["height"], data["timestamp"]
    else:
        return None, None

def main():
    start_date = datetime.date(2023, 9, 16)
    unix_timestamp = 1694822400
    data_rows = []

    for i in range(90):
        current_date = start_date + datetime.timedelta(days=i)
        block_number, block_timestamp = get_block_data(unix_timestamp)

        data_rows.append([
            i + 1,
            current_date.strftime("%Y/%m/%d"),
            unix_timestamp,
            block_number,
            block_timestamp
        ])

        unix_timestamp += 86400  # Increment by a day

    with open('blocks.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'date', 'timestamp', 'BlockNumber', 'BlockTimestamp'])
        writer.writerows(data_rows)

    print("CSV file has been created.")

if __name__ == '__main__':
    main()
