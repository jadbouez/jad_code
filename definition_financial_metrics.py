#!/usr/bin/env python
# coding: utf-8



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




company.balance_sheet.summary.head()




latest_account_payable = 25000
latest_account_receivable = 30000
latest_inventory = 15000
latest_dividends = 1000 #12 latest monthly dividends
latest_interest = 1000
market_cap = 100000
ST_debt = 10000
retained_earnings = 10000
latest_DA = 100
latest_capex = 10000 #Can potentially be computed as change in total assets + 12-month D&A
preferred_equity = 0
intangible_assets = 100





def latest_revenue(IS_df, BS_df, as_of = pd.Timestamp.max) :
    latest_revenue = IS_df.tail(12)['gross_cashflow'].sum()
    return latest_revenue





def latest_cost_of_revenue(IS_df, BS_df, as_of = pd.Timestamp.max) :
    latest_cost_rev = IS_df.tail(12)['investment_inventory'].sum() + IS_df.tail(12)['cogs'].sum()
    return latest_cost_rev





def latest_gross_margin(IS_df, BS_df, as_of = pd.Timestamp.max) :
    latest_gross_margin = IS_df.tail(12)['gross_cashflow'].sum() - latest_cost_of_revenue(IS_df, BS_df,as_of = pd.Timestamp.max) 
    return latest_gross_margin





def latest_EBITDA(IS_df, BS_df, as_of = pd.Timestamp.max) :
    latest_EBITDA = latest_gross_margin(IS_df, BS_df,as_of = pd.Timestamp.max) - IS_df.tail(12)['burn_other'].sum() - IS_df.tail(12)['excluded'].sum() - IS_df.tail(12)['investment_sales_marketing'].sum() - IS_df.tail(12)['burn_r_and_d'].sum() - IS_df.tail(12)['burn_g_and_a'].sum() 
    return latest_EBITDA





def latest_EBIT(IS_df, BS_df, DA, as_of = pd.Timestamp.max) :
    latest_EBIT = latest_EBITDA(IS_df, BS_df,as_of = pd.Timestamp.max) - DA 
    return latest_EBIT





def latest_EBT(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max) :
    latest_EBT = latest_EBIT(IS_df, BS_df, DA, as_of = pd.Timestamp.max) - interest
    return latest_EBT





def latest_Net_Income(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max) :
    latest_Net_Income = latest_EBIT(IS_df, BS_df, DA, as_of = pd.Timestamp.max) - interest - IS_df.tail(12)['burn_taxes'].sum() 
    return latest_Net_Income





def latest_NOPAT(IS_df, BS_df, DA, tax_rate = 0.3, as_of = pd.Timestamp.max) :
    latest_NOPAT = (latest_EBITDA(IS_df, BS_df,as_of = pd.Timestamp.max) - DA) * (1 - tax_rate)
    return latest_NOPAT





def Net_non_operating_expense(IS_df, BS_df, DA, interest, tax_rate = 0.3, as_of = pd.Timestamp.max) :
    NOPAT = latest_NOPAT(IS_df, BS_df, DA, tax_rate = 0.3, as_of = pd.Timestamp.max)
    Net_income = latest_Net_Income(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max)
    Net_non_operating_expense = NOPAT - Net_income
    return Net_non_operating_expense





def latest_D_and_A(IS_df, BS_df, DA, as_of = pd.Timestamp.max) :
    return DA





def latest_Opex(IS_df, BS_df, as_of = pd.Timestamp.max) :
    latest_Opex = IS_df.tail(12)['investment_sales_marketing'].sum() + IS_df.tail(12)['burn_r_and_d'].sum() + IS_df.tail(12)['burn_other'].sum() + IS_df.tail(12)['burn_g_and_a'].sum() + IS_df.tail(12)['excluded'].sum()
    return latest_Opex





def Net_Working_Cap(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max) : #NWC DOES include cash
    Net_Working_Cap = Inv + AR + BS_df.tail(1)['cash_balance'].sum() - AP
    return Net_Working_Cap





def Yearly_change_NWC_cashless(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max) : #This measure of NWC does NOT include cash
    latest_NWC = Inv + AR - AP 
    last_year_NWC = Inv + AR - AP
    Yearly_change_NWC_cashless = latest_NWC - last_year_NWC
    return Yearly_change_NWC_cashless





def Monthly_change_NWC_cashless(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max) : #This measure of NWC does NOT include cash
    latest_NWC = Inv + AR - AP 
    previous_month = Inv + AR - AP
    Monthly_change_NWC_cashless = latest_NWC - previous_month
    return Monthly_change_NWC_cashless




def Quarterly_change_NWC_cashless(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max) : #This measure of NWC does NOT include cash
    latest_NWC = Inv + AR - AP 
    quarter_old_NWC = Inv + AR - AP
    Quarterly_change_NWC_cashless = latest_NWC - quarter_old_NWC
    return Quarterly_change_NWC_cashless





def Semestrial_change_NWC_cashless(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max) : #This measure of NWC does NOT include cash
    latest_NWC = Inv + AR - AP 
    semester_old_NWC = Inv + AR - AP
    Semestrial_change_NWC_cashless = latest_NWC - semester_old_NWC
    return Semestrial_change_NWC_cashless





def Oldest_monthly_change_NWC_cashless(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max) : #This measure of NWC does NOT include cash
    oldest_NWC = Inv + AR - AP 
    second_oldest_NWC = Inv + AR - AP
    Oldest_monthly_change_NWC_cashless = second_oldest_NWC - oldest_NWC
    return Oldest_monthly_change_NWC_cashless





def latest_FCFF(IS_df, BS_df, Inv, AR, AP, DA, capex, tax_rate=0.3, as_of = pd.Timestamp.max) : #NWC does NOT include cash
    latest_FCFF = latest_EBIT(IS_df, BS_df, DA, as_of = pd.Timestamp.max) * (1 - tax_rate) + DA - capex - Yearly_change_NWC_cashless(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max)
    return latest_FCFF




def latest_OCF(IS_df, BS_df, Inv, AR, AP, DA, interest, as_of = pd.Timestamp.max) : #NWC does NOT include cash
    change_in_WC = Monthly_change_NWC_cashless(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max)
    latest_OCF = latest_Net_Income(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max) + DA - change_in_WC
    return latest_OCF





def Debt_free_NWC(IS_df, BS_df, Inv, AR, AP, STdebt, as_of = pd.Timestamp.max) :
    Debt_free_NWC = Net_Working_Cap(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max) - STdebt
    return Debt_free_NWC





def Debt_free_cash_free_NWC(IS_df, BS_df, Inv, AR, AP, STdebt, as_of = pd.Timestamp.max) :
    Debt_free_cash_free_NWC = Net_Working_Cap(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max) - BS_df.tail(1)['cash_balance'].sum() - STdebt
    return Debt_free_cash_free_NWC





def Total_debt(IS_df, BS_df, as_of = pd.Timestamp.max) :
    Total_debt = BS_df.tail(1)['senior_debt_balance'].sum() + BS_df.tail(1)['junior_debt_balance'].sum()
    return Total_debt





def LT_debt(IS_df, BS_df, STdebt, as_of = pd.Timestamp.max) :
    LT_debt = BS_df.tail(1)['senior_debt_balance'].sum() + BS_df.tail(1)['junior_debt_balance'].sum() - STdebt
    return LT_debt





def Total_Capital(IS_df, BS_df, as_of = pd.Timestamp.max) :
    Total_Capital = BS_df.tail(1)['senior_debt_balance'].sum() + BS_df.tail(1)['junior_debt_balance'].sum() + BS_df.tail(1)['equity_raised'].sum()
    return Total_Capital





