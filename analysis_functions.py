import urllib.request
from bs4 import BeautifulSoup as bs
import pprint                                  
pp = pprint.PrettyPrinter(indent=4) 
import re
import os
import re
import string 
import nltk
from nltk.tokenize import RegexpTokenizer      
from nltk.corpus import stopwords
english_stops = set(stopwords.words('english'))
import pprint 
pp = pprint.PrettyPrinter(indent=4)  
from nltk.tokenize import word_tokenize 
tokenizer = RegexpTokenizer("['\w']+")
punctuations = list(string.punctuation)
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures
import matplotlib.pyplot as plt

#This function reads hubspot, cleans the pagination from the categories and returns a sorted list, 
#read_hubspot(all_hubspot.csv)[1] returns all of the articles written by Dan Lyons
# read_hubspot(all_hubspot.csv)[0] returns all of the articles not written by Dan Lyons
def read_hubspot(file):
    fin = open(file)

    all_articles = []
    hubspot_non_lyons = []
    hubspot_dan_lyons = []
    
    for line in fin:
        if(line.startswith("Title")):      
                continue
        article_info = line.strip().split(",")
        
        article_info[4] = re.sub('\/page/.*', '', article_info[4])
        article_info[5] = re.sub('\/page/.*', '', article_info[5])
        article_info[6] = re.sub('\/page/.*', '', article_info[6])
        article_info[7] = re.sub('\/page/.*', '', article_info[7])
        article_info[8] = re.sub('\/page/.*', '', article_info[8])
        article_info[9] = re.sub('\/page/.*', '', article_info[9])
        article_info[10] = re.sub('\/page/.*', '', article_info[10])
        
        all_articles.append(article_info)

        res = re.search("Dan Lyon", article_info[1])
        if res:
            hubspot_dan_lyons.append(article_info[:11])
            
        else:
            hubspot_non_lyons.append(article_info[:11])
            
    return (hubspot_non_lyons, hubspot_dan_lyons)
        
    fin.close()

read_hubspot("data/pre_lyons.csv")

# This function reads the buzzfeed file and returns all of the articles with their categories. 
def read_buzzfeed():
    fin = open("data/buzzfeed.csv")

    all_articles = []
    
    for line in fin:
        if(line.startswith("Title")):      
                continue
        article_info = line.split(",")
        
        article_info = [info.strip() for info in article_info] #uses list comprehension to strip blank space from end of titles
        
        all_articles.append(article_info)
    return (all_articles)    
    fin.close()
read_buzzfeed()

articles = read_hubspot("data/all_hubspot.csv")[0]

def average_word_count(articles):
    titles = []
    total = 0
    for article in articles:
        
        titles.append(article[0])
    
    count = 0
    for title in titles:
        
        words = title.split()
        #print(words)
        length = len(words)
        
        total = total + length
    
        count = count + 1
    
    average = total/count
    return(average)

average_word_count(articles)

articles = read_hubspot("data/all_hubspot.csv")[0]
def average_len_word(articles):
    titles = []
    
    for article in articles:
        
        titles.append(article[0])
    all_words = []
    for title in titles:
        
        
        words = word_tokenize(title)
        
        for word in words:
            if word in punctuations:
                continue
            
            res = re.search("[0-9]", word) 
            if res: 
                
                continue
              
        all_words.append(word)
    average = sum(len(w) for w in all_words)/len(all_words) 
    return (average)   

average_len_word(articles)

articles = read_hubspot("data/all_hubspot.csv")[0]
def authors(articles):
    
    author_count = {}
    
    for line in articles:
        
        if line[1] not in author_count:
        
            author_count[line[1]] = 1
        else:
            author_count[line[1]] = author_count[line[1]] + 1
    
    author = list() # create a list that can be used to sort that dictionary in order of occurances 
    for key,value in list(author_count.items()):
        if value > 1:
            author.append((value,key))
    author.sort(reverse=True)
 
    author = ["\'" + a[1] + ": " + str(a[0]) + "\'" for a in author[:3]] #creates a list where each word in the bi grams are seperated by spaces 
    
    author = " ".join(author) 
    
    return(author)
authors(articles)

articles = read_hubspot("data/all_hubspot.csv")[0]
def hs_categories(articles):
        
    all_info = []
    all_titles = []
    all_authors = {}
    all_categories = {}
    
    for line in articles:
        
        if line[4] in all_categories:
                all_categories[line[4]] = all_categories[line[4]] + 1
        else:
            all_categories[line[4]] = 1
            
        if line[5] in all_categories:
            all_categories[line[5]] = all_categories[line[5]] + 1
        else:
            all_categories[line[5]] = 1
            
        if line[6] in all_categories:
            all_categories[line[6]] = all_categories[line[6]] + 1
        else:
            all_categories[line[6]] = 1
            
        if line[7] in all_categories:
            all_categories[line[7]] = all_categories[line[7]] + 1
        else:
            all_categories[line[7]] = 1
            
        if line[8] in all_categories:
            all_categories[line[8]] = all_categories[line[8]] + 1
        else:
            all_categories[line[8]] = 1
            
        if line[9] in all_categories:
            all_categories[line[9]] = all_categories[line[9]] + 1
        else:
            all_categories[line[9]] = 1
            
        if line[10] in all_categories:
            all_categories[line[10]] = all_categories[line[10]] + 1
        else:
            all_categories[line[10]] = 1
                
    categories = list()
    for key,value in list(all_categories.items()):
        
        categories.append((value,key))
    categories.sort(reverse=True)            
    
    categories = ["\'" + c[1] + ": " + str(c[0]) + "\'" for c in categories[1:4]] #creates a list where each word in the bi grams are seperated by spaces 
    
    # Using categories[1:4] because the top occuring category will be "" due to the way that blank space was dealt with earlier as a placehold in case there were not 7 categories per link
    categories = " ".join(categories) 

    return(categories)
    
