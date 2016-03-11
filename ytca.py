#!/usr/bin/python3
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from collections import OrderedDict
import argparse
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

config = configparser.ConfigParser()

parser = argparse.ArgumentParser()
input_type_group = parser.add_mutually_exclusive_group()
input_type_group.add_argument("--ini", help="Specify an alternative ini file to process.  Default is 'channels.ini'")
input_type_group.add_argument("--username", help="Run the caption auditor on a single youtube account, by username")
input_type_group.add_argument("--chid", help="Run the caption auditor on a single youtube account, by channel ID")

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

    @classmethod
    def from_username(cls, username):
        results = youtube.channels().list(
            part="snippet",
            forUsername=username
        ).execute()
        if(results['items']):
            items = results['items'][0]
            name = items['snippet']['title']
            channel_id = items['id']
            channel = cls(name, channel_id)
            return channel
        else:
            print("Error: YouTube username %s not found" % username)
            exit()


    #Query the channel in question for the id of the uplaods playlist
    def uploads_playlist(self):
        results = youtube.channels().list(
            part="contentDetails",
            id=self.channel_id
        ).execute()
        channel = results["items"][0]
        if "contentDetails" in channel:
           uploads_list_id = channel['contentDetails']['relatedPlaylists']['uploads']
           self.uploads_list_id = uploads_list_id

    #Go through the uploads plyalist and populate the list of video IDs
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

    #Helper function for find_captions that
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

    def run(self):
        print("Processing channel %s" % self.name)
        self.uploads_playlist()
        self.get_videos()
        self.find_captions()
        print("Total videos in channel: %d" % self.total_videos)
        print("Captioned Videos: %d" % self.captioned_videos)
        print("Percent captioned: %0.2f%%\n" % ((self.captioned_videos / self.total_videos)*100))

#-------------------------

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
    args = parser.parse_args()
    if args.ini:
        channels = load_channels_list(args.ini)
        for name, id in channels.items():
            this_channel = Channel(name, id)
            this_channel.run()
    elif args.chid:
        channel = Channel(None, args.chid)
        channel.run()
    elif args.username:
        channel = Channel.from_username(args.username)
        channel.run()
    else:
        parser.print_help()
        parser.exit()
