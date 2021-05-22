import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set()

df_birth = pd.read_csv('births.csv')

'''
print(df_birth.head())
print(df_birth.describe())
print('-----------------')
print(df_birth.info())
'''

# Les 480 dernieres lignes ont day = null, on les supprimes car négligeable pour notre dataset
df_birth = df_birth.dropna()

# on voit qu'il faut convertir day, il est en float64 on veut qu'il soit en int64
df_birth.day = df_birth.day.astype(int)

'''Les données de fin de mois sont souvent absurdes 
avec un jour 99 et un nombre de naissance anormalement faible,
parfois pour le 31 aussi. On recupere leurs index et on les supprimes
Cela ne pose que peu de probleme car ils sont uniformément répartis'''
indexNames = df_birth[df_birth['births'] <= 500].index
df_birth.drop(indexNames, inplace=True)

'''
print(df_birth.tail())
print(df_birth.describe())
print(df_birth.info())
'''
# Le dataset est maintenant nettoyé

# On fabrique la colone date de naissance complete
df_birth['full_birthdate'] = df_birth['year'].map(
    str) + '-' + df_birth['month'].map(str) + '-' + df_birth['day'].map(str)
df_birth['full_birthdate'] = pd.to_datetime(df_birth['full_birthdate'], format='%Y-%m-%d')

# On fabrique la colonne Jour de la semaine
df_birth['dayofweek'] = df_birth['full_birthdate'].dt.dayofweek

# On fabrique la colonne décenie
df_birth['decades'] = (df_birth['year'] // 10) * 10

print(df_birth.head())
# On crée finalement le tableau contenant les informations qui nous interressent
df_birth_weekday_by_decades = df_birth.pivot_table('births', index='dayofweek', columns='decades', aggfunc='sum')
print(df_birth_weekday_by_decades)

# il y a 10 fois moins de naissances dans les années 60 car notre dataset commence en 1969
df_average_birth_weekday_by_decades = df_birth.pivot_table(
    'births', index='dayofweek', columns='decades', aggfunc='mean')
print(df_average_birth_weekday_by_decades)

figure, axes = plt.subplots(2, 1)
g1=plt.subplot(211)
plt.title('Birth weekday by decades')
plt.plot(df_birth_weekday_by_decades)
plt.gca().set_xticklabels(['none', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
plt.ylabel('Births per day')

g2=plt.subplot(212)
df_average_birth_weekday_by_decades.plot(ax=axes[1])
plt.axes([0, 7, 0, 6000])
g2.set_ylabel('Average Births per day')
g2.legend(loc='lower left');

plt.show()
