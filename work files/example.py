import pandas as pd
import numpy  as np
import pycountry
import matplotlib.pyplot as plt
    
PLOT_LABEL_FONT_SIZE = 14

def dict_sort(my_dict):
    keys=[]
    values = []
    my_dict=sorted(my_dict.items(), key=lambda x : x[1], reverse=True)
    for k, v in my_dict:
        keys.append(k)
        values.append(v)
    return (keys, values)


df = pd.read_csv('./scrubbed.csv', escapechar='`', low_memory=False)
country_label_count = pd.value_counts(df['country'].values)
for label in list(country_label_count.keys()):    
      c = (pycountry.countries.get(alpha_2 = str(label).upper()))
      df = df.replace({'country':str(label)}, c.name)

colors=np.random.rand(7,3)

country_count = pd.value_counts(df['country'].values, sort=True)
country_count_keys, country_count_values = dict_sort(dict(country_count))
TOP_COUNTRY = len(country_count_keys)

plt.figure(1)
plt.title('Страны, где больше всего наблюдений', fontsize=PLOT_LABEL_FONT_SIZE)
plt.bar(np.arange(TOP_COUNTRY), country_count_values, color=colors)
plt.xticks(np.arange(TOP_COUNTRY), country_count_keys, rotation = 45, fontsize = 12)
plt.yticks(fontsize=PLOT_LABEL_FONT_SIZE)
plt.ylabel('Количество наблюдений', fontsize=PLOT_LABEL_FONT_SIZE)


MONTH_COUNT = [0,0,0,0,0,0,0,0,0,0,0,0]
MONTH_LABEL = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
  'Июль', 'Август', 'Сентябрь' ,'Октябрь' ,'Ноябрь' ,'Декабрь']
for i in df['datetime']:
    m, d, y_t = i.split('/')
    MONTH_COUNT[int(m)-1]=MONTH_COUNT[int(m)-1]+1
  
plt.figure(2)  
plt.bar(np.arange(12), MONTH_COUNT, color=colors)
plt.title('Частота появления объектов по месяцам', fontsize=PLOT_LABEL_FONT_SIZE)
plt.xticks(np.arange(12), MONTH_LABEL, rotation=90, fontsize=PLOT_LABEL_FONT_SIZE)
plt.yticks(fontsize=PLOT_LABEL_FONT_SIZE)
plt.ylabel('Частота появления', fontsize=PLOT_LABEL_FONT_SIZE)


plt.figure(3)
shapes_type_count = pd.value_counts(df['shape'].values)
shapes_type_count_keys, shapes_count_values = dict_sort(dict(shapes_type_count))
OBJECT_COUNT = len(shapes_type_count_keys)
plt.title('Типы объектов', fontsize=PLOT_LABEL_FONT_SIZE)
bar = plt.bar(np.arange(OBJECT_COUNT), shapes_count_values, color=colors)
plt.xticks(np.arange(OBJECT_COUNT), shapes_type_count_keys, rotation=90,
fontsize=PLOT_LABEL_FONT_SIZE)
plt.yticks(fontsize=PLOT_LABEL_FONT_SIZE)
plt.ylabel('Сколько раз видели', fontsize=PLOT_LABEL_FONT_SIZE)
    

plt.figure(4)
shapes_durations_dict = {}
for i in shapes_type_count_keys:
    dfs = df[['duration (seconds)', 'shape']].loc[df['shape'] == i]
    shapes_durations_dict[i] = dfs['duration (seconds)'].median(axis=0)/60.0/60.0
shapes_durations_dict_keys = []
shapes_durations_dict_values = []
for k in shapes_type_count_keys:
 shapes_durations_dict_keys.append(k)
 shapes_durations_dict_values.append(shapes_durations_dict[k])
plt.title('Среднее время появление каждого объекта', fontsize=12)
plt.bar(np.arange(OBJECT_COUNT), shapes_durations_dict_values, color=colors)
plt.xticks(np.arange(OBJECT_COUNT), shapes_durations_dict_keys, rotation=90,fontsize=16)
plt.ylabel('Среднее время появления в часах', fontsize=12)

for i in range(1, 4):
    plt.figure(i)
    plt.show()
