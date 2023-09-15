#!/usr/bin/env python3

import csv
import random
import datetime

generate_random_invoice_numbers = set()

def generate_random_invoice_number(*args):
    if len(args) < 2:
        raise ValueError("wymagane dwa argumenty")
    start,end = min(args), max(args)

    while True:
        invoice_number = random.randint(start, end)
        if invoice_number not in generate_random_invoice_numbers:
            generate_random_invoice_numbers.add(invoice_number) 
            return invoice_number

def generate_random_bruto():
    return random.randint(200, 10000)

def generate_random_vat():
    return random.randint(10, 199)

def generate_random_date_wys(start_date, end_date):
    time_difference = end_date - start_date
    random_days = random.randint(0, time_difference.days)
    random_date = start_date + datetime.timedelta(days=random_days)
    return random_date

def generate_random_date_wymg(start_date_wymg, end_date_wymg):
    time_difference_wymg = end_date_wymg - start_date_wymg
    random_days_wymg = random.randint(0, time_difference_wymg.days)
    random_date_wymg = start_date_wymg + datetime.timedelta(days=random_days_wymg) 
    return random_date_wymg


def add_row(data, csv_file):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter= ';')
        writer.writerow(data)

def main():
    csv_file = "data.csv"
    
    column_headers = ["Nip_Dluznika", "Numer_faktury", "Data_wystawienia_faktury","Data_wymg", "waluta", "Brutto", "VAT"]

    limit = 25
    #limit_2 = int(input('enter the limit of rows to be generated: '))
    print("wpisz zakres do generowania unikalnch numerow faktur")
    limit_inv_1 = int(input('zakres poczatkowy do generowania: '))
    limit_inv_2 = int(input('zakres koncowy do generowania: '))

    start_date = datetime.date(2026, 9, 11)
    end_date = datetime.date(2026, 9, 21)

    start_date_wymg = datetime.date(2028, 10, 5)
    end_date_wymg = datetime.date(2028, 10, 15)

    count = 0
    
    while count < limit:
        data = []
        for column in range((len(column_headers))):
            if column == 4:
                value = 'PLN' # wartosc stala waluty
            elif column == 5:
                value = generate_random_bruto() # generacja kwot
            elif column == 2:
                value = generate_random_date_wys(start_date, end_date) # generacja dat
            elif column == 0:
                value = '1111111' # nip dluznika staly
            elif column == 1:
                value = generate_random_invoice_number(limit_inv_1, limit_inv_2) # generacje nr faktur
            elif column == 6:   
                value = generate_random_vat() # genracje kwot vat
            elif column == 3:
                value = generate_random_date_wymg(start_date_wymg, end_date_wymg) # albo generator
            else:
                value = ''

            data.append(value)
        add_row(data, csv_file)
        count += 1
    
    print(f"CSV file '{csv_file}' generated with data.")

if __name__ == "__main__":
    main()

