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


def find_secondary_files(main_file_path):
    """
    Find all secondary files that correspond to a main file.
    Secondary files have the pattern: filename (number).csv
    
    Args:
        main_file_path (str): Path to the main CSV file
        
    Returns:
        list: List of paths to secondary files
    """
    main_file = Path(main_file_path)
    base_name = main_file.stem  # filename without extension
    directory = main_file.parent
    
    # Pattern to match files like "filename (1).csv", "filename (2).csv", etc.
    pattern = f"{re.escape(base_name)} \\(\\d+\\).csv"
    
    secondary_files = []
    for file_path in directory.glob("*.csv"):
        if re.match(pattern, file_path.name):
            secondary_files.append(str(file_path))
    
    return sorted(secondary_files)


def merge_csv_files(main_file, secondary_files):
    """
    Merge multiple CSV files into one DataFrame.
    
    Args:
        main_file (str): Path to the main CSV file
        secondary_files (list): List of paths to secondary CSV files
        
    Returns:
        pandas.DataFrame: Merged DataFrame
    """
    dfs = []
    
    try:
        # Read main file
        main_df = pd.read_csv(main_file)
        dfs.append(main_df)
        print(f"  Main file: {os.path.basename(main_file)} ({len(main_df)} rows)")
        
        # Read secondary files
        for secondary_file in secondary_files:
            try:
                secondary_df = pd.read_csv(secondary_file)
                dfs.append(secondary_df)
                print(f"  Secondary file: {os.path.basename(secondary_file)} ({len(secondary_df)} rows)")
            except Exception as e:
                print(f"  Error reading {secondary_file}: {e}")
                continue
        
        # Merge all DataFrames
        if dfs:
            merged_df = pd.concat(dfs, ignore_index=True)
            return merged_df
        else:
            return None
            
    except Exception as e:
        print(f"  Error reading main file {main_file}: {e}")
        return None


def clean_secondary_files(secondary_files):
    """
    Delete secondary files after successful merge.
    
    Args:
        secondary_files (list): List of paths to secondary CSV files to delete
    """
    for file_path in secondary_files:
        try:
            os.remove(file_path)
            print(f"  Deleted: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"  Error deleting {file_path}: {e}")


def process_folder(folder_path, sort_column):
    """
    Process all CSV files in a folder, merging secondary files with main files.
    
    Args:
        folder_path (str): Path to the folder containing CSV files
    """
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return
    
    # Process all the csv files
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))    
    processed_count = 0
    merged_count = 0
    
    for csv_file in csv_files:
        filename = os.path.basename(csv_file)
        # Skip files that match the secondary pattern (filename (number).csv)
        if re.search(r' \(\d+\)\.csv$', filename):
            continue    
    
        print(f"\nProcessing: {os.path.basename(csv_file)}")
        
        # Find secondary files
        secondary_files = find_secondary_files(csv_file)
        
        if not secondary_files:
            print("  No secondary files found.")
            processed_count += 1
            continue
        
        print(f"  Found {len(secondary_files)} secondary files")
        
        # Merge files
        merged_df = merge_csv_files(csv_file, secondary_files)
        
        if merged_df is not None:
            try:
                # Save merged file (overwrite main file)
                merged_df = merged_df.sort_values(by=sort_column).reset_index(drop=True)
                merged_df.to_csv(csv_file, index=False)
                print(f"  Merged file saved: {os.path.basename(csv_file)} ({len(merged_df)} total rows)")
                
                # Delete secondary files
                clean_secondary_files(secondary_files)
                
                merged_count += 1
                
            except Exception as e:
                print(f"  Error saving merged file: {e}")
        
        processed_count += 1
    
    print("\n=== Summary ===")
    print(f"Total files processed: {processed_count}")
    print(f"Files merged: {merged_count}")


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
        '--sort_column',
        type=str,
        help='Name of the sort column to keep the order',
        required=True
    )
    print("Parsing arguments...")
    args = parser.parse_args()
    print("Arguments parsed successfully.")
    
    # Get processing folder path and convert to absolute path
    folder_path = args.working_dir.strip()
    sort_column = args.sort_column.strip()
    
    # Clean potential problematic characters from path
    folder_path = folder_path.strip('\'"')  # Remove quotes
    folder_path = folder_path.rstrip('\\/')  # Remove trailing slashes
    
    # Convert relative path to absolute path
    folder_path = os.path.abspath(folder_path)
    
    print(f"\nProcessing folder: {folder_path}")
    
    process_folder(folder_path, sort_column)


if __name__ == "__main__":
    main()
