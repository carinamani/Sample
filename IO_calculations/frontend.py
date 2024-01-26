# -*- coding: utf-8 -*-
"""
Created on Thurs Jan 26 16:13:35 2024

@author: carinamani

This script uses a Leontif inverse matrix to calculate the supply chain impact of a specified industry in a specified country. 
Impact is seperated by first, second, and third+ tiers of the supply chain. 

"""

###########################
###### DEFINE INPUTS ######
###########################

### Define country (ISO code) and industry (ISIC REV4 code) of interest 
country_industry = ['AUS_01T03', 'USA_09'] # e.g. AUS_01T03 = Australian Agriculture, Forestry, and Fishing

### Set spending amount
spending = 1e6

##########################
###### RUN ANALYSIS ######
##########################

from f_Calculate_IO_impacts import SupplyChainImpact

for i, country_industry in enumerate(country_industry):
        SupplyChainImpact(country_industry, spending)









