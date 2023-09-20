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
        nvoice_number = random.randint(start, end)
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
    csv_file = 'data.csv'

    column_headers = ["Nip_Dluznika", "Numer_faktury", "Data_wystawienia_faktury","Data_wymg", "waluta", "Brutto", "VAT", "saldo_faktury"]

    limit_2 = int(input('wpisz ile faktur ma sie wygenerowac w pliku: '))
    print("wpisz zakres do generowania unikalnch numerow faktur")
    limit_inv_1 = int(input('zakres poczatkowy do generowania: '))
    limit_inv_2 = int(input('zakres koncowy do generowania: '))
    print("podany prefix bedzie ustawiony dla wszystkich faktur do tego zostanie dodana wylosowana wartosc z generatora numerow")
    prefix_inv = str(input("podaj prefix dla faktur w pliku: ")) + '/'
    start_date_str = input('zakres poczatkowy dat wystawienia faktur (YYYY-MM-DD): ')
    end_date_str = input('zakres koncowy dat wystawienia faktur (YYYY-MM-DD): ')
    start_date_wymg_str = input('zakres poczatkowy dat wymagalnosci faktur (YYYY-MM-DD): ')
    end_date_wymg_str = input('zakres koncowy dat wymagalnosci faktur (YYYY-MM-DD): ')
    waluta_faktur = str(input('wpisz walute faktury:')).upper()
    nip = int(input('wpisz nip dluznika: '))

    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()

    start_date_wymg = datetime.datetime.strptime(start_date_wymg_str, '%Y-%m-%d').date()
    end_date_wymg = datetime.datetime.strptime(end_date_wymg_str, '%Y-%m-%d').date()

    first_row = ['#SOF', str(datetime.date.today()), "1"] 
    add_row(first_row,csv_file)

    count = 0

    while count < limit_2:
        data = []
        for column in range((len(column_headers))):
#            match column:
#                case 0:
#                    value = nip
#                    break
            if column == 0:
                value = nip # nip dluznika
            elif column == 1:
                value = prefix_inv + str(generate_random_invoice_number(limit_inv_1, limit_inv_2)) # generacje nr faktur
            elif column == 2:
                value = generate_random_date_wys(start_date, end_date) # generacja dat wystawienia 
            elif column == 3:
                value = generate_random_date_wymg(start_date_wymg, end_date_wymg) # generacja dat wymagalnosci
            elif column == 4:
                value = waluta_faktur # wartosc waluty    
            elif column == 5:
                #value = generate_random_bruto() # generacja kwot
                value = 100
            elif column == 6:   
                #value = generate_random_vat() # genracje kwot vat
                value = 0
            elif column == 7:
                value = 100
            else:
                value = ''

            data.append(value)
        add_row(data, csv_file)
        count += 1

    last_row = ['#EOF', str(limit_2)] 
    add_row(last_row,csv_file)

    print(f"Plik CSV '{csv_file}' wygenerowany.")

if __name__ == "__main__":
    main()
