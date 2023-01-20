#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 23:33:22 2023

@author: cybergenLab


functions library 
"""

import pandas as pd
import requests 
import io 


def get_data(url):
    download = requests.get(url).content
    data = pd.read_csv(io.StringIO(download.decode('utf-8')))
    return data 


def wide_transform(df, lastcol, variable, values):
    transform = pd.melt(df, id_vars= df.columns[:lastcol], 
                        value_vars = df.columns[lastcol:], 
                        var_name = variable, 
                        value_name = values)
    return transform
    

def check_name(col1, col2):
    for name in col1:
        if name not in col2: 
            print(name)
    
def format_date(col1):
    date_transform = pd.to_datetime(col1).dt.strftime("%Y-%m-%d")
    return date_transform
    
def covid_formatting(df,df1, country, variable, lat, long):
    #Aggregate country number from different provinces
    confirmed_country = df[df['Country/Region'] == country].groupby('date').sum()[[variable]]
    
    #Template creation with only the country ticker 
    country_template = df1[df1['Country/Region'] == country]
    country_template = country_template[country_template.columns[:-2]].reset_index(drop=True)
    country_template = country_template.drop(columns=['UID', 'Province_State'])
    for x in range(len(country_template)): 
        country_template['Lat'] = lat
        country_template['Long'] =long
    
    confirmed_country = country_template.merge(confirmed_country, how= 'inner', left_on='date', right_index=True)
 
    df = df[df['Country/Region'] != country]
    df = df.append(confirmed_country)
       
    return df 


def save_excel(link, df1, df2, df3):
    writer = pd.ExcelWriter(link)
    df1.to_excel(writer, sheet_name='Covid')
    df2.to_excel(writer, sheet_name='Vaccine')
    df3.to_excel(writer, sheet_name='Population')
    writer.save()
    return print('Data save to excel file')






#---------------------------------------------------
    #TESTING
#---------------------------------------------------

if __name__ == "__main__":

    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    
#   get_data test
    test = get_data(url)

#   wideTransform test 
    test_transform = wide_transform(test, 4, 'date', 'confirmed')
    
#    check_name test
#    check_name(test_transform['Country/Region'], ['Province/State']) 
    
#    check format_date
    test_transform['date'] = format_date(test_transform['date'])

#   check vaccine formatting 
    test_transform = vaccine_formatting(test_transform, df3, 'Canada', 'confirmed', 56.1304, -106.3468)

#   check save_excel
    save_excel(link, test_transform, test1, confirmed_canada)








