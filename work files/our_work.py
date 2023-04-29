import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Функция суммирует значения в выбранном столбце
def summ_col(col):
    final= []
    for value in y:
        filter = (df.year == value) #Создание фильтра, чтобы брать значения в тех строках, где совпадает нужный год
        values_temp = list(df.loc[filter, col]) #Список из значений столбца для выбранного года
        values = sum(values_temp) #Сумма знаечний 
        final.append(values) #Добавляем сумму в список
    return final #Получаем список: суммарные значения для каждого года

#Функция находит числовое значение на основе процентов в столбце для выбранных параметров и суммирует итоговые значения для каждого года, тем самым формируя список      
def value_percent (x, perc):
    final =[]
    for value in y:
        temp= []
        filter = (df.year == value)
        percents = list(df.loc[filter, perc])#Получение списка процентов
        percents = [round(i/100, 3) for i in percents]#Перевод процентов в удобный для вычисления вид
        population = list(df.loc[filter, x])#Получение значений, для нахождения числового значения
        for i in range(len(y)):
            temp.append(population[i]*percents[i])#Находим числовое значение для каждого года и заносим значение в список
        final.append(sum(temp))#Находим суммарное значение для всего столбца
    return final

#Функция аналогична value_percent, но выполняет вычисления для одного года и конкретного региона
def invest(region, year, perc):
    temp =[]
    filter = (df.year == year) & (df.region == region)
    percents = list(df.loc[filter, perc])
    percents= [round(i/100, 3) for i in percents]
    invest = list(df.loc[filter, 'investment'])
    for i in range(len(invest)):
        temp.append(round(float(invest[i]*percents[i]), 4))
    return round(float(sum(temp)), 4)

#Функция формирует список значений для одного из 2 столбцов в зависимости от выбранных параметров и приведение значений в необходимый вид
def plots(settlement, value):
    temp = []
    for year in y:
        filter= (df.settlement == settlement) & (df.year == year)
        if value == 'wage':
            temp.append(df.loc[filter, value])
        if value == 'workers':
            temp.append(df.loc[filter, value] * 1000)
    return temp

path=input("Введите путь к DataFrame: ")
y=[2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016,2017, 2018, 2019] #Список годов для данного DF
df = pd.read_csv(path, escapechar='`', low_memory=False) #Чтение DF


x_pos = np.arange(1, len(y)+1) #Формирование позиций для необходимого распложения графиков гистограммы
wd=0.4 #Ширина столбца гистограммы

#Гистограмма состояния основных фондов
plt.figure(1)
plt.title('Размер основных фондов в России с 2008 по 2019 года, млн.руб.')
plt.xticks(x_pos, y, fontsize=14)

#Формирование основных столбов гистограммы (Наличие основных фондов)
Color = np.random.rand(7, 4)
plt.bar(x_pos, summ_col('assets'), color='blue', width=wd*2,  label='Наличие основных фондов', edgecolor='black')

#Формирование "подстолбов" гистограммы расположенных в нижней левой части основного столба
Color[:, 3] = 0.65
plt.bar(x_pos-wd/2, value_percent('assets','assets_depreciation'), color='yellow', width=wd, label='Степень износа основных фондов', edgecolor='black')

#Формирование "подстолбов" гистограммы расположенных в нижней правой части основного столба
Color = np.random.rand(7, 4)
Color[:, 3] = 0.65
plt.bar(x_pos+wd-wd/2, summ_col('assets_new'), color='green', width=wd, label='Ввод в действие основных фондов', edgecolor='black')

#Формирование "подстолбов" гистограммы расположенных в нижней левой части поверх столбов "Степень износа основных фондов"
Color[:, 3] = 0.3
plt.bar(x_pos-wd/2, value_percent('assets', 'assets_exhausted'), color='red', width=wd, label='Удельный вес полностью изношенных основных фондов в общем объеме', edgecolor='black')

plt.legend(loc='upper left', fontsize=10)


invest_value=round(float(sum(list(df.loc[(df.year == 2012) & (df.region == 'Алтайский край'), 'investment']))), 4) #Инвестиции в основной капитал в совокупности
invest_budg_value=invest('Алтайский край', 2012, 'invest_budg') #Инвестиции в основной капитал из бюджетных средств 
invest_fed_value=round(invest('Алтайский край', 2012, 'invest_fed'), 4) #Инвестиции в основной капитал из средств Федерального бюджета
invest_other_value=invest_value-invest_budg_value-invest_fed_value #Инвестиции в основной капитал из других источников финансирования

#Формирования списка источников финансирования в основной капитал 
values = []
values.append(invest_budg_value/invest_value*100)
values.append(invest_fed_value/invest_value*100)
values.append(invest_other_value/invest_value*100)

#Круговая диаграмма структуры инвестиций
labels=('Инвестиции в основной капитал,\nфинансируемые за счет бюджетных средств', 'Инвестиции в основной капитал,\n финансируемые за счет федерального бюджета', 'Другие источники инвестиций')
plt.figure(2)
plt.title('Структура инвестиций в основной капитал за 2012 год в Алтайском крае, млн.руб.')
plt.pie(values, autopct='%1.2f%%', labels=labels, explode=[0.1, 0.1, 0])
plt.axis('equal')


wage_values=plots('Тула', 'wage') #Среднемесячная номинальная начисленная з/п
workers_values=plots('Тула', 'workers') #Cреднегодовая численность работников в Туле

#Два графика: численность работников и номинальная з/п по годам в Туле
plt.figure(3)
fig, axs = plt.subplots(nrows=2, ncols=1)
axs[0].plot(y, workers_values, marker ='.', color='r')
axs[0].title.set_text('Среднегодовая численность работников в Туле')
axs[0].set_xlim([2007, 2020])

axs[1].plot(y, wage_values, marker='.', color='y')
axs[1].title.set_text('Среднемесячная номинальная начисленная з/п')
axs[1].set_xlim([2007, 2020])

for i in range(1, 2):
    plt.figure(i)
    plt.show()