def Enterprise_Value(IS_df, BS_df, marketcap, as_of = pd.Timestamp.max) :
    Enterprise_Value = marketcap + BS_df.tail(1)['senior_debt_balance'].sum() + BS_df.tail(1)['junior_debt_balance'].sum() - BS_df.tail(1)['cash_balance'].sum()
    return Enterprise_Value





def Net_debt(IS_df, BS_df, as_of = pd.Timestamp.max) :
    Net_debt = BS_df.tail(1)['senior_debt_balance'].sum() + BS_df.tail(1)['junior_debt_balance'].sum() - BS_df.tail(1)['cash_balance'].sum()
    return Net_debt





def Tangible_book_value(IS_df, BS_df, intangibles, as_of = pd.Timestamp.max) :
    Tangible_book_value = BS_df.tail(1)['collateral'].sum() - intangibles
    return Tangible_book_value 





def Invested_Capital(IS_df, BS_df, as_of = pd.Timestamp.max) :
    Invested_Capital = BS_df.tail(1)['collateral'].sum() - BS_df.tail(1)['cash_balance'].sum()
    return Invested_Capital





def Increase_in_Invested_Capital(IS_df, BS_df, as_of = pd.Timestamp.max) :
    increase_in_Invested_Capital = BS_df['collateral'].iloc[-1] - BS_df['cash_balance'].iloc[-1] - BS_df['collateral'].iloc[-2] - BS_df['cash_balance'].iloc[-2]
    return increase_in_Invested_Capital





def Growth_in_Invested_Capital_pct(IS_df, BS_df, as_of = pd.Timestamp.max) : #MONTHLY growth
        latest_invested_Capital = BS_df.tail(1)['collateral'].sum() - BS_df.tail(1)['cash_balance'].sum()
        oldest_invested_Capital = BS_df.head(1)['collateral'].sum() - BS_df.head(1)['cash_balance'].sum()
        if ((latest_invested_Capital == 0) or (oldest_invested_Capital == 0)):
            Growth_in_Invested_Capital_pct = 'Cannot be computed using current data'
        else:
            Growth_in_Invested_Capital_pct = (latest_invested_Capital / oldest_invested_Capital) ** (1/((len(IS_df.index)) - 1)) -1
        return Growth_in_Invested_Capital_pct





def Revenue_Growth(IS_df, BS_df, as_of = pd.Timestamp.max) : #MONTHLY growth
    if ((IS_df.head(1)['gross_cashflow'].sum() <= 0) | (IS_df.tail(1)['gross_cashflow'].sum() <= 0)):
        Revenue_Growth = 'Cannot be computed using current data'
    else :
        Revenue_Growth = (IS_df.tail(1)['gross_cashflow'].sum() / IS_df.head(1)['gross_cashflow'].sum()) ** (1/((len(IS_df.index)) - 1)) -1
    return Revenue_Growth





def EBITDA_Growth(IS_df, BS_df, as_of = pd.Timestamp.max) : #MONTHLY growth
    Newest_monthly_EBITDA = IS_df.tail(1)['gross_cashflow'].sum() - IS_df.tail(1)['investment_inventory'].sum() - IS_df.tail(1)['cogs'].sum() - IS_df.tail(1)['burn_other'].sum() - IS_df.tail(1)['excluded'].sum() - IS_df.tail(1)['investment_sales_marketing'].sum() - IS_df.tail(1)['burn_r_and_d'].sum() - IS_df.tail(1)['burn_g_and_a'].sum() 
    Oldest_monthly_EBITDA = IS_df.head(1)['gross_cashflow'].sum() - IS_df.head(1)['investment_inventory'].sum() - IS_df.head(1)['cogs'].sum() - IS_df.head(1)['burn_other'].sum() - IS_df.head(1)['excluded'].sum() - IS_df.head(1)['investment_sales_marketing'].sum() - IS_df.head(1)['burn_r_and_d'].sum() - IS_df.head(1)['burn_g_and_a'].sum() 
    if ((Newest_monthly_EBITDA <= 0) | (Oldest_monthly_EBITDA <= 0)) :
        EBITDA_Growth = 'Cannot be computed using current data'
    else :
        EBITDA_Growth = (Newest_monthly_EBITDA / Oldest_monthly_EBITDA) ** (1/((len(IS_df.index)) - 1)) -1
    return EBITDA_Growth





def EBIT_Growth(IS_df, BS_df, DA, as_of = pd.Timestamp.max) : #MONTHLY growth
    Monthly_DA = DA / 12
    Newest_monthly_EBIT = IS_df.tail(1)['gross_cashflow'].sum() - IS_df.tail(1)['investment_inventory'].sum() - IS_df.tail(1)['cogs'].sum() - IS_df.tail(1)['burn_other'].sum() - IS_df.tail(1)['excluded'].sum() - IS_df.tail(1)['investment_sales_marketing'].sum() - IS_df.tail(1)['burn_r_and_d'].sum() - IS_df.tail(1)['burn_g_and_a'].sum() - Monthly_DA 
    Oldest_monthly_EBIT = IS_df.head(1)['gross_cashflow'].sum() - IS_df.head(1)['investment_inventory'].sum() - IS_df.head(1)['cogs'].sum() - IS_df.head(1)['burn_other'].sum() - IS_df.head(1)['excluded'].sum() - IS_df.head(1)['investment_sales_marketing'].sum() - IS_df.head(1)['burn_r_and_d'].sum() - IS_df.head(1)['burn_g_and_a'].sum() - Monthly_DA
    if ((Newest_monthly_EBIT <= 0) | (Oldest_monthly_EBIT <= 0)) :
        EBIT_Growth = 'Cannot be computed using current data'
    else :
        EBIT_Growth = (Newest_monthly_EBIT / Oldest_monthly_EBIT) ** (1/((len(IS_df.index)) - 1)) -1
    return EBIT_Growth





def Net_income_Growth(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max) : #MONTHLY growth
    Monthly_DA = DA / 12
    Monthly_interest = interest / 12
    Newest_monthly_net_income = IS_df.tail(1)['gross_cashflow'].sum() - IS_df.tail(1)['investment_inventory'].sum() - IS_df.tail(1)['cogs'].sum() - IS_df.tail(1)['burn_other'].sum() - IS_df.tail(1)['excluded'].sum() - IS_df.tail(1)['investment_sales_marketing'].sum() - IS_df.tail(1)['burn_r_and_d'].sum() - IS_df.tail(1)['burn_g_and_a'].sum() - Monthly_DA - Monthly_interest - IS_df.tail(1)['burn_taxes'].sum() 
    Oldest_monthly_net_income = IS_df.head(1)['gross_cashflow'].sum() - IS_df.head(1)['investment_inventory'].sum() - IS_df.head(1)['cogs'].sum() - IS_df.head(1)['burn_other'].sum() - IS_df.head(1)['excluded'].sum() - IS_df.head(1)['investment_sales_marketing'].sum() - IS_df.head(1)['burn_r_and_d'].sum() - IS_df.head(1)['burn_g_and_a'].sum() - Monthly_DA - Monthly_interest - IS_df.head(12)['burn_taxes'].sum()
    if ((Newest_monthly_net_income <= 0) | (Oldest_monthly_net_income <= 0)) :
        Net_income_Growth = 'Cannot be computed using current data'
    else :
        Net_income_Growth = (Newest_monthly_EBIT / Oldest_monthly_EBIT) ** (1/((len(IS_df.index)) - 1)) -1
    return Net_income_Growth