hs_categories(articles)

articles = read_buzzfeed()

def bf_categories(articles):
        
    all_info = []
    all_titles = []
    all_authors = {}
    all_categories = {}
    
    for line in articles:
        
        if line[1] in all_categories:
                all_categories[line[1]] = all_categories[line[1]] + 1
        else:
            all_categories[line[1]] = 1
                
    categories = list()
    for key,value in list(all_categories.items()):
        
        categories.append((value,key))
    categories.sort(reverse=True)            
    
    categories = ["\'" + c[1] + ": " + str(c[0]) + "\'" for c in categories[:3]] #creates a list where each word in the bi grams are seperated by spaces 
    
    categories = " ".join(categories) 

    return(categories)
    
bf_categories(articles)

articles = read_hubspot("data/all_hubspot.csv")[1]

def hs_contains_number(articles):
    
    matches = 0 
    total = 0
    all_info = []
    all_titles = []
    all_authors = {}
    all_categories = {}
    matched_categories = {}
    for line in articles:
        
        total = total + 1
        #res = re.search(":", line[0]) 
        res = re.search("[0-9]", line[0]) # Regular Expression to find numbers at the beggining of titles, this is the only line of code that changes  
        
        if res:
            matches = matches + 1
            all_info.append(line)
            all_titles.append(line[0])
           
            if line[1] in all_authors:
                all_authors[line[1]] = all_authors[line[1]] + 1
            else:
                all_authors[line[1]] = 1
            
            if line[4] in matched_categories and matched_categories[line[4]] != 0:
                matched_categories[line[4]] = matched_categories[line[4]] + 1
            else:
                matched_categories[line[4]] = 1
            
            if line[5] in matched_categories and matched_categories[line[5]] != 0:
                matched_categories[line[5]] = matched_categories[line[5]] + 1
            else:
                matched_categories[line[5]] = 1
            
            if line[6] in matched_categories and matched_categories[line[6]] != 0:
                matched_categories[line[6]] = matched_categories[line[6]] + 1
            else:
                matched_categories[line[6]] = 1
            
            if line[7] in matched_categories and matched_categories[line[7]] != 0:
                matched_categories[line[7]] = matched_categories[line[7]] + 1
            else:
                matched_categories[line[7]] = 1
            
            if line[8] in matched_categories and matched_categories[line[8]] != 0:
                matched_categories[line[8]] = matched_categories[line[8]] + 1
            else:
                matched_categories[line[8]] = 1
            
            if line[9] in matched_categories and matched_categories[line[9]] != 0:
                matched_categories[line[9]] = matched_categories[line[9]] + 1
            else:
                matched_categories[line[9]] = 1
            
            if line[10] in matched_categories and matched_categories[line[10]] != 0:
                matched_categories[line[10]] = matched_categories[line[10]] + 1
            else:
                matched_categories[line[10]] = 1

        
        if line[4] in all_categories:
            all_categories[line[4]] = all_categories[line[4]] + 1
        else:
            all_categories[line[4]] = 1
            matched_categories[line[4]] = 0
            
        if line[5] in all_categories:
            all_categories[line[5]] = all_categories[line[5]] + 1
        else:
            all_categories[line[5]] = 1
            matched_categories[line[5]] = 0
            
        if line[6] in all_categories:
            all_categories[line[6]] = all_categories[line[6]] + 1
        else:
            all_categories[line[6]] = 1
            matched_categories[line[6]] = 0
            
        if line[7] in all_categories:
            all_categories[line[7]] = all_categories[line[7]] + 1
        else:
            all_categories[line[7]] = 1
            matched_categories[line[7]] = 0
            
        if line[8] in all_categories:
            all_categories[line[8]] = all_categories[line[8]] + 1
        else:
            all_categories[line[8]] = 1
            matched_categories[line[8]] = 0
            
        if line[9] in all_categories:
            all_categories[line[9]] = all_categories[line[9]] + 1
        else:
            all_categories[line[9]] = 1
            matched_categories[line[9]] = 0
            
        if line[10] in all_categories:
            all_categories[line[10]] = all_categories[line[10]] + 1
        else:
            all_categories[line[10]] = 1
            matched_categories[line[10]] = 0
        

    top_percent = [] 
    bottom_percent = []
    category_percent = []
    
    for cat in all_categories:
        
        cp = str(matched_categories[cat]/all_categories[cat]) 
    
        category_percent.append(cp[:4] + " " + cat)
    category_percent.sort()
    
    bottom_percent = str(category_percent[2]) + " " + str(category_percent[1]) + " " + str(category_percent[0])
    top_percent = str(category_percent[len(category_percent)-1]) + " " + str(category_percent[len(category_percent)-2]) + " " + str(category_percent[len(category_percent)-3])
    
            
    authors = list()
    for key,value in list(all_authors.items()):
        
        authors.append((value,key))
    authors.sort(reverse=True)            
    
    authors = ["\'" + a[1] + ": " + str(a[0]) + "\'" for a in authors[:3]] #creates a list where each word in the bi grams are seperated by spaces 
    
    authors = " ".join(authors) 
             
    categories = list()
    for key,value in list(matched_categories.items()):
        
        categories.append((value,key))
    categories.sort(reverse=True)            
    
    categories = ["\'" + c[1] + ": " + str(c[0]) + "\'" for c in categories[1:4]] #creates a list where each word in the bi grams are seperated by spaces 
    
    
    top_categories = " ".join(categories) 

    overall_percent = matches/ total
    
    example_title = all_titles[0] if len(all_titles) > 0 else ""
    
    return[len(all_titles), "%.2f" % overall_percent ,authors, top_categories, top_percent, bottom_percent, example_title, category_percent, all_titles,all_info]
# returns the number of articles that meet regular expression, the over all percent of articles, the top 3 authors, top 3 categories, the most occuring categories by percent, least occuring categories by percent, a smaple title, all of the categories by percent, all the titles, and then all of the articles information     
hs_contains_number(articles)


