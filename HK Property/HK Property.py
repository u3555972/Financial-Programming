#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 18:32:05 2021

@author: Chan, Cheuk Hang 3035559725

Webscrape Property Prices HK (Transactions). The current website only supports
the most recent 20 pages and nothing beyond. Thus, it can only shows the 20
pages of the most recent transactions instead of the full history. Additionally,
any record that has ANY missing data will be dropped. This program also assumes
no-error inputs from user.
"""

import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime as dt

def buildDataFrame():
    '''
    This function scrapes the property website and returns info into a DataFrame.
    Returns the final Dataframe for user and csv
    '''
    
    # Order of website options for locations (loc = 1, 2, 3, 4)
    website_region = {'HK':'Hong Kong','KLN':'Kowloon','NTE':'New Territories East',
                      'NTW':'New Territories West'}
    
    # Columns needed for dataframe
    df_columns = ['Recorded Date', 'Usage', 'Region', 'District', 'Address', 
               'Floor', 'Room', 'Area in Square Feet', 'Total Deal Price (M)',
               'Price per Square Feet']
    
    # Initialize Dataframe to concatenate data
    final_df = pd.DataFrame()
    region_lst = list(website_region.keys())
    region_counter = 0
    
   # Loop to go through each region
    while region_counter < len(website_region): # loops through all regions
        if region_counter == 0:
            temp_df = scrapeWebsite(region_lst, website_region, region_counter, hk_districts, usages, df_columns)
            # Since data will be overwritten when scraping, use of temporary dataframe to concatenate into final
            final_df = pd.concat([temp_df, final_df]) 
           
            
        elif region_counter == 1:
            temp_df = scrapeWebsite(region_lst, website_region, region_counter, kln_districts, usages, df_columns)
            # Since data will be overwritten when scraping, use of temporary dataframe to concatenate into final
            final_df = pd.concat([temp_df, final_df]) 
            
        elif region_counter == 2:
            temp_df = scrapeWebsite(region_lst, website_region, region_counter, nte_districts, usages, df_columns)
            # Since data will be overwritten when scraping, use of temporary dataframe to concatenate into final
            final_df = pd.concat([temp_df, final_df]) 
            
        elif region_counter == 3:
            temp_df = scrapeWebsite(region_lst, website_region, region_counter, ntw_districts, usages, df_columns)
            # Since data will be overwritten when scraping, use of temporary dataframe to concatenate into final
            final_df = pd.concat([temp_df, final_df]) 
            
        region_counter += 1
        
    return final_df
            

def scrapeWebsite(region_lst, website_region, region_counter, districts, usages, df_columns):
    '''
    Scrapes specifics of the website. Parameters is the dictionary of districts
    in order to scrape only from thoses districts. Returns a dataframe.
    '''
    df_scraped = pd.DataFrame()
    temp_df = pd.DataFrame()
    
    for district in districts.keys(): # loops through all districts
        for usage in usages.keys(): # loops through all usages
         page_counter = 1
         while page_counter <= 20:
             website_path = 'https://www.property.hk/eng/tran.php?dt={}&bldg=&prop={}&saleType=3&loc={}&page={}'.format(district, usage, region_lst[region_counter], page_counter)
             browser.get(website_path)
             col_counter = 0
             
             while col_counter < len(df_columns):
                 
                 if col_counter == 0:
                     info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[2]')
                     if len(info) == 0:
                         break # to speed up code if it detects no data based on date
                     else:
                         data = pd.Series([x.text for x in info])
                         temp_df[df_columns[col_counter]] = data
                     
                 elif col_counter == 1:
                     temp_df[df_columns[col_counter]] = usages[usage]
                     
                 elif col_counter == 2:
                     temp_df[df_columns[col_counter]] = website_region[region_lst[region_counter]]
                 
                 elif col_counter == 3:
                     temp_df[df_columns[col_counter]] = districts[district]
                 
                 elif col_counter == 4:
                     info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[3]')
                     data = pd.Series([x.text for x in info])
                     temp_df[df_columns[col_counter]] = data
                 
                 elif col_counter == 5:
                     info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[4]')
                     data = pd.Series([x.text for x in info])
                     temp_df[df_columns[col_counter]] = data
                     
                 elif col_counter == 6:
                     info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[5]')
                     data = pd.Series([x.text for x in info])
                     temp_df[df_columns[col_counter]] = data
                 
                 elif col_counter == 7:
                     info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[6]')
                     data = pd.Series([x.text for x in info])
                     temp_df[df_columns[col_counter]] = data
                 
                 elif col_counter == 8:
                     info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[7]')
                     data = pd.Series([x.text for x in info])
                     temp_df[df_columns[col_counter]] = data
                 
                 elif col_counter == 9:
                     info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[8]')
                     data = pd.Series([x.text for x in info])
                     temp_df[df_columns[col_counter]] = data
                     
                 col_counter +=1
             
             # use of concatenation since data will be overwritten when scraping.
             df_scraped = pd.concat([temp_df, df_scraped])                   
             page_counter+=1
             
    return df_scraped

def userProperties(hk_prop_price_df):
    '''
    This function displays which properties, depending on the user's 
    self defined input, will be shown. Parameter
    is the dataframe and it will return the modified data frame
    '''
    
    # to convert all dates into actual date format for comparison
    hk_prop_price_df['Recorded Date'] = pd.to_datetime(hk_prop_price_df['Recorded Date'])
    
    # explanation of code
    print('This program allows you to filter and only select the properties you want')
    print('To select a range of year, months, square feet, please use a "-"')
    print('To select region, please only type in ONE region code') # can only handle one region for now
    print('Regions in Hong Kong:', regions)
    print('\nTo select a district, a region must have been selected first, and please type in the district code. For multiple districts, please use a ",":')
    print('\nHK Districts:', hk_districts)
    print('\nKowloon Districts:', kln_districts)
    print('\nNew Territories East:', nte_districts)
    print('\nNew Territories West:', ntw_districts)
    print('\nTo select a usage, please type in the code of the usage. For multiple usages, please use a ",":')
    print('Usages:', usages)
    print('\nFor example Kowloon, Tsim Sha Tsui for the year of 2019, month 12, size in range 501-1000 square feet, with usage as residential:')
    print('Region: KLN\nDistrict: KTS\nYear: 2019\nMonth: 12\nSize (in square feet): 501-1000\nUsage: R')
    print('\nFor example for Hong Kong, Pokfulam, year of from 2020-2021, month from 2-4, size less than 1000 square feet, with usages as industry or office or parking')
    print('Region: HK\nDistrict: HPF\nYear: 2020-2021\nMonth: 2-4\nSize (in square feet): 0-1000\nUsage: I,O,P')
   
    print('\nRegions in Hong Kong:', regions)
    user_region = input('Region: ')
    if user_region != '':
        user_region_lst = user_region.split(',')
        for r in user_region_lst:
            if r == 'HK': # shows user hk districts
                print('\nHK Districts:', hk_districts)
            if r == 'KLN':
                print('\nKowloon Districts:', kln_districts)
            if r == 'NTE':
                print('\nNew Territories East:', nte_districts)
            if r == 'NTW':
                print('\nNew Territories West:', ntw_districts)
    elif user_region == '':
        user_region_lst = list(regions.keys())
    
    user_district = input('District: ')
    if user_district != '':
        user_district_lst = user_district.split(',') # make a list of districts user has chosen
    elif user_district == '':
        user_district_lst = []
        for r in user_region_lst: # Idea if user doesn't select a district but did select a region, show all districts of that region
            if r == 'HK':
                user_district_lst += list(hk_districts.keys())
            elif r == 'KLN':
                user_district_lst += list(kln_districts.keys())
            elif r == 'NTE':
                user_district_lst += list(nte_districts.keys())
            elif r == 'NTW':
                user_district_lst += list(ntw_districts.keys())

    user_year = input('Year: ')
    if user_year != '': # Split year range. Works without '-'
        user_year_lst = user_year.split('-')
    elif user_year == '': # if the user doesn't enter any year, assume all years
        user_year_lst = [hk_prop_price_df['Recorded Date'].dt.year.min(), hk_prop_price_df['Recorded Date'].dt.year.max()]
    
    user_month = input('Month: ')
    if user_month != '': # Split month range. Works without '-'
        user_month_lst = user_month.split('-')
    elif user_month == '': # if user doesn't enter any months, assume all months
        user_month_lst = [0, 12]
    
    user_size = input('Size (in square feet): ')
    if user_size != '': # Split square feet range. Works without '-'
        user_size_lst = user_size.split('-')
    elif user_size == '': # All sizes if no user input
        user_size_lst = [0, hk_prop_price_df['Area in Square Feet'].max()]
    
    user_usage = input('Usage: ')
    if user_usage != '': # Split usages
        user_usage_lst = user_usage.split(',')
    elif user_usage == '': # Assumes all usages
        user_usage_lst = list(usages.keys())
    
    temp_df = pd.DataFrame()
    user_df = pd.DataFrame()
    user_filtered_df = pd.DataFrame(columns = ['Recorded Date', 'Usage', 'Region', 'District', 'Address', 
               'Floor', 'Room', 'Area in Square Feet', 'Total Deal Price (M)',
               'Price per Square Feet'])

    for r in user_region_lst:
        if r  == 'HK': # Only works for one region for now
            user_df = userFiltered(hk_prop_price_df, temp_df, user_df, hk_districts, 
                         user_district_lst, user_usage_lst, user_year_lst, 
                         user_month_lst, user_size_lst, usages)
            
            user_filtered_df = pd.concat([user_df,user_filtered_df])
            
        elif r == 'KLN':
            user_df = userFiltered(hk_prop_price_df, temp_df, user_df, kln_districts, 
                         user_district_lst, user_usage_lst, user_year_lst, 
                         user_month_lst, user_size_lst, usages)
            
            user_filtered_df = pd.concat([user_df,user_filtered_df])
            
        elif r == 'NTE':
            user_df = userFiltered(hk_prop_price_df, temp_df, user_df, nte_districts, 
                         user_district_lst, user_usage_lst, user_year_lst, 
                         user_month_lst, user_size_lst, usages)
            
            user_filtered_df = pd.concat([user_df,user_filtered_df])
            
        elif r == 'NTW':
            user_df = userFiltered(hk_prop_price_df, temp_df, user_df, ntw_districts, 
                         user_district_lst, user_usage_lst, user_year_lst, 
                         user_month_lst, user_size_lst, usages)
            
            user_filtered_df = pd.concat([user_df,user_filtered_df])
        
    return user_filtered_df

def userFiltered(hk_prop_price_df, temp_df, user_df, district, user_district_lst, 
                 user_usage_lst, user_year_lst, user_month_lst, user_size_lst, usages):
    
    for d in user_district_lst:
        for u in user_usage_lst: # temp_df takes all the condition but will be overwritten
            temp_df = hk_prop_price_df[(hk_prop_price_df['District'] == district[d]) &
                                       (hk_prop_price_df['Recorded Date'].dt.year >= int(user_year_lst[0])) &
                                       (hk_prop_price_df['Recorded Date'].dt.year <= int(user_year_lst[-1])) &
                                       (hk_prop_price_df['Recorded Date'].dt.month >= int(user_month_lst[0])) &
                                       (hk_prop_price_df['Recorded Date'].dt.month <= int(user_month_lst[-1])) &
                                       (hk_prop_price_df['Area in Square Feet'] >= int(user_size_lst[0])) &
                                       (hk_prop_price_df['Area in Square Feet'] <= int(user_size_lst[-1])) &
                                       (hk_prop_price_df['Usage'] == usages[u])]
            # need for concat so data will not be overwritten in temp_df
            user_df = pd.concat([temp_df, user_df])
     
    return user_df
    
# Use of global variables/dictionaries to make it easier to call
regions = {'HK':'Hong Kong','KLN':'Kowloon','NTE':'New Territories East',
                      'NTW':'New Territories West'}
    
hk_districts = {'HS':'Peak / South District','HH':'Aberdeen / Wong Chuk Hang',
               'HPF':'Pokfulam','HKT':'Kennedy Town','HSY':'Sai Ying Pun',
               'HT':'Central / Sheung Wan', 'HMA':'Mid-levels Central / Mid-levels West',
               'HMH':'Mid-levels East / Happy Valley', 'HWB':'Wanchai / Causeway Bay',
               'HNP':'North Point / North Point Mid-levels', 'HQB':'Quarry Bay',
               'HSK':'Shau Kei Wan / Sai Wan Ho', 'HE':'Chai Wan / Siu Sai Wan'}

kln_districts = {'KTS':'Tsim Sha Tsui', 'KY':'Yau Ma Tei / Mong Kok',
                 'KSS':'Sham Shui Po', 'KTK':'Tai Kok Tsui', 'KCS':'Cheung Sha Wan',
                 'KLC':'Lai Chi Kok / Mei Foo', 'KHH':'Hung Hom', 'KTW':'To Kwa Wan',
                 'KHM':'Ho Man Tin', 'KKL':'Kowloon Tong', 'KCC':'Kowloon City',
                 'KSK':'Shek Kip Mei / Yau Yat Chuen', 'KSP':'San Po Kong',
                 'KW':'Wong Tai Sin / Wang Tau Hom', 'KD':'Diamond Hill / Ngai Chi Wan',
                 'KKB':'Kowloon Bay / Kai Tak', 'KNT':'Ngau Tau Kok',
                 'KT':'Kwun Tong / Lam Tin / Yau Tong'}

nte_districts = {'NTK':'Tseung Kwan O', 'NSK':'Sai Kung / Clear Water Bay',
                 'NMO':'Ma On Shan', 'NST':'Sha Tin / Tai Wo / Fo Tan',
                 'NTP':'Tai Po', 'NFL':'Fan Ling', 'NSS':'Sheng Shui'}

ntw_districts = {'NKC':'Kwai Chung', 'NTW':'Tsuen Wan', 'NC':'Castle Peak Road / Sham Tseng',
                 'NTM':'Tuen Mun', 'NTS':'Tin Shui Wai', 'NYL':'Yuen Long / Kam Tim',
                 'NTY':'Tsing Yi', 'NMW':'Ma Wan', 'NTC':'Tung Chung', 
                 'NDB':'Discovery Bay', 'NIS':'Island'}

usages = {'R':'Residential', 'C':'Shop', 'O':'Office', 'I':'Industrial', 
         'P':'Parking', 'V':'Village'}

# Chrome Webdriver
driver_path = r'/Users/XFlazer/Documents/HKU/FBE/Finance/FINA 2390/Web Scraping/chromedriver'
browser = webdriver.Chrome(executable_path=driver_path)

# Output to save CSV file
path = r'/Users/XFlazer/Documents/HKU/FBE/Finance/FINA 2390/Project 4'
hk_prop_df = buildDataFrame()
browser.quit()

# Output original scraped CSV without any cleaning and read it
hk_prop_df.to_csv(path + os.sep + 'original_prop_price.csv')
hk_prop_df.read_csv(path + os.sep + 'original_prop_price.csv')

# drop any duplicates or NaN in the date column
hk_prop_price_df = hk_prop_df.dropna(subset=['Recorded Date']).drop_duplicates()
# output csv file
hk_prop_price_df.to_csv(path + os.sep + 'hk_prop_price.csv', index = False)
user_filtered_df = userProperties(hk_prop_price_df)
# output user filtered csv file
user_f_name = input('Please name your filtered results: ')
user_filtered_df.to_csv(path + os.sep + user_f_name + '.csv', index = False)

#hk_prop_df = pd.read_csv(path + os.sep + 'original_prop_price.csv')

           # for district in hk_districts.keys():
           #     for usage in usages.keys():
           #      page_counter = 1
           #      while page_counter <= 20:
           #          website_path = 'https://www.property.hk/eng/tran.php?dt={}&bldg=&prop={}&saleType=3&loc={}&page={}'.format(district, usage, website_region[region_counter], page_counter)
           #          browser.get(website_path)
           #          col_counter = 0
                    
           #          while col_counter < len(df_columns):
                        
           #              if col_counter == 0:
           #                  info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[2]')
           #                  if len(info) == 0:
           #                      break
           #                  else:
           #                      data = pd.Series([x.text for x in info])
           #                      temp_df[df_columns[col_counter]] = data
                            
           #              elif col_counter == 1:
           #                  temp_df[df_columns[col_counter]] = usages[usage]
                            
           #              elif col_counter == 2:
           #                  temp_df[df_columns[col_counter]] = website_region[region_counter]
                        
           #              elif col_counter == 3:
           #                  temp_df[df_columns[col_counter]] = hk_districts[district]
                        
           #              elif col_counter == 4:
           #                  info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[3]')
           #                  data = pd.Series([x.text for x in info])
           #                  temp_df[df_columns[col_counter]] = data
                        
           #              elif col_counter == 5:
           #                  info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[4]')
           #                  data = pd.Series([x.text for x in info])
           #                  temp_df[df_columns[col_counter]] = data
                            
           #              elif col_counter == 6:
           #                  info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[5]')
           #                  data = pd.Series([x.text for x in info])
           #                  temp_df[df_columns[col_counter]] = data
                        
           #              elif col_counter == 7:
           #                  info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[6]')
           #                  data = pd.Series([x.text for x in info])
           #                  temp_df[df_columns[col_counter]] = data
                        
           #              elif col_counter == 8:
           #                  info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[7]')
           #                  data = pd.Series([x.text for x in info])
           #                  temp_df[df_columns[col_counter]] = data
                        
           #              elif col_counter == 9:
           #                  info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[8]')
           #                  data = pd.Series([x.text for x in info])
           #                  temp_df[df_columns[col_counter]] = data
                            
           #              col_counter +=1
                    
           #          df_scraped = pd.concat([temp_df, df_scraped])                   
           #          page_counter+=1
                    
                    
        
        #elif region_counter == 1:
            
            

    # Manual
    
    # info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[2]')
                    # data = pd.Series([x.text for x in info])
                    # temp_df[df_columns[col_counter]] = data
                    # col_counter += 1
                    
                    # temp_df[df_columns[col_counter]] = usages[usage]
                    # col_counter += 1
                    
                    # temp_df[df_columns[col_counter]] = website_region[region_counter]
                    # col_counter += 1
                    
                    # temp_df[df_columns[col_counter]] = hk_districts[district]
                    # col_counter += 1
                    
                    # info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[3]')
                    # data = pd.Series([x.text for x in info])
                    # temp_df[df_columns[col_counter]] = data
                    # col_counter += 1
                    
                    # info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[4]')
                    # data = pd.Series([x.text for x in info])
                    # temp_df[df_columns[col_counter]] = data
                    # col_counter += 1
                    
                    # info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[5]')
                    # data = pd.Series([x.text for x in info])
                    # temp_df[df_columns[col_counter]] = data
                    # col_counter += 1
                    
                    # info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[6]')
                    # data = pd.Series([x.text for x in info])
                    # temp_df[df_columns[col_counter]] = data
                    # col_counter += 1
                    
                    # info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[7]')
                    # data = pd.Series([x.text for x in info])
                    # temp_df[df_columns[col_counter]] = data
                    # col_counter += 1
                    
                    # info = browser.find_elements(By.XPATH, '//*[@id="proplist"]/div[1]/form/table[1]/tbody/tr[position()>=1]/td[8]')
                    # data = pd.Series([x.text for x in info])
                    # temp_df[df_columns[col_counter]] = data
                    # col_counter += 1
    
