#!/usr/bin/env python3
# pylint
# vim: tw=100 foldmethod=indent
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy, logging-format-interpolation
# pylint: disable=missing-docstring, trailing-whitespace, trailing-newlines, too-few-public-methods

import sys
from datetime import date, datetime, timedelta
import math
import json
import pandas as pd
import numpy as np
import argparse
from urllib.error import HTTPError

from datetime import date
day = (date.today())
day = str(day)
day = day[-2:]
day = int(day)

class Animation():
    animation = []
    animation.append ("\_(O_0)_/")
    animation.append ("|_(0_O)_/")
    animation.append ("/_(o_0)_/")
    animation.append ("-_(*_O)_/")
    animation.append ("\_(-_0)_/")
    animation.append ("|_(*_O)_/")
    animation.append ("/_(o_0)_/")
    animation.append ("-_(0_O)_/")
    animation.append ("\_(O_0)_/")
    animation.append ("|_(O_o)_|")
    animation.append ("/_(0_O)_\\")
    animation.append ("-_(0_0)_|")
    animation.append ("\_(0_O)_/")
    def __init__(self):
        self.anim_id=0
    def step(self):
        rv =self. animation[self.anim_id]
        self.anim_id += 1
        if self.anim_id >= len(self.animation):
            self.anim_id=0
        return rv

def parseOptions():
    '''Parse the commandline options'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action="count", default=0, help='Verbosity')
    parser.add_argument('--john', '-jhc', help='''Path to data of CSSE Data of Johns Hopkins.
            This may be a git clone of https://github.com/CSSEGISandData/COVID-19
            or the url https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/''',
            default='../CSSEGISandData/COVID-19')
            # default='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master')
    parser.add_argument('--rki', '-rki', help='''Path to data of German RKI Data
            This may be a git clone of this repository 
            or the url https://raw.githubusercontent.com/marcvs/Coronavirus/master/rki-fallzahlen''',
            default='rki-fallzahlen')
            # default='https://raw.githubusercontent.com/marcvs/Coronavirus/master/rki-fallzahlen')
    return parser

