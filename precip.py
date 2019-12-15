#!/usr/bin/env python

import csv
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
csv_name = os.getenv('csv_name')

def main():
  data = {}

  with open(csv_name, mode='r') as handle:
    csv_reader = csv.DictReader(handle)

    [process_row(data, row) for row in csv_reader]
    calc_totals(data)
    round_values(data)
    print_table(data)

def process_row(data, row):
  if row['precipType'] != 'rain':
    return

  date_parts = row['date'].split('-')
  
  year = date_parts[0]
  month = date_parts[1]

  if year not in data:
    data[year] = {}
  if month not in data[year]:
    data[year][month] = 0.0

  data[year][month] += float(row['precipIntensity'])*24

def calc_totals(data):
  for year in data:
    total = 0.0
    for month in data[year]:
      total += data[year][month]
    data[year]['total'] = total

def round_values(data):
  for year in data:
    for month in data[year]:
      data[year][month] = round(data[year][month], 1)

def print_table(data):
  print('Year   Jan   Feb   Mar   Apr   May   Jun   Jul   Aug   Sep   Oct   Nov   Dec   Tot')
  years = list(data.keys())
  years.sort()
  for year in years:
    print(f'{year}  ', end='')
    for i in range(1,13):
      month = str(i).zfill(2)
      val = data[year].get(month)
      if val is None:
        val = 0.0
      val = str(val)
      val = val.rjust(4)
      print(f'{val}  ', end='')
    print(data[year]['total'])


if __name__== "__main__":
  main()
