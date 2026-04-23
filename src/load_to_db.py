import pandas as pd
import os
from sqlalchemy import create_engine, text
import logging

# Configure logging to write to api.log
os.makedirs("logs", exist_ok=True) 
logging.basicConfig(
    filename='logs/api.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'  # Recommended for modern Python versions
)
silver_folder = 'data/silver'
DB_URL="postgresql://postgres:shahin2013@localhost:5432/weather_db"

def get_latest_silver_file():
    csv_paths = [
        f for f in os.listdir(silver_folder) 
        if f.endswith('.csv')
        ]
    if not csv_paths:
        logging.info("No CSV files found in the silver folder.")
        return None
    csv_paths.sort()
    latest_file=csv_paths[-1]
    return os.path.join(silver_folder, latest_file)

def get_engine():
    return create_engine(DB_URL)

def create_table(engine):
    create_sql="""
CREATE TABLE IF NOT EXISTS weather_data (
       timestamp TIMESTAMP,
        temp FLOAT,
        soil_temp FLOAT,
        city TEXT
    )"""
    with engine.connect() as conn:
        conn.execute(text(create_sql))
        conn.commit()
def load_data_to_db(engine, csv_path):
    logging.info(f"Loading data from {csv_path} to database...")
    df = pd.read_csv(csv_path)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.to_sql('weather_data', con=engine, if_exists='append', index=False)
    logging.info("Data loaded to database successfully.")

def quick_check(engine):
    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM weather_data")).scalar()
        logging.info(f"Total records in weather_data table: {count}")
        result=conn.execute(text("""
            SELECT TO_CHAR(timestamp, 'YYYY-MM-DD HH24:MI:SS'), temp, city 
            FROM weather_data
            order by timestamp DESC 
            LIMIT 5"""))
        logging.info("Latest 5 records:")
        for row in result:  
            logging.info(row)
def main():
    logging.info("Starting data load to database...")
    engine = get_engine()
    try:
        create_table(engine)
        latest_csv = get_latest_silver_file()
        if latest_csv:
            load_data_to_db(engine, latest_csv)
            quick_check(engine)
        else:
            logging.info("No CSV file to load.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        engine.dispose()
    logging.info("Data load to database completed.")

if __name__ == "__main__":
    main()           