articles = read_buzzfeed()

def bf_contains_number(articles):
    
    all_info = []
    all_titles = []
    all_categories = {}
    matches = 0
    total = 0
    matched_categories = {}
    
    for line in articles:
        
        total = total + 1
        
        res = re.search("[0-9]", line[0]) # Regular Expression to check if title contains number, only line that changes 
    
        if res:
            matches = matches + 1
            all_info.append(line)
            all_titles.append(line[0])
            
            if line[1] in matched_categories and matched_categories[line[1]] != 0:
                matched_categories[line[1]] = matched_categories[line[1]] + 1
            else:
                matched_categories[line[1]] = 1
            
        if line[1] in all_categories:
            all_categories[line[1]] = all_categories[line[1]] + 1
        else:
            all_categories[line[1]] = 1
            matched_categories[line[1]] = 0
            
    top_percent = [] 
    bottom_percent = []
    category_percent = []

    for cat in all_categories:
        
        cp = str(matched_categories[cat]/all_categories[cat]) 
    
        category_percent.append(cp[:4] + " " + cat)
    category_percent.sort()
    
    bottom_percent = str(category_percent[2]) + " " + str(category_percent[1]) + " " + str(category_percent[0])
    top_percent = str(category_percent[len(category_percent)-1]) + " " + str(category_percent[len(category_percent)-2]) + " " + str(category_percent[len(category_percent)-3])
    
    
    categories = list()
    for key,value in list(matched_categories.items()):
        
        categories.append((value,key))
    categories.sort(reverse=True)            
    
    categories = ["\'" + c[1] + ": " + str(c[0]) + "\'" for c in categories[1:4]] #creates a list where each word in the bi grams are seperated by spaces 
    
    top_categories = " ".join(categories) 
    
    overall_percent = matches/total

    example_title = all_titles[0] if len(all_titles) > 0 else ""

    return[len(all_titles), "%.2f" % overall_percent , "N/A", top_categories, top_percent, bottom_percent, example_title, category_percent, all_titles,all_info]
       
bf_contains_number(articles)

articles = read_hubspot("data/all_hubspot.csv")[0]

def hs_starts_number(articles):
    
    matches = 0 
    total = 0
    all_info = []
    all_titles = []
    all_authors = {}
    all_categories = {}
    matched_categories = {}
    for line in articles:
        
        total = total + 1
        res = re.search("^[0-9]", line[0]) # Regular Expression to find numbers at the beggining of titles, this is the only line of code that changes  
        
        if res:
            matches = matches + 1
            all_info.append(line)
            all_titles.append(line[0])
           
            if line[1] in all_authors:
                all_authors[line[1]] = all_authors[line[1]] + 1
            else:
                all_authors[line[1]] = 1
            
            if line[4] in matched_categories and matched_categories[line[4]] != 0:
                matched_categories[line[4]] = matched_categories[line[4]] + 1
            else:
                matched_categories[line[4]] = 1
            
            if line[5] in matched_categories and matched_categories[line[5]] != 0:
                matched_categories[line[5]] = matched_categories[line[5]] + 1
            else:
                matched_categories[line[5]] = 1
            
            if line[6] in matched_categories and matched_categories[line[6]] != 0:
                matched_categories[line[6]] = matched_categories[line[6]] + 1
            else:
                matched_categories[line[6]] = 1
            
            if line[7] in matched_categories and matched_categories[line[7]] != 0:
                matched_categories[line[7]] = matched_categories[line[7]] + 1
            else:
                matched_categories[line[7]] = 1
            
            if line[8] in matched_categories and matched_categories[line[8]] != 0:
                matched_categories[line[8]] = matched_categories[line[8]] + 1
            else:
                matched_categories[line[8]] = 1
            
            if line[9] in matched_categories and matched_categories[line[9]] != 0:
                matched_categories[line[9]] = matched_categories[line[9]] + 1
            else:
                matched_categories[line[9]] = 1
            
            if line[10] in matched_categories and matched_categories[line[10]] != 0:
                matched_categories[line[10]] = matched_categories[line[10]] + 1
            else:
                matched_categories[line[10]] = 1

        
        if line[4] in all_categories:
            all_categories[line[4]] = all_categories[line[4]] + 1
        else:
            all_categories[line[4]] = 1
            matched_categories[line[4]] = 0
            
        if line[5] in all_categories:
            all_categories[line[5]] = all_categories[line[5]] + 1
        else:
            all_categories[line[5]] = 1
            matched_categories[line[5]] = 0
            
        if line[6] in all_categories:
            all_categories[line[6]] = all_categories[line[6]] + 1
        else:
            all_categories[line[6]] = 1
            matched_categories[line[6]] = 0
            
        if line[7] in all_categories:
            all_categories[line[7]] = all_categories[line[7]] + 1
        else:
            all_categories[line[7]] = 1
            matched_categories[line[7]] = 0
            
        if line[8] in all_categories:
            all_categories[line[8]] = all_categories[line[8]] + 1
        else:
            all_categories[line[8]] = 1
            matched_categories[line[8]] = 0
            
        if line[9] in all_categories:
            all_categories[line[9]] = all_categories[line[9]] + 1
        else:
            all_categories[line[9]] = 1
            matched_categories[line[9]] = 0
            
        if line[10] in all_categories:
            all_categories[line[10]] = all_categories[line[10]] + 1
        else:
            all_categories[line[10]] = 1
            matched_categories[line[10]] = 0
        

    top_percent = [] 
    bottom_percent = []
    category_percent = []
    
    for cat in all_categories:
        
        cp = str(matched_categories[cat]/all_categories[cat]) 
    
        category_percent.append(cp[:4] + " " + cat)
    category_percent.sort()
    
    bottom_percent = str(category_percent[2]) + " " + str(category_percent[1]) + " " + str(category_percent[0])
    top_percent = str(category_percent[len(category_percent)-1]) + " " + str(category_percent[len(category_percent)-2]) + " " + str(category_percent[len(category_percent)-3])
    
            
    authors = list()
    for key,value in list(all_authors.items()):
        
        authors.append((value,key))
    authors.sort(reverse=True)            
    
    authors = ["\'" + a[1] + ": " + str(a[0]) + "\'" for a in authors[:3]] #creates a list where each word in the bi grams are seperated by spaces 
    
    authors = " ".join(authors) 
             
    categories = list()
    for key,value in list(matched_categories.items()):
        
        categories.append((value,key))
    categories.sort(reverse=True)            
    
    categories = ["\'" + c[1] + ": " + str(c[0]) + "\'" for c in categories[1:4]] #creates a list where each word in the bi grams are seperated by spaces 
    
    
    top_categories = " ".join(categories) 

    overall_percent = matches/ total
    
    example_title = all_titles[0] if len(all_titles) > 0 else ""
    
    return[len(all_titles), "%.2f" % overall_percent ,authors, top_categories, top_percent, bottom_percent, example_title, category_percent, all_titles,all_info]
