import pandas as pd
import os
from datetime import datetime
from logger import get_logger
from config_loader import load_config
logger = get_logger(__name__)
config = load_config()
paths_cfg = config["paths"]

def csv_to_parquet():
    # Read the CSV file into a DataFrame
    silver_folder = paths_cfg["silver_dir"]
    gold_folder = paths_cfg["gold_dir"]
    os.makedirs(gold_folder, exist_ok=True)    
    csv_file=[f for f in os.listdir(silver_folder) 
              if f.endswith('.csv') 
              ]
    if not csv_file:
        logger.info("No CSV files found in the silver folder.")
        return
    for file in csv_file:
        csv_path=os.path.join(silver_folder, file)
        base_name=file.replace('.csv', '')
        parquet_name=base_name+'.parquet'
        parquet_path=os.path.join(gold_folder, parquet_name)
        df = pd.read_csv(csv_path)
        # Convert the DataFrame to Parquet format
        df.to_parquet(parquet_path, index=False)
        logger.info(f"Converted to parquet {parquet_path} successfully.")
def main():
    logger.info("Starting CSV to Parquet conversion...")
    csv_to_parquet()
    logger.info("CSV to Parquet conversion completed.")

if __name__ == "__main__":
    main()