def OCF_Growth(IS_df, BS_df, Inv, AR, AP, DA, interest, as_of = pd.Timestamp.max) : #MONTHLY growth
    monthly_DA = DA / 12
    monthly_interest = interest / 12
    latest_monthly_change_in_WC = Monthly_change_NWC_cashless(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max)
    latest_montly_OCF = IS_df['gross_cashflow'].iloc[1] - IS_df['investment_inventory'].iloc[1] - IS_df['cogs'].iloc[1] - IS_df['burn_other'].iloc[1] - IS_df['excluded'].iloc[1] - IS_df['investment_sales_marketing'].iloc[1] - IS_df['burn_r_and_d'].iloc[1] - IS_df['burn_g_and_a'].iloc[1] - monthly_DA - monthly_interest - IS_df.tail(1)['burn_taxes'].sum() + monthly_DA - latest_monthly_change_in_WC
    oldest_monthly_change_in_WC = Oldest_monthly_change_NWC_cashless(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max)
    oldest_monthly_OCF = IS_df['gross_cashflow'].iloc[1] - IS_df['investment_inventory'].iloc[1] - IS_df['cogs'].iloc[1] - IS_df['burn_other'].iloc[1] - IS_df['excluded'].iloc[1] - IS_df['investment_sales_marketing'].iloc[1] - IS_df['burn_r_and_d'].iloc[1] - IS_df['burn_g_and_a'].iloc[1] - monthly_DA - monthly_interest - IS_df.tail(1)['burn_taxes'].sum() + monthly_DA - oldest_monthly_change_in_WC
#First month OCF cannot be computed since NWC is obtained starting END of first month thus we consider one less month
    OCF_Growth = (latest_montly_OCF / oldest_monthly_OCF) ** (1/((len(IS_df.index)) - 2)) -1 
    if ((latest_montly_OCF <= 0) | (oldest_monthly_OCF <= 0)) :
        OCF_Growth = 'Cannot be computed using negative data'
    return OCF_Growth





def FCFF_Growth(IS_df, BS_df, Inv, AR, AP, DA, capex, tax_rate=0.3, as_of = pd.Timestamp.max) : #MONTHLY growth
    Monthly_DA = DA / 12
    Monthly_capex = capex / 12
    Newest_monthly_FCFF = (IS_df['gross_cashflow'].iloc[-1] - IS_df['investment_inventory'].iloc[-1] - IS_df['cogs'].iloc[-1] - IS_df['burn_other'].iloc[-1] - IS_df['excluded'].iloc[-1] - IS_df['investment_sales_marketing'].iloc[-1] - IS_df['burn_r_and_d'].iloc[-1] - IS_df['burn_g_and_a'].iloc[-1] - Monthly_DA ) * (1 - tax_rate) + Monthly_DA - Monthly_capex - Monthly_change_NWC_cashless(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max)
    Oldest_monthly_FCFF = (IS_df['gross_cashflow'].iloc[1] - IS_df['investment_inventory'].iloc[1] - IS_df['cogs'].iloc[1] - IS_df['burn_other'].iloc[1] - IS_df['excluded'].iloc[1] - IS_df['investment_sales_marketing'].iloc[1] - IS_df['burn_r_and_d'].iloc[1] - IS_df['burn_g_and_a'].iloc[1] - Monthly_DA ) * (1 - tax_rate) + Monthly_DA - Monthly_capex - Oldest_monthly_change_NWC_cashless(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max)
#First month FCFF cannot be computed since NWC is obtained starting END of first month thus we consider one less month
    FCFF_Growth = (Newest_monthly_FCFF / Oldest_monthly_FCFF) ** (1/((len(IS_df.index)) - 2)) -1 
    if ((Newest_monthly_FCFF <= 0) | (Oldest_monthly_FCFF <= 0)) :
        FCFF_Growth = 'Cannot be computed using negative data'
    return FCFF_Growth





def NOPAT_Growth(IS_df, BS_df, DA, tax_rate=0.3, as_of = pd.Timestamp.max) : #MONTHLY growth
    Monthly_DA = DA / 12
    Newest_monthly_NOPAT = (IS_df.tail(1)['gross_cashflow'].sum() - IS_df.tail(1)['investment_inventory'].sum() - IS_df.tail(1)['cogs'].sum() - IS_df.tail(1)['burn_other'].sum() - IS_df.tail(1)['excluded'].sum() - IS_df.tail(1)['investment_sales_marketing'].sum() - IS_df.tail(1)['burn_r_and_d'].sum() - IS_df.tail(1)['burn_g_and_a'].sum() - Monthly_DA) * (1 - tax_rate) 
    Oldest_monthly_NOPAT = (IS_df.head(1)['gross_cashflow'].sum() - IS_df.head(1)['investment_inventory'].sum() - IS_df.head(1)['cogs'].sum() - IS_df.head(1)['burn_other'].sum() - IS_df.head(1)['excluded'].sum() - IS_df.head(1)['investment_sales_marketing'].sum() - IS_df.head(1)['burn_r_and_d'].sum() - IS_df.head(1)['burn_g_and_a'].sum() - Monthly_DA) * (1 - tax_rate)
    if ((Newest_monthly_NOPAT <= 0) | (Oldest_monthly_NOPAT <= 0)) :
        NOPAT_Growth = 'Cannot be computed using current data'
    else :
        NOPAT_Growth = (Newest_monthly_NOPAT / Oldest_monthly_NOPAT) ** (1/((len(IS_df.index)) - 1)) -1
    return NOPAT_Growth





def Revenue_Q_Q_growth(IS_df, BS_df, as_of = pd.Timestamp.max) : 
    Newest_quarterly_Revenue = IS_df.tail(3)['gross_cashflow'].sum() 
    Previous_quarterly_Revenue = IS_df.tail(6)['gross_cashflow'].sum() - Newest_quarterly_Revenue 
    if ((Newest_quarterly_Revenue <= 0) | (Previous_quarterly_Revenue <= 0)) :
        Revenue_Q_Q_growth = 'Cannot be computed using negative data'
    else:
        Revenue_Q_Q_growth = Newest_quarterly_Revenue / Previous_quarterly_Revenue -1
    return Revenue_Q_Q_growth





def EBITDA_Q_Q_growth(IS_df, BS_df, as_of = pd.Timestamp.max) : 
    Newest_quarterly_EBITDA = IS_df.tail(3)['gross_cashflow'].sum() - IS_df.tail(3)['investment_inventory'].sum() - IS_df.tail(3)['cogs'].sum() - IS_df.tail(3)['burn_other'].sum() - IS_df.tail(3)['excluded'].sum() - IS_df.tail(3)['investment_sales_marketing'].sum() - IS_df.tail(3)['burn_r_and_d'].sum() - IS_df.tail(3)['burn_g_and_a'].sum()
    Previous_quarterly_EBITDA = IS_df.tail(6)['gross_cashflow'].sum() - IS_df.tail(6)['investment_inventory'].sum() - IS_df.tail(6)['cogs'].sum() - IS_df.tail(6)['burn_other'].sum() - IS_df.tail(6)['excluded'].sum() - IS_df.tail(6)['investment_sales_marketing'].sum() - IS_df.tail(6)['burn_r_and_d'].sum() - IS_df.tail(6)['burn_g_and_a'].sum() - Newest_quarterly_EBITDA 
    EBITDA_Q_Q_growth = Newest_quarterly_EBITDA / Previous_quarterly_EBITDA -1
    if ((Newest_quarterly_EBITDA <= 0) | (Previous_quarterly_EBITDA <= 0)) :
        EBITDA_Q_Q_growth = 'Cannot be computed using negative data'
    return EBITDA_Q_Q_growth