# returns the number of articles that meet regular expression, the over all percent of articles, the top 3 authors, top 3 categories, the most occuring categories by percent, least occuring categories by percent, a smaple title, all of the categories by percent, all the titles, and then all of the articles information 
    
hs_starts_number(articles)

articles = read_buzzfeed()

def bf_starts_number(articles):
    
    all_info = []
    all_titles = []
    all_categories = {}
    matches = 0
    total = 0
    matched_categories = {}
    
    for line in articles:
        
        total = total + 1
        
        res = re.search("^[0-9]", line[0]) 
        if res:
            matches = matches + 1
            all_info.append(line)
            all_titles.append(line[0])
            
            if line[1] in matched_categories and matched_categories[line[1]] != 0:
                matched_categories[line[1]] = matched_categories[line[1]] + 1
            else:
                matched_categories[line[1]] = 1
            
        if line[1] in all_categories:
            all_categories[line[1]] = all_categories[line[1]] + 1
        else:
            all_categories[line[1]] = 1
            matched_categories[line[1]] = 0
            
    top_percent = [] 
    bottom_percent = []
    category_percent = []

    for cat in all_categories:
        
        cp = str(matched_categories[cat]/all_categories[cat]) 
    
        category_percent.append(cp[:4] + " " + cat)
    category_percent.sort()

    bottom_percent = str(category_percent[2]) + " " + str(category_percent[1]) + " " + str(category_percent[0])
    top_percent = str(category_percent[len(category_percent)-1]) + " " + str(category_percent[len(category_percent)-2]) + " " + str(category_percent[len(category_percent)-3])
    
    
    categories = list()
    for key,value in list(matched_categories.items()):
        
        categories.append((value,key))
    categories.sort(reverse=True)            
    
    categories = ["\'" + c[1] + ": " + str(c[0]) + "\'" for c in categories[1:4]] #creates a list where each word in the bi grams are seperated by spaces 
    
    top_categories = " ".join(categories) 
    
    overall_percent = matches/total

    example_title = all_titles[0] if len(all_titles) > 0 else ""

    return[len(all_titles), "%.2f" % overall_percent , "N/A", top_categories, top_percent, bottom_percent, example_title, category_percent, all_titles,all_info]
       
bf_starts_number(articles)

articles = read_hubspot("data/all_hubspot.csv")[0]

def hs_how_to(articles):
    
    matches = 0 
    total = 0
    all_info = []
    all_titles = []
    all_authors = {}
    all_categories = {}
    matched_categories = {}
    for line in articles:
        
        total = total + 1
        
        line[0] = line[0].lower()
        res = re.search("how to", line[0]) # Regular Expression to find numbers at the beggining of titles, this is the only line of code that changes  
        
        if res:
            matches = matches + 1
            all_info.append(line)
            all_titles.append(line[0])
           
            if line[1] in all_authors:
                all_authors[line[1]] = all_authors[line[1]] + 1
            else:
                all_authors[line[1]] = 1
            
            if line[4] in matched_categories and matched_categories[line[4]] != 0:
                matched_categories[line[4]] = matched_categories[line[4]] + 1
            else:
                matched_categories[line[4]] = 1
            
            if line[5] in matched_categories and matched_categories[line[5]] != 0:
                matched_categories[line[5]] = matched_categories[line[5]] + 1
            else:
                matched_categories[line[5]] = 1
            
            if line[6] in matched_categories and matched_categories[line[6]] != 0:
                matched_categories[line[6]] = matched_categories[line[6]] + 1
            else:
                matched_categories[line[6]] = 1
            
            if line[7] in matched_categories and matched_categories[line[7]] != 0:
                matched_categories[line[7]] = matched_categories[line[7]] + 1
            else:
                matched_categories[line[7]] = 1
            
            if line[8] in matched_categories and matched_categories[line[8]] != 0:
                matched_categories[line[8]] = matched_categories[line[8]] + 1
            else:
                matched_categories[line[8]] = 1
            
            if line[9] in matched_categories and matched_categories[line[9]] != 0:
                matched_categories[line[9]] = matched_categories[line[9]] + 1
            else:
                matched_categories[line[9]] = 1
            
            if line[10] in matched_categories and matched_categories[line[10]] != 0:
                matched_categories[line[10]] = matched_categories[line[10]] + 1
            else:
                matched_categories[line[10]] = 1

        
        if line[4] in all_categories:
            all_categories[line[4]] = all_categories[line[4]] + 1
        else:
            all_categories[line[4]] = 1
            matched_categories[line[4]] = 0
            
        if line[5] in all_categories:
            all_categories[line[5]] = all_categories[line[5]] + 1
        else:
            all_categories[line[5]] = 1
            matched_categories[line[5]] = 0
            
        if line[6] in all_categories:
            all_categories[line[6]] = all_categories[line[6]] + 1
        else:
            all_categories[line[6]] = 1
            matched_categories[line[6]] = 0
            
        if line[7] in all_categories:
            all_categories[line[7]] = all_categories[line[7]] + 1
        else:
            all_categories[line[7]] = 1
            matched_categories[line[7]] = 0
            
        if line[8] in all_categories:
            all_categories[line[8]] = all_categories[line[8]] + 1
        else:
            all_categories[line[8]] = 1
            matched_categories[line[8]] = 0
            
        if line[9] in all_categories:
            all_categories[line[9]] = all_categories[line[9]] + 1
        else:
            all_categories[line[9]] = 1
            matched_categories[line[9]] = 0
            
        if line[10] in all_categories:
            all_categories[line[10]] = all_categories[line[10]] + 1
        else:
            all_categories[line[10]] = 1
            matched_categories[line[10]] = 0
        

    top_percent = [] 
    bottom_percent = []
    category_percent = []
    
    for cat in all_categories:
        
        cp = str(matched_categories[cat]/all_categories[cat]) 
    
        category_percent.append(cp[:4] + " " + cat)
    category_percent.sort()
     
    bottom_percent = str(category_percent[2]) + " " + str(category_percent[1]) + " " + str(category_percent[0])
    top_percent = str(category_percent[len(category_percent)-1]) + " " + str(category_percent[len(category_percent)-2]) + " " + str(category_percent[len(category_percent)-3])
        
        
    authors = list()
    for key,value in list(all_authors.items()):
        
        authors.append((value,key))
    authors.sort(reverse=True)            
    
    authors = ["\'" + a[1] + ": " + str(a[0]) + "\'" for a in authors[:3]] #creates a list where each word in the bi grams are seperated by spaces 
    
    authors = " ".join(authors) 
             
    categories = list()
    for key,value in list(matched_categories.items()):
        
        categories.append((value,key))
    categories.sort(reverse=True)            
    
    categories = ["\'" + c[1] + ": " + str(c[0]) + "\'" for c in categories[1:4]] #creates a list where each word in the bi grams are seperated by spaces 
    
    
    top_categories = " ".join(categories) 

    overall_percent = matches/ total
    
    example_title = all_titles[0] if len(all_titles) > 0 else ""
    
    return[len(all_titles), "%.2f" % overall_percent ,authors, top_categories, top_percent, bottom_percent, example_title, category_percent, all_titles,all_info]
