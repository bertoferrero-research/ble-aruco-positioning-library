# TUT Corridor Fingerprint Dataset

This directory contains Bluetooth Low Energy (BLE) beacon fingerprint data collected in the TUT corridor environment for indoor localization research.

## Dataset Overview

**Location**: TUT Corridor  
**Environment**: Indoor corridor (2.02m × 28.7m)  
**Technology**: BLE RSSI fingerprinting  
**Collection Methods**: 
- Offline grid-based sampling (static measurements)
- Online trajectory-based sampling (dynamic measurements - two takes)
  - Take 1: Original collection with baseline ArUco markers
  - Take 2: Enhanced collection with expanded ArUco marker set

## Directory Structure

```
fingerprint/
├── README.md                  # This documentation file
├── settings/                  # Configuration files
│   ├── room_settings.json     # Room dimensions and grid configuration
│   ├── beacon_position.csv    # Beacon positions and identifiers
│   ├── mac_filter_list.json   # List of beacon MAC addresses
│   ├── aruco_markers.csv      # ArUco marker definitions (CSV format)
│   ├── aruco_markers.json     # Baseline ArUco marker definitions (JSON format)
│   └── aruco_markers_with_support.json  # Extended marker information
├── offline/                   # Static fingerprint data (grid-based)
│   ├── README.md             # Detailed offline dataset documentation
│   ├── with_noise/           # Data collected with environmental noise
│   └── without_noise/        # Data collected without environmental noise
└── online/                    # Dynamic trajectory data
    ├── README.md             # Detailed online dataset documentation
    └── trajectories/         # Trajectory-based measurements
        ├── take1/            # Original collection (November 2025)
        │   ├── raw/          # Original trajectory data (T1-T4, T6, T8)
        │   └── processed/    # Split and processed trajectory data
        └── take2/            # Enhanced collection (December 2025)
            ├── raw/          # Original trajectory data (T1-T4, T6-1, T6-2, T6-3, T6-4)
            └── processed/    # Split and processed trajectory data
```

## Beacon Configuration

The dataset includes measurements from **5 BLE beacons** strategically positioned throughout the corridor. Additionally, the **online dataset incorporates ArUco markers** for visual ground truth positioning, with Take 2 featuring an expanded marker set for improved coverage.

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

## Dataset Types

### Offline Dataset (Static Grid Sampling)
Static measurements collected at predefined grid positions throughout the corridor. Ideal for creating radio maps and training fingerprinting algorithms.

**Key Features**:
- Grid-based sampling with 0.5m resolution
- 171 measurement positions
- 2 minutes of data per position
- Two variants: with environmental noise and without noise

**See**: `offline/README.md` for detailed documentation

### Online Dataset (ArUco-based Measurements)
Measurements collected using ArUco markers for ground truth positioning, including both static positions and dynamic trajectories. Useful for testing real-time localization, tracking algorithms, and validating visual positioning systems.

**Key Features**:
- **Static measurements**: 20 positions with dual ground truth (laser + ArUco)
- **Dynamic trajectories - Two collection takes**:
  - **Take 1** (Original - November 2025): 6 trajectories (T1, T2, T3, T4, T6, T8) with baseline ArUco markers
  - **Take 2** (Enhanced - December 2025): 8 trajectories with support ArUco markers for improved detection coverage
    - Same trajectories as Take 1: T1, T2, T3, T4
    - Removed: T8 (random path)
    - Enhanced T6 variants exploring rotational movement:
      - T6 (T6-1): Zigzag with turning while advancing (rotation during forward motion)
      - T6-2: Zigzag with turning while advancing (rotation during forward motion)
      - T6-3: Zigzag stopping to rotate - stops at wall, rotates in place, then advances
      - T6-4: Zigzag stopping to rotate - stops at wall, rotates in place, then advances
- ArUco marker-based positioning validation
- Chest-mounted collection for realistic movement
- Continuous RSSI during natural walking speed

**See**: `online/README.md` for detailed documentation

## File Naming Conventions

### Offline Dataset
Individual beacon files:
```
{x}_{y}_{z}__{MAC_ADDRESS}.csv
```

Aggregated files:
```
{x}_{y}_{z}__all.csv
```

**Examples**:
- `1.5_14.5_1.5__68_9E_19_03_95_84.csv` - RSSI from beacon at position (1.5, 14.5, 1.5)
- `1.5_14.5_1.5__all.csv` - Combined RSSI from all beacons at position (1.5, 14.5, 1.5)

### Online Dataset

**Static Measurements**:
Individual beacon files (no position in filename):
```
{MAC_ADDRESS}.csv
all.csv
```

**Trajectory Measurements** (raw):
```
{start_x}_{start_y}_{start_z}__{MAC_ADDRESS}.csv
image_XXXX_TIMESTAMP.matphoto
```