def EBIT_Q_Q_growth(IS_df, BS_df, DA, as_of = pd.Timestamp.max) : 
    Newest_quarterly_EBIT = IS_df.tail(3)['gross_cashflow'].sum() - IS_df.tail(3)['investment_inventory'].sum() - IS_df.tail(3)['cogs'].sum() - IS_df.tail(3)['burn_other'].sum() - IS_df.tail(3)['excluded'].sum() - IS_df.tail(3)['investment_sales_marketing'].sum() - IS_df.tail(3)['burn_r_and_d'].sum() - IS_df.tail(3)['burn_g_and_a'].sum() - DA / 4
    Previous_quarterly_EBIT = IS_df.tail(6)['gross_cashflow'].sum() - IS_df.tail(6)['investment_inventory'].sum() - IS_df.tail(6)['cogs'].sum() - IS_df.tail(6)['burn_other'].sum() - IS_df.tail(6)['excluded'].sum() - IS_df.tail(6)['investment_sales_marketing'].sum() - IS_df.tail(6)['burn_r_and_d'].sum() - IS_df.tail(6)['burn_g_and_a'].sum() - DA / 2 - Newest_quarterly_EBIT 
    EBIT_Q_Q_growth = Newest_quarterly_EBIT / Previous_quarterly_EBIT -1
    if ((Newest_quarterly_EBIT <= 0) | (Previous_quarterly_EBIT <= 0)) :
        EBIT_Q_Q_growth = 'Cannot be computed using negative data'
    return EBIT_Q_Q_growth





def Net_income_Q_Q_growth(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max) :
    Latest_quarterly_net_income = IS_df.tail(3)['gross_cashflow'].sum() - IS_df.tail(3)['investment_inventory'].sum() - IS_df.tail(3)['cogs'].sum() - IS_df.tail(3)['burn_other'].sum() - IS_df.tail(3)['excluded'].sum() - IS_df.tail(3)['investment_sales_marketing'].sum() - IS_df.tail(3)['burn_r_and_d'].sum() - IS_df.tail(3)['burn_g_and_a'].sum() - DA / 4 - interest / 4 - IS_df.tail(3)['burn_taxes'].sum()   
    Latest_semestrial_net_income = IS_df.tail(6)['gross_cashflow'].sum() - IS_df.tail(6)['investment_inventory'].sum() - IS_df.tail(6)['cogs'].sum() - IS_df.tail(6)['burn_other'].sum() - IS_df.tail(6)['excluded'].sum() - IS_df.tail(6)['investment_sales_marketing'].sum() - IS_df.tail(6)['burn_r_and_d'].sum() - IS_df.tail(6)['burn_g_and_a'].sum() - DA / 4 - interest / 2 - IS_df.tail(6)['burn_taxes'].sum()
    Previous_quarterly_net_income = Latest_semestrial_net_income - Latest_quarterly_net_income
    Net_income_Q_Q_growth = Latest_semestrial_net_income / Previous_quarterly_net_income -1
    if ((Latest_semestrial_net_income <= 0) | (Previous_quarterly_net_income <= 0)) :
        Net_income_Q_Q_growth = 'Cannot be computed using negative data'
    return Net_income_Q_Q_growth





def OCF_Q_Q_growth(IS_df, BS_df, Inv, AR, AP, DA, interest, tax_rate=0.3, as_of = pd.Timestamp.max) :
    Latest_quarterly_OCF = IS_df.tail(3)['gross_cashflow'].sum() - IS_df.tail(3)['investment_inventory'].sum() - IS_df.tail(3)['cogs'].sum() - IS_df.tail(3)['burn_other'].sum() - IS_df.tail(3)['excluded'].sum() - IS_df.tail(3)['investment_sales_marketing'].sum() - IS_df.tail(3)['burn_r_and_d'].sum() - IS_df.tail(3)['burn_g_and_a'].sum() - DA / 4 - interest / 4 - IS_df.tail(3)['burn_taxes'].sum() + DA / 2 - Quarterly_change_NWC_cashless(IS_df, BS_df, Inv, AR, AP)
    Latest_semestrial_OCF = IS_df.tail(6)['gross_cashflow'].sum() - IS_df.tail(6)['investment_inventory'].sum() - IS_df.tail(6)['cogs'].sum() - IS_df.tail(6)['burn_other'].sum() - IS_df.tail(6)['excluded'].sum() - IS_df.tail(6)['investment_sales_marketing'].sum() - IS_df.tail(6)['burn_r_and_d'].sum() - IS_df.tail(6)['burn_g_and_a'].sum() - DA / 2 - interest / 2 - IS_df.tail(3)['burn_taxes'].sum() + DA / 2 - Semestrial_change_NWC_cashless(IS_df, BS_df, Inv, AR, AP) 
    Previous_quarterly_OCF = Latest_semestrial_OCF - Latest_quarterly_OCF
    OCF_Q_Q_growth = Latest_semestrial_OCF / Previous_quarterly_OCF -1
    if ((Latest_semestrial_OCF <= 0) | (Previous_quarterly_OCF <= 0)) :
        OCF_Q_Q_growth = 'Cannot be computed using negative data'
    return OCF_Q_Q_growth





def FCFF_Q_Q_growth(IS_df, BS_df, Inv, AR, AP, DA, capex, tax_rate=0.3, as_of = pd.Timestamp.max) :
    Latest_quarterly_FCFF = (IS_df.tail(3)['gross_cashflow'].sum() - IS_df.tail(3)['investment_inventory'].sum() - IS_df.tail(3)['cogs'].sum() - IS_df.tail(3)['burn_other'].sum() - IS_df.tail(3)['excluded'].sum() - IS_df.tail(3)['investment_sales_marketing'].sum() - IS_df.tail(3)['burn_r_and_d'].sum() - IS_df.tail(3)['burn_g_and_a'].sum() - DA / 4) * (1 - tax_rate) + DA / 4 - capex / 4 - Quarterly_change_NWC_cashless(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max)
    Latest_semestrial_FCFF = (IS_df.tail(6)['gross_cashflow'].sum() - IS_df.tail(6)['investment_inventory'].sum() - IS_df.tail(6)['cogs'].sum() - IS_df.tail(6)['burn_other'].sum() - IS_df.tail(6)['excluded'].sum() - IS_df.tail(6)['investment_sales_marketing'].sum() - IS_df.tail(6)['burn_r_and_d'].sum() - IS_df.tail(6)['burn_g_and_a'].sum() - DA / 2 ) * (1 - tax_rate) + DA/2 - capex / 4 - Semestrial_change_NWC_cashless(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max) 
    Previous_quarterly_FCFF = Latest_semestrial_FCFF - Latest_quarterly_FCFF
    FCFF_Q_Q_growth = Latest_semestrial_FCFF / Previous_quarterly_FCFF -1
    if ((Latest_semestrial_FCFF <= 0) | (Previous_quarterly_FCFF <= 0)) :
        FCFF_Q_Q_growth = 'Cannot be computed using negative data'
    return FCFF_Q_Q_growth





def NOPAT_Q_Q_growth(IS_df, BS_df, DA, tax_rate = 0.3, as_of = pd.Timestamp.max) : 
    Newest_quarterly_NOPAT = (IS_df.tail(3)['gross_cashflow'].sum() - IS_df.tail(3)['investment_inventory'].sum() - IS_df.tail(3)['cogs'].sum() - IS_df.tail(3)['burn_other'].sum() - IS_df.tail(3)['excluded'].sum() - IS_df.tail(3)['investment_sales_marketing'].sum() - IS_df.tail(3)['burn_r_and_d'].sum() - IS_df.tail(3)['burn_g_and_a'].sum() - DA / 4) * (1 - tax_rate)
    Previous_quarterly_NOPAT = (IS_df.tail(6)['gross_cashflow'].sum() - IS_df.tail(6)['investment_inventory'].sum() - IS_df.tail(6)['cogs'].sum() - IS_df.tail(6)['burn_other'].sum() - IS_df.tail(6)['excluded'].sum() - IS_df.tail(6)['investment_sales_marketing'].sum() - IS_df.tail(6)['burn_r_and_d'].sum() - IS_df.tail(6)['burn_g_and_a'].sum() - DA / 2) * (1 - tax_rate) - Newest_quarterly_NOPAT 
    NOPAT_Q_Q_growth = Newest_quarterly_NOPAT / Previous_quarterly_NOPAT -1
    if ((Newest_quarterly_NOPAT <= 0) | (Previous_quarterly_NOPAT <= 0)) :
        NOPAT_Q_Q_growth = 'Cannot be computed using negative data'
    return NOPAT_Q_Q_growth





