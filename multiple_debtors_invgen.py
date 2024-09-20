#!/usr/bin/env python3

import csv
import random
import datetime

generate_random_invoice_numbers = set()

def generate_random_invoice_number(*args: int):
    if len(args) < 2:
        raise ValueError("wymagane dwa argumenty")
    start,end = min(args), max(args)

    while True:
        invoice_number = random.randint(start, end)
        if invoice_number not in generate_random_invoice_numbers:
            generate_random_invoice_numbers.add(invoice_number) 
            return invoice_number

def generate_random_bruto(): return random.randint(200, 10000)

def generate_random_vat(): return random.randint(10, 199)

def generate_random_date(start_date, end_date):
    time_difference = end_date - start_date
    random_days = random.randint(0, time_difference.days)
    random_date = start_date + datetime.timedelta(days=random_days)
    return random_date

def add_row(data, csv_file):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter= ';')
        writer.writerow(data)

def generate_invoices(csv_file, nip, num_invoices, prefix_inv, start_date, end_date, start_date_wymg, end_date_wymg, waluta_faktur, limit_inv_1, limit_inv_2):
    for _ in range(num_invoices):
        data = [
            nip,
            prefix_inv + str(generate_random_invoice_number(limit_inv_1, limit_inv_2)),
            generate_random_date(start_date, end_date),
            generate_random_date(start_date_wymg, end_date_wymg),
            waluta_faktur,
            1000,  # Brutto
            0,     # VAT
            1000   # saldo_faktury
        ]
        add_row(data, csv_file)

def main():
    csv_file = "data19092.csv"
    column_headers = ["Nip_Dluznika", "Numer_faktury", "Data_wystawienia_faktury","Data_wymg", "waluta", "Brutto", "VAT", "saldo_faktury"]
    
    total_invoices = int(input('Wpisz całkowitą liczbę faktur do wygenerowania: '))
    limit_inv_1 = int(input('Zakres początkowy do generowania: '))
    limit_inv_2 = int(input('Zakres końcowy do generowania: '))
    
    # Maximum number of unique invoices that can be generated based on the range
    max_possible_uniq_invoices = limit_inv_2 - limit_inv_1 + 1
    
    # Ask for the maximum number of invoices per NIP
    max_invoices_per_nip = int(input(f'Wpisz maksymalną liczbę faktur do wygenerowania dla każdego NIP (max {max_possible_uniq_invoices}): '))
    
    # Ensure max_invoices_per_nip is not greater than the possible range
    max_invoices_per_nip = min(max_invoices_per_nip, max_possible_uniq_invoices)
    
    prefix_inv = str(input('Podaj prefix dla faktur w pliku: ')) + '/'
    start_date_str = input('Zakres początkowy dat wystawienia faktur (YYYY-MM-DD): ')
    end_date_str = input('Zakres końcowy dat wystawienia faktur (YYYY-MM-DD): ')
    start_date_wymg_str = input('Zakres początkowy dat wymagalności faktur (YYYY-MM-DD): ')
    end_date_wymg_str = input('Zakres końcowy dat wymagalności faktur (YYYY-MM-DD): ')
    waluta_faktur = str(input('Wpisz walutę faktury: ')).upper()

    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
    start_date_wymg = datetime.datetime.strptime(start_date_wymg_str, '%Y-%m-%d').date()
    end_date_wymg = datetime.datetime.strptime(end_date_wymg_str, '%Y-%m-%d').date()

    first_row = ['#SOF', str(datetime.date.today()), '1']
    add_row(first_row, csv_file)

    invoices_generated = 0
    while invoices_generated < total_invoices:
        nip = int(input('Wpisz NIP dłużnika: '))
        num_invoices = min(max_invoices_per_nip, total_invoices - invoices_generated)
        generate_invoices(csv_file, nip, num_invoices, prefix_inv, start_date, end_date, start_date_wymg, end_date_wymg, waluta_faktur, limit_inv_1, limit_inv_2)
        invoices_generated += num_invoices
        print(f"Wygenerowano {invoices_generated} faktur z {total_invoices}")
        
        if invoices_generated < total_invoices:
            continue_input = input("Naciśnij Enter, aby kontynuować z kolejnym NIP, lub wpisz 'q' aby zakończyć: ")
            if continue_input.lower() == 'q':
                break

    last_row = ['#EOF', str(invoices_generated)]
    add_row(last_row, csv_file)

    print(f"Plik CSV '{csv_file}' wygenerowany z {invoices_generated} fakturami.")

if __name__ == "__main__":
    main()