#!/usr/bin/env python
# coding: utf-8

# In[1]:


from capital_machine.sdk.company_data import CompanyData
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from pandas.tseries.offsets import MonthBegin
from dateutil.relativedelta import relativedelta

pd.options.display.float_format = '{:,}'.format
pd.options.display.max_rows = 999
pd.options.display.max_columns = 999


company = CompanyData('BurrowStaging')


company.income_statement.summary.head()


df = company.income_statement.raw_items
dfs = df[(df['category_one']=='gross_cashflow') | (df['category_one']=='investment_inventory') | (df['category_one']=='cogs')]


company.balance_sheet.summary.head()


IS = company.income_statement.summary.copy()


BS = company.balance_sheet.summary.copy()



IS_Company_FS = IS.loc[:,['period','investment_inventory','cogs','gross_cashflow','investment_sales_marketing','burn_r_and_d','burn_g_and_a','burn_taxes','excluded','burn_other']]



IS_Company_FS.index = IS_Company_FS['period']
del IS_Company_FS['period']



IS_Company_FS['Cost_of_revenues'] = IS_Company_FS['investment_inventory'] + IS_Company_FS['cogs']
IS_Company_FS['Gross_Margin'] = IS_Company_FS['gross_cashflow'] - IS_Company_FS['Cost_of_revenues']
IS_Company_FS['Other_expenses'] = IS_Company_FS['burn_other'] + IS_Company_FS['excluded'] 
IS_Company_FS['EBITDA'] = IS_Company_FS['Gross_Margin'] - IS_Company_FS['investment_sales_marketing'] - IS_Company_FS['burn_r_and_d'] - IS_Company_FS['burn_g_and_a'] - IS_Company_FS['Other_expenses']
IS_Company_FS['D&A'] = 0
IS_Company_FS['EBIT'] = IS_Company_FS['EBITDA'] - IS_Company_FS['D&A']
IS_Company_FS['interest'] = 0
IS_Company_FS['Net_Income'] = IS_Company_FS['EBITDA'] - IS_Company_FS['D&A'] - IS_Company_FS['interest'] - IS_Company_FS['burn_taxes']
del IS_Company_FS['burn_other']
del IS_Company_FS['excluded']


IS_Company_FS_transpose = IS_Company_FS.transpose()



IS_Company_FS_ordered = IS_Company_FS_transpose.reindex(['gross_cashflow',
                                                         'investment_inventory',
                                                         'cogs', 
                                                         'Cost_of_revenues', 
                                                         'Gross_Margin', 
                                                         'investment_sales_marketing',
                                                         'burn_r_and_d',
                                                         'burn_g_and_a',
                                                         'Other_expenses',
                                                         'EBITDA',
                                                         'D&A',
                                                         'EBIT',
                                                         'interest',
                                                         'burn_taxes',
                                                         'Net_Income'])




IS_Company_FS_ordered.index = ['GROSS CASHFLOW', 
                               'Investment inventory', 
                               'Other COGS', 
                               'Cost of revenues (COGS + Inv)', 
                               'GROSS MARGIN', 
                               'S&M', 
                               'R&D', 
                               'G&A', 
                               'Other expenses', 
                               'EBITDA',
                               'D&A',
                               'EBIT', 
                               'Interest', 
                               'Taxes', 
                               'NET INCOME']



BS_Company_FS = BS.loc[:,['collateral','cash_balance','junior_debt_balance','senior_debt_balance','period','equity_raised']]


BS_Company_FS['Long-term Assets'] = 0
BS_Company_FS['Current Assets (non-cash) '] = BS_Company_FS['collateral'] - BS_Company_FS['cash_balance']
BS_Company_FS['TOTAL ASSETS'] = BS_Company_FS['cash_balance'] + BS_Company_FS['Long-term Assets'] + BS_Company_FS['Current Assets (non-cash) ']
BS_Company_FS['Long-term Liabilities'] = BS_Company_FS['junior_debt_balance'] + BS_Company_FS['senior_debt_balance']
BS_Company_FS['Current Liabilities'] = 0
BS_Company_FS['TOTAL LIABILITIES'] = BS_Company_FS['Current Liabilities'] + BS_Company_FS['Long-term Liabilities']



BS_Company_FS.index = BS_Company_FS['period']
del BS_Company_FS['period']
del BS_Company_FS['collateral']


BS_Company_FS_transpose = BS_Company_FS.transpose()



BS_Company_FS_transpose.index = ['Cash', 
                                 'Junior debt balance', 
                                 'Senior debt balance', 
                                 'EQUITY',
                                 'Long-term Assets', 
                                 'Current Assets (non-cash)',
                                 'TOTAL ASSETS', 
                                 'Long-term Liabilities', 
                                 'Current Liabilities', 
                                 'TOTAL LIABILITIES']



BS_Company_FS_transpose = BS_Company_FS_transpose.reindex(['Cash',
                                                         'Current Assets (non-cash)', 
                                                         'Long-term Assets', 
                                                         'TOTAL ASSETS', 
                                                         'Current Liabilities',
                                                         'Junior debt balance',
                                                         'Senior debt balance',
                                                         'Long-term Liabilities',
                                                         'TOTAL LIABILITIES',
                                                         'EQUITY'])


BS_Company_FS_untranspose = BS_Company_FS_transpose.transpose()
IS_Company_FS_untranspose = IS_Company_FS_ordered.transpose()
Combo = IS_Company_FS_untranspose.merge(BS_Company_FS_untranspose, on='period')



Combo_final = Combo.transpose()

