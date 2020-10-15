import pandas as pd

df_carou = pd.read_csv('carousell_result.csv', index_col=[0])
df_gv = pd.read_csv('gv_result.csv', index_col=[0])
df_museum = pd.read_csv('museum_result.csv', index_col=[0])

# modify dataframes to add missing column attributes and values, then combine them into 1 csv file
# edit Carousell
df_temp = df_carou.iloc[:, 1:6]
carou_subtag = ['Nature']*22 + ['Others']*22 + ['Nature']*22 + ['Theme park']*44 + ['Nature']*66 + ['Theme park']*22 # Carousell doesn't have specific tags so need to give own labels 
df_temp.insert(loc=4, column='Subtag', value=carou_subtag) # add subtag column
df_temp.insert(loc=2, column='Duration', value='NA') # add duration column


# edit GV
df_temp2 = df_gv
df_temp2.columns = ['Title', 'Duration', 'Subtag', 'Description', 'Image link']
swap = ['Title', 'Duration', 'Description', 'Subtag', 'Image link']
df_temp2 = df_temp2.reindex(columns = swap)
df_temp2.insert(loc=3, column='Tag', value='Movies') # add tag column
df_temp2.insert(loc=1, column='Price', value='NA') # add price column

def check2Dor3D(row):
    if '3D' in row.Title:
        return '$11.00'

    else:
        return '$9.00'

df_temp2['Price'] = df_temp2.apply(lambda row: check2Dor3D(row), axis=1) # price depends if movie is 3D or 2D


# edit Museum
df_temp3 = df_museum
df_temp3.columns = ['Title', 'Price', 'Description', 'Tag', 'Subtag']
df_temp3.insert(loc=2, column='Duration', value='NA') # add duration column
df_temp3.insert(loc=4, column='Image link', value='NA') # add image link column


# write into csv file
df_final = df_temp
df_final = df_final.append(df_temp2)
df_final = df_final.append(df_temp3)
df_final = df_final.reset_index(drop=True) # make the index values correct
df_final.to_csv('final_result.csv')
print(df_final)
print('Done')
