from googleapiclient.discovery import build
#from google.oauth2 import service_account
#import pandas as pd
#import csv
from final_YT_stats import YTstats
import requests
import json

#cbdsearch =[]

api_key='AIzaSyCMsQyo1Z-gkeAATtj1JsrSWK8QzQH9mps' #omitamu
#api_key='AIzaSyAzgCDQAM6faMr1nImyW8vT2QOhE4xNeNU' #moumita.aich

youtube = build('youtube', 'v3', developerKey=api_key)

nextPageToken = None
while True:
    search_request = youtube.search().list(
			part='snippet',
			q='Fifa 2022',
			maxResults='9',
			pageToken=nextPageToken
		)

    search_response = search_request.execute()
    print(search_response['items'])
    
    for item in search_response['items']:
        channel_titles = (item['snippet']['channelTitle'])
        channel_ids = (item['snippet']['channelId'])
        video_titles = (item['snippet']['title'])
        
        print('CI',channel_ids)
        
        for i in range(len(channel_ids)):
            channel_Id = channel_ids #[i]
            print('channel',channel_Id)
            url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&part=snippet&channelId={channel_Id}&maxResults=50"
            print(url)
            response_data = requests.get(url)
            json_data = json.loads(response_data.text)

            limit = 5 
            video_Ids = []
            nextPageToken ="" #for 0th iteration let it be null
            #for i in range(limit):
            url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&part=snippet&channelId={channel_Id}&maxResults=50&pageToken={nextPageToken}"
            data = json.loads(requests.get(url).text)
            for item in data['items']:
                    video_Id = item['id']['videoId']
                    video_Ids.append(video_Id)
            nextPageToken = data['nextPageToken']

            for i,video_Id in enumerate(video_Ids):
                url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet&key={api_key}&id={video_Id}"
                data = json.loads(requests.get(url).text)
                channel_id = data['items'][0]['snippet']['channelId']      
                published_date = data['items'][0]['snippet']['publishedAt']    
                video_title =  data['items'][0]['snippet']['title']     
                video_description = data['items'][0]['snippet']['description']
                likes =  data["items"][0]["statistics"]["likeCount"]
                #dislikes = data["items"][0]["statistics"]["dislikeCount"]
                views = data["items"][0]["statistics"]["viewCount"]
                comment_count = data["items"][0]["statistics"]['commentCount']
                request=youtube.subscriptions().list(part="snippet,contentDetails",channelId=channel_id)
                subs=request.execute()
            
            # channel_id = ('items'][0]['snippet']['channelId'])      
            # published_date = (['items'][0]['snippet']['publishedAt'])    
            # video_title =  (['items'][0]['snippet']['title']) 
            # video_description = (['items'][0]['snippet']['description'])
            # likes =  (["items"][0]["statistics"]["likeCount"])
            # #dislikes = (["items"][0]["statistics"]["dislikeCount"])
            # views = (["items"][0]["statistics"]["viewCount"])
            # comment_count = (["items"][0]["statistics"]['commentCount'])
            
            yt = YTstats(api_key, channel_Id)
            yt.extract_all()
            yt.dump()
            
        
        #element_info = {
        #'Channel title': channel_title,
        #'Channel IDs': channel_id,
        #'Video Title': video_title,
        #'Video Link': yt_link,
        #'View': vid_view,
        #'Like': vid_like,
        #'Dislike': vid_dislike,
        #'Favourite': vid_favorite,
        #'Comment': vid_comment
        #}

        #cbdsearch.append(element_info)
        #print(cbdsearch)
        
        #yt = YTstats(api_key, channel_id)
        #yt.extract_all()
        #yt.dump()