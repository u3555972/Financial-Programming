#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 10:15:47 2021

@author: Chan, Cheuk Hang 3035559725
"""

# Data Transformation Project

# Libraries needed to carry out the project
import time
import os
import pandas as pd

# Track efficiency of code
t0 = time.time() 

def columnName(n_index):
    '''
    This function takes all relevant columns in deal_level_data needed for
    melting, converting, and puts it in a list. It also  into account
    special problems like Com_AvgSalary in Com_AvgSalary_log.
    '''
    
    col_lst = [] # reset list
    for col in deal_df.columns:
        if n_index in index_lst_not_in: # the indices that doesn't have .in problem
            if quarter_level_col_lst_rem[n_index] in col: # if col matches
                if 'avg' not in col: # don't append these columns
                    if 'chg' not in col:
                        col_lst.append(col)
        elif n_index in index_lst_in: # indices that have .in problem
            if quarter_level_col_lst_rem[n_index] in col: # if col matches
                if 'log' not in col: # take out _log since _log is its own column
                    if 'avg' not in col:
                        if 'chg' not in col:
                            col_lst.append(col)
        
    return col_lst

def convertDict(n_index):
    '''
    This function converts all 'name_' or 'name__' into integers and puts it
    in a dictionary. Needed for sorting later on.
    '''
    
    convert_dict = {} # reset dictionary
    for i in range(-12, 13): # since it's only from -12 to 12
        if i < 0:
            convert_dict[quarter_level_col_lst_rem[n_index] + '__' + str(abs(i))] = i 
        elif i == 0:
            convert_dict[quarter_level_col_lst_rem[n_index]] = i
        else:
            convert_dict[quarter_level_col_lst_rem[n_index] + '_' + str(abs(i))] = i
    return convert_dict

def convertRowToColumnSort(col_lst, converted_dict, n_index):
    '''
    This function converts rows into columns using df.melt. After, it resets
    the index and returns it so that the df.join can be accurate.
    '''
    
    if n_index == 0: # To initialize the dataframe
        # Initial dataframe to set up the identifiers and the quarter values
        new_df = deal_df.melt(id_vars = i_lst, value_vars = col_lst,
                              var_name = 'quarter_to_the_event_date', value_name = 'quarter_new')
        
        # Converts all the row data into integers where needed. Such as quarter__12 to -12
        for key in converted_dict.keys():
            new_df.loc[new_df['quarter_to_the_event_date'] == key, 
                       'quarter_to_the_event_date'] = converted_dict[key]
       
        # Sort it first by Deal_Number, then the integers [-12,12]
        new_df = new_df.sort_values(by = ['Deal_Number', 'quarter_to_the_event_date'])

        return new_df.reset_index(drop = True)
    
    else: # After creating the first dataframe
        # Create dataframe to later then .join the needed values
        new_df = deal_df.melt(id_vars = i_lst, value_vars = col_lst, 
                               var_name = quarter_level_col_lst_rem[n_index], 
                               value_name = (quarter_level_col_lst_rem[n_index] + '_new'))
        
        # Converts all the row data into integers where needed. Such as quarter__12 to -12
        for key in converted_dict.keys():
            new_df.loc[new_df[quarter_level_col_lst_rem[n_index]] == key, quarter_level_col_lst_rem[n_index]] = converted_dict[key]
        
        # Sort it first by Deal_Number, then the integers [-12,12]
        new_df = new_df.sort_values(by = ['Deal_Number', quarter_level_col_lst_rem[n_index]])
        
        return new_df.reset_index(drop = True)
        #return test_df
        #test_df_values = test_df[quarter_level_col_lst_rem[n_index]+'_new']
        #return test_df_values
        
        #return test_df[quarter_level_col_lst_rem[n_index]+'_new']

path = r'/Users/XFlazer/Documents/HKU/FBE/Finance/FINA 2390/Data Transformation'

deal_df = pd.read_csv(path + os.sep + 'deal_level_data.csv')

i_lst = deal_df.columns[0:14].tolist() # the list for id_vars

# Columns needed for quarter_level_df
quarter_level_col_lst_rem = ['quarter','Com_Net_Charge_Off',
 'Com_Insider_Loan',
 'Com_NIE',
 'Com_NII',
 'Com_NIM',
 'Com_ROA',
 'Com_Total_Assets',
 'Com_AvgSalary',
 'Com_EmployNum',
 'Com_TtlSalary',
 'Com_AvgSalary_log',
 'Com_EmployNum_log',
 'Com_TtlSalary_log',
 'Tar_Net_Charge_Off',
 'Tar_Insider_Loan',
 'Tar_NIE',
 'Tar_NII',
 'Tar_NIM',
 'Tar_ROA',
 'Tar_Total_Assets',
 'Tar_AvgSalary',
 'Tar_EmployNum',
 'Tar_TtlSalary',
 'Tar_AvgSalary_log',
 'Tar_EmployNum_log',
 'Tar_TtlSalary_log']

# for columnName function to deal with .in issues
index_lst_not_in = [0,1,2,3,4,5,6,7,11,12,13,14,15,16,17,18,19,20,24,25,26]
index_lst_in = [8,9,10,21,22,23]

# main
counter = 0
while counter < len(quarter_level_col_lst_rem): # circulates columns
    col_lst = columnName(counter)
    converted_dict = convertDict(counter)
    new_df_value = convertRowToColumnSort(col_lst, converted_dict, counter)
    if counter == 0: # initialize dataframe
        quarter_level_df = new_df_value
    else: # join the initial dataframe ONLY with needed values
        quarter_level_df = quarter_level_df.join(new_df_value[quarter_level_col_lst_rem[counter]+'_new'])
    
    counter += 1

# Rename needed columns
for i in quarter_level_col_lst_rem:
        quarter_level_df.rename(columns={i+'_new':i}, inplace=True)

#quarter_level_df.reset_index(drop = True, inplace=True)
print(quarter_level_df)
quarter_level_df.to_csv(path + os.sep + 'quarter_level_data.csv', index=False)
t1 = time.time()
print(t1-t0)