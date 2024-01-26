# -*- coding: utf-8 -*-
"""
Created on Thurs Jan 26 14:52:34 2024

@author: carinamani

This script defines a function for calculating the supply chain spending impact of a given country-industry. 
The impact is seperated by first, second, and third+ tiers of the supply chain. 

"""

### Import packages 
import numpy as np
import pandas as pd
import os

def SupplyChainImpact(country_industry, spending): 

    path = os.getcwd()

    ### Generate input vector with country_industry spend
    input_spending = pd.read_csv(path + '/Inputs/template_input_vector.csv', index_col=0, header=0).astype(float)
    input_spending.loc[country_industry, 'Spend_USD'] = spending

    ### Import IO tables
    leontif_inverse = pd.read_parquet(path + '/Inputs/dummy_leontif_inverse.parquet')
    technology = pd.read_parquet(path + '/Inputs/dummy_technology.parquet')
    technology[np.isnan(technology)]=0

    # Calculate the first round of supply chain spending impact using the technology matrix 
    output_First = technology @ input_spending 

    # Calculate output impact across entire supply chain, in USD current prices and exchange rates
    output_Total = leontif_inverse @ output_First 

    # Calculate the second round of supply chain spending (i.e. suppliers' suppliers) using the technology matrix
    output_Second = technology @ output_First

    # Calculate the remainder of the upstream supply chain spending by subtracting the first and second round spending from the total spending 
    output_Upstream = output_Total - output_First - output_Second 

    # Combine all of the supply chain spending impacts into one dataframe
    output = pd.concat([output_First, output_Second, output_Upstream, output_Total],axis='columns',join='inner', ignore_index=True)
    output.columns = ['output_First','output_Second', 'output_Upstream', 'output_Total']

    # Save as CSV
    output.to_csv(path + '/Outputs/' + country_industry + '_spend_impact.csv')

    print("Calculations complete for " + country_industry)





