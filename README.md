# Statistical Data Profiler

A clean, standalone Python tool for automated statistical profiling, descriptive metrics, and anomaly detection from numerical datasets and CSV files.

## Features

- **Central Tendency**: Mean, median.
- **Dispersion & Spread**: Variance (sample & population), standard deviation, range, IQR.
- **Percentiles & Quartiles**: Linear interpolation for Q1, Q2 (median), and Q3.
- **Distribution Shape**: Fisher-Pearson coefficient of skewness.
- **Outlier & Anomaly Detection**:
  - Tukey's Interquartile Range (IQR) fence rule ($Q_1 - 1.5 \times \text{IQR}$, $Q_3 + 1.5 \times \text{IQR}$).
  - Z-Score thresholding ($|z| \ge 2.5$).
- **Multi-Column CSV Parsing**: Automatically skips non-numeric values and extracts all numerical series.
- **Data Export**: Saves detailed analytical profiles into formatted JSON files.

## Project Structure

```text
profiler/
├── __init__.py
├── stats.py
├── reader.py
├── reporter.py
├── main.py
├── sample_data.csv
├── README.md
└── tests/
    ├── __init__.py
    └── test_stats.py
```

## Usage

### 1. Run on Sample Dataset

```bash
python -m profiler.main
```

### 2. Profile a Specific CSV File

```bash
python -m profiler.main profiler/sample_data.csv
```

### 3. Profile a Single Column from a CSV

```bash
python -m profiler.main profiler/sample_data.csv --column exam_score
```

### 4. Direct Numerical Input via Command Line

```bash
python -m profiler.main --data "12, 14, 15, 12, 19, 100, 14, 13"
```

### 5. Export Analytical Summary to JSON

```bash
python -m profiler.main profiler/sample_data.csv --output report.json
```

## Running Tests

```bash
pytest profiler/tests
```

