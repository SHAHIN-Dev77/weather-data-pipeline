import os 
from datetime import datetime
import logging

# Configure logging to write to api.log
os.makedirs("logs", exist_ok=True) 
logging.basicConfig(
    filename='logs/api.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'  # Recommended for modern Python versions
)



def create_folders():
    folders = [
        "data",
        "data/bronze",
        "data/silver",
        "data/gold",
        "data/archive",
        "logs",
        "config",
        "src",
        "database"
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        logging.info(f"[OK] Folder ready: {folder}")
def show_structure():
    for root, dirs, files in os.walk("."):
        logging.info(root)
        for d in dirs:
            logging.info(f"  ┗ {d}/")
def main():
    logging.info("Starting project setup...")
    logging.info(f"Time: {datetime.now()}")
    create_folders()
    logging.info("\nProject structure:")
    show_structure()
    logging.info("\nSetup completed successfully.")
if __name__ == "__main__":
    main()