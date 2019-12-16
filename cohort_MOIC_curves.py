#!/usr/bin/env python
# coding: utf-8



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px



# Create fake cohort df of 6 cohorts over 6 months
# Values are same organisation as true one

# Create a Total Investment df of 1 row and 6 columns with fake values (coherent)

# Call columns of each dataframe the same: A,B,C,D... like excel
# Call index (periods) of cohort dataframe 1,2,3,4,5,6



# Perfoms operations to compute MOIC



# Plot MOIC of best, median and worst cohorts



K = 6 #Cohort Length
L = 2 #Offset Months

A = [14660 , 2084 , 3452 , 4348, 3425 , 2836]   
B = [0, 56405 , 14984 , 14771 , 14666 , 11413]
C = [0 , 0 , 52006 , 10177, 10055, 8129]
D = [0 , 0 , 0 , 37746 , 6279 , 4680]
E = [0 , 0 , 0 , 0 , 32810 , 4903]
F = [0 , 0 , 0 , 0 , 0 , 76332]
period = [1 , 2 , 3 , 4 , 5 , 6]
GPMPerPeriod = [0.26 , 0.26 , 0.26 , 0.26 , 0.26 , 0.26]

initial_investment_list = [55000, 50000, 45000, 35000, 30000, 80279]
initial_investment_df = pd.DataFrame(initial_investment_list, index=['A','B','C','D','E','F']).transpose()




input_df = pd.DataFrame(data={
    'A': A,
    'B': B,
    'C':C,
    'D':D,
    'E':E,
    'F':F
}, index=period)
input_df




total_return = input_df.sum().to_frame().transpose()



input_df_return = input_df.copy()



for col in input_df_return.columns:
    input_df_return[col+'_return'] = input_df_return[col].values / initial_investment_df[col].values
    del input_df_return[col]



result_relative_basis = input_df_return.copy()

result = []
for col in input_df_return.columns:
    col_series = input_df_return[col][input_df_return[col] != 0]
    row = col_series.values.copy()
    row.resize((6,))
    result.append(row)

result_relative_basis = pd.DataFrame(result,index=['A','B','C','D','E','F'], columns=period)



result_relative_basis_extrapolated = result_relative_basis.copy()
for col in result_relative_basis_extrapolated.columns:
    for row_idx, row in enumerate(result_relative_basis_extrapolated[col].index):
        if result_relative_basis_extrapolated.at[row, col] == 0:
            start = max(0, row_idx-L)
            window = result_relative_basis_extrapolated[col][start:row_idx]
            result_relative_basis_extrapolated.at[row, col] = window.mean()




result_relative_basis_extrapolated_transposed=result_relative_basis_extrapolated.transpose()
#This table shall be used to plot MOIC graphs



MOIC = result_relative_basis_extrapolated_transposed.sum()




MOIC_1 = result_relative_basis_extrapolated_transposed.head(1).sum()




MOIC_3 = result_relative_basis_extrapolated_transposed.head(3).sum()




MOIC_5 = result_relative_basis_extrapolated_transposed.head(5).sum()




MOIC_Table = pd.DataFrame(data={
    'MOIC': MOIC,
    '1-period MOIC':MOIC_1 ,
    '3-period MOIC':MOIC_3,
    '5-period MOIC':MOIC_5,
}).transpose()




Best_MOIC = MOIC_Table.idxmax(axis='columns')




Worse_MOIC = MOIC_Table.idxmin(axis='columns')




MOIC_Table_First_Row_Total = MOIC_Table[MOIC_Table.index == "MOIC"].squeeze()




l_bound_median = int(MOIC_Table.columns.size/2)-1
u_bound_median = l_bound_median + 2
median_cohorts = MOIC_Table.apply(lambda r: r.sort_values()[l_bound_median:u_bound_median].idxmax(), axis=1)




l_bound_25 = int(MOIC_Table.columns.size/4)-1
u_bound_25 = l_bound_25 + 2
twenty_fifth_cohorts = MOIC_Table.apply(lambda r: r.sort_values()[l_bound_25:u_bound_25].idxmax(), axis=1)




l_bound_75 = int(MOIC_Table.columns.size*3/4)-1
u_bound_75 = l_bound_75 + 2
seventy_fifth_cohorts = MOIC_Table.apply(lambda r: r.sort_values()[l_bound_75:u_bound_75].idxmax(), axis=1)



