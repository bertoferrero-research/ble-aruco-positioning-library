# TUT Corridor - Online Fingerprint Dataset

This directory contains dynamic BLE RSSI fingerprint measurements collected during movement through the TUT corridor, using ArUco markers for ground truth positioning.

## Dataset Overview

**Collection Methods**: 
- Static positioning with ArUco validation (20 positions)
- Dynamic trajectory sampling (6 trajectories)

**Ground Truth**: ArUco marker-based visual positioning  
**Total Positions (Static)**: 20 measurement points  
**Total Trajectories**: 6 paths (T1, T2, T3, T4, T6, T8)  
**Equipment**: Android smartphone with chest-mounted harness  

## Directory Structure

```
online/
├── README.md                    # This documentation file
├── static/                      # Static position measurements
│   ├── with_noise/             # Data with environmental noise
│   │   ├── p01/                # Position 01 (6 files per position)
│   │   ├── p02/                # Position 02
│   │   └── ...                 # Positions 03-20
│   ├── without_noise/          # Data without environmental noise
│   │   ├── p01/                # Position 01 (6 files per position)
│   │   └── ...                 # Positions 02-20
│   └── visual_tags/            # ArUco marker images and positions
│       ├── combined_aruco_positions.csv  # All ArUco positions
│       ├── p01/                # Position 01 images and calculations
│       └── ...                 # Positions 02-20
└── trajectories/               # Dynamic trajectory data
    ├── raw/                    # Original trajectory recordings
    │   ├── T1/                 # Straight path along X=0 axis
    │   ├── T2/                 # Straight path through center
    │   ├── T3/                 # Straight path along X=2.02 axis
    │   ├── T4/                 # Center path (reverse direction)
    │   ├── T6/                 # Zigzag pattern
    │   └── T8/                 # Random/complex path
    └── processed/              # Processed and split data
        ├── plots/              # Trajectory visualizations
        ├── T1/                 # Processed T1 data (7 files)
        ├── T2/                 # Processed T2 data
        ├── T3/                 # Processed T3 data
        ├── T4/                 # Processed T4 data
        ├── T6/                 # Processed T6 data
        └── T8/                 # Processed T8 data
```

## Dataset Types

### Static Measurements (`static/`)

Static measurements at predefined positions using tripod mounting, similar to offline dataset but with ArUco-based positioning validation.

**Key Features**:
- 20 measurement positions distributed along corridor
- Positions every ~1.4m in Y-axis, randomized X positions
- 2 minutes of data per position
- Two variants: with environmental noise and without noise
- Dual ground truth: laser measurements + ArUco positioning

**Purpose**: 
- Compare ArUco positioning accuracy against laser measurements
- Validate ArUco system before trajectory collection
- Provide static reference points for trajectory calibration

### Dynamic Trajectories (`trajectories/`)

Continuous measurements collected while walking through corridor wearing chest-mounted smartphone.

**Key Features**:
- 6 different trajectory patterns
- Continuous RSSI collection during movement
- ArUco marker detection every 250ms
- Realistic walking scenarios at natural speed

**Purpose**:
- Real-time localization algorithm testing
- Tracking and motion prediction evaluation
- Realistic pedestrian movement patterns

## Trajectory Descriptions

### T1 - Straight Line (X=0 Axis)
**Path**: Straight walk along the wall (X ≈ 0m)  
**Direction**: South to North  
**Characteristics**: 
- Simple linear trajectory
- Close to beacon positions on one side
- Good for baseline tracking performance

### T2 - Straight Center
**Path**: Straight walk through corridor center (X ≈ 1m)  
**Direction**: South to North  
**Characteristics**:
- Balanced beacon visibility
- Optimal signal distribution
- Standard walking pattern

### T3 - Straight Line (X=2.02 Axis)
**Path**: Straight walk along opposite wall (X ≈ 2m)  
**Direction**: South to North  
**Characteristics**:
- Mirror of T1
- Different beacon proximity patterns
- Tests edge positioning accuracy

### T4 - Center Reverse
**Path**: Straight walk through corridor center (X ≈ 1m)  
**Direction**: North to South (reverse of T2)  
**Characteristics**:
- Same path as T2 but opposite direction
- Tests directional dependencies
- Different beacon encounter order

