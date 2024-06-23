"""
This code includes the functions which are related to the YouTube API.
These are mainly; connect_youtube, get_videos, upload_shorts
"""

import os
from time import sleep
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from config import repo_path, testing_cred, pause_minutes


class YouTubeConnector:
    def __init__(self) -> None:
        # If modifying these scopes, delete the file token.pickle.
        self.SCOPES = ['https://www.googleapis.com/auth/youtube']
        self.WishYouBest_id = "UCnoEfubD-FvugKnhCTEVXGQ"
        self.playlist_id = "PLc6oHh26s0md2mQCUaGkyjYruDORvuwGL"
        self.service = self.connect_youtube()
        self.local_temp_folder = repo_path + "/Data"
        self.short_upload_pause = pause_minutes


    def pause(self) -> None:
        """
        Pause the program for a while.
        Its called after each short video upload.
        """
        sleep(self.short_upload_pause * 60)


    def connect_youtube(self) -> object:
        """
        Connects to the YouTube API.
        :return: The YouTube API service object.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(repo_path + "/token_youtube.json"):
            creds = Credentials.from_authorized_user_file(repo_path + "/token_youtube.json", self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    repo_path + "/credentials.json", self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(repo_path + "/token_youtube.json", "w") as token:
                token.write(creds.to_json())

        try:
            service = build('youtube', 'v3', credentials=creds)
        except Exception as e:
            print(f"An error occurred: {e}")
            service = None
        return service


    def get_videos(self) -> list:
        """
        Lists the videos in the YouTube channel by iterating all pages.
        :return: The list of videos in the channel.
        """
        titles = []
        next_page_token = None
        while True:
            request = self.service.search().list(
                part="snippet",
                channelId=self.WishYouBest_id,
                maxResults=50,
                pageToken=next_page_token,
                q="Amazing Places, Foods, Hotels and More in",
                order="date"
            )
            response = request.execute()
            for item in response["items"]:
                titles.append(item["snippet"]["title"])
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
        titles.remove("Best Cities all Around World")
        return titles


    def upload_video(self, city_name) -> None:
        """
        Upload the video to YouTube.
        """
        video_path = [self.local_temp_folder+'/'+file for file in os.listdir(f"{self.local_temp_folder}") if file.endswith(".mp4")][0]
        video_title = f"Amazing Places, Foods, Hotels and More in {city_name}"
        mode = "public"
        catagory = "19" # Travel & Events
        path = self.local_temp_folder[:-4] + "/upload_video.py"
        tags = "Travel,Adventure,Explore,AmazingPlaces,CulinaryJourney,FoodieFinds,HotelLife,Wanderlust,TravelInspiration,ExoticEats,LuxuryHotels,HiddenGems,TravelVibes,AdventureAwaits,BucketListDestinations,TravelGoals,VacationDreams,WorldWonders,TravelDiaries,EpicJourneys,BestEats,LuxuryTravel,DreamDestinations,BoutiqueHotels,AdventureSeeker,UnforgettableExperiences,FoodExplorer,SpectacularViews,MustVisitPlaces,GlobalCuisine,ExploreTheWorld,TravelEnthusiast,VacationGoals,InspiringPlaces,HotelLuxury,hi,world"

        with open(f"{self.local_temp_folder}/video_description.txt", "r") as file:
            video_description = file.read()
        thumbnail_path = f"{self.local_temp_folder}/{city_name}.jpg"

        # call the upload code to upload the video to YouTube
        command = f"""
            python3 {path} --file="{video_path}" --title="{video_title}" --description="{video_description}" --keywords="{tags}" --category="{catagory}" --privacyStatus="{mode}"
        """
        os.system(command)

        if testing_cred:
            return

        # read video_id from video_id.txt
        with open("video_id.txt", "r") as file:
            video_id = file.read()
        os.remove("video_id.txt")

        # set thumbnail
        request = self.service.thumbnails().set(
            videoId=video_id,
            media_body=thumbnail_path
        )
        request.execute()

        # add video to playlist
        request = self.service.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": self.playlist_id,
                    "position": 0,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        request.execute()

        # set the video language to English
        request = self.service.videos().update(
            part="snippet",
            body={
                "id": video_id,
                "snippet": {
                    'title': video_title,
                    "defaultLanguage": "en",
                    "categoryId": catagory,
                    "description":video_description,
                    "tags":tags
                }
            }
        )
        request.execute()

        print(f"Uploaded {video_title} to YouTube.")


    def upload_shorts(self) -> None:
        """
        Upload the shorts to YouTube.
        """
        shorts = [self.local_temp_folder+'/short_videos/'+file for file in os.listdir(f"{self.local_temp_folder}/short_videos") if file.endswith(".mp4")]
        with open(f"{self.local_temp_folder}/short_videos/text.txt", "r") as file:
            short_description = file.read()
        mode = "public"
        catagory = "19" # Travel & Events
        path = self.local_temp_folder[:-4] + "/upload_video.py"
        tags = "Travel,Adventure,Explore,AmazingPlaces,CulinaryJourney,FoodieFinds,HotelLife,Wanderlust,TravelInspiration,ExoticEats,LuxuryHotels,HiddenGems,TravelVibes,AdventureAwaits,BucketListDestinations,TravelGoals,VacationDreams,WorldWonders,TravelDiaries,EpicJourneys,BestEats,LuxuryTravel,DreamDestinations,BoutiqueHotels,AdventureSeeker,UnforgettableExperiences,FoodExplorer,SpectacularViews,MustVisitPlaces,GlobalCuisine,ExploreTheWorld,TravelEnthusiast,VacationGoals,InspiringPlaces,HotelLuxury,hi,world"
        for short_path in shorts:
            self.pause()
            short_title = short_path.split("/")[-1].split(".")[0]

            # call the upload code to upload the video to YouTube
            command = f"""
                python3 {path} --file="{short_path}" --title="{short_title}" --description="{short_description}" --keywords="{tags}" --category="{catagory}" --privacyStatus="{mode}"
            """
            os.system(command)

            # read video_id from video_id.txt
            with open("video_id.txt", "r") as file:
                short_id = file.read()
            os.remove("video_id.txt")
            # no thumbnail for shorts for now

            # no playlist for shorts for now

            # set the video language to English
            # request = self.service.videos().update(
            #     part="snippet",
            #     body={
            #         "id": short_id,
            #         "snippet": {
            #             'title': short_title,
            #             "defaultLanguage": "en",
            #             "categoryId": catagory,
            #         }
            #     }
            # )
            # request.execute()

            print(f"Uploaded {short_title} to YouTube.")

