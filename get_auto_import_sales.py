# -*- coding: utf-8 -*-
import requests
import argparse
import json
import csv

# Set Parameters
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', action='store_true', help='Enable Test Mode')

args = parser.parse_args()

if args.test:
    range_year = list(range(2018, 2019))
    range_month = list(range(7, 9))
else:
    range_year = list(range(2003, 2019))
    range_month = list(range(1, 13))

iteration = 0
auto_sales_list = []

for year in range_year:
    for month in range_month:
        date_string = '{0:d}{1:02d}'.format(year, month)
        response = requests.post("https://www.kaida.co.kr/ko/statistics/AnalysisStatisticsAjax.do", {
            'programId': 515,
            'searchStart': int(date_string),
            'baseYear': year
        })
        auto_sales = json.loads(response.text)

        for auto_sale in auto_sales['jsonChart']:
            if iteration == 0:
                data = {
                    'brandId': auto_sale['brandId'],
                    'brandName': auto_sale['brandName'],
                    date_string: auto_sale['thisYearThisMon']
                }
                auto_sales_list.append(data)

            else:
                for item in auto_sales_list:
                    if item['brandId'] == auto_sale['brandId']:
                        item.update({
                            date_string: auto_sale['thisYearThisMon']
                        })
                    continue
        iteration = iteration + 1
        print('{0} : {1}th iteration is on progress...'.format(date_string, iteration))

keys = auto_sales_list[0].keys()
with open('auto_import_sales.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(auto_sales_list)
