#!/usr/bin/python3
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from collections import OrderedDict
import csv
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

with open('apikey', 'r') as f:
    DEVELOPER_KEY = f.readline()

#Initialize Data API object
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

class Channel(object):
    def __init__(self, name, channel_id):
        self.name = name
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
            chunk = []
            for playlist_item in response['items']:
                video_id = playlist_item['contentDetails']['videoId']
                chunk.append(video_id)

            self.total_videos += len(chunk)
            self.videos_list.append(chunk)

            #Get the next page
            playlist_results = youtube.playlistItems().list_next(playlist_results, response)

    def video_request(self, videos_str):
        video_response = youtube.videos().list(
            part="contentDetails",
            id=videos_str,
            maxResults=50
        ).execute()
        
        for video_result in video_response.get("items", []):
            if video_result['contentDetails']['caption'] == u'true':
                self.captioned_videos += 1

    def find_captions(self):
        for chunk in list(self.videos_list):
            #Turn video list into a comma separated string for the API query
            query_str = ",".join(chunk)
            self.video_request(query_str)

    def test(self):
        print("Processing channel %s" % self.name)
        self.uploads_playlist()
        self.get_videos()
        self.find_captions()
        print("Total videos in channel: %d" % self.total_videos)
        print("Captioned Videos: %d\n" % self.captioned_videos)

#-------------------------
config = configparser.ConfigParser()

def load_channels_list(filename):
    channels = OrderedDict()
    config.read(filename)
    for section in config._sections:
        name = config.get(section, "name")
        id = config.get(section, "id")
        if name.startswith('\''):
            name = name[1:-1]
        if id.startswith('\''):
            id = id[1:-1]
        channels.update({name:id})
    return channels

if __name__ == '__main__':
    channels = load_channels_list('channels.ini')
#    iep = Channel("CIIA", "UCA7BaH2FseUEQff1WlOEj2g")
#    iep.test()
    for name, id in channels.items():
        this_channel = Channel(name, id)
        this_channel.test()
