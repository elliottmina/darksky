#!/usr/bin/env python

import csv
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
csv_name = os.getenv('csv_name')

iters = 0;

def main():
  data = {}

  with open(csv_name, mode='r') as handle:
    global iters
    iters = 0;

    csv_reader = csv.DictReader(handle)

    [process_row(data, row) for row in csv_reader]
    round_values(data)
    pprint(data)

def process_row(data, row):
  global iters
  iters += 1
  if iters > 100:
    return

  if row['precipType'] != 'rain':
    return

  date_parts = row['date'].split('-')
  
  year = date_parts[0]
  month = date_parts[1]

  if year not in data:
    data[year] = {}
  if month not in data[year]:
    data[year][month] = 0.0

  data[year][month] += float(row['precipIntensity'])

def round_values(data):
  for year in data:
    for month in data[year]:
      data[year][month] = round(data[year][month], 1)


if __name__== "__main__":
  main()