def get_bessemer_cash_conversion(IS_df, BS_df, as_of = pd.Timestamp.max):
    arr = IS_df.tail(3)['gross_cashflow'].sum()*4
    net_capital_invested = BS_df.tail(1)['equity_raised'].sum() + BS_df.tail(1)['senior_debt_balance'].sum() + BS_df.tail(1)['junior_debt_balance'].sum() - BS_df.tail(1)['cash_balance'].sum()
    return arr/net_capital_invested





def Altman_Z_Score(IS_df, BS_df, Inv, AR, AP, retained, as_of = pd.Timestamp.max) :
    NWC = Net_Working_Cap(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max)
    EBITDA = latest_EBITDA(IS_df, BS_df, as_of = pd.Timestamp.max)
    Equity = BS_df.tail(1)['equity_raised'].sum()
    Total_Assets = BS_df.tail(1)['collateral'].sum()
    Total_Liabilities = AP + BS_df.tail(1)['junior_debt_balance'].sum() + BS_df.tail(1)['senior_debt_balance'].sum()
    Altman_Z_Score = 1.2 * NWC / Total_Assets + 1.4 * retained / Total_Assets + 3.3 * EBITDA / Total_Assets + 0.6 * Equity / Total_Liabilities + IS_df.tail(12)['gross_cashflow'].sum() / Total_Assets
    return Altman_Z_Score





def Asset_turnover(IS_df, BS_df, as_of = pd.Timestamp.max) :
    Total_Assets = BS_df.tail(1)['collateral'].sum()
    Revenue = IS_df.tail(12)['gross_cashflow'].sum() 
    Asset_turnover = Revenue / Total_Assets
    return Asset_turnover





def Invested_capital_turnover(IS_df, BS_df, as_of = pd.Timestamp.max) :
    Invested_cap = Invested_Capital(IS_df, BS_df, as_of = pd.Timestamp.max)
    Revenue = IS_df.tail(12)['gross_cashflow'].sum() 
    Invested_capital_turnover = Revenue / Invested_cap
    return Invested_capital_turnover





def AP_turnover(IS_df, BS_df, AP, as_of = pd.Timestamp.max) : #Assumption: COGS = Supplier purchases
    Cost_of_rev = latest_cost_of_revenue(IS_df, BS_df, as_of = pd.Timestamp.max)
    AP_turnover = Cost_of_rev / AP
    return AP_turnover





def AR_turnover(IS_df, BS_df, AR, as_of = pd.Timestamp.max) :
    Revenue = IS_df.tail(12)['gross_cashflow'].sum()
    AR_turnover = Revenue / AR
    return AR_turnover





def Inventory_turnover(IS_df, BS_df, Inv, as_of = pd.Timestamp.max) : #Assumption: COGS = Supplier purchases
    Cost_of_rev = latest_cost_of_revenue(IS_df, BS_df, as_of = pd.Timestamp.max)
    Inventory_turnover = Cost_of_rev / Inv
    return Inventory_turnover





def DSO(IS_df, BS_df, AR, as_of = pd.Timestamp.max) :
    Days_Sales_Outstanding = AR * 365 / IS_df.tail(12)['gross_cashflow'].sum()
    return Days_Sales_Outstanding





def DIO(IS_df, BS_df, Inv, as_of = pd.Timestamp.max) :
    Cost_of_rev = latest_cost_of_revenue(IS_df, BS_df, as_of = pd.Timestamp.max)
    Days_Inventory_Outstanding = Inv * 365 / Cost_of_rev
    return Days_Inventory_Outstanding





def DPO(IS_df, BS_df, AP, as_of = pd.Timestamp.max) :
    Cost_of_rev = latest_cost_of_revenue(IS_df, BS_df, as_of = pd.Timestamp.max)
    Days_Payable_Outstanding = AP * 365 / Cost_of_rev
    return Days_Payable_Outstanding





def CCC(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max) :
    Days_Sales_Outstanding = DSO(IS_df, BS_df, AR, as_of = pd.Timestamp.max)
    Days_Inventory_Outstanding = DIO(IS_df, BS_df, Inv, as_of = pd.Timestamp.max)
    Days_Payable_Outstanding = DPO(IS_df, BS_df, AP, as_of = pd.Timestamp.max)
    Cash_Conversion_Cycle = Days_Sales_Outstanding + Days_Inventory_Outstanding - Days_Payable_Outstanding
    return Cash_Conversion_Cycle





def Current_ratio(IS_df, BS_df, AR, Inv, AP, as_of = pd.Timestamp.max) :
    Current_ratio = (BS_df.tail(1)['cash_balance'].sum() + AR +Inv) / AP
    return Current_ratio





def Quick_ratio(IS_df, BS_df, AR, AP, as_of = pd.Timestamp.max) :
    Quick_ratio = (BS_df.tail(1)['cash_balance'].sum() + AR) / AP
    return Quick_ratio





def Cash_ratio(IS_df, BS_df, AP, as_of = pd.Timestamp.max) :
    Cash_ratio = (BS_df.tail(1)['cash_balance'].sum()) / AP
    return Cash_ratio





def NWC_to_Rev(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max) :
    NWC = Net_Working_Cap(IS_df, BS_df, Inv, AR, AP, as_of = pd.Timestamp.max)
    Revenue = IS_df.tail(12)['gross_cashflow'].sum()
    NWC_to_Rev = NWC / Revenue
    return NWC_to_Rev





def Debt_free_cash_free_NWC_to_Rev(IS_df, BS_df, Inv, AR, AP, STdebt, as_of = pd.Timestamp.max) :
    debt_free_cash_free_NWC = Debt_free_cash_free_NWC(IS_df, BS_df, Inv, AR, AP, STdebt, as_of = pd.Timestamp.max)
    Revenue = IS_df.tail(12)['gross_cashflow'].sum()
    Debt_free_cash_free_NWC_to_Rev = debt_free_cash_free_NWC / Revenue
    return Debt_free_cash_free_NWC_to_Rev





def Debt_free_NWC_to_Rev(IS_df, BS_df, Inv, AR, AP, STdebt, as_of = pd.Timestamp.max) :
    debt_free_cash_free_NWC = Debt_free_NWC(IS_df, BS_df, Inv, AR, AP, STdebt, as_of = pd.Timestamp.max)
    Revenue = IS_df.tail(12)['gross_cashflow'].sum()
    Debt_free_NWC_to_Rev = debt_free_cash_free_NWC / Revenue
    return Debt_free_NWC_to_Rev





def Equity_to_total_cap(IS_df, BS_df, as_of = pd.Timestamp.max) :
    Equity = BS_df.tail(1)['equity_raised'].sum()
    Debt = BS_df.tail(1)['junior_debt_balance'].sum() + BS_df.tail(1)['senior_debt_balance'].sum()
    Equity_to_total_cap = Equity / (Debt + Equity)
    return Equity_to_total_cap





def Debt_to_total_cap(IS_df, BS_df, as_of = pd.Timestamp.max) :
    Equity = BS_df.tail(1)['equity_raised'].sum()
    Debt = BS_df.tail(1)['junior_debt_balance'].sum() + BS_df.tail(1)['senior_debt_balance'].sum()
    Debt_to_total_cap = Debt / (Debt + Equity)
    return Debt_to_total_cap





