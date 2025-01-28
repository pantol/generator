#!/usr/bin/env python3

import csv
import random
import datetime

def generate_random_date(start_date, end_date):
    return start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))

def generate_invoices(csv_file, nip, num_invoices, prefix_inv, start_date, end_date, start_date_wymg, end_date_wymg, currency_list):
    used_invoice_numbers = set()
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['#SOF', str(datetime.date.today()), '1'])
        
        currency_iter = iter(currency_list)
        
        for i in range(num_invoices):
            invoice_number = random.randint(1, num_invoices * 10)
            while invoice_number in used_invoice_numbers:
                invoice_number = random.randint(1, num_invoices * 10)
            used_invoice_numbers.add(invoice_number)
            
            waluta = next(currency_iter)
            
            writer.writerow([
                nip,
                f"{prefix_inv}{invoice_number}",
                generate_random_date(start_date, end_date),
                generate_random_date(start_date_wymg, end_date_wymg),
                waluta,
                1000,  # Brutto
                0,     # VAT
                1000   # saldo_faktury
            ])
            
            if (i + 1) % 100 == 0:
                print(f"Generated {i + 1} invoices")
        
        writer.writerow(['#EOF', str(num_invoices)])

def main():
    # Get single NIP
    nip = input("Enter the single NIP to use: ").strip()
    while len(nip) != 10 or not nip.isdigit():
        print("NIP must be 10 digits")
        nip = input("Enter the single NIP to use: ").strip()

    num_invoices = int(input("Enter total number of invoices to generate: "))
    
    # Collect currency distribution
    currencies = []
    total_specified = 0
    while True:
        curr_input = input("Enter currency code (or 'done' to finish): ").strip().upper()
        if curr_input == 'DONE':
            break
        if not curr_input:
            print("Currency cannot be empty.")
            continue
        try:
            count = int(input(f"Enter number of invoices for {curr_input}: "))
        except ValueError:
            print("Invalid number. Please enter an integer.")
            continue
        if count < 0:
            print("Count cannot be negative.")
            continue
        if total_specified + count > num_invoices:
            print(f"Total specified invoices ({total_specified + count}) exceeds total needed ({num_invoices}).")
            continue
        currencies.append((curr_input, count))
        total_specified += count
        if total_specified == num_invoices:
            break

    # Handle remaining invoices if any
    if total_specified < num_invoices:
        remaining = num_invoices - total_specified
        default_curr = input(f"Enter default currency for remaining {remaining} invoices: ").strip().upper()
        currencies.append((default_curr, remaining))

    # Build and shuffle currency list
    currency_list = []
    for curr, cnt in currencies:
        currency_list.extend([curr] * cnt)
    random.shuffle(currency_list)

    generate_invoices(
        "dataOneDebtMultiCurr.csv",
        nip,
        num_invoices,
        input('Enter invoice prefix: ') + '/',
        datetime.datetime.strptime(input('Start date for invoice dates (YYYY-MM-DD): '), '%Y-%m-%d').date(),
        datetime.datetime.strptime(input('End date for invoice dates (YYYY-MM-DD): '), '%Y-%m-%d').date(),
        datetime.datetime.strptime(input('Start date for due dates (YYYY-MM-DD): '), '%Y-%m-%d').date(),
        datetime.datetime.strptime(input('End date for due dates (YYYY-MM-DD): '), '%Y-%m-%d').date(),
        currency_list
    )

    print(f"CSV file 'single_nip_invoices.csv' generated with {num_invoices} invoices for NIP: {nip}")

if __name__ == "__main__":
    main()