import pandas as pd
import chardet
# chunk_size = 1405
# batch_no = 1

# for chunk in pd.read_csv('Enrollment.csv', chunksize=chunk_size):
#     chunk.to_csv('Enrollment' + str(batch_no) + '.csv', index = False)
#     batch_no += 1

import os

   
file_path = '/Users/ramzie/Downloads/gitprojects/python/Enrollment.csv'
# Function to find the encoding of the file
def find_encoding(file_path):
    with open(file_path, 'rb') as file:
        rawdata = file.read(50000)  # Read enough sample data to reliably guess the encoding
        result = chardet.detect(rawdata)
        return result['encoding']

def process_data_by_state(file_path, column_name='LEA_STATE'):
    # Detect the encoding of the CSV file
    encoding = find_encoding(file_path)
    print(f"Detected encoding: {encoding}")

    current_state = None
    buffer_df = pd.DataFrame()  # Buffer for holding data across chunks

    # Use the detected encoding to read the CSV file
    for chunk in pd.read_csv(file_path, chunksize=1405, encoding=encoding):
        if not buffer_df.empty:
            chunk = pd.concat([buffer_df, chunk])  # Add buffered data to the new chunk
            buffer_df = pd.DataFrame()  # Clear the buffer

        grouped = chunk.groupby(column_name)

        for state, data in grouped:
            if state == current_state:
                # Continue writing to the current state file
                with open(f'Enrollment_{state}.csv', 'a', encoding=encoding) as file:
                    data.to_csv(file, index=False, header=False)
            else:
                if current_state is not None:
                    # Buffer this new state data for the next chunk
                    buffer_df = pd.concat([buffer_df, data])
                else:
                    # Start a new state file
                    with open(f'Enrollment_{state}.csv', 'w', encoding=encoding) as file:
                        data.to_csv(file, index=False, header=True)
                    current_state = state

    # Handle any remaining data in the buffer
    if not buffer_df.empty:
        with open(f'Enrollment_{current_state}.csv', 'a', encoding=encoding) as file:
            buffer_df.to_csv(file, index=False, header=False)

process_data_by_state(file_path)