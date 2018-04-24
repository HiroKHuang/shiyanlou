import json
import pandas as pd
import sys

def analysis(file, user_id):
    times = 0
    minutes = 0
    try:
        data_json = pd.read_json(file + '.json')
    except:
        return 0, 0
    times = data_json[data_json['user_id'] == int(user_id)]['lab'].count()
    minutes = data_json[data_json['user_id'] == int(user_id)]['minutes'].sum()
    return times,minutes

if __name__=='__main__':
    result = analysis(sys.argv[1], sys.argv[2])
    print(result)

