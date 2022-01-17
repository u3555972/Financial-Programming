#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 20:23:14 2021

@author: Chan Cheuk Hang 3035559725

Project to compare the distance between the closest 7-11 and Circle K only in 
Hong Kong Island. After, compare the opening hours to see if they match, 
then map it out.
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import os
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point

def scrapeSeven11():
    
    '''
    This function is used to scrape the 7-11 stores website to find the location,
    address, whether or not it's 24 hours, opening hours from mon-fri and sat
    if not 24 hours
    '''
    columns = ['Location', 'Address', '24 Hours', 'Mon-Fri', 'Sat', 'Latitude', 'Longitude']
    website_path = 'https://www.7-eleven.com.hk/en/store'
    browser.get(website_path)
    # Only take Hong Kong Island 7-11s
    browser.find_element(By.XPATH, '/html/body/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/a[1]').click()
    
    counter = 0
    df_scraped = pd.DataFrame()
    
    # Web Scrape 7-11 Address and Opening Hours
    while counter <= 4:
        if counter == 0:
            info = browser.find_elements(By.XPATH, '//*[@id="list-section"]/div[position()>=1]/div/div[1]/h3')
            data = pd.Series([x.text for x in info])
            df_scraped[columns[counter]] = data
        elif counter == 1:
            info = browser.find_elements(By.XPATH, '//*[@id="list-section"]/div[position()>=1]/div/div[1]/div[1]')
            data = pd.Series([x.text for x in info])
            df_scraped[columns[counter]] = data
        elif counter == 2:
            info = browser.find_elements(By.XPATH, '//*[@id="list-section"]/div[position()>=1]/div/div[1]/div[2]/div[1]')
            data = pd.Series([x.text for x in info])
            df_scraped[columns[counter]] = data
        elif counter == 3:
            info = browser.find_elements(By.XPATH, '//*[@id="list-section"]/div[position()>=1]/div/div[1]/div[2]/div[2]/div[1]')
            data = pd.Series([x.text for x in info])
            df_scraped[columns[counter]] = data
        elif counter == 4:
            info = browser.find_elements(By.XPATH, '//*[@id="list-section"]/div[position()>=1]/div/div[1]/div[2]/div[2]/div[2]')
            data = pd.Series([x.text for x in info])
            df_scraped[columns[counter]] = data
            
        counter+=1
    
    df_scraped['Latitude'] = ''
    df_scraped['Longitude'] = ''
    
    return df_scraped

def scrapeCircleK():
    
    '''
    This function is used to scrape the Circle K stores website to find the location,
    address, whether or not it's 24 hours, opening hours from mon-fri and sat
    if not 24 hours
    '''
    
    columns = ['Location', 'Address', 'Opening Hours', 'Latitude', 'Longitude']
    website_path = 'https://www.circlek.hk/en/store'
    browser.get(website_path)
    # Only take Hong Kong Island Circle Ks
    browser.find_element(By.XPATH, '//*[@id="r"]/option[1]').click()
    browser.find_element(By.XPATH, '//*[@id="submit"]').click()
    
    counter = 0
    df_scraped = pd.DataFrame()
    
    # Web Scrape Circle K Addresses and Opening Hours
    while counter <= 2:
        if counter == 0:
            info = browser.find_elements(By.XPATH, '//*[@id="ff_main"]/div/div/div/div[2]/div[2]/div[3]/table/tbody/tr[position()<=79]/td[1]')
            data = pd.Series([x.text for x in info])
            df_scraped[columns[counter]] = data
        elif counter == 1:
            info = browser.find_elements(By.XPATH, '//*[@id="ff_main"]/div/div/div/div[2]/div[2]/div[3]/table/tbody/tr[position()<=79]/td[2]')
            data = pd.Series([x.text for x in info])
            df_scraped[columns[counter]] = data
        elif counter == 2:
            info = browser.find_elements(By.XPATH, '//*[@id="ff_main"]/div/div/div/div[2]/div[2]/div[3]/table/tbody/tr[position()<=79]/td[4]')
            data = pd.Series([x.text for x in info])
            df_scraped[columns[counter]] = data
        
        counter+=1
    
    df_scraped['Latitude'] = ''
    df_scraped['Longitude'] = ''
    return df_scraped
    
