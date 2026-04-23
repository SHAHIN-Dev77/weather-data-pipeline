import pandas as pd
import os
from datetime import datetime
import logging

os.makedirs("logs", exist_ok=True) 
logging.basicConfig(
    filename='logs/api.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'  # Recommended for modern Python versions
)

def csv_to_parquet():
    # Read the CSV file into a DataFrame
    silver_folder = 'data/silver'
    gold_folder = 'data/gold'
    os.makedirs(gold_folder, exist_ok=True)    
    csv_file=[f for f in os.listdir(silver_folder) 
              if f.endswith('.csv') 
              ]
    if not csv_file:
        logging.info("No CSV files found in the silver folder.")
        return
    for file in csv_file:
        csv_path=os.path.join(silver_folder, file)
        base_name=file.replace('.csv', '')
        parquet_name=base_name+'.parquet'
        parquet_path=os.path.join(gold_folder, parquet_name)
        df = pd.read_csv(csv_path)
        # Convert the DataFrame to Parquet format
        df.to_parquet(parquet_path, index=False)
        logging.info(f"Converted to parquet {parquet_path} successfully.")
def main():
    logging.info("Starting CSV to Parquet conversion...")
    csv_to_parquet()
    logging.info("CSV to Parquet conversion completed.")

if __name__ == "__main__":
    main()