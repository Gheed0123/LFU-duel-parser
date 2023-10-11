# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 22:21:42 2023
#simple parser to get the zombie raid results for last fortress underground
@author: Gheed
"""

import os
import re
import pandas as pd

#%%input
log_folder = '\\'.join((os.getenv('appdata')).split('\\')[0:4])+'\\LocalLow\\im30\\Last Fortress\\Log\\'
output_loc=os.getcwd()+'\\zombie_raid.xlsx' #specify your path for the output xlsx here

#%%

latest_log=os.path.join(log_folder,os.listdir(log_folder)[-1])
with open(latest_log,encoding='utf-8') as f:
    lines = ''.join(f.readlines())

leaderboard=re.findall('..:..:..\........ - log\n# Message #<color=green>extension return <al.siege.panel.rewards> \|</color>.*\n',lines)
if(len(leaderboard)>0):
    data=re.findall('"name":"(.*?)","uid".*?"myScore":(.*?)}',leaderboard[-1])
    if(len(data)>0):
        try:
            data=pd.DataFrame(data)
            data.columns=['Names','Score']
            data.Names=data.Names.str.decode('unicode_escape')
            with pd.ExcelWriter(output_loc) as writer: 
                data.to_excel(writer,index=False)
        except:
            print('failed to write data to excel, check if you still have the file opened and have installed dependencies')
    print('done')
    