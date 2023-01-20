#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 16:22:26 2023

@author: goudurix


Covid Map data preprocessing 
"""


import os 
path = "YOUR PATH"
os.chdir(path)

from functions import * 
import pandas as pd 


#Dowloading the covid csv file from the public csse_covid_19_time_series repo 

#Download of the Covid19 confirmed cases dataset
url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
df = get_data(url)
confirmed = wide_transform(df, 4, 'date', 'confirmed')
confirmed['date'] = format_date(confirmed['date'])



#Download of the Covid19 deaths dataset 
url= "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
df = get_data(url)
deaths = wide_transform(df, 4, 'date', 'death')
deaths['date'] = format_date(deaths['date'])

#Download of the Covid19 vaccination dataset 
url= "https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/global_data/time_series_covid19_vaccine_global.csv"
vaccine = get_data(url)
vaccine.rename(columns= {'Country_Region':'Country/Region', 'Date':'date'}, inplace = True)

#Download of the population data from Worldbank dataset
population = pd.read_csv('Population.csv')
population = population[['Country Name', '2021']]
population.rename(columns= {'2021' : 'country population'}, inplace = True)


#Preprocessing Confirmed & Deaths dataset in order to add missing countries total
#List of missing countries: Australia, Canada, China, Denmark, France, Netherlands, New Zealand, United Kingdom 

#Confirmed dataset 
confirmed = covid_formatting(confirmed,vaccine, 'Australia', 'confirmed', -35.4735, 149.0124)
confirmed = covid_formatting(confirmed,vaccine, 'Canada', 'confirmed', 56.1304, -106.3468)
confirmed = covid_formatting(confirmed,vaccine, 'China', 'confirmed', 40.1824, 116.4142)
confirmed = covid_formatting(confirmed,vaccine, 'Denmark', 'confirmed', 56.2639, 9.5018)
confirmed = covid_formatting(confirmed,vaccine, 'France', 'confirmed', 46.2276, 2.2137)
confirmed = covid_formatting(confirmed,vaccine, 'Netherlands', 'confirmed', 52.1326, 5.2913)
confirmed = covid_formatting(confirmed,vaccine, 'New Zealand', 'confirmed', -40.9006, 174.886)
confirmed = covid_formatting(confirmed,vaccine, 'United Kingdom', 'confirmed', 55.3781, -3.436)

#Deaths dataset 
deaths = covid_formatting(deaths,vaccine, 'Australia', 'death', -35.4735, 149.0124)
deaths = covid_formatting(deaths,vaccine, 'Canada', 'death', 56.1304, -106.3468)
deaths = covid_formatting(deaths,vaccine, 'China', 'death', 40.1824, 116.4142)
deaths = covid_formatting(deaths,vaccine, 'Denmark', 'death', 56.2639, 9.5018)
deaths = covid_formatting(deaths,vaccine, 'France', 'death', 46.2276, 2.2137)
deaths = covid_formatting(deaths,vaccine, 'Netherlands', 'death', 52.1326, 5.2913)
deaths = covid_formatting(deaths,vaccine, 'New Zealand', 'death', -40.9006, 174.886)
deaths = covid_formatting(deaths,vaccine, 'United Kingdom', 'death', 55.3781, -3.436)

#Preprocessing country names in the Population dataset 

#Checking for mismatching country names
for c in population['Country Name'].unique():
    if c not in vaccine['Country/Region'].unique(): 
        print(c)

#Correcting country names
        
country_mapper = {
        'Bahamas, The':  'Bahamas',

        'Egypt, Arab Rep.' : 'Egypt' ,
        
        'Gambia, The' : 'Gambia' ,
        
        'Iran, Islamic Rep.' : 'Iran',
        
        'Korea, Rep.' : 'Korea, South' ,
        
        'St. Lucia' : 'Saint Lucia' ,
        
        'St. Kitts and Nevis' : 'Saint Kitts and Nevis',
        
        'Slovak Republic' : 'Slovakia',
        
        'Syrian Arab Republic' : 'Syria',
        
        'Turkiye' : 'Turkey',
        
        'United States' : 'US',
        
        'St. Vincent and the Grenadines' : 'Saint Vincent and the Grenadines', 
        
        'Venezuela, RB' : 'Venezuela' ,
        
        'Congo, Dem. Rep.' : 'Congo (Kinshasa)',
        
        'Congo, Rep.' : 'Congo (Brazzaville)', 
        
        'Russian Federation': 'Russia'
        }

population['Country Name'] = population['Country Name'] .replace(country_mapper)


#Tables creation 

#Creation of the Covid19 Cases table
Cases = confirmed.merge(deaths, on=['Country/Region', 'Province/State', 'date', 'Lat', 'Long'])

#Creation of the Vaccine table
Vaccine = confirmed.merge(vaccine, on=['Country/Region', 'date'])



#Creation of the excel file 

link= "YOUR PATH/DataSet.xlsx"
save_excel(link, Cases, Vaccine, population)


















