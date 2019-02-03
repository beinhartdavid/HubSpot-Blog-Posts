import urllib.request
from bs4 import BeautifulSoup as bs
import pprint                                  
pp = pprint.PrettyPrinter(indent=4) 
import re
import os
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

def scrape_hubspot():
    
    url = "http://blog.hubspot.com/topics" # URL containing list of all categories
    fhand = urllib.request.urlopen(url)            # open the URL
    html = fhand.read()                            # read the page

    soup = bs(html, "html.parser") #from sample code

    category_links = soup.find_all("a", { "class" : "topic-link" })  # find all the <div> tags, where class = topic-link  #This is where all of the titles were
    links = []

    for category in category_links:
        links.append((str(category.get('href', None))))

    categories_list = list()

    for link in links:
        link = link.strip()
        url = "http:" + link
        
        categories_list.append(url)

    print("Collected All {} Categories".format(len(categories_list)))
    
    #Paginates every category:
    
    every_page= []
    for category in categories_list: 
        url = str(category)
        every_page.append(url)
        for i in range(2,35):
            every_page.append(url + "/page/" + str(i))
    
    
    print("Paginated All {} Categories".format(len(categories_list)))
    print("Please Be Patient, Finding All Articles...")
    
    #Get Every Link to Every Article:
    
    title_cat_pair = {} # I initialized this dictionary because I didn't know how else to also keep track of what category each article was occuring in
    all_blog_titles = []
    all_blog_links = []
    
    for URL in every_page:
            
        try:

            fhand = urllib.request.urlopen(URL)            # open the URL
    
            html = fhand.read()                            # read the page

            soup = bs(html, "html.parser") #from sample code

            titles = soup.find_all("a", { "class" : "post-mob__title" })  

            blog_links = []

            for title in titles:
        
                all_blog_titles.append((title.get_text()))
    
                blog_links.append(str(title.get('href', None)))
            
            for urls in blog_links:
                all_blog_links.append(urls)

                if urls in title_cat_pair:
                    title_cat_pair[urls] = title_cat_pair[urls] + " " + url[24:]
                    print("yes")
            
                else:
                    title_cat_pair[urls] = url[24:]
              
        except:
            "Category does not have that high of a page number"
            
    
    print(str(len(all_blog_links)) + " Articles Found")
    
    #Open Each Link and Write Info to CSV File:
    
    dates = []
    authors = []
    titles = []
    results = []
    count = 0
    failed_hubspot = []
    
    print("Please Be Patient, Collecting All Information...")
    
    fout = open("data/scraped_hubspot.csv", 'w') 

    fout.write("{},{},{},{},{}\n".format("Title", "Category","Author","Date","Link"))
    
    for link in all_blog_links:
    
        try:
            fhand = urllib.request.urlopen(link)            # open the URL
    
            html = fhand.read()                            # read the page

            soup = bs(html, "html.parser") #from sample code

            date = soup.find("p", { "class" : "post-header__publish-date" })  
            author = soup.find("a", { "class" : "hubspot-author__link" })  
            title = soup.find("h1", { "class" : "post-header__title" })  
 
            d = date.get_text()
            d = d.replace(",","")
            d = d.replace("//","")
            d = d.replace("[","")
            d = d.replace("]","")
            d = d.replace("\n","")
            d = word_tokenize(d)
            d = " ".join(d)
            dates.append(d)
    
            a = author.get_text()
            a.strip() 
            a = re.sub(r'[^\x00-\x7F]+',' ', a) # I forgot to include this last time for "All_Titles.csv"
            a = a.replace(",","")
            a = a.replace("\n","")
            a = word_tokenize(a)
            a = " ".join(a)
            authors.append(a)
    
            t = title.get_text()
            t.strip()
            t = re.sub(r'[^\x00-\x7F]+',' ', t) #ignore all non latin chars
            t = t.replace(",","")
            t = t.replace("\n","")
            titles.append(t)
     
            fout.write("{},{},{},{},{}\n".format(str(t), str(title_cat_pair[link]) ,str(a),str(d),str(link)))
    
            print(str(len(all_blog_links) -1 - count) + " Links Remaining") 
            count = count + 1
            
        except:
            failed_hubspot.append(link)

    fout.close()
    print("Links That Failed:")
    pp.pprint(failed_hubspot)
    print("Done! Check scraped_hubspot.csv")
    return failed_hubspot
