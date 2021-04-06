
# coding: utf-8

# # Question 0

# In[1]:


import glob
import simplejson as json
import re


# In[2]:


job_list = glob.glob('./jobs/*.json')


# In[3]:


jd = []
for job in job_list:
    job_file = json.load(open(job, 'r'))
    jd.append(job_file["job_descriptions"])


# In[4]:


from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import EnglishStemmer
tokenizer = RegexpTokenizer(r'\w+')


# In[5]:


tok_job = []
for descs in jd:
    for string in descs:
        string = re.sub(r'http\S+', '', string, flags=re.MULTILINE) 
        # lower all the 
        # tokenize the sentense
        toks = tokenizer.tokenize(string)
        # Stem the tokens 
        tok_des = [EnglishStemmer().stem(tok) for tok in toks]
        # combine every loop result
        tok_job.append(tok_des)


# In[11]:


OUTPUT_FILE = "{tokenized_jobs.json"


# In[12]:


json.dump(tok_job, 
          open(OUTPUT_FILE, 'w'))


# # Question 1:

# In[16]:


from gensim.corpora.dictionary import Dictionary
# Create a corpus from tokenized job description
gen_dictionary = Dictionary(tok_job)
common_corpus = [gen_dictionary.doc2bow(text) for text in tok_job]


# In[19]:


from gensim.models.ldamodel import LdaModel


# Fit the LDA model with 2 topics

# In[20]:


# Train the model on the corpus.
lda = LdaModel(common_corpus, num_topics = 2, id2word=gen_dictionary, passes=10)


# Use the LdaModel.print_topics() method to check the top words for the topics.

# In[24]:


topics = lda.print_topics(num_words=5)
for topic in topics:
    print(topic)


# The topics are dominated by the most frequent words, which is stop words in English. Not so helpful for topic detecting, though statistically solid.

# # Question 2:

# Remove stop words and other unwanted words from Question 1 before fitting the LdaModel using NLTK

# In[32]:


import nltk
from nltk.corpus import stopwords


# In[36]:


stopwords = set(stopwords.words('english'))


# In[47]:


nostop_job = []

for word_list in tok_job:
    for word in word_list:
        nostop_list = [w for w in word_list if not w in stopwords]
    nostop_job.append(nostop_list)


# Try fitting different number of topics, starting at 2, increasing it slowly until 20
# topics.

# In[53]:


nostop_dictionary = Dictionary(nostop_job)
nostop_corpus = [nostop_dictionary.doc2bow(text) for text in nostop_job]
nonstop_lda = LdaModel(nostop_corpus, num_topics = 2, id2word=nostop_dictionary, passes=10)


# In[54]:


topics = nonstop_lda.print_topics(num_words=5)
for topic in topics:
    print(topic)


# In[58]:


top_nums = [5, 8, 11, 14, 17, 20]
for num in top_nums:
    incre_lda = LdaModel(nostop_corpus, num_topics = num, id2word=nostop_dictionary, passes=10)
    incre_topics = incre_lda.print_topics(num_words=5)
    for topic in incre_topics:
        print("number of topics: "+str(num))
        print(topic) 
    print("========================")


# After removing the stopwords, some topic words pop up in the LDA model, such as data, financial, product...

# # Question 3:

# Apply the same processing in Question 2 to the resumes you read in for Problem 0.

# In[59]:


resumes= json.load(open('resumes.json', 'r'))


# In[65]:


tok_resume = []
for descs in resumes['resume_string']:
        descs = re.sub(r'http\S+', '', descs, flags=re.MULTILINE) 
        # lower all the 
        # tokenize the sentense
        toks = tokenizer.tokenize(descs)      
        tok_des = [tok for tok in toks if tok not in stopwords]
        # Stem the tokens 
        stm_tok = [EnglishStemmer().stem(tok) for tok in tok_des]
        # combine every loop result
        tok_resume.append(stm_tok)


# In[67]:


len(tok_resume)


# In[69]:


resume_dictionary = Dictionary(tok_resume)
resume_corpus = [resume_dictionary.doc2bow(text) for text in tok_resume]
resume_lda = LdaModel(resume_corpus, num_topics = 11, id2word=resume_dictionary, passes=10)


# In[111]:


topics = resume_lda.print_topics(num_words=5)
for topic in topics:
    print(topic)


# What are the top 3 most popular topic for the class? Write out the top 5 key
# words for these 3 topics.

# # Question 4:

# Which job align best with your topic distribution? (choose randomly if there’s a tie)

# In[121]:


text = ["data analyst"]
bow =  resume_dictionary.doc2bow(text)
resume_lda.get_document_topics(bow)


# Please describe this job then comment on this job and your opinion of its fit, what makes sense and what doesn’t make sense.
