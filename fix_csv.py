import csv

# Input and output file paths
input_file = 'blockbasedholders_drop7.csv'  # Replace with your actual input file name
output_file = 'Holders7.csv'

# Open the input file and extract Ethereum addresses
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        # Write the first column (Ethereum address) followed by ,1 to the output file
        writer.writerow([row[0], '1'])

print(f"Ethereum addresses with additional info have been extracted to {output_file}.")