scrape_hubspot()



def scrape_buzzfeed():
    
    failed_buzzfeed = []
    
    # Had to manually populate this list from Buzzfeed.com,
    # I was unable to scrap: Big Stories, Buzz, Entertainment, Life, Podcasts due to the way the pages were outloaded
    
    categories = ["https://www.buzzfeed.com/animals?p={}&z=592ROL&r=1",
                  "https://www.buzzfeed.com/audio?p={}&z=592TY7&r=1",
                  "https://www.buzzfeed.com/books?p={}&z=592T9G&r=1",
                  "https://www.buzzfeed.com/business?p={}&z=592S3X&r=1",
                  "https://www.buzzfeed.com/celebrity?p={}&z=592TOF&r=1",
                  "https://www.buzzfeed.com/food?p={}&z=592S1E&r=1",
                  "https://www.buzzfeed.com/geeky?p={}&z=592SCV&r=1",
                  "https://www.buzzfeed.com/health?p={}&z=592SLJ&r=1",
                  "https://www.buzzfeed.com/lgbt?p={}&z=592TPB&r=1",
                  "https://www.buzzfeed.com/music?p={}&z=592TD4&r=1",
                  "https://www.buzzfeed.com/parents?p={}&z=592TDQ&r=1",
                  "https://www.buzzfeed.com/politics?p={}&z=592SLW&r=1",
                  "https://www.buzzfeed.com/puzzles?p={}&z=5931RD&r=1",
                  "https://www.buzzfeed.com/reader?p={}&z=5933B7&r=1",
                  "https://www.buzzfeed.com/rewind?p={}&z=5933CE&r=1",
                  "https://www.buzzfeed.com/science?p={}&z=5932WA&r=1",
                  "https://www.buzzfeed.com/sports?p={}&z=5931WN&r=1",
                  "https://www.buzzfeed.com/style?p={}&z=5933DA&r=1",
                  "https://www.buzzfeed.com/tech?p={}&z=5932U9&r=1",
                  "https://www.buzzfeed.com/travel?p={}&z=59332U&r=1",
                  "https://www.buzzfeed.com/weddings?p={}&z=5933J2&r=1",
                  "https://www.buzzfeed.com/world?p={}&z=5933TI&r=1"]
                  
    
    print(str(len(categories)) + " Categories Found") #Notifies the User How Many Categories were Scraped
    all_pages = []
    for category in categories:
        for i in range(1,16): #Paginates each category up to page 16
            all_pages.append(category.format(i)) # appends these paginated categories to a list to loop through later
    
    print("Please Be Patient, Collecting Articles...") #scraping can take a while...
    
    category_result = []
    title_result = []
    
    for url in all_pages:
    
        try:
    
            page_titles = []
            page_info = []
    
            fhand = urllib.request.urlopen(url)            # open the URL
            html = fhand.read()                            # read the page

            soup = bs(html, "html.parser") #from sample code

            titles = soup.find_all("a", { "class" : "lede__link" })  
    
            for title in titles:
        
                page_titles.append((title.get_text()))
        
            for t in page_titles: #looping through each title in the page_titles list that contains all of the titles collected
                t.strip()
                t = re.sub(r'[^\x00-\x7F]+',' ', t) #ignore all non latin chars
                t = t.replace(",","")
                t = t.replace("\n","")
                t = t.lstrip()
                if t == "":
                    continue
                title_result.append(t)
                
                res = re.search(".com/.*\?", url) #finds the category within the article's url
                if res:
                    match = res.group()[5:] #removes.com/ from the category
                    length = len(match)
                    match = match[:(length-1)] #removes the ? from the end of the match
                    category_result.append(match)
        
        except:
            
            failed_buzzfeed.append(url)
    print(str(len(title_result)) + " Links Found:")
    
    fout = open("data/scraped_buzzfeed.csv", 'w') 
    fout.write("{},{}\n".format("Title","Category"))

    for i in range(0,len(title_result)):

        fout.write("{},{}\n".format(title_result[i],category_result[i]))

    fout.close()
    
    print("Links That Failed:")
    print(failed_buzzfeed)
    print("Done! Check scraped_buzzfeed.csv")
    return failed_buzzfeed
    
scrape_buzzfeed()