### T6 - Zigzag Pattern
**Path**: Lateral zigzag movements across corridor width  
**Direction**: South to North with lateral movement  
**Characteristics**:
- Complex motion pattern
- Rapid X-coordinate changes
- Tests tracking during direction changes
- Most challenging for tracking algorithms

### T8 - Random/Complex Path
**Path**: Random walking pattern with various movements  
**Direction**: Mixed with turns and stops  
**Characteristics**:
- Natural unpredictable movement
- Variable speed and direction
- Most realistic pedestrian behavior
- Includes pauses and direction changes

## Static Dataset Details

### Sampling Configuration

**Position Distribution**:
- **Y-axis spacing**: Approximately 1.4m intervals
- **X-axis**: Randomized positions within corridor width
- **Z-axis**: Fixed at 1.5m (measurement height)
- **Total positions**: 20 points

**Collection Setup**:
- Device mounted on tripod at 1.5m height
- Position measured with laser distance meter
- ArUco markers captured for position validation
- 2 minutes of continuous RSSI sampling
- 2 seconds initial delay before sampling

**Image Capture**:
- 3 images per capture session
- 5 seconds between consecutive images
- 2 capture sessions per position (total 6 images)
- Images stored in `visual_tags/` directory

### File Naming Convention

Individual beacon files:
```
{MAC_ADDRESS}.csv
```

Aggregated files:
```
all.csv
```

**Directory structure per position**:
```
p01/
├── 68_9E_19_03_95_84.csv    # ALBEACON2 data
├── 68_9E_19_03_95_F1.csv    # ALBEACON1 data
├── AC_23_3F_26_3E_EF.csv    # TUTBEACON3 data
├── AC_23_3F_26_3E_F1.csv    # TUTBEACON1 data
├── AC_23_3F_26_3E_F2.csv    # TUTBEACON2 data
└── all.csv                   # Combined all beacons
```

### Static File Format

CSV files with dual positioning (ArUco + Laser):

| Column          | Type    | Description                              | Unit   |
|-----------------|---------|------------------------------------------|--------|
| `timestamp`     | int64   | Unix timestamp (milliseconds)           | ms     |
| `time`          | string  | Human-readable timestamp                 | -      |
| `mac_address`   | string  | Beacon MAC address                       | -      |
| `rssi`          | int     | Received Signal Strength Indicator      | dBm    |
| `tx_power`      | int     | Transmission power                       | dBm    |
| `aruco_pos_x`   | float   | X position from ArUco detection         | m      |
| `aruco_pos_y`   | float   | Y position from ArUco detection         | m      |
| `aruco_pos_z`   | float   | Z position from ArUco detection         | m      |
| `laser_pos_x`   | float   | X position from laser measurement       | m      |
| `laser_pos_y`   | float   | Y position from laser measurement       | m      |
| `laser_pos_z`   | float   | Z position from laser measurement       | m      |

**Sample Data**:
```csv
timestamp,time,mac_address,rssi,tx_power,aruco_pos_x,aruco_pos_y,aruco_pos_z,laser_pos_x,laser_pos_y,laser_pos_z
1761792236513,2025-10-30 11:43:56.513,AC:23:3F:26:3E:F2,-70,127,1.20,1.35,1.52,1.13,1.4,1.5
```

### Visual Tags Directory

Contains ArUco marker images and position calculations:

**Per Position**:
- Multiple `.matphoto` files (raw image data)
- Multiple `_preview.jpg` files (preview images)
- `aruco_positions_*.csv` files (calculated positions from each image)

**Combined File**:
- `combined_aruco_positions.csv`: All ArUco position calculations across all positions

## Trajectory Dataset Details

### Collection Setup

**Equipment Configuration**:
- Smartphone mounted in chest harness
- Camera facing forward
- BLE scanning active
- Continuous recording during walk

**Collection Protocol**:
1. Mount smartphone in chest harness on subject
2. Position subject at trajectory starting point
3. Configure application:
   - Initial position: (0, 0, 0)
   - Image capture: Every 250ms
   - No time limit
   - 0 seconds initial delay
4. Subject walks predefined trajectory at natural speed
5. Continuous RSSI and image capture
6. Stop at trajectory endpoint

### Trajectory File Naming