print (f'The Cohort showing the highest cumulative MOIC is : {Best_MOIC.iloc[0]}')
print (f'The Cohort showing the 75th percentile cumulative MOIC is : {twenty_fifth_cohorts.iloc[0]}')
print (f'The Cohort showing the median cumulative MOIC is : {median_cohorts.iloc[0]}')
print (f'The Cohort showing the 25th percentile cumulative MOIC is : {seventy_fifth_cohorts.iloc[0]}')
print (f'The Cohort showing the lowest cumulative MOIC is : {Worse_MOIC.iloc[0]}')




Cumulative_MOIC = result_relative_basis_extrapolated_transposed.copy()
for col in Cumulative_MOIC.columns:
    Cumulative_MOIC[col] = Cumulative_MOIC[col].cumsum()



plt.plot(Cumulative_MOIC[Best_MOIC.iloc[0]], color='blue', marker='o',linewidth=2, markersize=5)
plt.xlabel('Periods (months)')
plt.ylabel('Cumulative MOIC')
plt.title('Best Cumulative MOIC - Cohort '+ str(Best_MOIC.iloc[0]))
plt.yticks(np.arange(1.0, 2.4, 0.3), [str(x)+'x' for x in np.arange(10,24, 3)/10])



plt.plot(Cumulative_MOIC[Worse_MOIC.iloc[0]], color='red', marker='o', linewidth=2, markersize=5)
plt.xlabel('Periods (months)')
plt.ylabel('Cumulative MOIC')
plt.title('Worse Cumulative MOIC - Cohort '+ str(Worse_MOIC.iloc[0]))
plt.yticks(np.arange(0.1, 0.8, 0.2), [str(x)+'x' for x in np.arange(1, 8, 2)/10])



plt.plot(Cumulative_MOIC[median_cohorts.iloc[0]], color='green', marker='o',linewidth=2, markersize=5)
plt.xlabel('Periods (months)')
plt.ylabel('Cumulative MOIC')
plt.title('Median Cumulative MOIC - Cohort '+ str(median_cohorts.iloc[0]))
plt.yticks(np.arange(0.3, 2.1, 0.3), [str(x)+'x' for x in np.arange(3, 21, 3)/10])


plt.plot(Cumulative_MOIC[twenty_fifth_cohorts.iloc[0]], color='pink', marker='o', linewidth=2, markersize=5)
plt.xlabel('Periods (months)')
plt.ylabel('Cumulative MOIC')
plt.title('Twenty-Fifth Percentile Cumulative MOIC - Cohort '+ str(twenty_fifth_cohorts.iloc[0]))
plt.yticks(np.arange(0.8, 2.0, 0.3), [str(x)+'x' for x in np.arange(8, 20, 3)/10])


plt.plot(Cumulative_MOIC[seventy_fifth_cohorts.iloc[0]], color='purple', marker='o', linewidth=2, markersize=5)
plt.xlabel('Periods (months)')
plt.ylabel('Cumulative MOIC')
plt.title('Seventy-Fifth Percentile Cumulative MOIC - Cohort '+ str(seventy_fifth_cohorts.iloc[0]))
plt.yticks(np.arange(1.1, 2.2, 0.3), [str(x)+'x' for x in np.arange(11, 22, 3)/10])




graph_df = pd.DataFrame(data={
    'Best' : Cumulative_MOIC[Best_MOIC.iloc[0]],
    'Median' : Cumulative_MOIC[median_cohorts.iloc[0]],
    'Worse' : Cumulative_MOIC[Worse_MOIC.iloc[0]]})



plt.plot(graph_df)
plt.xlabel('Periods (months)')
plt.ylabel('Cumulative MOIC')





import plotly.graph_objects as go

df = graph_df

fig = go.Figure(layout=go.Layout(
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),))

fig.add_trace(go.Scatter(
                x=df.index,
                y=df['Best'],
                name="Best",
                line_color='deepskyblue',
                opacity=0.8))

fig.add_trace(go.Scatter(
                x=df.index,
                y=df['Median'],
                name="Median",
                line_color='dimgray',
                opacity=0.8))

fig.add_trace(go.Scatter(
                x=df.index,
                y=df['Worse'],
                name="Worse",
                line_color='red',
                opacity=0.8))

fig.update_layout(title_text="Cohort MOIC S&M Over Time", 
                  xaxis_title="Periods (months)",
                  yaxis_title="Cumulative MOIC", 
                  font=dict(family="Courier New, monospace",
                            size=18,color="#7f7f7f"))

fig.update_layout(
    yaxis = dict(
        tickmode = 'array',
        tickvals = [0, 0.5, 1, 1.5, 2, 2.5, 3],
        ticktext = [str(x)+'x' for x in [0, 0.5, 1, 1.5, 2, 2.5, 3]]))

fig.update_yaxes(range=[0, 2.8])
            
fig.show()

