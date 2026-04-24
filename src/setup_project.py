import os 
from datetime import datetime
from src.logger import get_logger
logger = get_logger(__name__)       



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
        logger.info(f"[OK] Folder ready: {folder}")
def show_structure():
    for root, dirs, files in os.walk("."):
        logger.info(root)
        for d in dirs:
            logger.info(f"  ┗ {d}/")
def main():
    logger.info("Starting project setup...")
    logger.info(f"Time: {datetime.now()}")
    create_folders()
    logger.info("\nProject structure:")
    show_structure()
    logger.info("\nSetup completed successfully.")
if __name__ == "__main__":
    main()