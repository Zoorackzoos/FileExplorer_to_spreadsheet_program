import os
import csv
from datetime import datetime
import xml.etree.ElementTree as ET

# 🔧 Set this to your RimWorld Mods folder
MODS_FOLDER = r"D:\SteamLibrary\steamapps\common\RimWorld\Mods"

OUTPUT_CSV = r"C:\Users\User\Desktop\spreadsheets\rimworld_mods.csv"

# Possible RimWorld versions from 1.0 to 1.6
RIMWORLD_VERSIONS = {f"1.{i}" for i in range(0, 7)}  # {'1.0', '1.1', ... '1.6'}


def get_mod_info(mod_path):
    """Extracts mod info from folder."""
    folder_name = os.path.basename(mod_path)

    mod_info = {
        "Name": folder_name,  # Will try to replace with About.xml value
        "Folder Name": folder_name,  # Exact folder name from Mods directory
        "Download Date": "",
        "Supported Versions": [],
        "Workshop URL": ""
    }

    # Get date
    try:
        ctime = os.path.getctime(mod_path)
    except Exception:
        ctime = os.path.getmtime(mod_path)
    mod_info["Download Date"] = datetime.fromtimestamp(ctime).strftime("%Y-%m-%d %H:%M:%S")

    # Detect supported versions by folder names
    for version in RIMWORLD_VERSIONS:
        if os.path.isdir(os.path.join(mod_path, version)):
            mod_info["Supported Versions"].append(version)

    # Try to read About.xml
    about_path = os.path.join(mod_path, "About", "About.xml")
    if os.path.exists(about_path):
        try:
            tree = ET.parse(about_path)
            root = tree.getroot()

            name_tag = root.find("name")
            if name_tag is not None and name_tag.text:
                mod_info["Name"] = name_tag.text.strip()

            # Try to get Steam Workshop URL from XML
            url_tag = root.find("url")
            if url_tag is not None and url_tag.text and "steamcommunity" in url_tag.text:
                mod_info["Workshop URL"] = url_tag.text.strip()

        except Exception as e:
            print(f"Error reading {about_path}: {e}")

    # If folder name is numeric → assume it's a Workshop ID
    if mod_info["Workshop URL"] == "" and folder_name.isdigit():
        mod_id = folder_name
        mod_info["Workshop URL"] = f"https://steamcommunity.com/sharedfiles/filedetails/?id={mod_id}"

    # Convert versions to a comma-separated string
    mod_info["Supported Versions"] = ", ".join(sorted(mod_info["Supported Versions"]))
    return mod_info


def scan_mods():
    mods = []
    for folder in os.listdir(MODS_FOLDER):
        mod_path = os.path.join(MODS_FOLDER, folder)
        if os.path.isdir(mod_path):
            mods.append(get_mod_info(mod_path))
    return mods


if __name__ == "__main__":
    mod_list = scan_mods()

    # Save to CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["Name", "Folder Name", "Download Date", "Supported Versions", "Workshop URL"]
        )
        writer.writeheader()
        writer.writerows(mod_list)

    print(f"Saved {len(mod_list)} mods to {OUTPUT_CSV}")