**Raw trajectory files** (in `raw/TX/`):
```
0.0_0.0_0.0__{MAC_ADDRESS}.csv
0.0_0.0_0.0__all.csv
image_XXXX_TIMESTAMP.matphoto
image_XXXX_TIMESTAMP_preview.jpg
```

**Processed trajectory files** (in `processed/TX/`):
```
{MAC_ADDRESS}.csv               # Individual beacon data
all.csv                         # Combined beacon data
all_processing_stats.csv        # Processing statistics
```

### Trajectory File Format

CSV files with ArUco-based positioning:

| Column                            | Type    | Description                              | Unit   |
|-----------------------------------|---------|------------------------------------------|--------|
| `timestamp`                       | int64   | Unix timestamp (milliseconds)           | ms     |
| `time`                            | string  | Human-readable timestamp                 | -      |
| `mac_address`                     | string  | Beacon MAC address                       | -      |
| `rssi`                            | int     | Received Signal Strength Indicator      | dBm    |
| `tx_power`                        | int     | Transmission power                       | dBm    |
| `pos_x`                           | float   | X position from ArUco (0 if not detected) | m     |
| `pos_y`                           | float   | Y position from ArUco (0 if not detected) | m     |
| `pos_z`                           | float   | Z position from ArUco (0 if not detected) | m     |
| `position_calculation_timestamp`  | string  | Timestamp of ArUco detection             | -      |
| `position_calculation_status`     | string  | Detection status (e.g., "no_images")     | -      |

**Sample Data**:
```csv
timestamp,time,mac_address,rssi,tx_power,pos_x,pos_y,pos_z,position_calculation_timestamp,position_calculation_status
1762306226188,2025-11-05 10:30:26.188,AC:23:3F:26:3E:F1,-62,127,0.0,0.0,0.0,,no_images
1762306235123,2025-11-05 10:30:35.123,AC:23:3F:26:3E:F1,-65,127,1.15,2.34,1.50,2025-11-05 10:30:35.100,success
```

**Important Notes**:
- `pos_x=0, pos_y=0, pos_z=0` indicates no ArUco marker detected
- Position updates only when ArUco markers are successfully detected
- Gaps between detections represent movement without visual reference

## Data Collection Details

### Static Collection Protocol

1. **Setup Phase**
   - Position tripod at measurement point
   - Measure exact position with laser meter (X, Y coordinates)
   - Record laser measurements as ground truth
   - Mount smartphone on tripod at 1.5m height

2. **Collection Phase**
   - Activate BLE scanning application
   - Configure position and image capture settings
   - 2 seconds initial delay
   - 2 minutes continuous RSSI collection
   - 3 images captured at 5-second intervals

3. **Repetition**
   - Perform 2 collection sessions per position
   - Total: 6 images per position for ArUco validation

4. **Storage**
   - Save RSSI data in position folders (p01-p20)
   - Store images and ArUco calculations in visual_tags/

### Trajectory Collection Protocol

1. **Preparation**
   - Mount smartphone in chest harness
   - Ensure camera has clear forward view
   - Check battery and storage capacity

2. **Trajectory Execution**
   - Position subject at starting point
   - Start application (position set to 0,0,0)
   - Subject walks defined trajectory path
   - Maintain natural walking speed
   - Avoid stopping unless trajectory requires

3. **Data Capture**
   - Continuous BLE scanning
   - Image capture every 250ms
   - Record full trajectory without interruption

4. **Post-Processing**
   - Extract ArUco positions from images
   - Associate positions with RSSI timestamps
   - Split data by beacon MAC address
   - Generate trajectory visualizations

## Processing Tools

### Static Dataset Processing

**ArUco Position Extraction**:
Process images to extract and validate ArUco positions against laser measurements.

**Data Validation**:
```bash
python tools/rssi_dataset_checker.py \
    --working_dir "location 2 - tut corridor/fingerprint/online/static/without_noise/" \
    --mac_filter_file "location 2 - tut corridor/fingerprint/settings/mac_filter_list.json" \
    --room_settings_file "location 2 - tut corridor/fingerprint/settings/room_settings.json"
```

### Trajectory Processing

**Split by Beacon**:
```bash
python tools/trajectory_split.py \
    --csv_file "location 2 - tut corridor/fingerprint/online/trajectories/raw/T1/0.0_0.0_0.0__all.csv" \
    --output_dir "location 2 - tut corridor/fingerprint/online/trajectories/processed/T1/"
```

