import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import json
from dataclasses import dataclass


API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CLIENT_SECRETS_FILE = "clientsecret.json"


@dataclass
class YoutubeChannel:
    name: str
    id: str
    desc: str
    thumbnail: str


def create_api_client(scopes: list[str]) -> googleapiclient.discovery.Resource:
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    return youtube


def get_subscribed_channels() -> list[YoutubeChannel]:
    '''
    Fetch all your subscribed channels.
    Choose your old google account (Which has all subscribed channels) when redirected.
    '''
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    youtube = create_api_client(scopes)


    subscribed_channels = []
    fetch = True
    page_token = None
    while fetch:
        request = youtube.subscriptions().list(
            part="id,snippet",
            channelId="UC3w7CEjnByJQcOdsltrqqdA",
            pageToken=page_token
        )
        response = request.execute()
        page_token = response.get("nextPageToken", None)
        fetch = page_token is not None

        for item in response['items']:
            snippet = item['snippet']
            youtube_channel = YoutubeChannel(
                name=snippet['title'],
                id=snippet['resourceId']['channelId'],
                desc=snippet['description'],
                thumbnail=snippet['thumbnails']['high']['url']
            )
            subscribed_channels.append(youtube_channel)
    
    return subscribed_channels


def write_subscribed_channels(subscribed_channels: list[YoutubeChannel]) -> None:
    '''
    Write all your subscribed channels data into a file.
    Use this function in case you want to keep a log, else
    this function can be ignored
    '''
    with open("subscribed_channels.json", "w") as f:
        json.dump([youtube_channel.__dict__ for youtube_channel in subscribed_channels], f)


def subscribe_channels(youtube_channels: list[YoutubeChannel]) -> None:
    '''
    Subscribes to all the channels from the youtube_channels list.
    Choose your new google account where you want to add
    these channels to your subscription list.
    '''
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    youtube = create_api_client(scopes)

    total_channels = len(youtube_channels)
    for i, youtube_channel in enumerate(youtube_channels, 1):
        request = youtube.subscriptions().insert(
            part="id,snippet",
            body={
            "snippet": {
                    "resourceId": {
                    "channelId": youtube_channel.id,
                    "kind": "youtube#subscription"
                    }
                }
            }
        )

        print(f"Subscribing to {youtube_channel.name} [{i}/{total_channels}]")
        try:
            response = request.execute()
        except Exception as e:
            print(e)


def main():
    print("--------------------------------------------------------------------------------------------")
    print("Click the link and choose the google account to fetch the youtube subscribed channels from: ")
    subscribed_channels = get_subscribed_channels()


    # Uncomment the code below if you want to store the list of channels in a json file
    # write_subscribed_channels(subscribed_channels)

    print("-----------------------------------------------------------------------------------------------------")
    print("Click the link and choose the google account to which you want to add youtube channel subscriptions: ")
    subscribe_channels(subscribed_channels)

    print("------------------------------------------------------------------------------------------")
    print("Successfully migrated all your youtube subscribed channels from old account to new account")


if __name__=='__main__':
    main()