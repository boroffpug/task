# -*- coding: utf-8 -*-
"""
Created on Thu May  6 18:39:27 2021

@author: Preda
"""

import numpy
import pandas
from datetime import *

df = pandas.read_csv('C:/Users/Preda/applicant_task.csv')
#Посмотрим на таблицу
#print(df)
#print(df.info())
#print(df.nunique())

#работа с полами
#print(len(df['gender'].unique()))#сколько уникальных полов
#print(df['gender'].unique())#Их значения
df['gender'].fillna(value=2, inplace=True)#заменяем пол NaN на пол 2
x=df['gender'].unique()
s=[]
for a in x:
    gender1_paid = df.loc[(df['is_paid'] == 1) & (df['gender']== a)]#полов, которые заплатили
    gender1_all=df.loc[(df['gender']== a)]#полов, всего
    gender1_ratio=len(gender1_paid)/len(gender1_all)
    #print("Пол = ", a, "отношение оплативших: ",gender1_ratio)  
    s.append(gender1_ratio)
s.sort(reverse=True)
print('\n1) Эффективность у разных полов:',s)
gender_diff=s[0]-s[2]
print("Разница Пол 0 + '' и Пол 1",gender_diff*100,"%\n")
#Видим, как пол 1 вырывается по эффективности относительно пола 0 и пустого пола.
#Необходимо выяснить методику работы маркетологов и операторов с полами и изменить её для полов 0 и не указавших пол.

#работа с типом группы операторов
#print(len(df['operator_group_type'].unique()))#Тип группы оператора 1 линии, количество
x=0;
x=df['operator_group_type'].unique()
s.clear();
for a in x:
    group1_paid = df.loc[(df['is_paid'] == 1) & (df['operator_group_type']== a)]#
    group1_all=df.loc[(df['operator_group_type']== a)]#
    if len(group1_all) > 9:#убираем варианты с слишком маленьким количеством заявок
        group1_ratio=len(group1_paid)/len(group1_all)
        #print("Группа", a, "отношение оплативших: ",group1_ratio)  
        s.append(group1_ratio)
s.sort(reverse=True)   
print('2) Эффективность у разных типов групп:',s)
print('Максимальный разброс:',(s[0]-s[len(s)-1])*100, '%\n')
#Видим, что 1 из типов сильно впереди. Необходимо установить отличия методов работы от других и перенять его опыт.
#Также, можно увеличить количество операторов этого типа группы.

#работа с названиями групп операторов
#print(len(df['operator_group_name'].unique()))#название группы оператора 1 линии, количество
x=0;
x=df['operator_group_name'].unique()
s.clear();
for a in x:
    group1_paid = df.loc[(df['is_paid'] == 1) & (df['operator_group_name']== a)]#
    group1_all=df.loc[(df['operator_group_name']== a)]#
    if len(group1_all) > 9:#убираем варианты с слишком маленьким количеством заявок
        group1_ratio=len(group1_paid)/len(group1_all)
        #print("Группа", a, "отношение оплативших: ",group1_ratio)  
        s.append(group1_ratio)
s.sort(reverse=True)        
print('3) Эффективность у групп разных названий:',s)
print('Максимальный разброс:',(s[0]-s[len(s)-1])*100, '%\n')
# Видим, что первые две группы сильно впереди. Необходимо выяснить, почему у этих групп такая эффективность,
# и, возможно, воспользоваться методами для других, более слабых групп.
# Также можно объединить малые группы с <10 заявок с этими группами для обучения.

#Работа с источниками заявок
x=0;
x=df['source'].unique()
s.clear();
for a in x:
    group1_paid = df.loc[(df['is_paid'] == 1) & (df['source']== a)]#
    group1_all=df.loc[(df['source']== a)]
    if len(group1_all) > 9:#убираем варианты с слишком маленьким количеством заявок
        group1_ratio=len(group1_paid)/len(group1_all)
        #print("Источник, a, "отношение оплативших: ",group1_ratio)  
        s.append(group1_ratio)
s.sort(reverse=True)        
print('4) Эффективность у разных источников:',s)
print('Максимальный разброс:',(s[0]-s[len(s)-1])*100, '%\n')
#Очень большая разница у источников. Необходимы подробности, что это за источники, для дальнейшего анализа причин такой большой разницы.
#Вероятно, нужно ребалансировать количество работы с теми или инимы источниками.
#На этот пункт необходимо обратить внимание в первую очередь! 

#Работа с полями этапов звонков, у которых тип является датой/временем
df["application_datetime"]=pandas.to_datetime(df["application_datetime"])
df["trial_appointment_datetime"]=pandas.to_datetime(df["trial_appointment_datetime"])
df["first_call"]=pandas.to_datetime(df["first_call"])
df["first_reach"]=pandas.to_datetime(df["first_reach"])

#Поступление заявки - первый звонок
result1 = df[df['is_paid']==1]
result2 = result1['first_call'] - result1['application_datetime']
print("5) Поступление заявки - первый звонок\nОтрезки времени в случаях с оплатой: ", result2.mean())
result1=df[df['is_paid']==0]
result2 = result1['first_call'] - result1['application_datetime']
print("Отрезки времени в случаях без оплаты: ", result2.mean())

#Первый звонок - первый дозвон
result1=df[df['is_paid']==1]
result2 = result1['first_reach'] - result1['first_call']
print("\n6) Первый дозвон - первый звонок\nОтрезки времени в случаях с оплатой: ", result2.mean())
result1 = df[df['is_paid']==0]
result2 = result1['first_reach'] - result1['first_call']
print("Отрезки времени в случаях без оплаты: ", result2.mean())

#Вводный урок - первый звонок
result1=df[df['is_paid']==1]
result2 = result1['first_call'] - result1['trial_appointment_datetime']
print("\n7) Вводный урок - первый звонок\nОтрезки времени в случаях с оплатой: ", result2.mean())
result1=df[df['is_paid']==0]
result2 = result1['first_call'] - result1['trial_appointment_datetime']
print("Отрезки времени в случаях без оплаты: ", result2.mean())

#вводный урок - первый дозвон
result1=df[df['is_paid']==1]
result2 = result1['first_reach'] - result1['trial_appointment_datetime']
print("\n8) Вводный урок - первый дозвон\nОтрезки времени в случаях с оплатой: ", result2.mean())
result1=df[df['is_paid']==0]
result2 = result1['first_reach'] - result1['trial_appointment_datetime']
print("Отрезки времени в случаях без оплаты: ", result2.mean())
# Видим, что чем меньше промежутки, тем выше шанс покупки курса.
# Необходимо по возможности сокращать промежутки между этапами звонков. 
