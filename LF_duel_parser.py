# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 00:17:49 2023

basic alliance duel ranking parser using LF PC Beta
reads log files in locallow folder and exports data to xlsx

Note that it outputs the total ranking value based on all existing logs in the log folder. These logs reset after a certain amount/time

using Python 3.9
@author: Gheed
"""
import os
import pandas as pd
import re
from datetime import datetime,timezone,timedelta
import json
import numpy as np

xlsx_path=os.getcwd() #specify your path for the xlsx here

def log_parse_duel(loc):
    #json parser
    with open(loc,encoding='utf8') as f:
        lines = ''.join(f.readlines())
    
    duel_results = {}
    duels = re.findall('..:..:..\........ - log\n# Message #<color=green>extension return <al.battle.rank.info> \|</color>.*\n',lines)
    
    for duel in duels:
        timing = duel[:16]
        data = pd.read_json(duel.split('</color> ')[1])
        datas = [(i['name'],i['abbr'],i['score']) for i in data.rankInfo]
        duel_results[loc[-18:-10]+'-'+timing] = datas
        
    return duel_results

def read_duel_results():
    #read log folder of LF PC beta
    duel_results = {}
    source_folder = '\\'.join((os.getenv('appdata')).split('\\')[0:4])+'\\LocalLow\\im30\\Last Fortress\\Log\\'
    
    for root, dirs, files in os.walk(source_folder):
        for _file in files:
            if(_file.endswith('.txt')):
                loc = root+'/'+_file
                duel_results = duel_results|log_parse_duel(loc)
                
    return duel_results

def duel_to_csv(duel_results,path):
    #grabs total highest score and plops it in xlsx
    pathname = path+'/'+'duel_results.xlsx'
    
    tz = datetime.now(timezone.utc).astimezone().tzinfo
    date = datetime.strptime(list(duel_results.keys())[-1][:-1],'%Y%m%d-%H:%M:%S.%f').replace(tzinfo=tz)
    date = datetime.fromtimestamp(date.timestamp(),timezone.utc)
    reset_date = date-timedelta(minutes=30)
    wday = datetime.weekday(reset_date)
    
    names = {0:'Gathering',1:'Building',2:'Research',3:'Hero Recruit',4:'Troop Training',5:'Kill',6:'NaN'}
    event = names[wday]
    
    keys = list(duel_results.keys())
    df = pd.concat([pd.DataFrame(duel_results[key]) for key in keys])
    df.columns = ['Name','Abbr',event]
    df = df.groupby(['Name','Abbr']).max().reset_index().sort_values(by=event,ascending=False)
    
    if(wday != 0):
        try:
        #read data and merge
            df2 = pd.read_excel(pathname,sheet_name='Duel_Results')
    
            #rerun ez pz fix
            if(event in df2.columns):
                df2 = df2.drop(event,axis=1)
                
            #do append
            df = df2.merge(df,how='outer',on=['Name','Abbr'])
        except:
            print('failed to open/merge with existing file')

    with pd.ExcelWriter(pathname) as writer:         
        df.to_excel(writer,sheet_name = 'Duel_Results',index=False)
        
    return
 
def main(path):    
    input("Did you open A/D results ? Press Enter to continue...")
    print("Reading log files")
    duel_results = read_duel_results()
    print("parsing results")
    duel_to_csv(duel_results,path)  
    print("saved AD results!")
    print("path: " +path)
    
    return

main(xlsx_path)