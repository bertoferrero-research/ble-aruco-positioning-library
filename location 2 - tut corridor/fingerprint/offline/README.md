# TUT Corridor - Offline Fingerprint Dataset

This directory contains static BLE RSSI fingerprint measurements collected at predefined grid positions throughout the TUT corridor.

## Dataset Overview

**Collection Method**: Grid-based static sampling  
**Measurement Duration**: 2 minutes per position  
**Total Grid Points**: 171 positions  
**Grid Resolution**: 0.5 meters  
**Measurement Height**: 1.5 meters  

## Directory Structure

```
offline/
├── README.md              # This documentation file
├── with_noise/           # Data collected with environmental noise
│   ├── p01/              # Position 01 data
│   │   ├── 0.5_0.5_1.5__68_9E_19_03_95_84.csv
│   │   ├── 0.5_0.5_1.5__68_9E_19_03_95_F1.csv
│   │   ├── 0.5_0.5_1.5__AC_23_3F_26_3E_EF.csv
│   │   ├── 0.5_0.5_1.5__AC_23_3F_26_3E_F1.csv
│   │   ├── 0.5_0.5_1.5__AC_23_3F_26_3E_F2.csv
│   │   └── 0.5_0.5_1.5__all.csv
│   ├── p02/              # Position 02 data
│   └── ...               # Positions 03-20
└── without_noise/        # Data collected without environmental noise
    ├── p01/              # Position 01 data
    ├── p02/              # Position 02 data
    └── ...               # Positions 03-20
```

## Sampling Grid Configuration

**Grid Parameters**:
- **X Range**: 0.5m to 1.5m (3 positions along corridor width)
- **Y Range**: 0.5m to 28.5m (57 positions along corridor length)
- **Z Position**: 1.5m (fixed measurement height)
- **Resolution**: 0.5m spacing between adjacent points
- **Total Points**: 3 × 57 = 171 measurement positions

**Grid Layout**:
```
Y (m)
28.5 ----o----o----o----
     :    :    :    :
28.0 ----o----o----o----
     :    :    :    :
     ... (continues)
     :    :    :    :
1.0  ----o----o----o----
     :    :    :    :
0.5  ----o----o----o----
     0.5  1.0  1.5    X (m)
```

Each 'o' represents a measurement position where data was collected for 2 minutes.

## Dataset Variants

### With Noise (`with_noise/`)
**Collection Conditions**: 
- Normal operational environment
- People walking through corridor during measurements
- Typical ambient noise and interference

**Purpose**: 
- Realistic indoor localization scenarios
- Testing algorithm robustness against environmental factors
- Real-world performance evaluation

**Total Files**: 1026 CSV files (6 files per position × 171 positions)

### Without Noise (`without_noise/`)
**Collection Conditions**: 
- Controlled environment with restricted access
- Minimal people movement during data collection
- Reduced environmental interference

**Purpose**: 
- Baseline measurements for comparison
- Algorithm development and training
- Understanding signal propagation in ideal conditions

**Total Files**: 1026 CSV files (6 files per position × 171 positions)

## File Naming Convention

Individual beacon files:
```
{x}_{y}_{z}__{MAC_ADDRESS}.csv
```

Aggregated files (all beacons):
```
{x}_{y}_{z}__all.csv
```

**Components**:
- `x`: X coordinate of measurement position (meters)
- `y`: Y coordinate of measurement position (meters)
- `z`: Z coordinate of measurement position (meters)
- `MAC_ADDRESS`: Beacon MAC address with colons replaced by underscores

**Examples**:
- `0.5_0.5_1.5__68_9E_19_03_95_84.csv` - RSSI from ALBEACON2 at position (0.5, 0.5, 1.5)
- `1.5_14.5_1.5__AC_23_3F_26_3E_F1.csv` - RSSI from TUTBEACON1 at position (1.5, 14.5, 1.5)
- `1.0_28.5_1.5__all.csv` - Combined RSSI from all beacons at position (1.0, 28.5, 1.5)

## File Format

Each CSV file contains RSSI measurements with the following columns:

