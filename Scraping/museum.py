import pandas as pd

# create a dataframe to hold products and attributes
attr = ['Name', 'Price', 'Description', 'Tag', 'Subtag']
df = pd.DataFrame(columns=attr)
df = df.fillna(0)

# omitted museums with free admission to all, hence no ticketing needed
# standard adult price for tourists (most of these are free admission for Sporeans)
df.loc[len(df)] = ['National Museum of Singapore', '$15', 'Oldest museum in Singapore, with history dating back to 1887.', 'Museums', 'History']
df.loc[len(df)] = ['Asian Civilisations Museum', '$8', 'Opened in 1997, the museum is devoted to exploring the rich artistic heritage of Asia, especially the ancestral cultures of Singaporeans', 'Museums', 'History']
df.loc[len(df)] = ['ArtScience Museum', '$19', 'ArtScience Museum is an iconic cultural landmark in Singapore. Our mission is to explore where art, science, culture and technology come together.', 'Museums', 'Art/Design']
df.loc[len(df)] = ['Indian Heritage Center', '$8', 'The Indian Heritage Centre traces the history of the Indian and South Asian communities in the Southeast Asian region.', 'Museums', 'History' ]
df.loc[len(df)] = ['Lee Kong Chian Natural History Museum', '$20', 'The Lee Kong Chian Natural History Museum strives to be a leader in Southeast Asian biodiversity – in research, education and outreach.', 'Museums', 'History']
df.loc[len(df)] = ['Fort Canning Battlebox', '$15', 'Embark on an unforgettable journey 9 metres underground into the Battlebox, an authentic World War II secret underground command centre built in the late 1930s.', 'Museums', 'History']
df.loc[len(df)] = ['Red Dot Museum', '$6.40', 'Red Dot Design Museum is the physical embodiment of the international Red Dot Design Award — one of the largest design awards in the World.', 'Museums', 'Art/Design']
df.loc[len(df)] = ['Malay Heritage Centre', '$8', 'Officially opened by Prime Minister Lee Hsien Loong in June 2005, the Malay Heritage Centre (MHC) provides wonderful cultural exposure and learning opportunities for visitors of all ages and interests.', 'Museums', 'History']
df.loc[len(df)] = ['Former Ford Factory', '$3', 'The Ford Motor Company which was first established in Singapore at Anson Road in 1926, moved to its new state-of-the-art factory located at Upper Bukit Timah Road in October 1941.', 'Museums', 'History']
df.loc[len(df)] = ['Singapore Musical Box Museum', '$12', "In this Singapore's first musical box museum, we aim to share the historical background from the rise to the fall of the musical boxes to how it made its way to Singapore in the 19th century to the public.", 'Museums', 'History']
df.loc[len(df)] = ['Chinatown Heritage Centre', '$18', 'Restored shophouses displaying living spaces, furnishings & artifacts of early Chinatown settlers.', 'Museums', 'History']
df.loc[len(df)] = ['Singapore Discovery Centre', '$10', 'Singapore Discovery Centre (SDC) is a non-profit organisation whose mission is to share the Singapore Story and inspire a desire to contribute to Singapore’s future.', 'Museums', 'History']
df.loc[len(df)] = ['Trick Eye Museum', '$21.25', 'Trick Eye Museum brings you closer to art through the use of optical illusions. Immerse yourself in different settings at 6 themed zones and recreate into memorable photographs with your imagination.', 'Museums', 'Art/Design']
df.loc[len(df)] = ['Vintage Cameras Museum', '$20', "The Vintage Camera's Museum, itself is set in the form of a camera, and the entry is shaped like a lens.", 'Museums', 'History']

print(df)
df.to_csv('museum_result.csv')
