YouTube Caption Auditor (YTCA)
==============================

*YTCA* is a utility to collect stats from one or more YouTube channels.
It was designed to collect data related to captioning, but could be extended
to support other data collection needs.

Data Collected for each YouTube Channel
---------------------------------------

* Number of videos
* Total duration of all videos
* Number of videos with captions (does not include YouTube's machine-generated captions)
* Percent of videos that are captioned
* Mean number of views per video
* Number of "high traffic" videos (see High Traffic section below for details)
* Number of high traffic videos that are captioned
* Percent of high traffic videos that are captioned
* Total duration of uncaptioned videos
* Total duration of uncaptioned high traffic videos

High Traffic Videos
-------------------

In order to prioritize captioning efforts, it can be focus on videos that are "high traffic".
By default, YTCA considers a video "high traffic" if its number of views is greater than the
mean for that channel.

Alternatively, you can define your own high traffic threshold using the designated
variable in the Configuration block within [ytca.php][]. If this variable is greater than 0,
YTCA uses that as the high traffic threshold instead of the mean number of views.

Requirements
------------

* PHP 5.3 or higher
* A YouTube API key. For more information see the [YouTube Data API Reference][].


Instructions
------------

1. Get an API key from Google/Youtube.  If you're with Webtech, you can find the link and login in Confluence by searching under 'Youtube Caption Auditor'.
2. Create a file called 'apikey' and paste the key in there.
3. Add the google python api library to your environment. pip install --upgrade google-api-python-client
4. Run the application by passing in the channels listing ini file. $ python ytca.py --ini channels.ini

YouTube Channel IDs
-------------------

The Configuration block includes an array of YouTube Channel IDs.
The YouTube Channel ID is a 24-character string that starts with the characters "UC".
This sometimes appears in the URL for the channel.
For example, the URL for the main University of Washington channel is

**https://www.youtube.com/channel/UCJgq3uJ5jFCbNB06TC9BFBw**

The channel ID is **UCJgq3uJ5jFCbNB06TC9BFBw**

If the channel URL is not presented in the above form, here's one way to
find the channel ID for that channel:

1. View source
2. Search the source code for the attribute *data-channel-external-id*
3. The value of that attribute is the channel ID

Alternatively, you can substitute the *user name* for any channel ID in the YTCA Configuration block.
As long as it's a valid user name and is not a 24-character string starting with "UC",
YTCA can look up the channel ID without you having to follow the above steps.

For example, here's an alternative URL for accessing the main University of Washington channel:

**https://www.youtube.com/user/uwhuskies**

The user name is **uwhuskies**

In the YTCA Configuration block we can enter either **uwhuskies** or **UCJgq3uJ5jFCbNB06TC9BFBw**
as the channel ID; both work just fine, although the former adds overhead because YTCA needs to
lookup each unknown channel ID via an extra query to the YouTube Data API.

Output
------

ytca.py prints the output to the terminal screen directly.

About Quotas
------------

The YouTube Data API has a limit on how many API queries can be executed per day.
For additional details, see [Quota usage][] in the API documentation.

Quotas can be estimated using YouTube's [Quota Calculator][].

As of June 2015, quota costs associated with running this application are:
* 100 units for each channel (search query)
* 5 units for each video
* 5 units for each channel ID lookup from a user name

For example, if you have a daily quota of 5,000,000 units you could run this application
to collect data from 100 channels (10,000 units) containing 998,000 videos.


[YouTube Data API Reference]: https://developers.google.com/youtube/v3/docs/
[Quota Usage]: https://developers.google.com/youtube/v3/getting-started#quota
[Quota Calculator]: https://developers.google.com/youtube/v3/determine_quota_cost
[ytca.php]: ytca.php
