# TUT Corridor - Online Fingerprint Dataset

This directory contains dynamic BLE RSSI fingerprint measurements collected during movement through the TUT corridor, using ArUco markers for ground truth positioning.

## Dataset Overview

**Collection Methods**: 
- Static positioning with ArUco validation (20 positions)
- Dynamic trajectory sampling (two collection takes)

**Ground Truth**: ArUco marker-based visual positioning  
**Total Positions (Static)**: 20 measurement points  
**Total Trajectories**: 
- Take 1: 6 trajectories (T1, T2, T3, T4, T6, T8) with 32 ArUco markers
- Take 2: 8 trajectories (T1, T2, T3, T4, T6, T6-2, T6-3, T6-4) with 52 ArUco markers  
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
    ├── take1/                  # Original collection (November 2025)
    │   ├── raw/                # Original trajectory recordings
    │   │   ├── T1/             # Straight path along X=0 axis
    │   │   ├── T2/             # Straight path through center
    │   │   ├── T3/             # Straight path along X=2.02 axis
    │   │   ├── T4/             # Center path (reverse direction)
    │   │   ├── T6/             # Zigzag pattern
    │   │   └── T8/             # Random/complex path
    │   └── processed/          # Processed and split data
    │       ├── plots/          # Trajectory visualizations
    │       ├── T1/             # Processed T1 data (7 files)
    │       ├── T2/             # Processed T2 data
    │       ├── T3/             # Processed T3 data
    │       ├── T4/             # Processed T4 data
    │       ├── T6/             # Processed T6 data
    │       └── T8/             # Processed T8 data
    └── take2/                  # Enhanced collection (December 2025)
        ├── raw/                # Original trajectory recordings
        │   ├── T1/             # Straight path along X=0 axis
        │   ├── T2/             # Straight path through center
        │   ├── T3/             # Straight path along X=2.02 axis
        │   ├── T4/             # Center path (reverse direction)
        │   ├── T6/             # Zigzag with turning while advancing
        │   ├── T6-2/           # Zigzag with combined translation + rotation
        │   ├── T6-3/           # Static rotation then forward movement
        │   └── T6-4/           # Static rotation then forward movement
        └── processed/          # Processed and split data
            ├── plots/          # Trajectory visualizations
            ├── T1/             # Processed T1 data
            ├── T2/             # Processed T2 data
            ├── T3/             # Processed T3 data
            ├── T4/             # Processed T4 data
            ├── T6/             # Processed T6 data (T6-1)
            ├── T62/            # Processed T6-2 data
            ├── T63/            # Processed T6-3 data
            └── T64/            # Processed T6-4 data
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

Continuous measurements collected while walking through corridor wearing chest-mounted smartphone. Collected in two takes with different ArUco marker configurations.

**Take 1 (November 2025)**:
- 6 trajectory patterns (T1, T2, T3, T4, T6, T8)
- 32 ArUco markers distributed across 11 positions
- Original collection for method validation

**Take 2 (December 2025)**:
- 8 trajectory patterns focusing on rotational movement
- 52 ArUco markers distributed across 21 positions
- Enhanced coverage for improved position detection
- Removed T8 (random) in favor of structured T6 variants
- Four T6 variants exploring rotation dynamics:
  - T6 and T6-2: Turning while advancing (rotation during forward motion)
  - T6-3 and T6-4: Stopping to rotate (stop at wall, rotate in place, then advance)

**Key Features**:
- Continuous RSSI collection during movement
- ArUco marker detection every 250ms
- Realistic walking scenarios at natural speed

**Purpose**:
- Real-time localization algorithm testing
- Tracking and motion prediction evaluation
- Realistic pedestrian movement patterns
- Analysis of rotational movement effects (Take 2)

## Trajectory Descriptions

### Common Trajectories (Both Take 1 and Take 2)

### T1 - Straight Line (X=0 Axis)
**Path**: Straight walk along the wall (X ≈ 0m)  
**Direction**: South to North  
**Available in**: Take 1, Take 2  
**Characteristics**: 
- Simple linear trajectory
- Close to beacon positions on one side
- Good for baseline tracking performance

### T2 - Straight Center
**Path**: Straight walk through corridor center (X ≈ 1m)  
**Direction**: South to North  
**Available in**: Take 1, Take 2  
**Characteristics**:
- Balanced beacon visibility
- Optimal signal distribution
- Standard walking pattern

### T3 - Straight Line (X=2.02 Axis)
**Path**: Straight walk along opposite wall (X ≈ 2m)  
**Direction**: South to North  
**Available in**: Take 1, Take 2  
**Characteristics**:
- Mirror of T1
- Different beacon proximity patterns
- Tests edge positioning accuracy

