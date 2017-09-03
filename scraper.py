#!/usr/bin/env python
# Dublin Bikes scraper
import pandas as pd
import requests
import time 
import json
import pywapi
import sqlite3
import os

def getStationData(dt):
    """
    Scrapes Dublin Bikes JSON station data, returns free bikes at each station
    (column) with time as row index in a pandas dataframe
    """
    #grabs the current info for all Dublin Bikes from citybikes API
    station_data =  pd.read_json("http://api.citybik.es/dublinbikes.json")
    # Set columns to names
    station_data = station_data.set_index('name')
    # Transpose data frame
    station_data =  station_data[['bikes']].transpose()
    # Add time as row index name
    station_data.index = [dt]
    # Formats the station names (columns) appropriately for pandas
    station_data.columns = [col.replace(" ","_") for col in station_data]
    return station_data

def getWeatherData(dt):
    """
    Scrapes weather.com for "Dublin's current in pandas dataframe
    """
    weather_result = pywapi.get_weather_from_weather_com("EIXX0014") 
    return pd.DataFrame([[dt,
                            str(weather_result['current_conditions']['text']), \
                            str(weather_result['current_conditions']['temperature']), \
                            str(weather_result['current_conditions']['feels_like']), \
                            str(weather_result['current_conditions']['wind']['speed']) \
                            ]], \

                        columns=['Time','Weather','Temperature','Feels_Like','Wind_Speed'])

def fileWrite(today, bikes, weather, form='sqlite'):
    """
    Write weather and station data to a CSV or sql db file
    """
    if form == 'CSV':
        bikes.to_csv('bikes_'+today+'.csv', header=False, mode="a")
        weather.to_csv('weather_'+today+'.csv', header=False, mode="a", \
                                                 index = False)
    elif form == 'sqlite':
        con = sqlite3.connect(today+'_bikes_and_weather.db')
        bikes.to_sql('bikes', con, if_exists='append')
#        print weather
        weather.to_sql('weather', con, if_exists='append', index = False)
    else:
        print 'Incompatible file type' 

if __name__ == "__main__":
 
    while True:
        try:
            # Define global datetime of scraping 
            theDate = time.strftime("%Y-%m-%d")
            theTime = time.strftime("%H:%M:%S") 
            # Date
    
            df_bikes = getStationData(theTime)
            df_weather = getWeatherData(theTime)
     
            fileWrite(theDate,df_bikes,df_weather)
            print "Data scraped successfully at " + theTime

        except Exception as e: print(e)
        
        time.sleep(120)