def coordinatesStore(df_scraped):
    
    '''
    This function is used to find the coordinates of 7-11 stores in HK Island.
    Paramters: df_scraped
    The dataframe that will use the address to find coordinates
    '''
    
    for i in range(len(df_scraped)):
        parameters= {"key":"AIzaSyC0DM3CqpVufyqks9nKhyuKqjuN9HOKqsA", 
        "address":df_scraped.Address.iloc[i]}
        
        base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
        response = requests.get(base_url, params = parameters).json()
        response.keys()
        if response['status'] == 'OK':
            geometry = response['results'][0]['geometry']
            lat = geometry['location']['lat']
            lon = geometry['location']['lng']
            df_scraped.Latitude.iloc[i] = lat
            df_scraped.Longitude.iloc[i] = lon
    
    return df_scraped

def compareDistance(seven_11, circle_k):
    '''
    This function takes in both dataframes and compares the distance between
    each other. The closest one will then be selected and will return
    both dataframes
    '''
    
    seven_11['Distance_km'] = ''
    seven_11['Closest_Circle_K_Loc'] = ''
    seven_11['Closest_Circle_K_Add'] = ''
    seven_11['Circle_K_Latitude'] = ''
    seven_11['Circle_K_Longitude'] = ''
    circle_k['Distance_km'] = ''
    circle_k['Closest_7_11_Loc'] = ''
    circle_k['Closest_7_11_Add'] = ''
    circle_k['7_11_Latitude'] = ''
    circle_k['7_11_Longitude'] = ''
    
    for i in range(len(seven_11)):
        distance_temp = 99999999
        for j in range(len(circle_k)):
            distance = geodesic((seven_11.Latitude[i], seven_11.Longitude[i]),
                                (circle_k.Latitude[j], circle_k.Longitude[j]))
            if distance < distance_temp:
                seven_11['Distance_km'].iloc[i] = float(str(distance)[:-3])
                seven_11['Closest_Circle_K_Loc'].iloc[i] = circle_k.Location[j]
                seven_11['Closest_Circle_K_Add'].iloc[i] = circle_k.Address[j]
                seven_11['Circle_K_Latitude'].iloc[i] = circle_k.Latitude[j]
                seven_11['Circle_K_Longitude'].iloc[i] = circle_k.Longitude[j]
                distance_temp = distance

    for j in range(len(circle_k)):
        distance_temp = 99999999
        for i in range(len(seven_11)):
            distance = geodesic((seven_11.Latitude[i], seven_11.Longitude[i]),
                                (circle_k.Latitude[j], circle_k.Longitude[j]))
            if distance < distance_temp:
                circle_k['Distance_km'].iloc[j] = float(str(distance)[:-3])
                circle_k['Closest_7_11_Loc'].iloc[j] = seven_11.Location[i]
                circle_k['Closest_7_11_Add'].iloc[j] = seven_11.Address[i]
                circle_k['7_11_Latitude'].iloc[j] = seven_11.Latitude[i]
                circle_k['7_11_Longitude'].iloc[j] = seven_11.Longitude[i]
                distance_temp = distance
                
    return seven_11, circle_k

