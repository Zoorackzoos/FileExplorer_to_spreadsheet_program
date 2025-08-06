import os
import csv
from datetime import datetime

# List of common video file extensions
VIDEO_EXTENSIONS = {
    ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".mpeg", ".mpg"
}


def scan_videos(root_dir, output_csv="video_index.csv"):  # Main function
    """
    Walks through root_dir and its subfolders to find video files and write their metadata to a CSV.

    Columns:
    - Title: file name without extension
    - Download Date: file creation time (formatted)
    - Path: full file path
    """
    rows = []  # List to hold info for each video file

    # Walk through all directories and subdirectories
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for fname in filenames:
            _, ext = os.path.splitext(fname)  # Get file extension
            if ext.lower() in VIDEO_EXTENSIONS:
                full_path = os.path.join(dirpath, fname)  # Absolute path to file

                # Try to get creation time, fallback to modified time
                try:
                    ctime = os.path.getctime(full_path)
                except Exception:                       #dunno under what circumstances this occurs but whatever :-/
                    ctime = os.path.getmtime(full_path) #this is getting the modification time.

                #shwanky ass "make dateTime object out of a time-stamp" method usage.
                download_dt = datetime.fromtimestamp(ctime).strftime("%Y-%m-%d %H:%M:%S")

                #splitText's usage here is scary
                title = os.path.splitext(fname)[0]  # Filename without extension

                # Store row info
                rows.append({
                    "Title": title,
                    "Download Date": download_dt,
                    "Path": full_path
                })

    # If the output CSV already exists, delete it
    if os.path.exists(output_csv):
        os.remove(output_csv)

    # Write video data to the CSV
    with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Title", "Download Date", "Path"]

        #csv has it's own writer i guess.
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader() #this writes the title of the csv file as the 1st row
        writer.writerows(rows) #this fills in the rows with video data. the feilds are above them, written automatically i guess

    print(f"Indexed {len(rows)} videos. Output saved to {output_csv}")


if __name__ == "__main__":
    # Instead of using argparse, we use hardcoded paths for simplicity

    # 🔧 Paste your local directory path below (raw string to handle backslashes)
    directory_path = r"E:\0 - Personal\Film"

    # 🔧 Change the output filename as desired
    output_csv = r"C:\Users\User\Desktop\spreadsheets\video_spreadsheet.csv"

    # Run the scan
    scan_videos(directory_path, output_csv)

    """
    #just in case you want regular people to use this. 
    import argparse

    parser = argparse.ArgumentParser(
        description="Scan your filesystem for video files and output their metadata to a CSV."
    )
    parser.add_argument(
        "root",
        help="Root directory to start scanning (e.g., C:/Users/You/Videos)"
    )
    parser.add_argument(
        "--output", "-o",
        default="video_index.csv",
        help="Path to output CSV file"
    )

    args = parser.parse_args()
    scan_videos(args.root, args.output)
    """