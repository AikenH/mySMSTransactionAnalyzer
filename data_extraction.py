# data_extraction.py

import os
import re
from utils import log_execution, parse_date, setup_logger


logger = setup_logger()


@log_execution(verbose=False)
def read_and_sort_messages(message_dir, initial_year):
    """
    Reads messages from .txt files in a specified directory, sorts them by date, and returns a list of messages.
    Args:
        message_dir (str): The directory where message files are stored.
        initial_year (int): The initial year to use for parsing dates in messages.
    Returns:
        list: A list of sorted messages with their associated year.
    """
    message_files = [
        file for file in os.listdir(message_dir) if file.endswith('.txt')
    ]
    all_messages = []
    
    for file_name in message_files:
        current_year = initial_year
        last_month = 0
        std_year = 2000
        file_path = os.path.join(message_dir, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                messages = file.readlines()
                for message in messages:
                    # NOTE: 前面会读到一个标准年份，作为年份校准，如果和后面同时都++的时候再添加
                    std_year_match = re.search(r'(\d{4})-', message)
                    if std_year_match:
                        std_year = int(std_year_match.group(1))
                    month_match = re.search(r'(\d+)月', message)
                    if month_match:
                        month = int(month_match.group(1))
                        if month < last_month:
                            current_year += 1
                            if current_year > std_year:
                                current_year = std_year
                        last_month = month
                        all_messages.append((message, current_year))
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
        except Exception as e:
            logger.error(f"An error occurred while processing {file_name}: {e}")
    return sorted(all_messages, key=lambda msg: parse_date(re.search(r'\d+月\d+日', msg[0]).group(), msg[1]))


@log_execution(verbose=False)
def extract_messages(messages, keywords):
    """
    Extracts messages that contain any of the specified keywords.
    Args:
        messages (list): The list of messages to search through.
        keywords (list): The list of keywords to search for in messages.
    Returns:
        list: A list of messages that contain any of the keywords.
    """
    return [message for message in messages if any(keyword in message[0] for keyword in keywords)]


@log_execution(verbose=False)
def extract_details(messages):
    """
    Extracts detailed information from messages, including date, account number, transaction type, amount, balance, and bank name.
    Args:
        messages (list): The list of messages to extract details from.
    Returns:
        list: A list of dictionaries, each containing the details of a transaction.
    """
    details = []
    for message, year in messages:
        # Extracting date
        date = parse_date(re.search(r'\d+月\d+日', message).group(), year)

        # Extracting account number
        account_number_match = re.search(r'(\d+账户|账户\d+|\d+公司账户|\d+个人账户)', message)
        if not account_number_match:
            account_number_match = re.search(r'尾号(\d+)', message)
        # Extracting the digits from the match
        if account_number_match:
            # Removing "账户" to get only the account number
            account_number = re.search(r'\d+', account_number_match.group(0)).group(0)
        else:
            account_number = ' '

        # Extracting objects using regular expressions
        object1_match = re.search(r'(.+?)于', message)
        object2_match = re.search(r'向(.+?)完成', message)
        object1 = object1_match.group(1) if object1_match else f"您尾号{account_number}账户"
        object2 = object2_match.group(1) if object2_match else ' '
        try:
            amount = re.search(r'(?:收入|支出|人民币|金额为)((?:-)?\d+\.\d{2})(?:元|人民币)?', message).group(1)
        except AttributeError:
            try:
                amount = re.search(r'金额为((?:-)?\d+\.\d{2})', message).group(1)
            except AttributeError:
                amount = re.search(r'(收入|支出)((?:-)?\d+\.\d{2})(人民币|元)', message).group(2)

        try:
            balance = re.search(r'余额(\d+\.\d{2})', message).group(1)
        except AttributeError:
            balance = '0.00'

        # Extracting transaction type, amount and balance
        if '收入' in message or '转存' in message or '结息' in message:
            transaction_type = 'income'
            amount_sign = '+'
        elif '支出' in message or '支付支取' in message or '转支' in message or '通知存款交易' in message or '-' in amount:
            transaction_type = 'outcome'
            amount_sign = '-'
        else:
            transaction_type = 'income'
            amount_sign = ''
        # Extracting bank name, ensuring it ends with '银行'
        bank_name_match = re.search(r'【(.*?)】|\[(.*?银行)\]', message)
        bank_name = bank_name_match.group(1) or bank_name_match.group(2) if bank_name_match else 'Unknown'
        amount = f"{amount_sign}{amount}" if (amount != 'Unknown' and '-' not in amount) else amount

        details.append({
            'date': date.strftime('%Y-%m-%d'),
            'object1': object1,
            'object2': object2,
            'account_number': account_number,
            'type': transaction_type,
            'amount': amount,
            'balance': balance,
            'bank_name': bank_name,
        })

    return details