### T4 - Center Reverse
**Path**: Straight walk through corridor center (X ≈ 1m)  
**Direction**: North to South (reverse of T2)  
**Available in**: Take 1, Take 2  
**Characteristics**:
- Same path as T2 but opposite direction
- Tests directional dependencies
- Different beacon encounter order

### T6 - Zigzag Pattern (Turning While Advancing)
**Path**: Lateral zigzag movements across corridor width  
**Direction**: South to North with lateral movement  
**Available in**: Take 1, Take 2
**Characteristics**:
- Complex motion pattern with rotation during forward motion
- Rapid X-coordinate changes
- Subject turns while continuing to advance
- Tests tracking during direction changes
- Most challenging for tracking algorithms

### Take 1 Specific Trajectories

### T8 - Random/Complex Path (Take 1)
**Path**: Random walking pattern with various movements  
**Direction**: Mixed with turns and stops  
**Available in**: Take 1 only  
**Characteristics**:
- Natural unpredictable movement
- Variable speed and direction
- Most realistic pedestrian behavior
- Includes pauses and direction changes

### Take 2 Specific Trajectories

### T6-2 - Zigzag Pattern Bis (Turning While Advancing) (Take 2)
**Path**: Lateral zigzag movements across corridor width  
**Direction**: South to North with lateral movement  
**Available in**: Take 2
**Characteristics**:
- Complex motion pattern with rotation during forward motion
- Similar to T6 but second collection run
- Rapid X-coordinate changes
- Subject turns while continuing to advance
- Tests tracking during simultaneous translation and rotation

### T6-3 - Zigzag Stopping to Rotate (Take 2)
**Path**: Zigzag pattern where subject stops at wall to rotate before advancing  
**Direction**: South to North with lateral movement, stopping at walls to rotate  
**Available in**: Take 2 only  
**Characteristics**:
- Two-phase motion at each turn: stop, rotate in place, then advance
- No rotation during forward movement (unlike T6 and T6-2)
- Sequential motion phases (rotation and translation separated)
- Tests algorithm handling of motion mode transitions
- Clear separation between rotational and translational phases
- Evaluates impact of stopping to reorient on tracking accuracy

### T6-4 - Zigzag Stopping to Rotate Bis (Take 2)
**Path**: Zigzag pattern where subject stops at wall to rotate before advancing  
**Direction**: South to North with lateral movement, stopping at walls to rotate  
**Available in**: Take 2 only  
**Characteristics**:
- Two-phase motion at each turn: stop, rotate in place, then advance
- Similar to T6-3 but second collection run
- No rotation during forward movement (unlike T6 and T6-2)
- Sequential motion phases (rotation and translation separated)
- Tests algorithm handling of motion mode transitions
- Evaluates repeatability of stop-rotate-advance pattern

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

**Raw trajectory files** (in `take1/raw/TX/` or `take2/raw/TX/`):
```
0.0_0.0_0.0__{MAC_ADDRESS}.csv
0.0_0.0_0.0__all.csv
image_XXXX_TIMESTAMP.matphoto
image_XXXX_TIMESTAMP_preview.jpg
```

**Processed trajectory files** (in `take1/processed/TX/` or `take2/processed/TX/`):
```
{MAC_ADDRESS}.csv               # Individual beacon data
all.csv                         # Combined beacon data
all_processing_stats.csv        # Processing statistics
```

**Note**: In Take 2 raw data, T6 variants are stored as:
- `T6/` for T6-1 
- `T6-2/` for T6-2 
- `T6-3/` for T6-3 
- `T6-4/` for T6-4 

In Take 2 processed data, these become `T6/`, `T62/`, `T63/`, and `T64/` respectively.

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

**Split by Beacon (Take 1 example)**:
```bash
python tools/trajectory_split.py \
    --csv_file "location 2 - tut corridor/fingerprint/online/trajectories/take1/raw/T1/0.0_0.0_0.0__all.csv" \
    --output_dir "location 2 - tut corridor/fingerprint/online/trajectories/take1/processed/T1/"
```

**Split by Beacon (Take 2 example)**:
```bash
python tools/trajectory_split.py \
    --csv_file "location 2 - tut corridor/fingerprint/online/trajectories/take2/raw/T1/0.0_0.0_0.0__all.csv" \
    --output_dir "location 2 - tut corridor/fingerprint/online/trajectories/take2/processed/T1/"
```

**Batch Processing**:
```bash
python tools/trajectory_split_all.py
```

**Visualization (Take 1)**:
```bash
python tools/trajectory_plotter.py \
    --csv_file "location 2 - tut corridor/fingerprint/online/trajectories/take1/processed/T1/all.csv" \
    --room_settings_file "location 2 - tut corridor/fingerprint/settings/room_settings.json"
```

