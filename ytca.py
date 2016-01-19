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

def uploads_playlist(channel_id):
    results = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()

    channel = results["items"][0]
    if "contentDetails" in channel:
       uploads_playlist = channel['contentDetails']['relatedPlaylists']['uploads']
       print(uploads_playlist)

uploads_playlist('UCT845gB1xx0wrqfCIhUYeAg')
