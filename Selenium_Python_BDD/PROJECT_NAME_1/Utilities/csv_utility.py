import re
import pandas as pd
from random import randint
from datetime import date, datetime
import csv
from sqlalchemy import column

def csvReader(filepath,random_no,CSV_Val_List):
    length = len(CSV_Val_List)
    fileread = pd.read_csv(filepath, sep=",")
    print(length)
    print(random_no)
    list=[]
    for i in range(length):
        value= fileread[CSV_Val_List[i]][random_no]
        list.append(value)
    return list

def csvWriter(filepath, column_list, value_list):
    content = pd.DataFrame([value_list], columns=column_list)
    content.to_csv(filepath, index=False,sep='|')

def rowcountfetch(filepath):
    fileread = pd.read_csv(filepath)
    filelength = len(fileread)
    return filelength

# Below function works on updating the mentioned csv column value for mentioned column name
def csvUpdate(filepath, column_to_update, column_value):
    fileread = pd.read_csv(filepath, sep="|")
    fileread.loc[0, column_to_update] = column_value
    fileread.to_csv(filepath, index=False, sep='|')   

def csvHeaderReader(filepath):
    df = pd.read_csv(filepath)
    list_of_column_names = list(df.columns)
    return list_of_column_names
    # fileread = pd.read_csv(filepath, sep="|")
    # columns = fileread.columns[0]
    # columnslist = []
    # columnslist = columns.split(",")
    # return columnslist

def compareLists(list1, list2):
    if list1 == list2:
        return "Equal"
    else:
        return "Not Equal"

    # return [x for x in list1 if x not in list2]

    # for item in list1:
    #     for item2 in list2:
    #         if item != item2:
    #             return item
    #         else:
    #             continue


# list1=[1,2,3]
# list2=[1,3,3]
# val=compareLists(list1,list2)
# print(val)









