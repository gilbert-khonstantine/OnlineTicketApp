import pandas as pd
from selenium import webdriver
import time

PATH = "C:\Program Files (x86)\phantomjs.exe"

movie_title = []
duration = []
genre = []
desc = []
image = []
search_format = ['3505-3525', '4505-4511', '4512-4525', '5505-5510', '5511-5525', '6505-6525', '7155-7175']
#search_format = ['7150-7152', '7173-7175'] # simple test

for i in range(len(search_format)):
    s = search_format[i].split('-')
    start = int(s[0])
    end = int(s[1])

    for j in range(start, end):
        print(j)
        driver = webdriver.PhantomJS(PATH)
        driver.get('https://www.gv.com.sg/GVMovieDetails#/movie/' + str(j))
        main = driver.find_element_by_id('movie-detail')
        temp = main.text
        temp = temp.splitlines()

        temp_image = driver.find_element_by_id('movie-details-img').get_attribute('src')
        temp_title = temp[1]

        for k in range(len(temp)):
            if temp[k] == 'Genre:':
                temp_genre = temp[k+1]

            elif temp[k] == 'Running Time:':
                temp_duration = temp[k+1]

            elif temp[k] == 'Synopsis':
                temp_desc = temp[k+1]
                break

        #print(temp_title, temp_genre, temp_duration, temp_desc, temp_image)
        movie_title.append(temp_title)
        genre.append(temp_genre)
        duration.append(temp_duration)
        desc.append(temp_desc)
        image.append(temp_image)


#print(movie_title, genre, duration, desc, image)
# create a dataframe to hold products and attributes
attr = ['Movie title', 'Duration', 'Genre', 'Description', 'Image link']
df = pd.DataFrame(columns=attr)
df = df.fillna(0)


# put all results in dataframe
df = pd.DataFrame(
    {
        'Movie title': movie_title,
        'Duration': duration,
        'Genre': genre,
        'Description': desc,
        'Image link': image,
        })

print(df)
print('Total rows (number of products):', len(df.index))
df.to_csv('gv_result.csv')
