#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

with open('apikey', 'r') as f:
    DEVELOPER_KEY = f.readline()

#Initialize Data API object
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

class Channel(object):
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.uploads_list_id = ""
        self.videos_list = []
        self.total_videos = 0
        self.captioned_videos = 0

    def uploads_playlist(self):
        results = youtube.channels().list(
            part="contentDetails",
            id=self.channel_id
        ).execute()
        channel = results["items"][0]
        if "contentDetails" in channel:
           uploads_list_id = channel['contentDetails']['relatedPlaylists']['uploads']
           self.uploads_list_id = uploads_list_id
           print(uploads_list_id)

    def get_videos(self):
        playlist_results = youtube.playlistItems().list(
            playlistId=self.uploads_list_id,
            part="contentDetails",
            maxResults=50
        )
        
        #Iterate through all pages in result set
        print("Populating videos list...")
        while playlist_results:
            response = playlist_results.execute()

            #Build list of video IDs to grab caption data from
            for playlist_item in response['items']:
                video_id = playlist_item['contentDetails']['videoId']
                self.videos_list.append(video_id)

            #Get the next page
            playlist_results = youtube.playlistItems().list_next(playlist_results, response)
        self.total_videos = len(self.videos_list)

    def find_captions(self):
        #Turn video list into a comma separated string for the API query
        videos_str = ",".join(self.videos_list)
        video_response = youtube.videos().list(
            part="contentDetails",
            id=videos_str,
            maxResults=50
        ).execute()

        for video_result in video_response.get("items", []):
            if video_result['contentDetails']['caption'] == u'true':
                self.captioned_videos += 1

    def test(self):
        self.uploads_playlist()
        self.get_videos()
        self.find_captions()
        print(self.videos_list)
        print("Total videos in channel: %d" % self.total_videos)
        print("Captioned Videos: %d" % self.captioned_videos)

#WWU IEP
ch = Channel('UC3uOM3GRMJg4Fu93t-HdHBQ')
ch.test()
