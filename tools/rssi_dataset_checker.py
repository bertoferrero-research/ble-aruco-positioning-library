#!/usr/bin/env python3
"""
RSSI Sample Cleaner Script

This script reads all the csv files in the processing folder.
It reads all nonspace files, for each one checks if there is secondary files with a number on its name 
(e.g. 1.5_28.5_1.5__all.csv -> 1.5_28.5_1.5__all (1).csv)
If there are secondary files, it merges them into the main file and deletes the secondary files.
It saves the merged file in the same folder.
"""

import os
import pandas as pd
import glob
import re
from pathlib import Path
import argparse
import common_tools



def process_folder(folder_path:str, mac_filter_file:str, room_settings_file:str):
    
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return
    if not os.path.exists(mac_filter_file):
        print(f"Error: Folder '{mac_filter_file}' does not exist.")
        return
    if not os.path.exists(room_settings_file):
        print(f"Error: Folder '{room_settings_file}' does not exist.")
        return

    # Load the settings
    mac_list = common_tools.load_mac_filter_file(mac_filter_file)
    room_settings = common_tools.load_room_settings(room_settings_file)

    #Extract grid settings
    grid_settings = room_settings.get('offline_grid', {})
    x_min = float(grid_settings.get('x_min'))
    x_max = float(grid_settings.get('x_max'))
    y_min = float(grid_settings.get('y_min'))
    y_max = float(grid_settings.get('y_max'))
    z = float(grid_settings.get('z'))
    resolution = float(grid_settings.get('resolution'))

    # We include the key "all" to the mac list in order to check its existence
    mac_list.append('all')

    print("Phase 1: Checking existence of expected fingerprint files...")
    not_existing_files = []
    x = x_min
    while x <= x_max:
        y = y_min
        while y <= y_max:
            for mac in mac_list:
                fingerprint_filepath = common_tools.compose_fingerprint_filepath(folder_path, x, y, z, mac)
                #print(f"Checking existence of file: {fingerprint_filepath}")
                if not os.path.exists(fingerprint_filepath):
                    not_existing_files.append(fingerprint_filepath)
            y += resolution
        x += resolution

    if not_existing_files:
        print("Warning!!!: The following fingerprint files do not exist:")
        for filepath in not_existing_files:
            print(f" - {filepath}")
        return
    
    print("Phase 2: Checking the fingerprints sum rows in 'all'...")
    position_errors = []
    x = x_min
    while x <= x_max:
        y = y_min
        while y <= y_max:
            rows_sum = 0
            rows_in_all = 0
            for mac in mac_list:
                # Get the fingerprint rows
                fingerprint_filepath = common_tools.compose_fingerprint_filepath(folder_path, x, y, z, mac)
                rows = common_tools.count_rows_in_csv(fingerprint_filepath)
                if mac == "all":
                    rows_in_all = rows
                else:
                    rows_sum += rows
            # Compare the rows
            if rows_sum != rows_in_all:
                position_errors.append((x, y, z, rows_sum, rows_in_all))
            y += resolution
        x += resolution

    if position_errors:
        print("Warning!!!: The following positions have mismatched row counts:")
        for error in position_errors:
            print(f" - Position (X: {error[0]}, Y: {error[1]}, Z: {error[2]}): "
                  f"Sum = {error[3]}, All = {error[4]}")

    print("Finish. If not error has been printed, everything is OK.")

def main():
    """
    Main function to run the RSSI sample cleaner.
    """
    print("RSSI Sample Cleaner")
    print("===================")
    # Load arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--working_dir',
        type=str,
        help='Path the directory where the splited csv are stored',
        required=True
    )
    parser.add_argument(
        '--mac_filter_file',
        type=str,
        help='Path to the MAC filter file (json file with a list of allowed MAC addresses)',
        required=True
    )
    parser.add_argument(
        '--room_settings_file',
        type=str,
        help='Path to the room settings file (json file with room configuration)',
        required=True
    )
    print("Parsing arguments...")
    args = parser.parse_args()
    print("Arguments parsed successfully.")
    
    # Get processing folder path and convert to absolute path
    folder_path = common_tools.clean_path(args.working_dir.strip())
    mac_filter_file = common_tools.clean_path(args.mac_filter_file.strip())
    room_settings_file = common_tools.clean_path(args.room_settings_file.strip())

    process_folder(folder_path, mac_filter_file, room_settings_file)


if __name__ == "__main__":
    main()