def Debt_to_EBITDA(IS_df, BS_df, as_of = pd.Timestamp.max) :
    if latest_EBITDA(IS_df, BS_df,as_of = pd.Timestamp.max) < 0:
        Debt_to_EBITDA = 'Cannot be computed using current data'
    else:
        Debt_to_EBITDA = (BS_df.tail(1)['junior_debt_balance'].sum() + BS_df.tail(1)['senior_debt_balance'].sum()) / latest_EBITDA(IS_df, BS_df,as_of = pd.Timestamp.max)
    return Debt_to_EBITDA





def Debt_to_equity(IS_df, BS_df, as_of = pd.Timestamp.max) :
    if BS_df.tail(1)['equity_raised'].sum() == 0 : 
        Debt_to_equity = 'Cannot be computed since equity = 0'
    else :
        Debt_to_equity = (BS_df.tail(1)['junior_debt_balance'].sum() + BS_df.tail(1)['senior_debt_balance'].sum()) / BS_df.tail(1)['equity_raised'].sum()
    return Debt_to_equity





def ST_debt_to_total_cap(IS_df, BS_df, STdebt, as_of = pd.Timestamp.max) :
    Equity = BS_df.tail(1)['equity_raised'].sum()
    Debt = BS_df.tail(1)['junior_debt_balance'].sum() + BS_df.tail(1)['senior_debt_balance'].sum()
    ST_debt_to_total_cap = STdebt / (Debt + Equity)
    return ST_debt_to_total_cap





def LT_debt_to_total_cap(IS_df, BS_df, STdebt, as_of = pd.Timestamp.max) :
    Equity = BS_df.tail(1)['equity_raised'].sum()
    LT_Debt = LT_debt(IS_df, BS_df, STdebt)
    Debt = BS_df.tail(1)['junior_debt_balance'].sum() + BS_df.tail(1)['senior_debt_balance'].sum()
    LT_debt_to_total_cap = LT_Debt / (Debt + Equity)
    return LT_debt_to_total_cap





def LT_debt_to_EBITDA(IS_df, BS_df, STdebt, as_of = pd.Timestamp.max) :
    LT_Debt = LT_debt(IS_df, BS_df, STdebt)
    EBITDA = latest_EBITDA(IS_df, BS_df)
    LT_debt_to_total_cap = LT_Debt / EBITDA
    if EBITDA <= 0 :
        LT_debt_to_total_cap = 'Cannot be computed with a negative EBITDA'
    return LT_debt_to_total_cap





def LT_debt_to_equity(IS_df, BS_df, STdebt, as_of = pd.Timestamp.max) :
    Equity = BS_df.tail(1)['equity_raised'].sum()
    LT_Debt = LT_debt(IS_df, BS_df, STdebt)
    if Equity <= 0:
        LT_debt_to_equity = 'Cannot be computed since equity = 0'
    else:
        LT_debt_to_equity = LT_Debt / Equity
    return LT_debt_to_equity





def LT_debt_to_NOPAT(IS_df, BS_df, STdebt, DA, tax_rate = 0.3, as_of = pd.Timestamp.max) :
    LT_Debt = LT_debt(IS_df, BS_df, STdebt, as_of = pd.Timestamp.max)
    NOPAT = latest_NOPAT(IS_df, BS_df, DA, tax_rate = tax_rate, as_of = pd.Timestamp.max)
    LT_debt_to_NOPAT = LT_Debt / NOPAT
    if NOPAT <= 0 :
        LT_debt_to_NOPAT = 'Cannot be computed with a negative NOPAT'
    return LT_debt_to_NOPAT





def Financial_leverage(IS_df, BS_df, as_of = pd.Timestamp.max) :
    if BS_df.tail(1)['equity_raised'].sum() == 0 : 
        Financial_leverage = 'Cannot be computed since equity = 0'
    else :
        Financial_leverage = (BS_df.tail(1)['junior_debt_balance'].sum() + BS_df.tail(1)['senior_debt_balance'].sum()) / BS_df.tail(1)['equity_raised'].sum()
    return Financial_leverage





def Net_Debt_to_EBITDA(IS_df, BS_df, as_of = pd.Timestamp.max) :
    net_debt = Net_debt(IS_df, BS_df, as_of = pd.Timestamp.max)
    EBITDA = latest_EBITDA(IS_df, BS_df, as_of = pd.Timestamp.max)
    if ((net_debt > 0) & (EBITDA > 0)):
        Net_Debt_to_EBITDA = net_debt / EBITDA
    else:
        Net_Debt_to_EBITDA = 'Cannot be computed if both metrics are not positive'
    return Net_Debt_to_EBITDA





def Debt_to_NOPAT(IS_df, BS_df, DA, tax_rate = 0.3, as_of = pd.Timestamp.max) :
    NOPAT = latest_NOPAT(IS_df, BS_df, DA, tax_rate = tax_rate, as_of = pd.Timestamp.max)
    if NOPAT < 0:
        Debt_to_NOPAT = 'Cannot be computed with a negative NOPAT'
    else:
        Debt_to_NOPAT = (BS_df.tail(1)['junior_debt_balance'].sum() + BS_df.tail(1)['senior_debt_balance'].sum()) / NOPAT
    return Debt_to_NOPAT





def Net_debt_to_NOPAT(IS_df, BS_df, DA, tax_rate = 0.3, as_of = pd.Timestamp.max) :
    net_debt = Net_debt(IS_df, BS_df, as_of = pd.Timestamp.max)
    NOPAT = latest_NOPAT(IS_df, BS_df, DA, tax_rate = tax_rate, as_of = pd.Timestamp.max)
    if ((NOPAT <= 0) or (net_debt <=0)):
        Net_debt_to_NOPAT = 'Cannot be computed with a negative NOPAT'
    else:
        Net_debt_to_NOPAT = (BS_df.tail(1)['junior_debt_balance'].sum() + BS_df.tail(1)['senior_debt_balance'].sum()) / NOPAT
    return Net_debt_to_NOPAT





def Coumpound_leverage_factor(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max) :
    Equity = BS_df.tail(1)['equity_raised'].sum()
    Assets = BS_df.tail(1)['collateral'].sum()
    EBIT = latest_EBIT(IS_df, BS_df, DA)
    EBT = latest_EBT(IS_df, BS_df, DA, interest) 
    if ((EBIT>0) or (EBT>0)):
        Coumpound_leverage_factor = (EBT / EBIT) * Assets / Equity
    else:
        Coumpound_leverage_factor = 'Cannot be computed if metrics are not positive'
    return Coumpound_leverage_factor





def EBIT_to_interest_expense(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max) :
    EBIT_to_interest_expense = latest_EBIT(IS_df, BS_df, DA, as_of = pd.Timestamp.max) / interest
    return EBIT_to_interest_expense





def EBIT_less_CapEx_to_interest_expense(IS_df, BS_df, DA, capex, interest, as_of = pd.Timestamp.max) :
    EBIT_less_CapEx_to_interest_expense = (latest_EBIT(IS_df, BS_df, DA, as_of = pd.Timestamp.max) - capex) / interest
    return EBIT_less_CapEx_to_interest_expense





def FCFF_to_interest_expense(IS_df, BS_df, Inv, AR, AP, DA, capex, interest, tax_rate=0.3, as_of = pd.Timestamp.max) :
    FCFF = latest_FCFF(IS_df, BS_df, Inv, AR, AP, DA, capex, tax_rate=tax_rate, as_of = pd.Timestamp.max)
    FCFF_to_interest_expense = FCFF / interest
    return FCFF_to_interest_expense





