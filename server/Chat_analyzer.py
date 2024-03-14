from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
import pandas as pd
import numpy as np
import re
from pickle import encode_long
from collections import Counter
# from urlextract import URLExtract

df=pd.read_fwf('/content/drive/MyDrive/Dataset/ML Projects/Chat Analyzer/WhatsApp Chat with 4 idiotz.txt',encode_long='utf-8')
df['3/20/21, 22:09 - You created group "3 idiotz"'][1616]
df.rename(columns={'3/20/21, 22:09 - You created group "3 idiotz"': 'user_message'}, inplace=True)
df['message_date']=df['user_message'].str.split('-').str.get(0)
df['user_message']=df['user_message'].str.split('-').str.get(1)
df['message_date'] = pd.to_datetime(df['message_date'].str.strip(), format='%m/%d/%y, %H:%M', errors='coerce')
df['user']=df['user_message'].str.split(':').str.get(0)
df['message']=df['user_message'].str.split(':').str.get(1)
df['message2']=np.where(df['message'].isnull(),df['user'],df['message'])
df['message'].fillna('Group Notification',inplace=True)
df['only_date'] = df['message_date'].dt.date
df['year'] = df['message_date'].dt.year
df['month_num'] = df['message_date'].dt.month
df['month'] = df['message_date'].dt.month_name()
df['day'] = df['message_date'].dt.day
df['day_name'] = df['message_date'].dt.day_name()
df['hour'] = df['message_date'].dt.hour
df['minute'] = df['message_date'].dt.minute
df.drop(columns=['message_date','user_message','message'],inplace=True)
np.where(df['user'] == df['message2'],print('haha'),print('bandyal'))
df['user'] = np.where(df['user'] == df['message2'], 'Group Notification', df['user'])
#Total Messages
df['user'].shape
#Total Number of messages by different users
df['user'].value_counts()
# Group Notification
df[df['user']=='Group Notification']
# number of Group Notification
df[df['user']=='Group Notification'].shape

df['user']=df['user'].str.strip()
# Messages by hamza
df['user']=='Hamza Uni'
df[df['user']=='Hamza Uni']
#total Words
newdf=df[df['user']!='Group Notification']
newdf['message2']=newdf['message2'].str.strip()
words= newdf[newdf['message2']!='<Media omitted>']['message2'].str.split().str.join(' ')
words.count()
#total Media
newdf=df[df['user']!='Group Notification']
newdf['message2']=newdf['message2'].str.strip()
words= newdf[newdf['message2']=='<Media omitted>']['message2'].str.split().str.join(' ')
words.shape

pd.DataFrame(Counter(words).most_common(20))
# extractor=URLExtract()
#total URL
# for message in df['message2']:
#   print(message)
#   url=(extractor.find_urls(str(message)))

#users and no of messages
x=df['user'].value_counts()
name=x.index
count=x.values
print(name)
print(count)

#users and no of messages per month
df.groupby(['month_num','month','year']).count()['message2'].reset_index()

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    # data_dict = json.loads(data)							
    # response = Predict_Win([[data_dict['batting_team'],data_dict['bowling_team'],data_dict['city'],data_dict['remaining_score'],data_dict['balls_left'],data_dict['wickets'],data_dict['total_runs_x']]])
    response = Predict_Win([[data['batting_team'],data['bowling_team'],data['city'],data['remaining_score'],data['balls_left'],data['wickets'],data['total_runs_x']]])
    print(response)
    response = np.array(response)
    response_list = response.tolist()
    return jsonify({'response': response_list})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)        