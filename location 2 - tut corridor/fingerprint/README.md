# TUT Corridor Fingerprint Dataset

This directory contains Bluetooth Low Energy (BLE) beacon fingerprint data collected in the TUT corridor environment for indoor localization research.

## Dataset Overview

**Location**: TUT Corridor  
**Environment**: Indoor corridor (2.02m × 28.7m)  
**Technology**: BLE RSSI fingerprinting  
**Collection Method**: Offline grid-based sampling  

## Directory Structure

```
fingerprint/
├── README.md                  # This documentation file
├── settings/                  # Configuration files
│   ├── room_settings.json     # Room dimensions and grid configuration
│   ├── beacon_position.csv    # Beacon positions and identifiers
│   └── mac_filter_list.json   # List of beacon MAC addresses
├── offline/                   # Fingerprint data
│   ├── with noise/           # Data collected with environmental noise
│   └── wout noise/           # Data collected without environmental noise
└── [additional folders]       # Future datasets or processing results
```

## Beacon Configuration

The dataset includes measurements from **5 BLE beacons** strategically positioned throughout the corridor:

| Beacon ID | MAC Address        | Name        | Position (x, y, z) |
|-----------|-------------------|-------------|-------------------|
| 1         | AC:23:3F:26:3E:F1 | TUTBEACON1  | (2.02, 20.47, 2.0) |
| 2         | 68:9E:19:03:95:F1 | ALBEACON1   | (2.02, 14.28, 2.0) |
| 3         | AC:23:3F:26:3E:F2 | TUTBEACON2  | (2.02, 7.14, 2.0)  |
| 4         | 68:9E:19:03:95:84 | ALBEACON2   | (0.0, 19.04, 2.0)   |
| 5         | AC:23:3F:26:3E:EF | TUTBEACON3  | (0.0, 9.52, 2.1)    |

**Coordinate System**: 
- Origin (0,0) at the corridor corner
- X-axis: corridor width (0-2.02m)
- Y-axis: corridor length (0-28.7m)
- Z-axis: height above floor (meters)

## Sampling Grid Configuration

**Grid Parameters**:
- **Resolution**: 0.5 meters
- **X Range**: 0.5m to 1.5m (corridor center line)
- **Y Range**: 0.5m to 28.5m (full corridor length)
- **Z Position**: 1.5m (measurement height)
- **Total Grid Points**: 171 positions

**Sampling Method**:
- Static positioning at each grid point
- Multiple RSSI measurements per beacon per position
- Measurements collected using Android devices
- Duration: 2 minutes per grid point

## Dataset Variants

### 1. With Noise (`offline/with noise/`)
- **Collection Conditions**: Normal operational environment
- **Noise Sources**: People movement
- **Purpose**: Realistic indoor localization scenarios
- **File Count**: 1026 CSV files (6 files per grid point)

### 2. Without Noise (`offline/wout noise/`)
- **Collection Conditions**: Controlled environment
- **Noise Mitigation**: Restricted access
- **Purpose**: Baseline measurements and algorithm comparison
- **File Count**: 1026 CSV files (6 files per grid point)

## File Naming Convention

Individual beacon files:
```
{x}_{y}_{z}__{MAC_ADDRESS}.csv
```

Aggregated files:
```
{x}_{y}_{z}__all.csv
```

**Examples**:
- `1.5_14.5_1.5__68_9E_19_03_95_84.csv` - RSSI data from beacon ALBEACON2 at position (1.5, 14.5, 1.5)
- `1.5_14.5_1.5__all.csv` - Combined RSSI data from all beacons at position (1.5, 14.5, 1.5)

## File Format

Each CSV file contains the following columns:

| Column        | Type    | Description                           | Unit   | Example                    |
|---------------|---------|---------------------------------------|--------|----------------------------|
| `timestamp`   | int64   | Unix timestamp (milliseconds)        | ms     | 1757927674075              |
| `time`        | string  | Human-readable timestamp              | -      | 2025-09-15 18:14:34.075    |
| `mac_address` | string  | Beacon MAC address                    | -      | AC:23:3F:26:3E:F2          |
| `rssi`        | int     | Received Signal Strength Indicator   | dBm    | -70                        |
| `tx_power`    | int     | Transmission power (usually 127)     | dBm    | 127                        |
| `pos_x`       | float   | X coordinate of measurement position  | m      | 0.5                        |
| `pos_y`       | float   | Y coordinate of measurement position  | m      | 0.5                        |
| `pos_z`       | float   | Z coordinate of measurement position  | m      | 1.5                        |

**Sample Data**:
```csv
timestamp,time,mac_address,rssi,tx_power,pos_x,pos_y,pos_z
1757927674075,2025-09-15 18:14:34.075,AC:23:3F:26:3E:F2,-70,127,0.5,0.5,1.5
1757927674243,2025-09-15 18:14:34.243,68:9E:19:03:95:84,-87,127,0.5,0.5,1.5
1757927674311,2025-09-15 18:14:34.311,68:9E:19:03:95:F1,-75,127,0.5,0.5,1.5
```

## Data Collection Details

**Equipment Used**:
- Android smartphones with BLE scanning capabilities
- Laser meter for fine positioning
- Tripods for consistent measurement height

**Collection Protocol**:
1. Position device at grid point using measuring laser meter
2. Activate BLE scanning application
3. Collect measurements for 2 minutes
4. Save data with standardized filename
5. Move to next grid position

## Validation Tools

The dataset includes validation scripts in the `tools/` directory:

- `rssi_dataset_checker.py`: Validates file completeness and data consistency
- `rssi_sample_cleaner.py`: Merges duplicate files and sorts data
- `common_tools.py`: Utility functions for data loading and processing

### Running Validation
```bash
python tools/rssi_dataset_checker.py \
    --working_dir "location 2 - tut corridor/fingerprint/offline/with noise/" \
    --mac_filter_file "location 2 - tut corridor/fingerprint/settings/mac_filter_list.json" \
    --room_settings_file "location 2 - tut corridor/fingerprint/settings/room_settings.json"
```

## Known Issues and Limitations

### Data Collection Limitations
- **Temporal Gaps**: Some positions may have brief interruptions in data collection
- **Device Variations**: Measurements collected using different Android devices may show slight variations
- **Environmental Changes**: Conditions may vary slightly between collection sessions

### Technical Limitations
- **BLE Range**: Some beacons may not be visible from distant grid positions
- **Interference**: Occasional WiFi or other 2.4GHz interference
- **Battery Effects**: Beacon transmission power may vary with battery level

### Data Processing Notes
- **Duplicate Files**: Some positions may have duplicate files (resolved by cleaning scripts)
- **Timestamp Precision**: Timestamps are in milliseconds but actual precision may vary

## Citation and Usage

If you use this dataset in your research, please cite:

```bibtex
@dataset{tut_corridor_fingerprint_2025,
  title={TUT Corridor BLE Fingerprint Dataset},
  author={[Author Names]},
  year={2025},
  institution={[Institution Name]},
  location={TUT Corridor},
  note={Indoor localization research dataset}
}
```

## Contact Information

For questions, issues, or additional information about this dataset:

- **Dataset Maintainer**: [Your Name]
- **Institution**: [Your Institution]
- **Email**: [your.email@domain.com]
- **Repository**: [GitHub Repository URL]

## Version History

- **v1.0** (2025-10-07): Initial dataset release
  - Complete grid coverage for both noise conditions
  - 5 beacon configuration
  - Validation tools included

## License

This dataset is released under [specify license, e.g., CC BY 4.0, MIT, etc.].

---

**Last Updated**: October 7, 2025  
**Dataset Version**: 1.0  
**Total File Size**: [Approximate size]  
**Collection Period**: [Start Date] - [End Date]