**Visualization (Take 2)**:
```bash
python tools/trajectory_plotter.py \
    --csv_file "location 2 - tut corridor/fingerprint/online/trajectories/take2/processed/T1/all.csv" \
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

### Trajectory Dataset - Take 1
- **Total Trajectories**: 6 (T1, T2, T3, T4, T6, T8)
- **ArUco Markers**: 32 baseline markers
- **Files per Trajectory (raw)**: Multiple (RSSI + images)
- **Files per Trajectory (processed)**: 7 (5 beacons + combined + stats)
- **Image Capture Rate**: 250ms (4 Hz)
- **Typical Duration**: 1-3 minutes per trajectory
- **RSSI Samples**: 500-1500 per trajectory

### Trajectory Dataset - Take 2
- **Total Trajectories**: 8 (T1, T2, T3, T4, T6, T6-2, T6-3, T6-4)
- **ArUco Markers**: 52 markers across 21 positions
- **Files per Trajectory (raw)**: Multiple (RSSI + images)
- **Files per Trajectory (processed)**: 7 (5 beacons + combined + stats)
- **Image Capture Rate**: 250ms (4 Hz)
- **Typical Duration**: 1-3 minutes per trajectory
- **RSSI Samples**: 500-1500 per trajectory
- **Improved Detection**: Significantly higher position coverage compared to Take 1

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
- **Take 1**: Large gaps where no ArUco markers detected (32 markers)
- **Take 2**: Improved coverage with 52 markers
- Position only available at marker locations
- Interpolation needed for continuous tracking

**Movement Artifacts**:
- Motion blur in some images
- Natural speed variation during walking
- Occasional direction uncertainties

**Trajectory Complexity**:
- **Take 1**: T6 (zigzag) and T8 (random) have most detection challenges
- **Take 2**: Better overall detection due to more markers
- **Take 2**: T6-3 and T6-4 have deliberate stationary phases for rotation analysis
- Simple trajectories (T1-T4) have better coverage in both takes

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

**Take Selection**:
- **Take 1**: Original dataset for baseline comparison, includes T8 random path
- **Take 2**: Enhanced coverage with 52 markers for improved position accuracy
- **Both Takes**: Common trajectories (T1-T4) for cross-validation and comparison

**Trajectory Selection**:
- **T1-T4**: Simple linear paths for basic testing (both takes)
- **T6 (Take 1 & Take 2)**: Zigzag turning while advancing
- **T6-2 (Take 2)**: Zigzag turning while advancing (repeat run)
- **T6-3 (Take 2)**: Zigzag stopping to rotate - sequential motion phases
- **T6-4 (Take 2)**: Zigzag stopping to rotate - sequential motion phases (repeat run)
- **T8 (Take 1)**: Realistic random movement for real-world simulation

**Rotational Movement Analysis (Take 2)**:
- Compare T6/T6-2 (rotation during motion) vs T6-3/T6-4 (stop to rotate)
- Study simultaneous translation+rotation (T6, T6-2) vs sequential phases (T6-3, T6-4)
- Analyze impact of stopping to reorient on tracking accuracy
- Evaluate motion mode transition handling in stop-rotate-advance patterns
- Compare repeatability between first and second runs of each variant

**Missing Position Handling**:
- Implement interpolation for gaps
- Use motion models between detections
- Filter out zero-position records
- **Take 2**: Fewer gaps due to increased marker density

## Related Files

- `../settings/room_settings.json` - Corridor dimensions and configuration
- `../settings/mac_filter_list.json` - Beacon MAC addresses
- `../settings/beacon_position.csv` - Beacon positions
- `../README.md` - General fingerprint dataset documentation
- `../offline/README.md` - Offline static dataset documentation

## Data Quality Assessment

### High Quality Sections
- **Static positions**: Generally good ArUco detection
- **T1-T4 trajectories (both takes)**: Linear paths with consistent detection
- **Take 2 trajectories**: Significantly improved marker coverage
- **Center corridor**: Better beacon visibility

### Challenging Sections
- **Take 1 trajectory gaps**: Areas without ArUco markers (32 markers in 11 positions)
- **Take 1 T6 zigzag**: Complex motion with rotation during advance affects detection
- **Take 1 T8 random**: Unpredictable path reduces coverage
- **Take 2**: Fewer gaps with 52 markers in 21 positions but still present between positions
- **Corridor ends**: Fewer marker opportunities in both takes
- **Take 2 T6-3, T6-4**: Stop-rotate-advance pattern may show different RSSI patterns during stationary rotation phases

---

**Collection Period**: 
- Static dataset: October 2025
- Take 1 trajectories: November 2025
- Take 2 trajectories: December 2025  
**Dataset Version**: 2.1  
**Last Updated**: December 12, 2025  
**Total Raw Data Size**: 
- Take 1: ~2.9 GB (6 trajectories)
- Take 2: ~2.5+ GB (8 trajectories)
