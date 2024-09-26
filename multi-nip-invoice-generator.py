#!/usr/bin/env python3

import csv
import random
import datetime

def generate_random_invoice_number(start, end, used_numbers):
    while True:
        invoice_number = random.randint(start, end)
        if invoice_number not in used_numbers:
            used_numbers.add(invoice_number)
            return invoice_number

def generate_random_date(start_date, end_date):
    time_difference = end_date - start_date
    random_days = random.randint(0, time_difference.days)
    return start_date + datetime.timedelta(days=random_days)

def add_row(data, csv_file):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(data)

def generate_invoices(csv_file, nip, num_invoices, prefix_inv, start_date, end_date, start_date_wymg, end_date_wymg, waluta_faktur, limit_inv_1, limit_inv_2, used_invoice_numbers):
    for _ in range(num_invoices):
        invoice_number = generate_random_invoice_number(limit_inv_1, limit_inv_2, used_invoice_numbers)
        data = [
            nip,
            f"{prefix_inv}{invoice_number}",
            generate_random_date(start_date, end_date),
            generate_random_date(start_date_wymg, end_date_wymg),
            waluta_faktur,
            1000,  # Brutto
            0,     # VAT
            1000   # saldo_faktury
        ]
        add_row(data, csv_file)

def get_nips():
    choice = input("Do you want to (1) read NIPs from a file or (2) use a hardcoded list? Enter 1 or 2: ")
    if choice == "1":
        file_path = input("Enter the path to the file containing NIPs (one NIP per line): ")
        with open(file_path, 'r') as file:
            return [line.strip() for line in file]
    else:
        # Replace this list with your actual 10,000 NIPs if you choose to hardcode them
        return [
            "1234567890",
            "2345678901",
            "3456789012",
            # ... add all 10,000 NIPs here ...
            "9876543210"
        ]

def main():
    csv_file = "data_10000_nips.csv"
    invoices_per_nip = 7

    nips = get_nips()
    total_nips = len(nips)
    if total_nips != 10000:
        print(f"Warning: The number of NIPs provided ({total_nips}) is not 10,000.")
        proceed = input("Do you want to proceed? (y/n): ")
        if proceed.lower() != 'y':
            return

    # Input parameters
    prefix_inv = input('Podaj prefix dla faktur w pliku: ') + '/'
    start_date = datetime.datetime.strptime(input('Zakres początkowy dat wystawienia faktur (YYYY-MM-DD): '), '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(input('Zakres końcowy dat wystawienia faktur (YYYY-MM-DD): '), '%Y-%m-%d').date()
    start_date_wymg = datetime.datetime.strptime(input('Zakres początkowy dat wymagalności faktur (YYYY-MM-DD): '), '%Y-%m-%d').date()
    end_date_wymg = datetime.datetime.strptime(input('Zakres końcowy dat wymagalności faktur (YYYY-MM-DD): '), '%Y-%m-%d').date()
    waluta_faktur = input('Wpisz walutę faktury: ').upper()
    
    limit_inv_1 = 1
    limit_inv_2 = total_nips * invoices_per_nip

    first_row = ['#SOF', str(datetime.date.today()), '1']
    add_row(first_row, csv_file)

    used_invoice_numbers = set()
    invoices_generated = 0

    for nip in nips:
        generate_invoices(csv_file, nip, invoices_per_nip, prefix_inv, start_date, end_date, start_date_wymg, end_date_wymg, waluta_faktur, limit_inv_1, limit_inv_2, used_invoice_numbers)
        invoices_generated += invoices_per_nip

        if invoices_generated % 10000 == 0:
            print(f"Wygenerowano {invoices_generated} faktur z {total_nips * invoices_per_nip}")

    last_row = ['#EOF', str(invoices_generated)]
    add_row(last_row, csv_file)

    print(f"Plik CSV '{csv_file}' wygenerowany z {invoices_generated} fakturami dla {total_nips} unikalnych NIP-ów.")

if __name__ == "__main__":
    main()
