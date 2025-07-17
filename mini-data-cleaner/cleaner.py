# Import required libraries
import pandas as pd
import os
import logging
from datetime import datetime

# Create the logs folder if not present
if not os.path.exists('logs'):
    os.makedirs('logs')

#  Setup the Logging
logging.basicConfig(
    filename=f"logs/run_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Below is Data Cleaning Function
def clean_data(input_file, output_file):
    try:
        logging.info(f"Reading file: {input_file}")
        df = pd.read_csv(input_file)

        logging.info("Cleaning data...")

        # Normalize the column names
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        # Drop rows with null values
        df = df.dropna()

        # Save the cleaned data
        df.to_csv(output_file, index=False)
        logging.info(f"Saved cleaned data to: {output_file}")
        logging.info("Cleaning complete.")
    except Exception as e:
        logging.error(f"Error occurred: {e}")

# Run the function
if __name__ == "__main__":
    raw_data_path = "/Users/aravind.barla/Desktop/Python  Linkdn Projects/mini-data-cleaner/sample.csv"
    cleaned_data_path = "cleaned_data/cleaned_sample.csv"

    # Create output folder if needed
    if not os.path.exists("cleaned_data"):
        os.makedirs("cleaned_data")

    # Run cleaning
    clean_data(raw_data_path, cleaned_data_path)
