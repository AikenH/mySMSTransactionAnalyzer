# Financial Transaction Analyzer

## Overview

The Financial Transaction Analyzer is a Python-based tool designed to process, analyze, and report financial transactions extracted from bank SMS messages. It aims to provide a detailed understanding of an individual's or organization's financial activity by categorizing transactions into income and expenses, ensuring data integrity, and generating comprehensive reports.

## Features

- **Data Extraction**: Processes SMS messages to extract transaction data, including date, account number, transaction type, amount, balance, and associated bank.
- **Transaction Verification**: Verifies the consistency of transactions by comparing running balances with reported balances, flagging any discrepancies for review.
- **Report Generation**: Generates CSV files for each account, providing a structured view of all transactions, useful for further analysis or record-keeping.
- **Logging and Monitoring**: Includes detailed logging for monitoring the process and debugging potential issues.

## Project Structure

- `config.py`: Handles reading of configuration settings.
- `utils.py`: Provides utility functions and logging setup.
- `data_extraction.py`: Contains functions for reading, sorting, and extracting data from message files.
- `report_generation.py`: Responsible for generating CSV reports.
- `data_verification.py`: Contains logic for verifying transaction consistency.
- `main.py`: The main script that orchestrates the entire process.

## Usage

1. **Configuration**: Set up the `config.yaml` file with the appropriate parameters, including the message directory, initial year, and output directory.
2. **Running the Analyzer**: Execute the `main.py` script to start the process. The script reads the messages, extracts transaction details, verifies the data integrity, and generates CSV reports.

## Requirements

- Python 3.x
- PyYAML

## Installation

1. Clone the repository:
2. Install the required packages:

```shell
pip install -r requirements.txt
```

## Contributing

Contributions to the Financial Transaction Analyzer are welcome. Please feel free to report any issues or suggest enhancements through the issue tracker.

## FI

this readme file generate by chatgpt. thx a lot.