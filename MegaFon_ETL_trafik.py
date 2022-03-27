import pandas as pd
import numpy as np

# Определим количество строк
n=500

# Генерируем таблицу 1
table_1 = pd.DataFrame(columns=['id',
                                'Текущий баланс',
                                'Дата добавления',
                                'Возраст',
                                'Город проживания',
                                'Временная метка последней активности',
                                'Активный тариф']
                                )
                                
table_1['id'] = range(1,n+1)
table_1['Текущий баланс'] = (np.random.random(n)*100).round(2)

start_date = pd.to_datetime('2021-01-01')
last_activity_date = pd.to_datetime('2022-03-01')

time = pd.date_range(start_date, periods=n, freq='D')
activity_random = pd.date_range(last_activity_date, periods=n, freq='H')

table_1['Дата добавления'] = np.random.choice(time, n)

ages = np.arange(18, 85)
table_1['Возраст'] = np.random.choice(ages, n)

city = ['Москва','Санкт-Петербург','Уфа','Самара','Калининград','Краснодар','Омск','Таганрог']

table_1['Город проживания'] = np.random.choice(city, n)

table_1['Временная метка последней активности'] = np.random.choice(activity_random, n)

tarif_activ= np.arange(1,6) # 5 тарифов
table_1['Активный тариф'] = np.random.choice(tarif_activ,n)
table_1.to_csv('./table_1.csv', index=False)

# Генерируем таблицу 2
table_2 = pd.DataFrame(columns=['id',
                                'Название',
                                'Дата начала действия',
                                'Дата конца действия*',
                                'Объем минут',
                                'Объем смс',
                                'Объем трафика (мб)']
                                )
table_2['id'] = range(1,6)
table_2['Название'] = ['БезПереплат','Максимум','МегаТариф','VIP','Звонки']
table_2['Дата начала действия'] = ['2020-01-01','2021-11-15','2021-05-12','2021-01-31','2020-10-27']
table_2['Дата конца действия*'] = ['2021-01-01','2030-01-01','2025-09-11','2028-01-01','2024-12-01']
table_2['Объем минут'] = [300,800,600,1500,600]
table_2['Объем смс'] = [150,200,300,500,50]
table_2['Объем трафика (мб)'] = [1024,16384,1024*35,1024*45,1024*8]
table_2.to_csv('./table_2.csv', index=False)

# Генерируем таблицу 3
table_3 = pd.DataFrame(columns=['id',
                                'Метка времени',
                                'id абонента',
                                'Тип услуги (звонок, смс, трафик)',
                                'Объем затраченных единиц']
                                )
H = 3000 # Возьмём количество истории в 3000 строк
table_3['id'] = range(1,H+1)
target_date = pd.to_datetime('2022-03-01')
table_3['Метка времени'] = pd.date_range(target_date, periods=H, freq='H')
table_3['id абонента'] = np.random.choice(table_1['id'],H)
type_serv = ['звонок', 'смс', 'трафик']
table_3['Тип услуги (звонок, смс, трафик)'] = np.random.choice(type_serv,H)

# Запустим цикл по генерации чисел по каждой группе отдельно
for i in table_3.index:
    if table_3.loc[i,'Тип услуги (звонок, смс, трафик)'] == 'звонок':
        table_3.loc[i,'Объем затраченных единиц'] = np.random.randint(1,50)
    if table_3.loc[i,'Тип услуги (звонок, смс, трафик)'] == 'смс':
        table_3.loc[i,'Объем затраченных единиц'] = np.random.randint(1,3)
    if table_3.loc[i,'Тип услуги (звонок, смс, трафик)'] == 'трафик':
        table_3.loc[i,'Объем затраченных единиц'] = np.random.randint(80,500)    

#table_3['Объем затраченных единиц'] = table_3['Объем затраченных единиц'].astype('int') # Преобразуем тип в целочисленный
table_3.to_csv('./table_3.csv', index=False)


# Создадим отдельный класс для преобразования таблицы полученной на вход
class EveryDayTrafik:
        # инициализируем данные
        def __init__(self, table):
            self.next = None
            self.data = table

        # объявим метод, который позволит получить преобразованную таблицу
        def get_table(self):
            # Добавим столбцы в зависимости от типа трафика
            self['Потрачено минут'] = 0
            self['Потрачено смс'] = 0
            self['Потрачено трафика'] = 0
            
            # Запишем в каждый из столбцов соответсвующие значения при помощи цикла
            for i in self.index:
                if self.loc[i,'Тип услуги (звонок, смс, трафик)'] == 'звонок':
                    self.loc[i,'Потрачено минут'] = self.loc[i,'Объем затраченных единиц']
                if self.loc[i,'Тип услуги (звонок, смс, трафик)'] == 'смс':
                    self.loc[i,'Потрачено смс'] = self.loc[i,'Объем затраченных единиц']
                if self.loc[i,'Тип услуги (звонок, смс, трафик)'] == 'трафик':
                    self.loc[i,'Потрачено трафика'] = self.loc[i,'Объем затраченных единиц'] 
           
            # Преобразуем тип в целочисленный
            self['Объем затраченных единиц'] = self['Объем затраченных единиц'].astype('int')
            # Добавим преобразование даты в дату, чтобы в дальнейшем мы смогли осуществить ресемплироавние по дате
            self['Метка времени'] = pd.to_datetime(self['Метка времени'])

            # Соберём финальную таблицу по заданному формату
            fin_table = self\
                        .pivot_table(values=['Потрачено минут','Потрачено смс','Потрачено трафика'], index=['id абонента',pd.Grouper(key="Метка времени", freq="D")], aggfunc=('sum'))\
                        .reset_index()
            fin_table.columns = ['Абонент','Дата','Потрачено минут','Потрачено смс','Потрачено трафика']
            return fin_table

        # Определим метод при вызове которого будет преобразовываться таблица и сохраняться в локальной директории
        def save_table(self):
            save_table = EveryDayTrafik.get_table(self)
            save_table.to_csv('./EveryDayTrafik.csv', index=False)

        # объявим метод для вывода преобразованной таблицы на печать
        def print_table(self):
            print(EveryDayTrafik.get_table(self))

EveryDayTrafik.save_table(table_3)            