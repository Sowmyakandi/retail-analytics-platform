from pathlib import Path

RAW_DATA_PATH = Path("data/raw")

RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)

print("Retail Analytics Project Started")
print(f"Raw data folder: {RAW_DATA_PATH.resolve()}")