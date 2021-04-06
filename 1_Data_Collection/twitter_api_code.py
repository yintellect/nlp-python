
# coding: utf-8

# In[8]:


import os
import requests
import json
from base64 import b64encode
from urllib.parse import quote


# In[10]:


consumer_key=os.environ['TWI_API_KEY'] 
consumer_secret = os.environ['TWI_SECRET_KEY'] 


# In[11]:


TWITTER_POST = 'https://api.twitter.com/oauth2/token'

def get_token(consumer_key, consumer_secret):

    consumer_key = quote(consumer_key)

    consumer_secret = quote(consumer_secret)

    token = consumer_key + ':' + consumer_secret

    bearer_b64 = b64encode(token.encode('utf-8')).decode('utf-8')

    auth_headers = {
        "Authorization": "Basic " + bearer_b64 + "",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Content-Length": "29"}

    response = requests.post(TWITTER_POST, 
                             headers=auth_headers, 
                             data={'grant_type': 'client_credentials'})
    to_json = response.json()
    return to_json['access_token']


# In[13]:


access_token = get_token(consumer_key,consumer_secret)


# In[56]:


def get_tweets(key_word, count):
    
    base_url = 'https://api.twitter.com/'   
    
    search_params = {
    'q': key_word,
    'result_type': 'recent',
    'count': count}

    search_headers = {'Authorization': 'Bearer {}'.format(access_token)}
    
    search_url = '{}1.1/search/tweets.json'.format(base_url)

    search_response = requests.get(search_url, headers=search_headers, params=search_params)
    
    if search_response.status_code ==200:
        tweet_data = search_response.json()
        return tweet_data
    else:
        print ("Failed to search tweets")


# In[66]:


tweet_data=get_tweets("Columbia University", 100 )


# In[67]:


statuses = []
for x in tweet_data['statuses']:
    if len(x['text'])>1: statuses.append(x)    


# In[68]:


len(statuses)


# In[39]:


search_metadata = tweet_data['search_metadata']


# In[63]:


OUTPUT_FILE = './twitter_api_data.json'


# In[123]:


json.dump({'search_metadata': search_metadata,
           'statuses': statuses},
          open(OUTPUT_FILE, 'w'))


# In[64]:


import json
h12 = json.load(open('twitter_api_data.json', 'r'))


# In[65]:


len(h12['statuses'])

