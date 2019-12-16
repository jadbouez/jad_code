#!/usr/bin/env python
# coding: utf-8


from capital_machine.sdk.company_data import CompanyData
import pandas as pd


company = CompanyData('BurrowStaging')


company.income_statement.summary.head()


company.balance_sheet.summary.head()


company.customer_tape.head()



custape = company.customer_tape.copy()
acquired_date_custape_series = custape.groupby('customer_id')['transaction_date'].min()
acquired_date_custape_df = pd.DataFrame(acquired_date_custape_series)
acquired_date_custape_df.columns=['acquisition_date']
acquired_date_custape_df.head()



from pandas.tseries.offsets import MonthBegin
import numpy as np
custape_plus_acquisition_dates = custape.merge(acquired_date_custape_df, on='customer_id')
custape_plus_acquisition_dates['acquisition_month'] = custape_plus_acquisition_dates['acquisition_date'] - MonthBegin()
custape_plus_acquisition_dates['transaction_month'] = custape_plus_acquisition_dates['transaction_date'] - MonthBegin()



custape_plus_acquisition_dates[custape_plus_acquisition_dates['acquisition_month'] == '2016-07-01'].sort_values(by=['transaction_month'])



same_transaction_month_acquisition_month = custape_plus_acquisition_dates.pivot_table(index='transaction_month', columns='acquisition_month', values='amount', aggfunc=sum, fill_value=0)
same_transaction_month_acquisition_month.index = np.arange(1, len(same_transaction_month_acquisition_month)+1)
same_transaction_month_acquisition_month.index.name='period'
#same_transaction_month_acquisition_month.columns = same_transaction_month_acquisition_month.columns.strftime('%b %y')
#same_transaction_month_acquisition_month.index = same_transaction_month_acquisition_month.index.strftime('%B %Y')
same_transaction_month_acquisition_month.columns.name='cohort'



IS = company.income_statement.summary.copy()
IS['total_investment'] = IS['investment_inventory']+IS['investment_originations']+IS['investment_sales_marketing']
initial_investment_df = IS[['total_investment']].transpose()
initial_investment_df.columns = IS['period'].astype('datetime64[M]')
#initial_investment_df.columns = initial_investment_df.columns.strftime('%b %Y')



GPM_df = IS[['gross_margin_p']].transpose()
GPM_df.columns = IS['period']
GPM_df = GPM_df.fillna(method='ffill', axis=1)
GPM_df = GPM_df.fillna(method='bfill', axis=1)
GPM_df.columns = IS['period'].astype('datetime64[M]')
#GPM_df.columns = GPM_df.columns.strftime('%b %Y')



same_transaction_month_acquisition_month_2 = same_transaction_month_acquisition_month.copy()
new_GPM = [same_transaction_month_acquisition_month_2, GPM_df]
new_GPM_2 = pd.concat(new_GPM, sort = False)
new_GPM_2.columns = new_GPM_2.columns.strftime('%b %Y')
new_GPM_2 = new_GPM_2.dropna(axis=1, thresh=len(new_GPM_2.columns)-1)



new_GPM_3 = new_GPM_2.iloc[-1:]
new_GPM_3.iloc[-1:] = new_GPM_3.fillna(method='ffill', axis=1)
new_GPM_3.iloc[-1:] = new_GPM_3.fillna(method='bfill', axis=1)



same_transaction_month_acquisition_month_3 = same_transaction_month_acquisition_month.copy()
new_Inv = [same_transaction_month_acquisition_month_2, initial_investment_df]
new_Inv_2 = pd.concat(new_Inv, sort = False)
new_Inv_2.columns = new_Inv_2.columns.strftime('%b %Y')
new_Inv_2 = new_Inv_2.dropna(axis=1, thresh=len(new_Inv_2.columns)-1)
        


new_Inv_3 = new_Inv_2.iloc[-1:]
new_Inv_3.iloc[-1:] = new_Inv_3.fillna(method='ffill', axis=1)


