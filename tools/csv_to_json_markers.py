"""
ArUco Markers CSV to JSON Converter

This script converts ArUco marker data from CSV format to JSON format,
maintaining the nested structure for position and rotation fields.

Usage:
    python csv_to_json_markers.py --input markers.csv --output markers.json
    python csv_to_json_markers.py --input markers.csv  # outputs to markers_output.json
"""

import csv
import json
import argparse
from pathlib import Path


def parse_float(value: str) -> float:
    """
    Parse a float value that may use comma as decimal separator.
    
    Args:
        value: String representation of a number
        
    Returns:
        Float value
    """
    # Replace comma with dot for decimal separator
    return float(value.replace(',', '.').strip())


def parse_int(value: str) -> int:
    """
    Parse an integer value.
    
    Args:
        value: String representation of an integer
        
    Returns:
        Integer value
    """
    return int(value.strip())


def convert_csv_to_json(csv_file_path: str, json_file_path: str) -> None:
    """
    Convert ArUco markers CSV file to JSON format.
    
    The CSV must contain the following columns:
    - id: Marker ID (integer)
    - marker_type: Type of marker (string, optional)
    - size: Marker size in meters (float)
    - max_distance: Maximum detection distance (integer)
    - position: Position name (string, optional)
    - position/x: X coordinate (float)
    - position/y: Y coordinate (float)
    - position/z: Z coordinate (float)
    - rotation/roll: Roll angle (integer)
    - rotation/pitch: Pitch angle (integer)
    - rotation/yaw: Yaw angle (integer)
    - comment: Description (string, optional)
    
    Args:
        csv_file_path: Path to input CSV file
        json_file_path: Path to output JSON file
    """
    markers = []
    
    # Read CSV file
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            # Create marker object with nested structure
            marker = {
                "id": parse_int(row['id']),
                "size": parse_float(row['size']),
                "max_distance": parse_float(row['max_distance']),
                "comment": row['comment'].strip(),
                "marker_type": row['marker_type'].strip(),
                "position_name": row['position'].strip(),
                "position": {
                    "x": parse_float(row['position/x']),
                    "y": parse_float(row['position/y']),
                    "z": parse_float(row['position/z'])
                },
                "rotation": {
                    "roll": parse_int(row['rotation/roll']),
                    "pitch": parse_int(row['rotation/pitch']),
                    "yaw": parse_int(row['rotation/yaw'])
                }
            }
            
            markers.append(marker)
    
    # Write JSON file with proper formatting
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(markers, json_file, indent=4, ensure_ascii=False)
    
    print(f"Successfully converted {len(markers)} markers from CSV to JSON")
    print(f"Input file: {csv_file_path}")
    print(f"Output file: {json_file_path}")


def main():
    """
    Main entry point for the script.
    Parses command line arguments and executes the conversion.
    """
    parser = argparse.ArgumentParser(
        description='Convert ArUco markers CSV file to JSON format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python csv_to_json_markers.py --input aruco_markers.csv --output aruco_markers.json
  python csv_to_json_markers.py -i markers.csv -o markers.json
  python csv_to_json_markers.py --input markers.csv  # outputs to markers_output.json
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        required=True,
        help='Path to input CSV file'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        required=False,
        help='Path to output JSON file (optional, defaults to input_output.json)'
    )
    
    args = parser.parse_args()
    
    # Determine output file path
    if args.output:
        output_path = args.output
    else:
        # Generate default output path
        input_path = Path(args.input)
        output_path = input_path.with_stem(f"{input_path.stem}_output").with_suffix('.json')
    
    # Validate input file exists
    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}")
        return
    
    # Execute conversion
    try:
        convert_csv_to_json(args.input, str(output_path))
    except Exception as e:
        print(f"Error during conversion: {e}")
        raise


if __name__ == '__main__':
    main()