def plotMapAll(seven_11, circle_k):
    '''
    This function then plots every 7-11 and Circle_K. It shows all the 
    plotted points and Hong Kong Island map
    '''
    hk_map = gpd.read_file(r'/Users/XFlazer/Documents/HKU/FBE/Finance/FINA 2390/Project 3/Hong_Kong_18_Districts/HKDistrict18.shp')
    fig, ax = plt.subplots(figsize = (20, 6))
    xlim=(114.112, 114.263); ylim=(22.19,22.31)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    hk_map.plot(ax=ax, facecolor = 'White', edgecolor = 'Black', alpha = 1, linewidth = 1, cmap = "jet")
    crs = 32610 # CRS tells python the coordinate reference system
    seven_geometry = [Point(xy) for xy in zip(seven_11["Longitude"], seven_11["Latitude"])]
    seven_geodata=gpd.GeoDataFrame(seven_11, crs=crs, geometry = seven_geometry)
    seven_geodata.to_crs(4236) # Needed to plot on map
    seven_geodata.plot(ax=ax, color = 'green', markersize = 50, edgecolor = 'black', label = '7-11')
    k_geometry = [Point(xy) for xy in zip(circle_k["Longitude"], circle_k["Latitude"])]
    k_geodata = gpd.GeoDataFrame(circle_k, crs=crs, geometry = k_geometry)
    k_geodata.to_crs(4236)
    k_geodata.plot(ax=ax, color = 'red', markersize = 50, edgecolor = 'black', label = 'Circle K')
    ax.set_title("Hong Kong Island 7-11s and Circle Ks")
    plt.legend()
    plt.savefig(path + os.sep + 'HK Island Map of 7-11s and Circle Ks')
    plt.show()
    
def plotClosest(store_df, corr_df, store, company_1, company_2):
    '''
    This functions takes in any store's main dataframe and the correlation of
    another store's to ensure they match. It also takes which store the user
    has chosen. The function then uses this to plot both points and connect 
    them for visualization purposes.
    '''
    
    if company_1 == '7-11':
        marker_color_1 = 'green'
        marker_color_2 = 'red'
    else:
        marker_color_1 = 'red'
        marker_color_2 = 'green'
    
    hk_map = gpd.read_file(r'/Users/XFlazer/Documents/HKU/FBE/Finance/FINA 2390/Project 3/Hong_Kong_18_Districts/HKDistrict18.shp')
    fig, ax = plt.subplots(figsize = (20, 6))
    hk_map.plot(ax=ax, facecolor = 'White', edgecolor = 'Black', alpha = 1, linewidth = 1, cmap = "jet", legend = True)
    ax.relim()
    ax.autoscale_view()
    x_values = store_df['Longitude'].iloc[store], corr_df['Longitude'].iloc[0]
    y_values = store_df['Latitude'].iloc[store], corr_df['Latitude'].iloc[0]
    ax.plot(x_values[0], y_values[0], markersize = 20, marker = '.', 
            markerfacecolor = marker_color_1, markeredgecolor = 'black')
    ax.annotate(company_1, (x_values[0], y_values[0]))
    ax.plot(x_values[1], y_values[1], markersize = 20, marker = '.', 
            markerfacecolor = marker_color_2, markeredgecolor = 'black')
    ax.annotate(company_2, (x_values[1], y_values[1]))
    plt.plot(x_values, y_values, linewidth = 1, color = 'black')
    ax.set_title(store_df['Location'].iloc[store])
    ax.set_title("{}\nDistance: {} km\n".format(store_df['Location'].iloc[store], 
                                                store_df['Distance_km'].iloc[store]))
    plt.show()
   

