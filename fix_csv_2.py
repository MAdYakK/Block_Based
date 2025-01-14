import csv

# Input file path
input_file = 'blockbasedholders_drop7.csv'  # Replace with your actual input file name

# Constants
output_prefix = 'Holders7_'  # Prefix for output files
max_entries_per_file = 225  # Maximum number of entries per file
special_address = '0xbca0B94f8F8c925A95af2C2C0248aA5f6581e005'
header = ['HolderAddress', 'edition']

# Read input file and process
with open(input_file, 'r') as infile:
    reader = csv.reader(infile)
    rows = [row[0] for row in reader]

# Adjust the count for the special address
adjusted_rows = []
for row in rows:
    if row == special_address:
        adjusted_rows.extend([[row, '5']])  # Add 5 editions
    else:
        adjusted_rows.append([row, '1'])  # Add 1 edition

# Write to multiple CSV files
file_index = 1
for i in range(0, len(adjusted_rows), max_entries_per_file):
    chunk = adjusted_rows[i:i + max_entries_per_file]
    output_file = f'{output_prefix}{file_index}.csv'
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)  # Write the header to each file
        writer.writerows(chunk)  # Write the rows
    print(f"Created {output_file} with {len(chunk)} entries.")
    file_index += 1

print("All entries have been processed into multiple CSV files.")
