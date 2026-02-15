#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import sys


# In[2]:


# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

headers = {"user-agent": USER_AGENT}
r = requests.get("https://www.techtarget.com/searchenterpriseai/definition/machine-learning-ML", headers=headers)

print("Status code: ", r.status_code)


# In[3]:


if r.status_code == 200:
    # resp = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
else:
    print("Scrapping is not possible")
    sys.exit(0)


# In[4]:


# name the output file to write to local disk
out_filename = "test_t.txt"

# title
# content
text = soup.find("div",{"class":"main-content"})

t1 = text.find("section", {"class":"section definition-section"})

anchor = text.find_all("section",{"class":"section main-article-chapter"})

# opens file, and writes headers
f = open(out_filename, "w")
#summary = t1.find("p").text
#print(summary)
#print(summary, file=open(out_filename, "a"))
t2 = t1.find_all("p")
for p in t2:
    summary = p.text
    print(summary)
    print(summary, file=open(out_filename, "a"))

for p in anchor:

    summary = p.find("p").text
    print(summary)
    print(summary, file=open(out_filename, "a"))

f.close() # Close the file


