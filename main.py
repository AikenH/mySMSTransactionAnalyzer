from config import read_config_file
from data_extraction import read_and_sort_messages, extract_messages, extract_details
from report_generation import generate_csv_files, calculate_monthly_totals, plot_monthly_totals
from data_verification import verify_transactions

if __name__ == "__main__":
    config = read_config_file()

    sorted_messages = read_and_sort_messages(config['message_dir'], config['initial_year'])
    bank_messages = extract_messages(sorted_messages, config['keywords'])
    transactions = extract_details(bank_messages)

    verified_transactions = verify_transactions(transactions)
    generate_csv_files(verified_transactions, config['output_dir'])

    # monthly_totals = calculate_monthly_totals(transactions)
    # plot_monthly_totals(monthly_totals, config['output_dir'])
