#!/usr/bin/env python

# TODO: auto discover header rows

import requests
import csv
from datetime import timedelta, date
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()
apikey = os.getenv('darksky_api_key')
lat_long = os.getenv('lat_long')
csv_name = os.getenv('csv_name')

start_date = date(2009, 1, 1)
finish_date = date(2018, 1, 1)

expected_keys = 'apparentTemperatureHigh','apparentTemperatureHighTime','apparentTemperatureLow','apparentTemperatureLowTime','apparentTemperatureMax','apparentTemperatureMaxTime','apparentTemperatureMin','apparentTemperatureMinTime','cloudCover','dewPoint','humidity','icon','moonPhase','ozone','precipIntensity','precipIntensityMax','precipIntensityMaxTime','precipProbability','precipType','pressure','summary','sunriseTime','sunsetTime','temperatureHigh','temperatureHighTime','temperatureLow','temperatureLowTime','temperatureMax','temperatureMaxTime','temperatureMin','temperatureMinTime','time','uvIndex','uvIndexTime','visibility','windBearing','windGust','windGustTime','windSpeed'

def main():

  print(f'Starting download of {start_date} - {finish_date}')
  create_header = not os.path.isfile(csv_name)

  with open(csv_name, 'a') as file:
    writer = csv.writer(file, delimiter = ',')

    if create_header:
      header_row = ('date',) + expected_keys
      writer.writerow(header_row)

    for currday in daterange(start_date, finish_date):
      datestr = currday.strftime("%Y-%m-%d")

      response = fetch(datestr)
      if response.status_code != 200:
        print(f'Failed to get {datestr}')
        continue

      write(datestr, response, writer)

def daterange(start_date, finish_date):
  for n in range(int ((finish_date - start_date).days)):
    yield start_date + timedelta(n)

def fetch(datestr):
  time = f'{datestr}T00:00:00'
  url = f'https://api.darksky.net/forecast/{apikey}/{lat_long},{time}?exclude=currently,minutely,hourly,alerts,flags'
  return requests.get(url)

def write(datestr, response, writer):
  data = response.json()
  values = extract_values(data['daily']['data'][0])
  writer.writerow([datestr,] + values)

def extract_values(dict):
  return [dict.get(key) for key in expected_keys]

if __name__== "__main__":
  main()