# returns the number of articles that meet regular expression, the over all percent of articles, the top 3 authors, top 3 categories, the most occuring categories by percent, least occuring categories by percent, a smaple title, all of the categories by percent, all the titles, and then all of the articles information 
    
hs_how_to(articles)

articles = read_buzzfeed()

def bf_how_to(articles):
    
    all_info = []
    all_titles = []
    all_categories = {}
    matches = 0
    total = 0
    matched_categories = {}
    
    for line in articles:
        
        total = total + 1
        line[0] = line[0].lower()
        res = re.search("how to", line[0]) # Regular Expression to check if title contains number, only line that changes 
    
        if res:
            matches = matches + 1
            all_info.append(line)
            all_titles.append(line[0])
            
            if line[1] in matched_categories and matched_categories[line[1]] != 0:
                matched_categories[line[1]] = matched_categories[line[1]] + 1
            else:
                matched_categories[line[1]] = 1
            
        if line[1] in all_categories:
            all_categories[line[1]] = all_categories[line[1]] + 1
        else:
            all_categories[line[1]] = 1
            matched_categories[line[1]] = 0
            
    top_percent = [] 
    bottom_percent = []
    category_percent = []

    for cat in all_categories:
        
        cp = str(matched_categories[cat]/all_categories[cat]) 
    
        category_percent.append(cp[:4] + " " + cat)
    category_percent.sort()
    
    bottom_percent = str(category_percent[2]) + " " + str(category_percent[1]) + " " + str(category_percent[0])
    top_percent = str(category_percent[len(category_percent)-1]) + " " + str(category_percent[len(category_percent)-2]) + " " + str(category_percent[len(category_percent)-3])

    categories = list()
    for key,value in list(matched_categories.items()):
        
        categories.append((value,key))
    categories.sort(reverse=True)            
    
    categories = ["\'" + c[1] + ": " + str(c[0]) + "\'" for c in categories[1:4]] #creates a list where each word in the bi grams are seperated by spaces 
    
    top_categories = " ".join(categories) 
    
    overall_percent = matches/total

    example_title = all_titles[0] if len(all_titles) > 0 else ""

    return[len(all_titles), "%.2f" % overall_percent , "N/A", top_categories, top_percent, bottom_percent, example_title, category_percent, all_titles,all_info]
       
bf_how_to(articles)

articles = read_hubspot("data/all_hubspot.csv")[0]

