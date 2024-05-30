# Snapshot Util

## Description

Snapshot Util is a simple system monitoring tool that takes snapshots of your system's state at configurable intervals and outputs the results to a JSON file and the console.

## Installation

1. Clone the repository or download the package.
2. Navigate to the package directory and install it using pip:

    ```bash
    pip install -U .
    ```

## Usage

Run the `snapshot` command with optional arguments:

```bash
snapshot -i <interval> -f <output_file> -n <snapshot_count>