def Interest_burden_percent(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max) :
    Interest_burden_percent = latest_EBT(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max) / latest_EBIT(IS_df, BS_df, DA, as_of = pd.Timestamp.max)
    return Interest_burden_percent





def OCF_to_interest_expense(IS_df, BS_df, Inv, AR, AP, DA, interest, as_of = pd.Timestamp.max) :
    OCF = latest_OCF(IS_df, BS_df, Inv, AR, AP, DA, interest, as_of = pd.Timestamp.max)
    OCF_to_interest_expense = OCF / interest
    return OCF_to_interest_expense





def NOPAT_to_interest_expense(IS_df, BS_df, DA, capex, interest, tax_rate=0.3, as_of = pd.Timestamp.max) :
    NOPAT = latest_NOPAT(IS_df, BS_df, DA, tax_rate=tax_rate, as_of = pd.Timestamp.max)
    NOPAT_to_interest_expense = NOPAT / interest
    return NOPAT_to_interest_expense





def OCF_less_capex_to_interest_expense(IS_df, BS_df, Inv, AR, AP, DA, capex, interest, as_of = pd.Timestamp.max) :
    OCF_less_capex = latest_OCF(IS_df, BS_df, Inv, AR, AP, DA, interest, as_of = pd.Timestamp.max) - capex
    OCF_less_capex_to_interest_expense = OCF_less_capex / interest
    return OCF_less_capex_to_interest_expense





def NOPAT_less_capex_to_interest_expense(IS_df, BS_df, DA, capex, interest, tax_rate=0.3, as_of = pd.Timestamp.max) :
    NOPAT_less_capex = latest_NOPAT(IS_df, BS_df, DA, tax_rate=tax_rate, as_of = pd.Timestamp.max) - capex
    NOPAT_less_capex_to_interest_expense = NOPAT_less_capex / interest
    return NOPAT_less_capex_to_interest_expense





def Cost_of_Rev_to_Rev(IS_df, BS_df, as_of = pd.Timestamp.max) :
    Cost_of_Rev_to_Rev = latest_cost_of_revenue(IS_df, BS_df,as_of = pd.Timestamp.max) / IS_df.tail(12)['gross_cashflow'].sum()
    return Cost_of_Rev_to_Rev





def EBITDA_Margin(IS_df, BS_df, as_of = pd.Timestamp.max) :
    if latest_EBITDA(IS_df, BS_df,as_of = pd.Timestamp.max) < 0 :
        EBITDA_Margin = 'Cannot be computed with a negative EBITDA'
    else:
        EBITDA_Margin = latest_EBITDA(IS_df, BS_df,as_of = pd.Timestamp.max) / IS_df.tail(12)['gross_cashflow'].sum()
    return EBITDA_Margin





def EBIT_Margin(IS_df, BS_df, DA, as_of = pd.Timestamp.max) :
    if latest_EBIT(IS_df, BS_df, DA, as_of = pd.Timestamp.max) < 0 :
        EBIT_Margin = 'Cannot be computed with a negative EBIT'
    else:
        EBIT_Margin = latest_EBIT(IS_df, BS_df,as_of = pd.Timestamp.max) / IS_df.tail(12)['gross_cashflow'].sum()
    return EBIT_Margin





def EBT_Margin(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max) :
    if latest_EBT(IS_df, BS_df, DA, interest) <= 0 :
        EBT_Margin = 'Cannot be computed with a negative EBT'
    else:
        EBT_Margin = latest_EBT(IS_df, BS_df) / IS_df.tail(12)['gross_cashflow'].sum()
    return EBT_Margin





def Profit_Margin(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max) :
    if latest_Net_Income(IS_df, BS_df, DA, interest) < 0 :
        Profit_Margin = 'Cannot be computed with a negative net income'
    else:
        Profit_Margin = latest_Net_Income(IS_df, BS_df, DA, interest) / IS_df.tail(12)['gross_cashflow'].sum()
    return Profit_Margin





def OpEx_to_Revenue(IS_df, BS_df, as_of = pd.Timestamp.max) :
    OpEx_to_Revenue = latest_Opex(IS_df, BS_df) / IS_df.tail(12)['gross_cashflow'].sum()
    return OpEx_to_Revenue





def RD_to_Revenue(IS_df, BS_df, as_of = pd.Timestamp.max) :
    RD_to_Revenue = IS_df.tail(12)['burn_r_and_d'].sum() / IS_df.tail(12)['gross_cashflow'].sum()
    return RD_to_Revenue





def SGA_to_Revenue(IS_df, BS_df, as_of = pd.Timestamp.max) :
    SGA = IS_df.tail(12)['investment_sales_marketing'].sum() - IS_df.tail(12)['burn_g_and_a'].sum()
    SGA_to_Revenue = SGA / IS_df.tail(12)['gross_cashflow'].sum()
    return SGA_to_Revenue





def NOPAT_Margin(IS_df, BS_df, DA, tax_rate=0.3, as_of = pd.Timestamp.max) :
    if latest_NOPAT(IS_df, BS_df, DA, tax_rate=tax_rate, as_of = pd.Timestamp.max) < 0 :
        NOPAT_Margin = 'Cannot be computed with a negative NOPAT'
    else:
        NOPAT_Margin = latest_NOPAT(IS_df, BS_df, DA, tax_rate=tax_rate, as_of = pd.Timestamp.max) / IS_df.tail(12)['gross_cashflow'].sum()
    return NOPAT_Margin





def Tax_burden_percent(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max) :
    net_income = latest_Net_Income(IS_df, BS_df, DA, interest)
    ebt = latest_EBT(IS_df, BS_df, DA, interest)
    if ((net_income < 0) or (EBT <= 0)):
        Tax_burden_percent = 'Cannot be computed since net income and EBT are not both positive'
    else:
        Tax_burden_percent = net_income / ebt
    return Tax_burden_percent





def ROE(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max) :
    if (latest_Net_Income(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max) <= 0) |  (BS_df.tail(1)['equity_raised'].sum() == 0) :
        ROE = 'Cannot be computed if net income and book value of equity are not both positive'
    else:
        ROE = latest_Net_Income(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max) / BS_df.tail(1)['equity_raised'].sum()
    return ROE





def ROA(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max) :
    if latest_Net_Income(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max) <= 0 :
        ROA = 'Cannot be computed with a negative net income'
    else:
        ROA = latest_Net_Income(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max) / BS_df.tail(1)['collateral'].sum()
    return ROA





def ROCE(IS_df, BS_df, DA, as_of = pd.Timestamp.max) :
    ROCE = (latest_EBITDA(IS_df, BS_df, as_of = pd.Timestamp.max) - DA) / (BS_df.tail(1)['equity_raised'].sum() + BS_df.tail(1)['junior_debt_balance'].sum() + BS_df.tail(1)['senior_debt_balance'].sum())
    return ROCE





def ROIC(IS_df, BS_df, DA, tax_rate=0.3, as_of = pd.Timestamp.max) :
    NOPAT = latest_NOPAT(IS_df, BS_df, DA, tax_rate=tax_rate, as_of = pd.Timestamp.max)
    Invest_Cap = Invested_Capital(IS_df, BS_df, as_of = pd.Timestamp.max)
    ROIC = NOPAT / Invest_Cap
    return ROIC





def Operating_return_on_assets(IS_df, BS_df, DA, as_of = pd.Timestamp.max) :
    EBIT = latest_EBIT(IS_df, BS_df, DA, as_of = pd.Timestamp.max)
    Total_Assets = BS_df.tail(1)['collateral'].sum()
    Operating_return_on_assets = EBIT / Total_Assets
    if EBIT <= 0:
        Operating_return_on_assets = 'Cannot be computed with a negative EBIT'
    return Operating_return_on_assets