**Trajectory Measurements** (processed):
```
{MAC_ADDRESS}.csv
all.csv
all_processing_stats.csv
```

**Examples**:
- Static: `AC_23_3F_26_3E_F1.csv` - RSSI from TUTBEACON1 at a static position
- Trajectory raw: `0.0_0.0_0.0__all.csv` - Combined RSSI during trajectory
- Trajectory processed: `all.csv` - Processed trajectory with positions

## File Format

CSV file formats vary by dataset type:

### Offline Dataset
Standard columns with fixed positions:

| Column        | Type    | Description                           | Unit   |
|---------------|---------|---------------------------------------|--------|
| `timestamp`   | int64   | Unix timestamp (milliseconds)        | ms     |
| `time`        | string  | Human-readable timestamp              | -      |
| `mac_address` | string  | Beacon MAC address                    | -      |
| `rssi`        | int     | Received Signal Strength Indicator   | dBm    |
| `tx_power`    | int     | Transmission power (usually 127)     | dBm    |
| `pos_x`       | float   | X coordinate (fixed per file)         | m      |
| `pos_y`       | float   | Y coordinate (fixed per file)         | m      |
| `pos_z`       | float   | Z coordinate (fixed per file)         | m      |

### Online Dataset - Static
Dual positioning (ArUco + Laser):

| Column          | Type    | Description                           | Unit   |
|-----------------|---------|---------------------------------------|--------|
| `timestamp`     | int64   | Unix timestamp                        | ms     |
| `time`          | string  | Human-readable timestamp              | -      |
| `mac_address`   | string  | Beacon MAC address                    | -      |
| `rssi`          | int     | Signal strength                       | dBm    |
| `tx_power`      | int     | Transmission power                    | dBm    |
| `aruco_pos_x`   | float   | X from ArUco detection                | m      |
| `aruco_pos_y`   | float   | Y from ArUco detection                | m      |
| `aruco_pos_z`   | float   | Z from ArUco detection                | m      |
| `laser_pos_x`   | float   | X from laser measurement              | m      |
| `laser_pos_y`   | float   | Y from laser measurement              | m      |
| `laser_pos_z`   | float   | Z from laser measurement              | m      |

### Online Dataset - Trajectories
Dynamic positioning with detection status:

| Column                            | Type    | Description                           | Unit   |
|-----------------------------------|---------|---------------------------------------|--------|
| `timestamp`                       | int64   | Unix timestamp                        | ms     |
| `time`                            | string  | Human-readable timestamp              | -      |
| `mac_address`                     | string  | Beacon MAC address                    | -      |
| `rssi`                            | int     | Signal strength                       | dBm    |
| `tx_power`                        | int     | Transmission power                    | dBm    |
| `pos_x`                           | float   | X from ArUco (0 if not detected)      | m      |
| `pos_y`                           | float   | Y from ArUco (0 if not detected)      | m      |
| `pos_z`                           | float   | Z from ArUco (0 if not detected)      | m      |
| `position_calculation_timestamp`  | string  | ArUco detection timestamp             | -      |
| `position_calculation_status`     | string  | Detection status                      | -      |

**Note**: In trajectory files, `pos_x=0, pos_y=0, pos_z=0` indicates no ArUco marker was detected at that timestamp.

## Data Collection Details

**Equipment Used**:
- Android smartphones with BLE scanning capabilities
- Laser meter for precise positioning (offline dataset)
- ArUco markers for ground truth positioning (online dataset)
- Tripods for consistent measurement height (offline dataset)

**Collection Protocols**:

### Offline Dataset
1. Position device at grid point using laser meter
2. Mount on tripod at 1.5m height
3. Activate BLE scanning application
4. Collect measurements for 2 minutes
5. Save data with standardized filename
6. Move to next grid position

### Online Dataset - Static
1. Position device on tripod at measurement point
2. Measure exact position with laser meter (ground truth)
3. Activate BLE scanning with image capture enabled
4. Collect 2 minutes of data with periodic ArUco images (3 images, 5s apart)
5. Perform 2 sessions per position (total 6 images)
6. Process images to extract ArUco positions
7. Compare ArUco vs laser positioning accuracy

### Online Dataset - Trajectories
1. Place ArUco markers at known positions along corridor
2. Mount smartphone in chest harness on subject
3. Position subject at trajectory starting point
4. Activate BLE scanning and continuous camera recording (250ms interval)
5. Walk predefined trajectory path at natural speed
6. Continuously record RSSI and camera frames
7. Post-process images to extract ArUco positions
8. Associate positions with RSSI timestamps

## Processing Tools

The dataset includes various processing and validation scripts in the `tools/` directory:

### Offline Dataset Tools
- `rssi_dataset_checker.py`: Validates file completeness and data consistency
- `rssi_sample_cleaner.py`: Merges duplicate files and sorts data
- `common_tools.py`: Utility functions for data loading and processing