def hs_brackets(articles):
    
    matches = 0 
    total = 0
    all_info = []
    all_titles = []
    all_authors = {}
    all_categories = {}
    matched_categories = {}
    for line in articles:
        
        total = total + 1
        
        
        res = re.search( "\[.*\]", line[0])  
        
        if res:
            matches = matches + 1
            all_info.append(line)
            all_titles.append(line[0])
           
            if line[1] in all_authors:
                all_authors[line[1]] = all_authors[line[1]] + 1
            else:
                all_authors[line[1]] = 1
            
            if line[4] in matched_categories and matched_categories[line[4]] != 0:
                matched_categories[line[4]] = matched_categories[line[4]] + 1
            else:
                matched_categories[line[4]] = 1
            
            if line[5] in matched_categories and matched_categories[line[5]] != 0:
                matched_categories[line[5]] = matched_categories[line[5]] + 1
            else:
                matched_categories[line[5]] = 1
            
            if line[6] in matched_categories and matched_categories[line[6]] != 0:
                matched_categories[line[6]] = matched_categories[line[6]] + 1
            else:
                matched_categories[line[6]] = 1
            
            if line[7] in matched_categories and matched_categories[line[7]] != 0:
                matched_categories[line[7]] = matched_categories[line[7]] + 1
            else:
                matched_categories[line[7]] = 1
            
            if line[8] in matched_categories and matched_categories[line[8]] != 0:
                matched_categories[line[8]] = matched_categories[line[8]] + 1
            else:
                matched_categories[line[8]] = 1
            
            if line[9] in matched_categories and matched_categories[line[9]] != 0:
                matched_categories[line[9]] = matched_categories[line[9]] + 1
            else:
                matched_categories[line[9]] = 1
            
            if line[10] in matched_categories and matched_categories[line[10]] != 0:
                matched_categories[line[10]] = matched_categories[line[10]] + 1
            else:
                matched_categories[line[10]] = 1

        
        if line[4] in all_categories:
            all_categories[line[4]] = all_categories[line[4]] + 1
        else:
            all_categories[line[4]] = 1
            matched_categories[line[4]] = 0
            
        if line[5] in all_categories:
            all_categories[line[5]] = all_categories[line[5]] + 1
        else:
            all_categories[line[5]] = 1
            matched_categories[line[5]] = 0
            
        if line[6] in all_categories:
            all_categories[line[6]] = all_categories[line[6]] + 1
        else:
            all_categories[line[6]] = 1
            matched_categories[line[6]] = 0
            
        if line[7] in all_categories:
            all_categories[line[7]] = all_categories[line[7]] + 1
        else:
            all_categories[line[7]] = 1
            matched_categories[line[7]] = 0
            
        if line[8] in all_categories:
            all_categories[line[8]] = all_categories[line[8]] + 1
        else:
            all_categories[line[8]] = 1
            matched_categories[line[8]] = 0
            
        if line[9] in all_categories:
            all_categories[line[9]] = all_categories[line[9]] + 1
        else:
            all_categories[line[9]] = 1
            matched_categories[line[9]] = 0
            
        if line[10] in all_categories:
            all_categories[line[10]] = all_categories[line[10]] + 1
        else:
            all_categories[line[10]] = 1
            matched_categories[line[10]] = 0
        

    top_percent = [] 
    bottom_percent = []
    category_percent = []
    
    for cat in all_categories:
        
        cp = str(matched_categories[cat]/all_categories[cat]) 
    
        category_percent.append(cp[:4] + " " + cat)
    category_percent.sort()    
    
    bottom_percent = str(category_percent[2]) + " " + str(category_percent[1]) + " " + str(category_percent[0])
    top_percent = str(category_percent[len(category_percent)-1]) + " " + str(category_percent[len(category_percent)-2]) + " " + str(category_percent[len(category_percent)-3])
    
    authors = list()
    for key,value in list(all_authors.items()):
        
        authors.append((value,key))
    authors.sort(reverse=True)            
    
    authors = ["\'" + a[1] + ": " + str(a[0]) + "\'" for a in authors[:3]] #creates a list where each word in the bi grams are seperated by spaces 
    
    authors = " ".join(authors) 
             
    categories = list()
    for key,value in list(matched_categories.items()):
        
        categories.append((value,key))
    categories.sort(reverse=True)            
    
    categories = ["\'" + c[1] + ": " + str(c[0]) + "\'" for c in categories[1:4]] #creates a list where each word in the bi grams are seperated by spaces 
    
    
    top_categories = " ".join(categories) 

    overall_percent = matches/ total
    
    example_title = all_titles[0] if len(all_titles) > 0 else ""
    
    return[len(all_titles), "%.2f" % overall_percent ,authors, top_categories, top_percent, bottom_percent, example_title, category_percent, all_titles,all_info]
# returns the number of articles that meet regular expression, the over all percent of articles, the top 3 authors, top 3 categories, the most occuring categories by percent, least occuring categories by percent, a smaple title, all of the categories by percent, all the titles, and then all of the articles information 
    
hs_brackets(articles)

articles = read_buzzfeed()

def bf_brackets(articles):
    
    all_info = []
    all_titles = []
    all_categories = {}
    matches = 0
    total = 0
    matched_categories = {}
    
    for line in articles:
        
        total = total + 1
        
        res = re.search( "\[.*\]", line[0])  
        if res:
            matches = matches + 1
            all_info.append(line)
            all_titles.append(line[0])
            
            if line[1] in matched_categories and matched_categories[line[1]] != 0:
                matched_categories[line[1]] = matched_categories[line[1]] + 1
            else:
                matched_categories[line[1]] = 1
            
        if line[1] in all_categories:
            all_categories[line[1]] = all_categories[line[1]] + 1
        else:
            all_categories[line[1]] = 1
            matched_categories[line[1]] = 0
            
    top_percent = [] 
    bottom_percent = []
    category_percent = []

    for cat in all_categories:
        
        cp = str(matched_categories[cat]/all_categories[cat]) 
    
        category_percent.append(cp[:4] + " " + cat)
    category_percent.sort()
    
    bottom_percent = str(category_percent[2]) + " " + str(category_percent[1]) + " " + str(category_percent[0])
    top_percent = str(category_percent[len(category_percent)-1]) + " " + str(category_percent[len(category_percent)-2]) + " " + str(category_percent[len(category_percent)-3])
    
    categories = list()
    for key,value in list(matched_categories.items()):
        
        categories.append((value,key))
    categories.sort(reverse=True)   
    
    
    categories = ["\'" + c[1] + ": " + str(c[0]) + "\'" for c in categories[1:4]] #creates a list where each word in the bi grams are seperated by spaces 
    
    top_categories = " ".join(categories) 
    
    overall_percent = matches/total

    example_title = all_titles[0] if len(all_titles) > 0 else ""

    return[len(all_titles), "%.2f" % overall_percent , "N/A", top_categories, top_percent, bottom_percent, example_title, category_percent, all_titles,all_info]
       
