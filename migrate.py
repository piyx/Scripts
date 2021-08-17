import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CLIENT_SECRETS_FILE = "clientsecret.json"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def get_subscription_ids(youtube):
    subscription_ids = []
    fetch = True
    page_token = None
    while fetch:
        request = youtube.subscriptions().list(
            part="id",
            channelId="UC3w7CEjnByJQcOdsltrqqdA",
            pageToken=page_token
        )
        response = request.execute()
        page_token = response.get("nextPageToken", None)
        fetch = page_token is not None

        for item in response['items']:
            subscription_ids.append(item['id'])
    
    return subscription_ids

print(len(get_subscription_ids(youtube)))