def main(seven_11, circle_k):
    '''
    This function takes in the 7-11 and Circle K scraped data and coordinates.
    It then asks the user if they want to compare the distance between a 7-11
    to the closest Circle K or vice versa. Then, it displays it on the map.
    '''
    
    # Asks user to compare which stores
    company = 'true'
    
    print("\nThis program helps find the closest convenience store from each other.")
    
    while company != 'end' :
        
        print("To end the program, type 'end'")
        
        company = input("Which company do you want to compare distance to (7-11 or Circle K): ")
       
        if company == '7-11':
            print(seven_11[['Location', 'Address']])
            store = int(input("Select a store by number (0-{}): ".format(len(seven_11)-1)))
            print("\nThe 7-11 store is in", seven_11['Location'].iloc[store], 
                  "and the address is", seven_11['Address'].iloc[store] + '.')
           
            corr_lat, corr_lon = seven_11['Circle_K_Latitude'].iloc[store], seven_11['Circle_K_Longitude'].iloc[store]
            corr_k = circle_k[(circle_k.Latitude == corr_lat) & (circle_k.Longitude == corr_lon)]
           
            print("The closest Circle K store is in", corr_k['Location'].iloc[0],
                  "and the address is", corr_k['Address'].iloc[0] + '.\n')
            print("The two stores are {} km apart.".format(seven_11['Distance_km'].iloc[store]))
            
            if seven_11['24 Hours'].iloc[store] != '':
                print("The 7-11 store is open 24/7!")
            else:
                print("The 7-11 store opens on", seven_11['Mon-Fri'].iloc[store], 
                      "and", seven_11['Sat'] + '.')
            if corr_k['Opening Hours'].iloc[0] == '24 Hours':
                print("The Circle K store is open 24/7!")
                print("Both are open 24/7!\n")
            else:
                print("The Circle K store opens on", corr_k['Opening Hours'].iloc[0] + '.\n')
            
            plotClosest(seven_11, corr_k, store, '7-11', 'Circle K')
       
        elif company == 'Circle K':
            print(circle_k[['Location', 'Address']])
            store = int(input("Select a store by number (0-{}): ".format(len(circle_k)-1)))
            print("The Circle K store is in", circle_k['Location'].iloc[store], 
                  "and the address is", circle_k['Address'].iloc[store] + '.')
            
            corr_lat, corr_lon = circle_k['7_11_Latitude'].iloc[store], circle_k['7_11_Longitude'].iloc[store]
            corr_7 = seven_11[(seven_11.Latitude == corr_lat) & (seven_11.Longitude == corr_lon)]
            
            print("The closest 7-11 store is in", corr_7['Location'].iloc[0],
                  "and the address is", corr_7['Address'].iloc[0] + '.\n')
            print("The two stores are {} km apart.".format(circle_k['Distance_km'].iloc[store]))
            
            if circle_k['Opening Hours'].iloc[store] == '24 Hours':
                print("The Circle K store is open 24/7!")
            else:
                print("The Circle K store opens on", circle_k['Opening Hours'].iloc[store] + '.')
            if corr_7['24 Hours'].iloc[0] == '24 Hours':
                print("The 7-11 store is open 24/7!")
                print("Both are open 24/7!\n")
            else:
                print("The 7-11 store opens on", corr_7['Mon-Fri'].iloc[0], 
                      "and", corr_7['Sat'].iloc[0] + '.\n')

            plotClosest(circle_k, corr_7, store, 'Circle K', '7-11')

# Chrome Webdriver
driver_path = r'/Users/XFlazer/Documents/HKU/FBE/Finance/FINA 2390/Web Scraping/chromedriver'

browser = webdriver.Chrome(executable_path=driver_path)

path = r'/Users/XFlazer/Documents/HKU/FBE/Finance/FINA 2390/Project 3'
seven_11_df = scrapeSeven11()
circle_k_df = scrapeCircleK()
seven_11_df = coordinatesStore(seven_11_df)
circle_k_df = coordinatesStore(circle_k_df)

# Manually input missing coordinates
seven_11_df.to_csv(path + os.sep + '7_11_scraped.csv', index=False)
circle_k_df.to_csv(path + os.sep + 'circle_k_scraped.csv', index=False)

browser.quit()

seven_11_df, circle_k_df = compareDistance(seven_11_df, circle_k_df)
seven_11_df = pd.read_csv('7_11_scraped.csv')
circle_k_df = pd.read_csv('circle_k_scraped.csv')
plotMapAll(seven_11_df, circle_k_df)
main(seven_11_df, circle_k_df)