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
import matplotlib.pyplot as plt



def process_trajectory(csv_file:str, room_settings_file:str):
    
    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' does not exist.")
        return
    if not os.path.exists(room_settings_file):
        print(f"Error: File '{room_settings_file}' does not exist.")
        return

    # Load the room settings
    room_settings = common_tools.load_room_settings(room_settings_file)
    
    # Extract room size
    room_size = room_settings.get('size', [2.02, 28.7])
    room_width = float(room_size[0])
    room_height = float(room_size[1])

    # Cargamos el fichero a dividir
    df = pd.read_csv(csv_file)

    df = df[(df["pos_x"] != 0) & (df["pos_y"] != 0) ]

    # Extraemos x e y
    x_coords = df["pos_x"].to_numpy(dtype=float)
    y_coords = df["pos_y"].to_numpy(dtype=float)

    # Calculate figure size proportional to room dimensions (maintain aspect ratio)
    fig_width = 8
    fig_height = fig_width * (room_height / room_width)

    # Create a figure and an axes object with proportional size
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    # Plot the trajectory as a line
    ax.plot(x_coords, y_coords, marker='o', linestyle='-', color='blue', label='Trajectory')

    # Plot the room shape using settings from file
    room_x = [0, room_width, room_width, 0, 0]
    room_y = [0, 0, room_height, room_height, 0]
    ax.plot(room_x, room_y, color='red', linestyle='solid', marker='o')

    # Set equal aspect ratio to display real room proportions
    ax.set_aspect('equal', adjustable='box')

    # Add labels and title
    ax.set_xlabel('X-coordinate (m)')
    ax.set_ylabel('Y-coordinate (m)')
    ax.set_title('2D Trajectory Plot')

    # Add a grid with 0.5m intervals for better readability
    ax.set_xticks([i * 0.5 for i in range(int((room_width + 0.5) / 0.5) + 1)])
    ax.set_yticks([i * 0.5 for i in range(int((room_height + 0.5) / 0.5) + 1)])
    ax.grid(True, alpha=0.3)

    # Add a legend
    ax.legend()

    # Display the plot
    plt.show()

def main():
    """
    Main function to run the trajectory plotter.
    """
    print("Trajectory Plotter")
    print("==================")
    # Load arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--csv_file',
        type=str,
        help='Csv file with the trajectory samples to be plotted',
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
    
    # Get file paths and convert to absolute paths
    csv_file = common_tools.clean_path(args.csv_file.strip())
    room_settings_file = common_tools.clean_path(args.room_settings_file.strip())

    process_trajectory(csv_file, room_settings_file)


if __name__ == "__main__":
    main()