**Example - Validation**:
```bash
python tools/rssi_dataset_checker.py \
    --working_dir "location 2 - tut corridor/fingerprint/offline/without_noise/" \
    --mac_filter_file "location 2 - tut corridor/fingerprint/settings/mac_filter_list.json" \
    --room_settings_file "location 2 - tut corridor/fingerprint/settings/room_settings.json"
```

### Online Dataset Tools
- `trajectory_split.py`: Splits trajectory files by MAC address
- `trajectory_split_all.py`: Batch processes all trajectories
- `trajectory_plotter.py`: Visualizes trajectory paths with room layout
- `csv_to_json_markers.py`: Converts ArUco marker definitions from CSV to JSON format

**Example - Trajectory Visualization**:
```bash
python tools/trajectory_plotter.py \
    --csv_file "location 2 - tut corridor/fingerprint/online/trajectories/take1/processed/T1/all.csv" \
    --room_settings_file "location 2 - tut corridor/fingerprint/settings/room_settings.json"
```

**Example - ArUco Marker CSV to JSON Conversion**:
```bash
python tools/csv_to_json_markers.py \
    --input "location 2 - tut corridor/fingerprint/settings/aruco_markers.csv" \
    --output "location 2 - tut corridor/fingerprint/settings/aruco_markers.json"
```

## Known Issues and Limitations

### General Limitations
- **Device Variations**: Measurements collected using different Android devices may show slight variations
- **Environmental Changes**: Conditions may vary slightly between collection sessions
- **BLE Range**: Some beacons may not be visible from distant positions
- **Interference**: Occasional WiFi or other 2.4GHz interference
- **Battery Effects**: Beacon transmission power may vary with battery level

### Offline Dataset Specific
- **Temporal Gaps**: Some grid positions may have brief interruptions
- **Duplicate Files**: Some positions may have duplicate files (resolved by cleaning scripts)
- **Static Nature**: Does not capture dynamic movement effects

### Online Dataset Specific
- **ArUco Detection**: Position accuracy depends on marker visibility and detection quality
- **Missing Positions**: Large gaps in trajectories where no markers detected (pos_x=0, pos_y=0)
- **Static Coverage**: Only 20 positions (vs 171 in offline), sparser spatial distribution
- **Walking Speed Variation**: Natural variation in movement speed during trajectories
- **Trajectory Complexity**: T6 (zigzag) and T8 (random) have most detection challenges
- **Dual Ground Truth**: Static positions have both laser and ArUco measurements with expected differences (~2-5cm)

### Data Processing Notes
- **Timestamp Precision**: Timestamps are in milliseconds but actual precision may vary
- **Position Interpolation**: Online positions are based on detected markers, not continuous tracking

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

- **v2.1** (2025-12-05): Take 2 Enhanced Online Dataset
  - 8 trajectories with expanded ArUco marker coverage
  - Repeated trajectories from Take 1: T1, T2, T3, T4
  - Removed T8 (random path) for more focused rotational analysis
  - New T6 variants for rotational movement analysis:
    - T6 (T6-1): Original zigzag with turning while advancing
    - T6-2: Original zigzag with turning while advancing
    - T6-3: Static rotation only (spin in place at wall)
    - T6-4: Static rotation only (spin in place at wall)
  - Extended ArUco marker set: 52 markers in 21 positions (vs 32 markers in 11 positions in Take 1)
  - Marker sizes: A2 (0.385m), A3 (0.273m), A4 (0.173m) for multi-range detection
  - CSV format for ArUco marker definitions (`aruco_markers.csv`)
  - CSV-to-JSON marker definition conversion tool (`csv_to_json_markers.py`)
  - Improved position detection consistency and coverage vs Take 1
  
- **v2.0** (2025-11-21): Online dataset added (Take 1)
  - Static measurements: 20 positions with dual ground truth (laser + ArUco)
  - Dynamic trajectories: 6 paths (T1, T2, T3, T4, T6, T8)
  - 21 baseline ArUco markers
  - Both variants: with environmental noise and without noise
  - ArUco-based positioning system
  - Trajectory processing and visualization tools
  - Chest-harness collection for realistic movement
  
- **v1.0** (2025-10-07): Initial offline dataset release
  - Complete grid coverage for both noise conditions
  - 5 beacon configuration
  - Validation tools included

## License

This dataset is released under [specify license, e.g., CC BY 4.0, MIT, etc.].

---

**Last Updated**: December 12, 2025  
**Dataset Version**: 2.1  
**Collection Period**: October - December 2025  
**Total Data**:
  - Offline: ~5 GB
  - Online Take 1: ~2.9 GB (git submodule)
  - Online Take 2: ~2.5+ GB (git submodule)
  - Total Online: ~5.4+ GB
  - Total Dataset: ~10.4+ GB