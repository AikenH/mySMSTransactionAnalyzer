import csv
import os
from utils import log_execution, setup_logger
from collections import defaultdict

logger = setup_logger()


@log_execution(verbose=True)
def generate_csv_files(transactions, output_dir):
    """
    Generates CSV files for transactions, grouped by account number.
    Each account's transactions are written to a separate CSV file.

    Args:
        transactions (list): The list of transaction details.
        output_dir (str): The directory where the CSV files will be saved.
    """
    transactions_by_account = defaultdict(list)
    for transaction in transactions:
        account_number = transaction['account_number']
        transactions_by_account[account_number].append(transaction)

    for account_number, account_transactions in transactions_by_account.items():
        file_path = os.path.join(output_dir, f'{account_number}.csv')
        try:
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.DictWriter(file, fieldnames=account_transactions[0].keys())
                writer.writeheader()
                writer.writerows(account_transactions)
        except IOError as e:
            logger.error(f"IO error occurred while writing to {file_path}: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
