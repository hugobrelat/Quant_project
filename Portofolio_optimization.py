import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import math
import random 

stocks = {}
stocks_lists = stocks_lists = ['MC.PA','ORA.PA','AC.PA','STLAP.PA' ,'ETH-USD','BTC-USD','GC=F']
portfolio = 10000
scenarios = 10000

#read chaque stock, implémentation dans le dictionnaire, avec index 0 = Date, et les dates coverti en date 
for i_stock in stocks_lists:
    stocks[i_stock] = pd.read_csv(f"module 6/{i_stock}.csv",parse_dates=True,index_col='Date')

#On créer une colone return comparé aux jour 1
for stock_name,stock_data in stocks.items(): 
    first_adj_close = stock_data.iloc[0]['Adj Close']
    stock_data['Return'] = stock_data['Adj Close']/ first_adj_close

#On créer une colone allocation pour dire qu'on met 25% du capital sur chaque stock 
for stock_name,stock_data in stocks.items(): 
    stock_data['Allocation'] = stock_data['Return']*1/len(stocks)

#On transforme cette allocation en position value
for stock_name, stock_data in stocks.items(): 
    stock_data['Position_Value'] = stock_data['Allocation']*portfolio


positions_value = {}
# Création du dict complet avec les value du portfolio chaque jour
for stock_name, stock_data in stocks.items():
    positions_value[stock_name] = stock_data['Position_Value']  

#Mise en place dans un dataframe + on affiche la somme de chaque ligne (chaque jour)
positions_value = pd.DataFrame(data=positions_value)
positions_value['Total'] = positions_value.sum(axis=1)

#Création d'un colonne daily return (pour les data statistique plus tard)
start_date = positions_value['Total'][0]
end_date = positions_value['Total'][-1]
cumulative_return = (end_date /start_date)-1
positions_value['Daily Return'] = positions_value['Total'].pct_change()

#calcul des datas statistiques 
mean = positions_value['Daily Return'].mean()
std = positions_value['Daily Return'].std()
Sharpe_ratio = mean/std
Sharpe_ratio_annualized = Sharpe_ratio * math.sqrt(252)


# Création d'un dataframe avec les values de chaque stock par jour 
stock_adj_close = {}
for stock_name,stock_data in stocks.items(): 
    stock_adj_close[stock_name] = stock_data['Adj Close']
stock_adj_close = pd.DataFrame(data=stock_adj_close)

stock_return = stock_adj_close.pct_change()

# génération de l'aléatoire 
#On met des 0 dans des tableaux 
weights_array = np.zeros((scenarios,len(stock_return.columns)))
returns_array = np.zeros(scenarios)
volatility_array = np.zeros(scenarios)
Sharpe_ratio_array = np.zeros(scenarios)

#fixe les résultats de l'aléatoire 
#random.seed(3)
#np.random.seed(3)


for index in range(scenarios):
    numbers = np.array(np.random.random(len(stocks)))
    weights = numbers /np.sum(numbers)
    weights_array[index,:] = weights
    returns_array[index] = np.sum(stock_return.mean() *252*weights)
    volatility_array[index] = np.sqrt(np.dot(weights.T,np.dot(stock_return.cov()*252,weights)))
    Sharpe_ratio_array[index] = returns_array[index] / volatility_array[index]


# Optimisation du portfolio 
index_max_sharpe = Sharpe_ratio_array.argmax() #valeur de l'index de la grosse valeur de sharpe ratio sur 10k

#on récupère le point optimal du portfolio (X;Y)
max_sharpe_return = returns_array[index_max_sharpe] 
max_sharpe_volatility = volatility_array[index_max_sharpe]

weights_df = pd.DataFrame(weights_array)
all = pd.concat([stocks_lists,weights_df],ignore_index=True)
print(weights_df.iloc[index_max_sharpe]*100,'%')
print(all)

plt.figure(figsize=(12,8))
plt.scatter(volatility_array,returns_array,c=Sharpe_ratio_array,cmap='viridis',)
plt.colorbar(label='sharpe_array')
plt.title('Frontière Optmial du Portfolio x stocks')
plt.xlabel('Volatility')
plt.ylabel("E(X)")

#ajout du point optimal en orange et bordure noir
plt.scatter(max_sharpe_volatility,max_sharpe_return,c='orange',edgecolors='black') 
plt.annotate("This is my first 'big' project thanks to the classes from Coursera\n(Fundamentals Python, BRELAT Hugo)", 
             xy=(0.03, 0.92),            
             xycoords='axes fraction', 
             fontsize=10.5, 
             fontweight='bold',
             color='darkblue',
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.5)) # Petit encadré propre
plt.show()
#This is my first "big" project thanks to the classes from Coursera (Fundamentals Python)
#Brelat Hugo