def CROIC(IS_df, BS_df, as_of = pd.Timestamp.max) :
    if BS_df.tail(1)['equity_raised'].sum() == 0 :
        Cash_Return_on_Capital_Invested = 'Cannot be computed if book value of equity is not strictly positive'
    else :
        Cash_Return_on_Capital_Invested = latest_EBITDA(IS_df, BS_df,as_of = pd.Timestamp.max) / BS_df.tail(1)['equity_raised'].sum()
    return Cash_Return_on_Capital_Invested





def Augmented_Payout_Ratio(IS_df, BS_df, DA, interest, dividends, as_of = pd.Timestamp.max) :
    Net_income = latest_Net_Income(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max)
    Buybacks =  BS_df['equity_raised'].iloc[-13] - BS_df['equity_raised'].iloc[-1]
    Augmented_Payout_Ratio = (dividends + Buybacks) / Net_income
    return Augmented_Payout_Ratio





def Dividend_Payout_Ratio(IS_df, BS_df, DA, interest, dividends, as_of = pd.Timestamp.max) :
    Net_income = latest_Net_Income(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max)
    Dividend_Payout_Ratio = dividends / Net_income
    if Dividend_Payout_Ratio < 0:
        Dividend_Payout_Ratio = 'Cannot be computed with a negative net income'
    return Dividend_Payout_Ratio





def Dividend_yield(IS_df, BS_df, dividends, marketcap, as_of = pd.Timestamp.max) :
    Dividend_yield = dividends / marketcap
    return Dividend_yield





def Earnings_yield(IS_df, BS_df, DA, interest, marketcap, as_of = pd.Timestamp.max) :
    Dividend_yield = latest_Net_Income(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max) / marketcap
    return Dividend_yield





def EV_to_EBITDA(IS_df, BS_df, marketcap, as_of = pd.Timestamp.max) :
    EV_to_EBITDA =  Enterprise_Value(IS_df, BS_df, marketcap) / latest_EBITDA(IS_df, BS_df)
    if ((Enterprise_Value(IS_df, BS_df, marketcap) < 0) or (latest_EBITDA(IS_df, BS_df) < 0)):
        EV_to_EBITDA = 'Cannot be computed if both metrics are not positive'
    return EV_to_EBITDA





def EV_to_EBIT(IS_df, BS_df, DA, marketcap, as_of = pd.Timestamp.max) :
    EV_to_EBIT =  Enterprise_Value(IS_df, BS_df, marketcap) / latest_EBIT(IS_df, BS_df, DA)
    if ((Enterprise_Value(IS_df, BS_df, marketcap) < 0) or (latest_EBIT(IS_df, BS_df, DA) < 0)):
        EV_to_EBIT = 'Cannot be computed if both metrics are not positive'
    return EV_to_EBIT





def EV_to_FCFF(IS_df, BS_df, Inv, AR, AP, DA, capex, marketcap, tax_rate=0.3, as_of = pd.Timestamp.max) :
    EV_to_FCFF =  Enterprise_Value(IS_df, BS_df, marketcap, as_of = pd.Timestamp.max) / latest_FCFF(IS_df, BS_df, Inv, AR, AP, DA, capex, tax_rate=tax_rate, as_of = pd.Timestamp.max)
    if ((Enterprise_Value(IS_df, BS_df, marketcap, as_of = pd.Timestamp.max) < 0) or (latest_FCFF(IS_df, BS_df, Inv, AR, AP, DA, capex, tax_rate=tax_rate, as_of = pd.Timestamp.max) < 0)):
        EV_to_FCFF = 'Cannot be computed if both metrics are not positive'
    return EV_to_FCFF





def EV_to_Invested_Capital(IS_df, BS_df, DA, marketcap, tax_rate=0.3, as_of = pd.Timestamp.max) :
    Invest_Cap = Invested_Capital(IS_df, BS_df, as_of = pd.Timestamp.max)
    EV_to_Invested_Capital =  Enterprise_Value(IS_df, BS_df, marketcap, as_of = pd.Timestamp.max) / Invest_Cap
    if ((Enterprise_Value(IS_df, BS_df, marketcap, as_of = pd.Timestamp.max) < 0) or (Invest_Cap < 0)):
        EV_to_Invested_Capital = 'Cannot be computed if both metrics are not positive'
    return EV_to_Invested_Capital





def EV_to_OCF(IS_df, BS_df, Inv, AR, AP, DA, interest, marketcap, tax_rate=0.3, as_of = pd.Timestamp.max) :
    EV_to_FCFF =  Enterprise_Value(IS_df, BS_df, marketcap, as_of = pd.Timestamp.max) / latest_OCF(IS_df, BS_df, Inv, AR, AP, DA, interest, as_of = pd.Timestamp.max)
    if ((Enterprise_Value(IS_df, BS_df, marketcap, as_of = pd.Timestamp.max) < 0) or (latest_OCF(IS_df, BS_df, Inv, AR, AP, DA, interest, as_of = pd.Timestamp.max) < 0)):
        EV_to_FCFF = 'Cannot be computed if both metrics are not positive'
    return EV_to_FCFF





def EV_to_NOPAT(IS_df, BS_df, DA, marketcap, tax_rate=0.3, as_of = pd.Timestamp.max) :
    EV = Enterprise_Value(IS_df, BS_df, marketcap, as_of = pd.Timestamp.max)
    NOPAT = latest_NOPAT(IS_df, BS_df, DA, tax_rate = tax_rate, as_of = pd.Timestamp.max)
    EV_to_NOPAT = EV / NOPAT
    if ((EV < 0) or (NOPAT < 0)):
        EV_to_NOPAT = 'Cannot be computed if both metrics are not positive'
    return EV_to_NOPAT





def EV_to_Revenue(IS_df, BS_df, marketcap, as_of = pd.Timestamp.max) :
    EV =  Enterprise_Value(IS_df, BS_df, marketcap, as_of = pd.Timestamp.max) 
    Revenue = IS_df.tail(12)['gross_cashflow'].sum()
    EV_to_Revenue = EV / Revenue
    if ((EV < 0) or (Revenue < 0)):
        EV_to_Revenue = 'Cannot be computed if both metrics are not positive'
    return EV_to_Revenue





def P_to_book(IS_df, BS_df, marketcap, as_of = pd.Timestamp.max) :
    BV = BS_df.tail(1)['equity_raised'].sum()
    if BV <= 0:
        P_to_book = 'Cannot be computed if the book value of equity is not positive'
    else:
        P_to_book = marketcap / BV
    return P_to_book





def P_to_revenue(IS_df, BS_df, marketcap, as_of = pd.Timestamp.max) :
    Revenue = latest_revenue(IS_df, BS_df, as_of = pd.Timestamp.max)
    if Revenue <= 0:
        P_to_revenue = 'Cannot be computed if revenue is not positive'
    else:
        P_to_revenue = marketcap / Revenue
    return P_to_revenue





def P_to_earnings(IS_df, BS_df, marketcap, DA, interest, as_of = pd.Timestamp.max) :
    net_income = latest_Net_Income(IS_df, BS_df, DA, interest, as_of = pd.Timestamp.max)
    if net_income <= 0:
        P_to_earnings = 'Cannot be computed if net income is not positive'
    else:
        P_to_earnings = marketcap / net_income
    return P_to_earnings





def P_to_tangible_book(IS_df, BS_df, marketcap, intangibles, as_of = pd.Timestamp.max) :
    tangible_BV = Tangible_book_value(IS_df, BS_df, intangibles, as_of = pd.Timestamp.max)
    if tangible_BV <= 0:
        P_to_tangible_book = 'Cannot be computed if the tangible book value of equity is not positive'
    else:
        P_to_tangible_book = marketcap / tangible_BV
    return P_to_tangible_book
