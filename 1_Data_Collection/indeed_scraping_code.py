
# coding: utf-8

# In[6]:


import json
from random import uniform
from time import sleep


# In[7]:


import requests
from bs4 import BeautifulSoup


# In[9]:


INDEED_URL = 'https://www.indeed.com'
NUM_PAGES = 9
OUTPUT_FILE = './indeed_scraping_data.json'


# In[10]:


request_params = {
    'q': 'market research',
    'l': 'New York State',
    'jt': 'internship'}


# In[11]:


job_descs = []
job_ids = []
for i in range(NUM_PAGES):
    # Step 1, get the search page results
    request_params.update({'start': i * 10})
    indeed_response = requests.get(url=INDEED_URL + '/jobs',
                                   params=request_params)

    if indeed_response.status_code != 200:
        print('non-200 response for search page, skipping')
        continue

    indeed_search_html = indeed_response.text
    
    parsed_job_searches = BeautifulSoup(indeed_search_html, 'html.parser')
    
    posting_divs = parsed_job_searches.find_all(
        'div',
        attrs={"class": ["row", "result", "clickcard"]})
    
    for div in posting_divs:  
        if div.has_attr('data-jk') == True:
            job_ids.append(div.attrs['data-jk'])


  


# In[12]:


# Get the individual job descriptions
for job_id in job_ids:
    posting_response = requests.get(url=INDEED_URL + '/viewjob',
                                    params={'jk': job_id})
    indeed_job_html = posting_response.text
    if posting_response.status_code != 200:
        print('non-200 response for job description page, skipping')
        continue
    parsed_job_post = BeautifulSoup(indeed_job_html, 'html.parser')
    job_div = parsed_job_post.find(
        'div',
        attrs={'class': ['jobsearch-JobComponent-description']})
    
    # Checks if there's data at all
    if len(job_div.get_text())>1:
        job_descs.append(job_div.get_text())

        # DO NOT REMOVE THIS!
        # You're scraping, this slows down your request so you
        # do not overwhelm the site
    sleep(uniform(1, 5))


# In[21]:


json.dump({'request_params': request_params,
           'job_descriptions': job_descs},
          open(OUTPUT_FILE, 'w'))