| Column        | Type    | Description                           | Unit   | Example                    |
|---------------|---------|---------------------------------------|--------|----------------------------|
| `timestamp`   | int64   | Unix timestamp (milliseconds)        | ms     | 1757927674075              |
| `time`        | string  | Human-readable timestamp              | -      | 2025-09-15 18:14:34.075    |
| `mac_address` | string  | Beacon MAC address                    | -      | AC:23:3F:26:3E:F2          |
| `rssi`        | int     | Received Signal Strength Indicator   | dBm    | -70                        |
| `tx_power`    | int     | Transmission power (usually 127)     | dBm    | 127                        |
| `pos_x`       | float   | X coordinate (fixed for each file)    | m      | 0.5                        |
| `pos_y`       | float   | Y coordinate (fixed for each file)    | m      | 0.5                        |
| `pos_z`       | float   | Z coordinate (fixed for each file)    | m      | 1.5                        |

**Sample Data** from `0.5_0.5_1.5__AC_23_3F_26_3E_F2.csv`:
```csv
timestamp,time,mac_address,rssi,tx_power,pos_x,pos_y,pos_z
1757927674075,2025-09-15 18:14:34.075,AC:23:3F:26:3E:F2,-70,127,0.5,0.5,1.5
1757927674243,2025-09-15 18:14:34.243,AC:23:3F:26:3E:F2,-72,127,0.5,0.5,1.5
1757927674311,2025-09-15 18:14:34.311,AC:23:3F:26:3E:F2,-68,127,0.5,0.5,1.5
```

## Data Collection Protocol

### Equipment
- Android smartphone with BLE scanning capabilities
- Laser distance meter for precise positioning
- Tripod for consistent device height (1.5m)
- Measuring tape for grid setup

### Procedure

1. **Grid Setup**
   - Mark reference points along corridor walls
   - Use laser meter to measure exact positions
   - Verify grid alignment and spacing

2. **Device Positioning**
   - Place smartphone on tripod at 1.5m height
   - Position tripod at grid point using laser measurements
   - Ensure device orientation is consistent

3. **Data Collection**
   - Activate BLE scanning application
   - Collect continuous measurements for 2 minutes
   - Monitor for any collection errors or interruptions

4. **Data Storage**
   - Save data with standardized filename format
   - Verify file integrity and completeness
   - Document any collection anomalies

5. **Grid Progression**
   - Move to next grid point
   - Repeat steps 2-4 for all 171 positions

### Collection Order
- Systematic row-by-row progression along Y-axis
- Multiple X positions collected before moving to next Y
- Both noise conditions collected separately (different sessions)

## Data Statistics

### Typical Measurement Count per Position
- **Individual beacon file**: 400-600 RSSI samples (2 minutes @ ~4-5 Hz)
- **All beacons combined**: 2000-3000 total samples per position

## Validation and Processing Tools

### Validation
Use `rssi_dataset_checker.py` to verify dataset integrity:

```bash
python tools/rssi_dataset_checker.py \
    --working_dir "location 2 - tut corridor/fingerprint/offline/without_noise/" \
    --mac_filter_file "location 2 - tut corridor/fingerprint/settings/mac_filter_list.json" \
    --room_settings_file "location 2 - tut corridor/fingerprint/settings/room_settings.json"
```

**Checks performed**:
- All expected files exist (171 positions × 6 files)
- Row counts match between individual and aggregated files
- No missing or corrupted data

### Data Cleaning
Use `rssi_sample_cleaner.py` to merge duplicate files:

```bash
python tools/rssi_sample_cleaner.py \
    --processing_folder "location 2 - tut corridor/fingerprint/offline/without_noise/"
```

**Processing steps**:
- Identifies duplicate files (e.g., `file.csv` and `file (1).csv`)
- Merges duplicate data
- Sorts by timestamp
- Removes duplicates

## Known Issues and Limitations
### Physical Limitations
- **Static Measurements**: Does not capture motion dynamics
- **Height Fixed**: Only collected at 1.5m height
- **Center Line Bias**: X positions concentrated near corridor center (0.5m to 1.5m)

### Environmental Factors
- **Temporal Variation**: Measurements collected over multiple sessions
- **Battery Degradation**: Beacon transmission power may vary slightly over time
- **Temperature Effects**: Not controlled or monitored during collection

## Related Files

- `../settings/room_settings.json` - Grid configuration and room dimensions
- `../settings/mac_filter_list.json` - List of beacon MAC addresses
- `../settings/beacon_position.csv` - Beacon positions and identifiers
- `../README.md` - General fingerprint dataset documentation

---

**Collection Period**: September-October 2025  
**Total Collection Time**: ~11.4 hours (171 positions × 2 minutes × 2 conditions)  
**Dataset Version**: 1.0  
**Last Updated**: November 21, 2025
