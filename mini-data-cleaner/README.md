# 🧹 Mini Data Cleaner

This is a simple beginner-friendly Data Engineering project written in Python.  
It reads raw data from a CSV, cleans it by removing nulls and normalizing column names, and saves the cleaned file.

---

## 📂 Project Structure

mini-data-cleaner/
├── sample.csv # Original unclean CSV
├── cleaned_data/ # Output cleaned CSV
├── logs/ # Execution logs
├── cleaner.py # Main script
├── README.md # Project documentation

---

## 🧠 What This Project Does

- Reads unformated and uncleaned CSV data
- Cleans column names (lowercase, no spaces)
- Drops rows with null values
- Saves clean version to `cleaned_data/`
- Logs process steps in `logs/`

---

## 🚀 How to Run

python cleaner.py


"Made with 💛 by Barla Aravind" 