bf_brackets(articles)

def all_results():
# This function writes everything to a CSV file to easily compare results between Dan Lyons, HubSpot and BUzzFeed
    d = {} # initialize an empty dictionary to contain all results
    

    non_lyons = read_hubspot("data/all_hubspot.csv")[0] # All articles not written by Dan Lyons during the time he was working at HubSpot 2013-2014
    lyons = read_hubspot("data/during_lyons.csv")[1] # All Articles written by Dan Lyons 2013-2014
    buzzfeed = read_buzzfeed() # Recent Articles from Buzzfeed ~2016
    
    d["Hubspot Average Number Words"] =  average_word_count(non_lyons) 
    d["Dan Lyons Average Number Words"] =  average_word_count(lyons) 
    d["Buzzfeed Average Number Words"] = average_word_count(buzzfeed)
    
    
    d["Hubspot Average Length Words"] =  average_len_word(non_lyons) 
    d["Dan Lyons Average Length Words"] =  average_len_word(non_lyons) 
    d["Buzzfeed Average Length Words"] = average_len_word(buzzfeed)
    
    
    d["Hubspot Top Authors"] = authors(non_lyons)
    

    
    d["Hubspot Top Categories"] = hs_categories(non_lyons)
    d["Dan Lyons Top Categories"] = hs_categories(lyons)
    d["Buzzfeed Top Categories"] = bf_categories(buzzfeed)

    
    d["Hubspot Titles Contain Numbers"] = hs_contains_number(non_lyons)[:7]
    d["Dan Lyons Titles Contain Numbers"] = hs_contains_number(lyons)[:7]
    d["Buzzfeed Titles Contain Numbers"] = bf_contains_number(buzzfeed)[:7]

    
    d["Hubspot Titles Start Numbers"] = hs_starts_number(non_lyons)[:7]
    d["Dan Lyons Titles Start Numbers"] = hs_starts_number(lyons)[:7]
    d["Buzzfeed Titles Start Numbers"] = bf_starts_number(buzzfeed)[:7]
    
    
    d["Hubspot Titles How To"] = hs_how_to(non_lyons)[:7]
    d["Dan Lyons Titles How To"] = hs_how_to(lyons)[:7]
    d["Buzzfeed Titles How To"] = bf_how_to(buzzfeed)[:7]
    
    
    d["Hubspot Titles Brackets"] = hs_brackets(non_lyons)[:7]
    d["Dan Lyons Titles Brackets"] = hs_brackets(lyons)[:7]
    d["Buzzfeed Titles Brackets"] = bf_brackets(buzzfeed)[:7]
    
    fout = open("data/All_Results.csv", 'w') 
    fout.write("{},{}\n".format("Company:", "HubSpot"))
    fout.write("\n")
    fout.write("\n")
    fout.write("{},11277\n".format("Total Number of Articles"))
    fout.write("{},3080\n".format("Number of Exact Duplicates"))
    fout.write("{},27%\n".format("Percentage of Duplicates"))
    fout.write("{},8144\n".format("Number of Unique Articles"))
    fout.write("{},84\n".format("Number of Articles Written by Dan Lyons"))
    fout.write("\n")
    fout.write("\n")
    fout.write("{},{}\n".format("Company:", "Buzzfeed"))
    fout.write("\n")
    fout.write("\n")
    fout.write("{},9074\n".format("Total Number of Articles"))
    fout.write("{},1589\n".format("Number of Exact Duplicates"))
    fout.write("{},17%\n".format("Percentage of Duplicates"))
    fout.write("{},7485\n".format("Number of Unique Articles"))
    
    fout.write("\n")
    fout.write("\n")
    
    fout.write("{},{}\n".format("Hubspot Average Number Words:", d["Hubspot Average Number Words"]  ))
    fout.write("{},{}\n".format("Dan Lyons Average Number Words:", d["Dan Lyons Average Number Words"]  ))
    fout.write("{},{}\n".format("Buzzfeed Average Number Words:", d["Buzzfeed Average Number Words"]  ))
        
    fout.write("\n")
    fout.write("\n")
    
    fout.write("{},{}\n".format("Hubspot Average Length of Words Per Title:", d["Hubspot Average Length Words"]  ))
    fout.write("{},{}\n".format("Dan Lyons Average Length of Words Per Title:", d["Dan Lyons Average Length Words"]  ))
    fout.write("{},{}\n".format("Buzzfeed Average Length of Words Per Title:", d["Buzzfeed Average Length Words"]  ))
    
    fout.write("\n")
    fout.write("\n")

    fout.write("{},64\n".format("Total Number of Categories (HubSpot):"))
    fout.write("{},22\n".format("Total Number of Categories (Buzzfeed):"))


    fout.write("\n")
    fout.write("\n")

    fout.write("{},{},{},{}\n".format("Hubspot Most Occuring Authors:","","", d["Hubspot Top Authors"]))
    
    fout.write("\n")
    fout.write("\n")
    
    
    fout.write("{},{},{},{},{}\n".format("Hubspot Most Occuring Categories:","","","",d["Hubspot Top Categories"]))
    fout.write("{},{},{},{},{}\n".format("Dan Lyons Most Occuring Categories:","","","",d["Dan Lyons Top Categories"]))
    fout.write("{},{},{},{},{}\n".format("Buzzfeed Most Occuring Categories:","","","",d["Buzzfeed Top Categories"]))


    fout.write("\n")
    fout.write("\n")
    
    fout.write("{},{},{},{},{},{},{},{}\n".format("Common Patterns:", "Number of Articles:","Percent%", "Top Authors:", "Top Categories","Top Categories By Percent:", "Bottom Categories By Percent", "Example"))

    fout.write("\n")
    fout.write("\n")

    
    fout.write("{},{}\n".format("Hubspot Contain Numbers", str(d["Hubspot Titles Contain Numbers"])[1:-1]))
    fout.write("{},{}\n".format("Dan Lyons Contain Numbers", str( d["Dan Lyons Titles Contain Numbers"])[1:-1]))
    fout.write("{},{}\n".format("Buzzfeed Contain Numbers", str(d["Buzzfeed Titles Contain Numbers"])[1:-1]))

    fout.write("\n")
    fout.write("\n")
    
    
    fout.write("{},{}\n".format("Hubspot Starts With Numbers", str(d["Hubspot Titles Start Numbers"])[1:-1]))
    fout.write("{},{}\n".format("Dan Lyons Starts With Numbers", str( d["Dan Lyons Titles Start Numbers"])[1:-1]))
    fout.write("{},{}\n".format("Buzzfeed Starts With Numbers", str(d["Buzzfeed Titles Start Numbers"])[1:-1]))

    fout.write("\n")
    fout.write("\n")

    
    fout.write("{},{}\n".format("Hubspot How To", str(d["Hubspot Titles How To"])[1:-1]))
    fout.write("{},{}\n".format("Dan Lyons How To", str(d["Dan Lyons Titles How To"])[1:-1]))
    fout.write("{},{}\n".format("Buzzfeed How To", str(d["Buzzfeed Titles How To"])[1:-1]))

    fout.write("\n")
    fout.write("\n")
    

    fout.write("{},{}\n".format("Hubspot Bracket Subtitles", str(d["Hubspot Titles Brackets"])[1:-1]))
    fout.write("{},{}\n".format("Dan Lyons Bracket Subtitles", str(d["Dan Lyons Titles Brackets"])[1:-1]))
    fout.write("{},{}\n".format("Buzzfeed Bracket Subtitles", str(d["Buzzfeed Titles Brackets"])[1:-1]))


    fout.close()
