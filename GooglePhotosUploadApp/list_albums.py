import pandas as pd
from create_service import service


response = service.albums().list(
    pageSize=50,
    excludeNonAppCreatedData=False
).execute()

album_list = response.get('albums')
nextPageToken = response.get('nextPageToken')

while nextPageToken:
    response = service.albums().list(
        pageSize=50,
        excludeNonAppCreatedData=False,
        pageToken=nextPageToken
    ).execute()

    album_list.append(response.get('albums'))
    nextPageToken = response.get('nextPageToken')


album_df = pd.DataFrame(album_list)
print(album_df.head())