def try_parsing_date(text):
    for fmt in ('%m/%d/%y %H:%M', '%m/%d/%Y %H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError(F'no valid date format found: >>{text}<<')


args = parseOptions().parse_args()

sys.stdout.write("Reading data:       ")
sys.stdout.flush()
data = str(date.today())
# base_path_cs = '/home/marcus/github/covid-19/CSSEGISandData/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports'
# base_path_de = 'rki-fallzahlen'
base_path_cs = args.john
base_path_de = args.rki
path_list = []

# https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports
# Jan
for d in range(22, 32):
    path_list.append (str(base_path_cs+f'/csse_covid_19_data/csse_covid_19_daily_reports/01-{d}-2020.csv'))
# Feb
for d in range(1, 30):
    path_list.append (str(base_path_cs+f'/csse_covid_19_data/csse_covid_19_daily_reports/02-{d:02}-2020.csv'))
    if d >= 28:
        path_list.append (str(base_path_de+f'/2020-02-{d:02}.csv'))
# Mar
for d in range(11, 31):
    path_list.append (str(base_path_cs+f'/csse_covid_19_data/csse_covid_19_daily_reports/03-{d:02}-2020.csv'))
    path_list.append (str(base_path_de+f'/2020-03-{d:02}.csv'))
# Apr
for d in range(11, day+1):
    path_list.append (str(base_path_cs+f'/csse_covid_19_data/csse_covid_19_daily_reports/04-{d:02}-2020.csv'))
    path_list.append (str(base_path_de+f'/2020-04-{d:02}.csv'))

csv_list = []
for d in path_list:
    try:
        if args.verbose:
            print (F"Load from {d}")
        else:
            sys.stdout.write('.')
            sys.stdout.flush()
        dates = pd.read_csv(d)
        np.array(dates)
        csv_list.append(dates)
    except FileNotFoundError:
        if args.verbose:
            print (F"\n  Could not read {d}")
        pass
    except HTTPError:
        if args.verbose:
            print (F"\n  Could not read {d}")
        pass

# print (csv_list[10])
# print (csv_list[40].head())
# exit(0)
# print(csv_list[40][50:100])
# Find country indices:
categories    = ['Confirmed','Deaths', 'Recovered', 'Last Update']
colors        = {'Confirmed': '#ddddff', 'Deaths': '#ffbbbb', 'Recovered': '#bbffbb'}
colors_diff   = {'Confirmed': '#bbbbff', 'Deaths': '#ff2222', 'Recovered': '#22ff22'}
colors_e      = {'Confirmed': '#8899dd', 'Deaths': '#ffbbff', 'Recovered': '#23ffff'}
colors_diff_e = {'Confirmed': '#22aadd', 'Deaths': '#ff22ff', 'Recovered': '#bbffff'}
countries = { 
        'Albania': ['Main'],
        'Austria': ['Main'],
        'Belgium': ['Main'],
        'Bosnia and Herzegovina': ['Main'],
        'Croatia': ['Main'],
        'Cyprus': ['Main'],
        'Czechia': ['Main'],
        'Estonia': ['Main'],
        'Finland': ['Main'],
        'France': ['France', 'Main'],
        'Germany': [
            'Main',
            'Gesamt',
            'Baden-Württemberg',
            'Bayern',
            'Berlin',
            'Brandenburg',
            'Bremen',
            'Hamburg',
            'Hessen',
            'Mecklenburg-Vorpommern',
            'Niedersachsen',
            'Nordrhein-Westfalen',
            'Rheinland-Pfalz',
            'Saarland',
            'Sachsen',
            'Sachsen-Anhalt',
            'SchleswigHolstein',
            'Thüringen'],
        'eGermany': [
            'Gesamt',
            'Baden-Württemberg',
            'Bayern',
            'Berlin',
            'Brandenburg',
            'Bremen',
            'Hamburg',
            'Hessen',
            'Mecklenburg-Vorpommern',
            'Niedersachsen',
            'Nordrhein-Westfalen',
            'Rheinland-Pfalz',
            'Saarland',
            'Sachsen',
            'Sachsen-Anhalt',
            'SchleswigHolstein',
            'Thüringen'],
        # 'Germany': ['Main', 'Gesamt', 'Baden-Württemberg'],
        # 'eGermany': ['Main', 'Gesamt', 'Baden-Württemberg'],
        'Greece': ['Main'],
        'Hungary': ['Main'],
        'Iceland': ['Main'],
        'Iran': ['Main'],
        'Ireland': ['Main'],
        'Italy': ['Main'],
        'Japan': ['Main'],
        'Korea, South': ['Main'],
        'South Korea': ['Main'],
        'Kosovo': ['Main'],
        'Luxembourg': ['Main'],
        'Malta': ['Main'],
        'Monaco': ['Main'],
        'Netherlands': ['Main', 'Netherlands'],
        'Norway': ['Main'],
        'occupied Palestinian territory': ['Main'],
        'Poland': ['Main'],
        'Portugal': ['Main'],
        'Romania': ['Main'],
        'Russia': ['Main'],
        'Serbia': ['Main'],
        'Slovenia': ['Main'],
        'Spain': ['Main'],
        'Switzerland': ['Main'],
        'Turkey': ['Main'],
        'Ukraine': ['Main'],
        'United Kingdom': ['United Kingdom', 'Gibraltar'],
}
# countries = {'Germany': '', 'United Kingdom':['Cayman Islands', 'Gibraltar']}
# countries = ['Germany']

print (" done")
sys.stdout.write("initialising:       ")
sys.stdout.flush()

country_list = {}
country_diff = {}

# init data structures 
for country in countries:
    sys.stdout.write('-')
    sys.stdout.flush()
    # print (F"Country: {country}")
    country_list[country]  = {}
    country_diff[country]  = {}
    for region in countries[country]:
        # print (F" Region: {region}")
        country_list[country][region] = {}
        country_list[country][region] = {}
        country_diff[country][region] = {}
        for cat in categories:
            country_list[country][region][cat]=[]
            country_diff[country][region][cat]=[]

print (" done")

anim = Animation()

# Preprocess to reflect changes in data structure at Johns':
for d in range(0,len(csv_list)):
    try:
        csv_list[d]['Province/State'] = csv_list[d]['Province_State']
    except KeyError:
        pass

    try:
        csv_list[d]['Country/Region'] = csv_list[d]['Country_Region']
    except KeyError:
        pass

    try:
        csv_list[d]['Last Update'] = csv_list[d]['Last_Update']
    except KeyError:
        pass

    try:
        csv_list[d]['Long'] = csv_list[d]['Long_']
    except KeyError:
        pass



# exit (0)

sys.stdout.write("restructuring data\n")
sys.stdout.flush()
# copy data from csv_list into plotable countries_list
# Province/State,   Country/Region, Last Update,    Confirmed,  Deaths, Recovered,  Latitude,   Longitude
# FIPS, Admin2, Province_State, Country_Region, Last_Update,    Lat,    Long_,  Confirmed,  Deaths, Recovered,  Active, Combined_Key
for d in range(0,len(csv_list)):
    sys.stdout.write(F'\r{anim.step()}')
    sys.stdout.flush()
    for country in countries:
        for region in countries[country]:
            # sys.stdout.write(f'{d}:{country}/{region}\n')
            for csv_country in range (0,len(csv_list[d])):
                if country == csv_list[d]['Country/Region'][csv_country]:
                    prov_state = csv_list[d]['Province/State'][csv_country]
                    if (region == prov_state) or \
                        ((region == 'Main') and (type(prov_state) != type (""))):
                        for cat in categories:
                            if cat == 'Last Update':
                                # print (F"Processing: {csv_list[d][cat][csv_country]}")
                                date = try_parsing_date(csv_list[d][cat][csv_country])
                                country_list[country][region][cat].append(date)
                            else:
                                country_list[country][region][cat].append(csv_list[d][cat][csv_country])
            # print (F"  len({country}.{region}.{cat}): {len(country_list[country][region][cat])}")

# country_diff = country_list

sys.stdout.write ("\n                    ")
sys.stdout.flush()
global_max = {}
german_max = {}
for cat in categories:
    global_max[cat] = 0
    german_max[cat] = 0
# create diffs and find global max:
for country in countries:
    sys.stdout.write(F'\r{anim.step()}')
    sys.stdout.flush()
    for region in countries[country]:
        for cat in ['Confirmed', 'Deaths', 'Recovered']:
            country_diff[country][region][cat].append(0)
            for i in range(1,len(country_list[country][region][cat])):
                # find max
                a           = country_list[country][region][cat][i]
                b           = country_list[country][region][cat][i-1]
                # print (f"a: {a}")
                if math.isnan(b):
                    # print (f"b country: {country}/{region}-{cat}-{i} a: {a} b: {b}")
                    b=0
                if math.isnan(a):
                    # print (f"a country: {country}/{region}-{cat}-{i} a: {a} b:{b}")
                    a=0

                if global_max[cat] < a:
                    global_max[cat] = a
                if country in ['Germany', 'eGermany'] and region not in ['Main', 'Gesamt']:
                    if german_max[cat] < a:
                        german_max[cat] = a
                # do the diff thing
                delta       = a - b
                lu          = country_list[country][region]['Last Update'][i]
                time_a      = country_list[country][region]['Last Update'][i]
                time_b      = country_list[country][region]['Last Update'][i-1]
                # timedelta = timedelta(time_a, time_b)
                timedelta   = time_a - time_b
                if timedelta.total_seconds() != 0:
                    delta_corr  = delta * (24*60*60) / timedelta.total_seconds()
                    # if cat in ['Confirmed', 'Deaths']:
                        # print(F"{lu}:  {cat:10}   {a:4} - {b:4} = {delta:4} (timedelta: {timedelta.total_seconds()/(24*60*60):8}) => {delta_corr:8}")
                    if delta_corr != 0:
                        country_diff[country][region][cat].append(delta_corr)
                    else:
                        country_diff[country][region][cat].append(country_diff[country][region][cat][-1])
                else: # Division by Zero
                    country_diff[country][region][cat].append(delta)



print (" done")
sys.stdout.write("generating plots:   \n")
sys.stdout.flush()
# show statistics
# for country in countries:
#     for region in countries[country]:
#         print (F"{country}/{region}: {country_list[country][region]['Confirmed'][-1]}")
#         cat = 'Last Update'
#         # print (F"    len: {len(country_list[country][region][cat])}")
# #         print (F"    len diff {cat}: {len(country_diff[country][region][cat])}")

list_dead = []
list_conf = []
list_surv = []

# Compute totals:
for d in range(0,len(csv_list)):
    list_dead.append((csv_list[d]['Deaths']).sum())
    list_conf.append((csv_list[d]['Confirmed']).sum())
    list_surv.append((csv_list[d]['Recovered']).sum())

# PLOT 
import matplotlib.pyplot as plt
from matplotlib import dates

# plt.style.use('seaborn-talk')
plt.style.use('classic')
# plt.plot(x, list_dead, color='red', label='Dead', linewidth=1.0)
# plt.plot(x, list_conf, color='green', label='Confirmed', linewidth=1.0)
# plt.plot(x, list_surv, color='blue', label='Cured', linewidth=1.0)
for country in countries:
    if country == 'eGermany':
        # print ("skipping eGermany")
        continue
    for region in countries[country]:
        sys.stdout.write(F'\r{anim.step()}')
        sys.stdout.flush()

        # set y axis limit
        fig = plt.gcf()
        # fig.set_size_inches(19.2,12.0)
        fig.set_size_inches(23.62,15.245)
        fig.autofmt_xdate(rotation=45)

        ax = fig.gca()
        y_max = ax.get_ylim()[1]
        # ax.set_ylim([-y_max/100, y_max])
        ax.set_ylim([0, global_max['Confirmed']])
        # if country in ['Germany', 'eGermany']:
        if country in ['Germany', 'eGermany'] and region not in ['Main', 'Gesamt']:
            ax.set_ylim([0, german_max['Confirmed']])
        # ax.set_ylim([0, y_max])

        if region != 'Main':
            # print (F"{country}/{region}")
            plt.title(F'{country}/{region} Virus development')
        else:
            # print (F"{country}")
            plt.title(F'{country} Virus development')

        x = dates.date2num(country_list[country][region]['Last Update'])
        for cat in ['Confirmed', 'Deaths', 'Recovered']:
            plt.plot_date(x, country_list[country][region][cat], fmt='o-', 
                    color=colors[cat], label=F'{cat} (total)', linewidth=2.0)
        for cat in ['Confirmed', 'Deaths']:
            plt.plot_date(x, country_diff[country][region][cat], fmt='o-', 
                    color=colors_diff[cat], label=F'{cat} (new)', linewidth=2.0)
        if country == 'Germany' and not region == 'Main':
            x_e = dates.date2num(country_list['eGermany'][region]['Last Update'])
            for cat in ['Confirmed', 'Deaths', 'Recovered']:
                plt.plot_date(x_e, country_list['eGermany'][region][cat], fmt='P-', 
                        color=colors_e[cat], label=F'{cat} (total,e))', linewidth=2.0)
            for cat in ['Confirmed', 'Deaths']:
                plt.plot_date(x_e, country_diff['eGermany'][region][cat], fmt='P-', 
                        color=colors_diff_e[cat], label=F'{cat} (new,e)', linewidth=2.0)

        # plt.xlabel('D')
        plt.xticks(rotation=45)
        plt.ylabel('Cases')

        plt.grid(True)
        plt.legend(loc='upper center')

        country_no_spaces = country.replace(" ", "-").replace(",","-")

        if region != 'Main':
            plt.savefig(F'{country_no_spaces}-{region}.jpg', bbox_inches='tight')
        else:
            plt.savefig(F'{country_no_spaces}.jpg', bbox_inches='tight')
        plt.close()
        # plt.show()
print (" done")
