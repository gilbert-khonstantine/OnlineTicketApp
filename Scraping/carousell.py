import pandas as pd
import requests
from bs4 import BeautifulSoup

# define products and attributes we want to have in database
search_list = (['singapore zoo ticket', 'cable car ticket', 'gardens by the bay',
                'universal studios ticket', 'wild wild wet ticket', 'jurong bird park ticket',
                'night safari ticket', 'sea aquarium ticket', 'adventure cove ticket'])
attr = ['Name', 'Title',' Price', 'Description', 'Tag', 'Image link']

# create a dataframe to hold products and attributes
df = pd.DataFrame(columns=attr)
df = df.fillna(0)

seller_name = []
#time_of_listing = []
title = []
price = []
desc = []
image = []


# web scrape products from Carousell
for i in range(len(search_list)):
    search_format = search_list[i].replace(' ', '%20')
    page = requests.get('https://www.carousell.sg/search/' + search_format)
    soup = BeautifulSoup(page.content,'html.parser')
    
    search = soup.find(id = 'root')
    all_items = search.find(class_ = '_2RJeLsMmpi') # entire listing result from typed-in search
    item = all_items.find_all(class_= 'An6bc8d5sQ _9IlksbU0Mo _2t71A7rHgH') # each item

    #[temp.find(class_ = '').get_text() for temp in item]
    temp_seller_name = [temp.find(class_ = '_1gJzwc_bJS _2NNa9Zomqk Rmplp6XJNu mT74Grr7MA nCFolhPlNA lqg5eVwdBz uxIDPd3H13 _30RANjWDIv').get_text() for temp in item]
    #temp_time_of_listing = [temp.find(class_ = '_1gJzwc_bJS _2rwkILN6KA Rmplp6XJNu mT74Grr7MA nCFolhPlNA lqg5eVwdBz _19l6iUes6V _3HOr_TevCw _30RANjWDIv').get_text() for temp in item]
    temp_title = [temp.find(class_ = '_1gJzwc_bJS _2rwkILN6KA Rmplp6XJNu mT74Grr7MA nCFolhPlNA lqg5eVwdBz uxIDPd3H13 _30RANjWDIv').get_text() for temp in item]
    temp_price = [temp.find(class_ = '_1gJzwc_bJS _2rwkILN6KA Rmplp6XJNu mT74Grr7MA nCFolhPlNA lqg5eVwdBz _19l6iUes6V _3k5LISAlf6').get_text() for temp in item]
    temp_desc = [temp.find(class_ = '_1gJzwc_bJS _2rwkILN6KA Rmplp6XJNu mT74Grr7MA nCFolhPlNA lqg5eVwdBz _19l6iUes6V _30RANjWDIv').get_text() for temp in item]
    temp_image = [temp.find(class_ = 'P2llUzsDMi').get('src') for temp in item] # get image link for each item


    # extend the list
    seller_name.extend(temp_seller_name)
    #time_of_listing.extend(temp_time_of_listing)
    title.extend(temp_title)
    price.extend(temp_price)
    desc.extend(temp_desc)
    image.extend(temp_image)


tag = ['Attractions']*len(seller_name)

# put all results in dataframe
df = pd.DataFrame(
    {
        'Name': seller_name,
        #'Time of listing': time_of_listing,
        'Title': title,
        'Price': price,
        'Description': desc,
        'Tag': tag,
        'Image link': image
        })

print(df)
print('Total rows (number of products):', len(df.index))
df.to_csv('carousell_result.csv')

