#!/usr/bin/env python3
"""
RSSI Sample Splitter

This script reads a CSV file containing RSSI samples with various MAC addresses.
It splits the samples into separate CSV files for each unique MAC address found in the data.
"""

import os
import pandas as pd
import glob
import re
from pathlib import Path
import argparse
import common_tools



def process_trajectory(csv_file:str, output_dir:str):
    
    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' does not exist.")
        return
    if not os.path.exists(output_dir):
        print(f"Error: Directory '{output_dir}' does not exist.")
        return

    # Cargamos el fichero a dividir
    df = pd.read_csv(csv_file)
    if 'mac_address' not in df.columns:
            print(f"  ⚠ Warning: No 'timestamp' column in {os.path.basename(csv_file)}")
            return

    # Obtenemos los distintos macs
    mac_list = df["mac_address"].unique()

    # Los recorremos y solicitamos las filas filtradas para cada uno, para guardarlas en un csv a parte
    for mac_address in mac_list:
        df_mac = df[df['mac_address'] == mac_address]               # Filtramos
        df_mac.sort_values(by='timestamp').reset_index(drop=True)   # Por si acaso reordenamos por timestamp
        #Guardamos
        mac_address = mac_address.replace(":","_")
        mac_csv_path = os.path.join(output_dir, f"{mac_address}.csv")
        df_mac.to_csv(mac_csv_path, index=False)

def main():
    """
    Main function to run the RSSI sample cleaner.
    """
    print("RSSI Sample Cleaner")
    print("===================")
    # Load arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--csv_file',
        type=str,
        help='Csv file with the trajectory samples to be splitted',
        required=True
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        help='Path the directory where the splited csvs must be stored. If it is not defined, the resultant csvs will be put in the same directory as the input csv file.',
        required=False
    )
    print("Parsing arguments...")
    args = parser.parse_args()
    print("Arguments parsed successfully.")
    
    # Get processing folder path and convert to absolute path
    csv_file = common_tools.clean_path(args.csv_file.strip())
    output_dir = common_tools.clean_path(args.output_dir.strip()) if args.output_dir else os.path.dirname(csv_file)

    process_trajectory(csv_file, output_dir)


if __name__ == "__main__":
    main()
