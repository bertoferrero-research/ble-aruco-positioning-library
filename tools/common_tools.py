# ============================================================================
# Imports
# ============================================================================
import os
import json
import pandas as pd

# ============================================================================
# Configuration Loading
# ============================================================================

def load_json_file(file_path: str) -> dict:
    """
    Load a JSON file and return its content.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        dict or list: Content of the JSON file
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file is not valid JSON
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in {file_path}: {str(e)}", e.doc, e.pos)


def load_mac_filter_file(file_path:str) -> list:
    """
    Load MAC filter file (JSON) and return list of allowed MAC addresses.

    Args:
        file_path (str): Path to the MAC filter JSON file

    Returns:
        list: List of allowed MAC addresses
    """
    return load_json_file(file_path)


def load_room_settings(file_path:str) -> dict:
    """
    Load room settings file (JSON) and return room configuration.
    
    Args:
        file_path (str): Path to the room settings JSON file
    Returns:
        dict: Room configuration dictionary
    """
    return load_json_file(file_path)

# ============================================================================
# CSV Utilities
# ============================================================================

def count_rows_in_csv(file_path: str) -> int:
    """
    Count the number of rows in a CSV file using pandas.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        int: Number of rows in the file.
    """
    try:
        df = pd.read_csv(file_path)
        return len(df)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return 0

# ============================================================================
# Path Utilities
# ============================================================================

def clean_path(input_path:str )-> str:
    """
    Clean potential problematic characters from path.
    
    Args:
        input_path (str): Input path string

    Returns:
        str: Cleaned path string
    """
    # Remove quotes
    cleaned_path = input_path.strip('\'"')
    # Remove trailing slashes
    cleaned_path = cleaned_path.rstrip('\\/')
    # Convert relative path to absolute path
    cleaned_path = os.path.abspath(cleaned_path)
    return cleaned_path

def compose_fingerprint_filename(x:float, y:float, z:float, mac:str) -> str:
    """
    Compose a standardized filename for fingerprint data based on coordinates and MAC address.

    Args:
        x (float): X coordinate
        y (float): Y coordinate
        z (float): Z coordinate
        mac (str): MAC address

    Returns:
        str: Formatted filename
    """
    if mac != "all":
        mac = mac.replace(":", "_").replace("-", "_").upper()
    return f"{x}_{y}_{z}__{mac}.csv"

def compose_fingerprint_filepath(base_dir:str, x:float, y:float, z:float, mac:str) -> str:
    """
    Compose a full file path for fingerprint data based on base directory, coordinates, and MAC address.

    Args:
        base_dir (str): Base directory path
        x (float): X coordinate
        y (float): Y coordinate
        z (float): Z coordinate
        mac (str): MAC address

    Returns:
        str: Full file path
    """
    filename = compose_fingerprint_filename(x, y, z, mac)
    return os.path.join(base_dir, filename)
