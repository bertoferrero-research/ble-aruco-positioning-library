#!/usr/bin/env python3
"""
RSSI Dataset Time Duration Validator

This script validates that the time duration of RSSI data collection at each
grid point does not exceed a specified threshold. It checks all *.csv files
in a directory to ensure data collection duration is within expected limits.

Usage:
    python check_collection_duration.py --working_dir "path/to/data" --max_duration 120
"""

import os
import pandas as pd
import glob
import argparse
import sys
from pathlib import Path


def check_csv_duration(file_path, max_duration_seconds, margin_seconds=1.0):
    """
    Check if the duration of data collection in a CSV file exceeds the limit.
    
    Args:
        file_path (str): Path to the CSV file
        max_duration_seconds (int): Maximum allowed duration in seconds
        margin_seconds (float): Margin in seconds to avoid false positives (default: 1.0)
        
    Returns:
        tuple: (is_valid, duration_seconds, first_timestamp, last_timestamp)
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Check if timestamp column exists
        if 'timestamp' not in df.columns:
            print(f"  ⚠ Warning: No 'timestamp' column in {os.path.basename(file_path)}")
            return None, None, None, None
        
        # Check if dataframe is empty
        if len(df) == 0:
            print(f"  ⚠ Warning: Empty file {os.path.basename(file_path)}")
            return None, None, None, None
        
        # Get first and last timestamps (in milliseconds)
        first_timestamp = df['timestamp'].min()
        last_timestamp = df['timestamp'].max()
        
        # Calculate duration in seconds
        duration_ms = last_timestamp - first_timestamp
        duration_seconds = duration_ms / 1000.0
        
        # Check if duration exceeds limit (with margin to avoid false positives)
        is_valid = duration_seconds <= (max_duration_seconds + margin_seconds)
        
        return is_valid, duration_seconds, first_timestamp, last_timestamp
        
    except Exception as e:
        print(f"  ❌ Error reading {os.path.basename(file_path)}: {e}")
        return None, None, None, None


def format_duration(seconds):
    """Format duration in seconds to human-readable format."""
    if seconds is None:
        return "N/A"
    
    minutes = int(seconds // 60)
    secs = seconds % 60
    
    if minutes > 0:
        return f"{minutes}m {secs:.1f}s"
    else:
        return f"{secs:.1f}s"


def check_folder_durations(folder_path, max_duration_seconds, margin_seconds=1.0, show_valid=False, output_file=None):
    """
    Check all *.csv files in a folder for duration violations.
    
    Args:
        folder_path (str): Path to the folder containing CSV files
        max_duration_seconds (int): Maximum allowed duration in seconds
        margin_seconds (float): Margin in seconds to avoid false positives (default: 1.0)
        show_valid (bool): Whether to show files that pass validation
        output_file (str): Optional path to export invalid files list
        
    Returns:
        tuple: (total_files, valid_files, invalid_files, error_files)
    """
    if not os.path.exists(folder_path):
        print(f"❌ Error: Folder '{folder_path}' does not exist.")
        return 0, 0, 0, 0
    
    # Find all *.csv files
    pattern = os.path.join(folder_path, "*.csv")
    csv_files = glob.glob(pattern)
    
    if not csv_files:
        print(f"⚠ Warning: No '*.csv' files found in {folder_path}")
        return 0, 0, 0, 0
    
    print(f"Found {len(csv_files)} *.csv files to validate")
    print(f"Maximum allowed duration: {format_duration(max_duration_seconds)} (+ {margin_seconds}s margin)")
    print()
    
    # Statistics
    total_files = len(csv_files)
    valid_files = 0
    invalid_files = 0
    error_files = 0
    
    invalid_details = []
    
    # Check each file
    for csv_file in sorted(csv_files):
        filename = os.path.basename(csv_file)
        is_valid, duration, first_ts, last_ts = check_csv_duration(csv_file, max_duration_seconds, margin_seconds)
        
        if is_valid is None:
            # Error occurred
            error_files += 1
            continue
        
        if is_valid:
            valid_files += 1
            if show_valid:
                print(f"✅ {filename}: {format_duration(duration)} (OK)")
        else:
            invalid_files += 1
            excess = duration - max_duration_seconds
            invalid_details.append({
                'file': filename,
                'duration': duration,
                'excess': excess,
                'first_ts': first_ts,
                'last_ts': last_ts
            })
    
    # Report invalid files
    if invalid_files > 0:
        print("\n=== FILES EXCEEDING DURATION LIMIT ===")
        print(f"{'File':<40} {'Duration':>12} {'Excess':>12}")
        print("-" * 65)
        for detail in sorted(invalid_details, key=lambda x: x['duration'], reverse=True):
            print(f"{detail['file']:<40} {format_duration(detail['duration']):>12} {format_duration(detail['excess']):>12}")
        
        # Export to file if requested
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write("Invalid Files - Collection Duration Exceeds Limit\n")
                    f.write("=" * 80 + "\n")
                    f.write(f"Maximum allowed duration: {format_duration(max_duration_seconds)}\n")
                    f.write(f"Total invalid files: {invalid_files}\n\n")
                    f.write(f"{'File':<40} {'Duration':>12} {'Excess':>12}\n")
                    f.write("-" * 65 + "\n")
                    for detail in sorted(invalid_details, key=lambda x: x['duration'], reverse=True):
                        f.write(f"{detail['file']:<40} {format_duration(detail['duration']):>12} {format_duration(detail['excess']):>12}\n")
                    f.write("\n\nDetailed Information:\n")
                    f.write("=" * 80 + "\n\n")
                    for detail in invalid_details:
                        f.write(f"File: {detail['file']}\n")
                        f.write(f"  Duration: {format_duration(detail['duration'])} (Exceeds by {format_duration(detail['excess'])})\n")
                        f.write(f"  First timestamp: {detail['first_ts']} ({pd.to_datetime(detail['first_ts'], unit='ms')})\n")
                        f.write(f"  Last timestamp:  {detail['last_ts']} ({pd.to_datetime(detail['last_ts'], unit='ms')})\n\n")
                print(f"\n✅ Invalid files list exported to: {output_file}")
            except Exception as e:
                print(f"\n⚠ Warning: Could not export to file: {e}")
        
        print("\n=== DETAILED INFORMATION ===")
        for detail in invalid_details:
            print(f"\n❌ {detail['file']}")
            print(f"   Duration: {format_duration(detail['duration'])} "
                  f"(Exceeds by {format_duration(detail['excess'])})")
            print(f"   First timestamp: {detail['first_ts']} ({pd.to_datetime(detail['first_ts'], unit='ms')})")
            print(f"   Last timestamp:  {detail['last_ts']} ({pd.to_datetime(detail['last_ts'], unit='ms')})")
    
    return total_files, valid_files, invalid_files, error_files


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Validate RSSI data collection duration in CSV files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Check with default 120 seconds limit
    python check_collection_duration.py --working_dir "offline/with noise"
    
    # Check with custom 150 seconds limit
    python check_collection_duration.py --working_dir "offline/with noise" --max_duration 150
    
    # Show all files including valid ones
    python check_collection_duration.py --working_dir "offline/with noise" --show_valid
        """
    )
    
    parser.add_argument(
        '--working_dir',
        type=str,
        required=True,
        help='Path to the directory containing *.csv files'
    )
    
    parser.add_argument(
        '--max_duration',
        type=int,
        default=120,
        help='Maximum allowed duration in seconds (default: 120)'
    )
    
    parser.add_argument(
        '--show_valid',
        action='store_true',
        help='Show files that pass validation (default: only show invalid)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Export invalid files list to a text file'
    )
    
    args = parser.parse_args()
    
    # Clean and convert path to absolute
    folder_path = args.working_dir.strip().strip('\'"').rstrip('\\/')
    folder_path = os.path.abspath(folder_path)
    
    print("=== RSSI COLLECTION DURATION VALIDATOR ===")
    print(f"Working directory: {folder_path}")
    print()
    
    # Run validation
    total, valid, invalid, errors = check_folder_durations(
        folder_path,
        args.max_duration,
        margin_seconds=1.0,
        show_valid=args.show_valid,
        output_file=args.output
    )
    
    # Print summary
    print("=== VALIDATION SUMMARY ===")
    print(f"Total files analyzed:    {total}")
    print(f"✅ Valid files:          {valid} ({valid/total*100:.1f}%)" if total > 0 else "✅ Valid files: 0")
    print(f"❌ Invalid files:        {invalid} ({invalid/total*100:.1f}%)" if total > 0 else "❌ Invalid files: 0")
    if errors > 0:
        print(f"⚠  Files with errors:    {errors} ({errors/total*100:.1f}%)")
    
    print()
    
    if invalid == 0 and errors == 0:
        print("✅ ALL FILES PASSED - All collection durations are within limits")
        sys.exit(0)
    elif invalid > 0:
        print(f"❌ VALIDATION FAILED - {invalid} file(s) exceed the duration limit")
        sys.exit(1)
    else:
        print(f"⚠  VALIDATION WARNING - {errors} file(s) had errors during processing")
        sys.exit(2)


if __name__ == "__main__":
    main()
