import pandas as pd
import seaborn as sns
from numpy import log
from itertools import combinations
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


register_matplotlib_converters()
plt.style.use('seaborn-notebook')
myFmt = mdates.DateFormatter('%d/%m')

xbox = pd.read_excel('xbox one.xlsx',converters={'Data':pd.to_datetime})
xbox.drop(['Preco','Unnamed: 0'],axis=1,inplace=True)
xbox['Dia da Semana'] = [x.weekday() for x in xbox['Data']]
xbox['Semana'] = [int(x.strftime('%W')) for x in xbox['Data']]

tipo = []
for modelo in xbox['Modelo']:
    if ' S ' in modelo:
        tipo.append('S')
    elif ' X ' in modelo:
        tipo.append('X')
    else:
        tipo.append('Normal')
xbox['Tipo de Xbox'] = tipo


pmedio_data = xbox.groupby('Data',as_index=False).mean()
pmedio_data['MA7'] = pmedio_data['Preço'].rolling(7).mean()
pmedio_data['MA14'] = pmedio_data['Preço'].rolling(14).mean()
pmedio_data.index = [pmedio_data['Data'][i].strftime('%d/%m') for i in range(len(pmedio_data))]

xoneS = xbox[xbox['Tipo de Xbox']=='S'].groupby('Data',as_index=False).mean()
xoneS['MA7'] = xoneS['Preço'].rolling(7).mean()
xoneS['MA14'] = xoneS['Preço'].rolling(14).mean()
xoneS.index = [xoneS['Data'][i].strftime('%d/%m') for i in range(len(xoneS))]

#Plotar MA(7) e MA(14)
#Mostra tendência de queda
f, ax = plt.subplots(2,1,sharex=True,figsize=(12,6))
ax[0].set_title('Média Xbox One')
ax[0].plot(pmedio_data['Data'],pmedio_data['Preço'])
ax[0].plot(pmedio_data['Data'],pmedio_data['MA7'],linestyle='dotted')
ax[0].plot(pmedio_data['Data'],pmedio_data['MA14'],linestyle='dotted')
ax[0].xaxis.set_visible(False)

ax[1].set_title('Xbox One S')
ax[1].plot(xoneS['Data'],xoneS['Preço'])
ax[1].plot(xoneS['Data'],xoneS['MA7'],linestyle='dotted')
ax[1].plot(xoneS['Data'],xoneS['MA14'],linestyle='dotted')

ax[0].legend(['Preço Médio','MA7','MA14'])
plt.show()

#Distribuição dos Preços
f,ax=plt.subplots(1,1,figsize=(12,6))
sns.kdeplot(pmedio_data['Preço'],shade=True,legend=False)
sns.kdeplot(xoneS['Preço'],shade=True,legend=False)
plt.legend(['Média Xbox One','Xbox One S'])
plt.show()

#Analise semanas no ano
f, ax = plt.subplots(2,1,figsize=(12,6))
ax[0].set_title('Média Xbox One')
sns.boxplot(data=pmedio_data,x='Semana',y='Preço',ax=ax[0])
ax[0].xaxis.set_visible(False)

ax[1].set_title('Xbox One S')
sns.boxplot(data=xoneS,x='Semana',y='Preço',ax=ax[1])
plt.show()

#Analise dia da semana
f, ax = plt.subplots(2,1,figsize=(12,6))
ax[0].set_title('Média Xbox One')
sns.violinplot(data=pmedio_data,x='Dia da Semana',y='Preço',ax=ax[0])
ax[0].xaxis.set_visible(False)

ax[1].set_title('Xbox One S')
sns.violinplot(data=xoneS,x='Dia da Semana',y='Preço',ax=ax[1])
ax[1].set_xticklabels(['Segunda','Terça','Quarta','Quinta','Sexta','Sabado','Domingo'])
plt.show()
