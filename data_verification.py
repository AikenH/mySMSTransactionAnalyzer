from utils import log_execution
from collections import defaultdict
import math
from datetime import datetime


@log_execution(verbose=True)
def verify_transactions(transactions):
    """
    Verifies the consistency of transaction records by checking the running balance against the reported balance for each account.

    Args:
        transactions (list): The list of transaction details.

    Returns:
        list: The list of transactions with a 'note' field indicating any discrepancies found.
    """
    if not transactions:
        return "No transactions to verify."

    # Group transactions by account number
    transactions_by_account = defaultdict(list)
    for transaction in transactions:
        account_number = transaction['account_number']
        transactions_by_account[account_number].append(transaction)

    # process each account's transactions
    for account_number, account_transactions in transactions_by_account.items():
        # Sort transactions by date for the current account
        account_transactions.sort(key=lambda x: datetime.strptime((x['date']), '%Y-%m-%d'))

        # Initalize starting balance for the current account
        starting_balance = float(account_transactions[0]['balance'])
        running_balance = starting_balance
        first_transaction = True

        for transaction in account_transactions:
            amount = float(transaction['amount'])
            reported_balance = float(transaction['balance'])

            if first_transaction:
                first_transaction = False
                transaction['note'] = ''
            else:
                running_balance += amount
                if not math.isclose(running_balance, reported_balance, rel_tol=1e-5):
                    print(f'Discrepancy found for account {account_number}: running balance is {running_balance} but the reported balance is {reported_balance}.')
                    transaction['note'] = 'number need check, message may miss'
                    running_balance = reported_balance
                else:
                    transaction['note'] = ''
    return transactions