all_results()

all_hubspot = read_hubspot("data/all_hubspot.csv")[0]
article = hs_contains_number(all_hubspot)[9] #The ninth thing returned by all functions is the comlete data of all matches.
# given any of results from any of the functions ("how to" contains a number ect) this functuion can create a bar graph
def bar_chart(article):
   
    all_dates = {}
    years = []
    articles = []

    for line in article:
        
        date = line[2]
        
        year = date.split(" ")[2]
        
        if year in all_dates:
            all_dates[year] = all_dates[year] + 1
        else:
            all_dates[year] = 1 
    
    percent = []
    articles = list(all_dates.values())
    years = list(all_dates.keys())

    years.sort(reverse = False)
    articles.sort(reverse = False)
    
    xs = [i + 0.5 for i, _ in enumerate(years)]   # See above for what 'enumerate()' does.

    plt.bar(xs, articles)
    plt.ylabel("# of Articles")
    plt.title("Number of {} Articles Over Time".format(input("What Category Are You Analyzing? (ie How To, Brackets, Contains Number)")))

    plt.xticks([i + 0.9 for i, _ in enumerate(years)], years)
    
    plt.show()


bar_chart(article)

def bar_chart_percent():
# This function opens the all_hubspot csv and reads its contents, finding articles that contain a number, my approximation for list articles.     
# It is limited in its flexibility due to the fact that I would need to know the total number of articles in addition to each match.  
    fin = open("data/all_hubspot.csv")

    d = {}
    all_dates = {}
    years = []
    articles = []
    all_years = []
    all_articles =[]
    for line in fin:
        if(line.startswith("Title")):      
                continue
        article_info = line.strip().lower().split(",")
        res = re.search("[0-9]", article_info[0])
        date = article_info[2].split(" ")
        if date[2] in all_dates:
            all_dates[date[2]] = all_dates[date[2]] + 1
        else:
            all_dates[date[2]] = 1 
    
        if res:
        #date = article_info[2].split(" ")
            years.append(date[2])
            if date[2] in d:
                d[date[2]] = d[date[2]] + 1
            
            else:
                d[date[2]] = 1 
            
    percent = []
    articles = list(d.values())
    years = list(d.keys())

    all_articles = list(all_dates.values())
    all_years = list(all_dates.keys())

    years.sort(reverse = False)
    articles.sort(reverse = False)

    all_years.sort(reverse = False)
    all_articles.sort(reverse = False)

    for i in range(0,len(articles)):
        percent.append((articles[i]/all_articles[i]))
   
    xs = [i + 0.5 for i, _ in enumerate(years)]   

    plt.bar(xs, percent)
    plt.ylabel("# of List Articles")
    plt.title("Percentage of List Articles Over Time")

    plt.xticks([i + 0.9 for i, _ in enumerate(years)], years, rotation = 90)
    
    plt.show()

    fin.close()
bar_chart_percent()

all_hubspot = read_hubspot("data/all_hubspot.csv")[0]
article = hs_how_to(all_hubspot)[9] #The ninth thing returned by all functions is the comlete data of all matches.
#For This Example we are using the how to function so when prompted, input "How To"

def top_authors_graph(article):
    authors = []
    num_art = []
    list_author = []
    d = {}

    for line in article:
    
        author = line[1] 
    
        if author in d:
            d[author] = d[author] + 1
        else:
            d[author] = 1
 
    lst = list() # initialize an empty list
    for key, val in d.items(): # looping through the dictionary
        lst.append((val, key)) # keep adding the value, key pairs to our empty list
        
    lst.sort(reverse=True) # sort the list, Big to smallest
    a = lst[:10]

    for i in a:
        num_art.append(i[0])
        list_author.append(i[1])

    xs = [i + 0.1 for i, _ in enumerate(list_author)]   

    plt.bar(xs, num_art)
    plt.ylabel("# of Articles")
    plt.title("Top 10 {} Article Authors".format(input("What Category Are You Analyzing? (ie How To, Brackets, Contains Number)")))

    plt.xticks([i + 0.5 for i, _ in enumerate(list_author)], list_author, rotation = 90)
    
    plt.show()

top_authors_graph(article)