**Batch Processing**:
```bash
python tools/trajectory_split_all.py
```

**Visualization**:
```bash
python tools/trajectory_plotter.py \
    --csv_file "location 2 - tut corridor/fingerprint/online/trajectories/processed/T1/all.csv" \
    --room_settings_file "location 2 - tut corridor/fingerprint/settings/room_settings.json"
```

## Dataset Statistics

### Static Dataset
- **Total Positions**: 20
- **Files per Position**: 6 (5 individual beacons + 1 combined)
- **Total Files (with_noise)**: 120 CSV files
- **Total Files (without_noise)**: 120 CSV files
- **Images per Position**: 6 (across 2 sessions)
- **Total Images**: 120 per noise condition

### Trajectory Dataset
- **Total Trajectories**: 6 (T1, T2, T3, T4, T6, T8)
- **Files per Trajectory (raw)**: Multiple (RSSI + images)
- **Files per Trajectory (processed)**: 7 (5 beacons + combined + stats)
- **Image Capture Rate**: 250ms (4 Hz)
- **Typical Duration**: 1-3 minutes per trajectory
- **RSSI Samples**: 500-1500 per trajectory

## Known Issues and Limitations

### Static Dataset

**ArUco Detection**:
- Not all images successfully detect markers
- Detection accuracy varies with lighting conditions
- Marker visibility depends on distance and angle

**Position Accuracy**:
- ArUco position has ~2-5cm accuracy
- Laser measurements have ~1-2cm accuracy
- Differences expected between two methods

**Data Collection**:
- Only 20 positions (vs 171 in offline)
- Sparser spatial coverage
- Positions not on regular grid

### Trajectory Dataset

**Position Coverage**:
- Large gaps where no ArUco markers detected
- Position only available at marker locations
- Interpolation needed for continuous tracking

**Movement Artifacts**:
- Motion blur in some images
- Natural speed variation during walking
- Occasional direction uncertainties

**Trajectory Complexity**:
- T6 (zigzag) has most detection challenges
- T8 (random) has irregular sampling
- Simple trajectories (T1-T4) have better coverage

### General Limitations

**Environmental Factors**:
- Lighting variations affect ArUco detection
- People movement creates noise (with_noise variant)
- Time-of-day variations in both datasets

**Equipment Constraints**:
- Single device type (one Android model)
- Harness position may vary slightly
- Camera orientation affects detection

## Usage Recommendations

### For Static Dataset

**ArUco Validation Studies**:
- Compare ArUco vs laser positioning accuracy
- Analyze position estimation errors
- Validate marker-based localization

**Static Positioning**:
- Use as reference points for trajectory calibration
- Benchmark against offline dataset positions
- Evaluate noise impact with dual variants

### For Trajectory Dataset

**Tracking Algorithms**:
- Test particle filters and Kalman filters
- Evaluate motion prediction models
- Compare across different trajectory types

**Trajectory Selection**:
- **T1-T4**: Simple linear paths for basic testing
- **T6**: Complex pattern for robustness testing  
- **T8**: Realistic random movement for real-world simulation

**Missing Position Handling**:
- Implement interpolation for gaps
- Use motion models between detections
- Filter out zero-position records

## Related Files

- `../settings/room_settings.json` - Corridor dimensions and configuration
- `../settings/mac_filter_list.json` - Beacon MAC addresses
- `../settings/beacon_position.csv` - Beacon positions
- `../README.md` - General fingerprint dataset documentation
- `../offline/README.md` - Offline static dataset documentation

## Data Quality Assessment

### High Quality Sections
- **Static positions**: Generally good ArUco detection
- **T1-T4 trajectories**: Linear paths with consistent detection
- **Center corridor**: Better beacon visibility

### Challenging Sections
- **Trajectory gaps**: Areas without ArUco markers
- **T6 zigzag**: Complex motion affects detection
- **T8 random**: Unpredictable path reduces coverage
- **Corridor ends**: Fewer marker opportunities

---

**Collection Period**: October-November 2025  
**Dataset Version**: 2.0  
**Last Updated**: November 21, 2025  
**Total Raw Data Size**: ~2.9 GB (trajectories)
