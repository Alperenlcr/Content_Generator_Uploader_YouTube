"""
This code includes the functions which call the YouTube API and Google Drive API.
This code runs like main code.
"""

import os
import random
from youtube_connector import YouTubeConnector
from drive_connector import DriveConnector
from config import repo_path, testing_cred


class Helper:
    def __init__(self) -> None:
        self.youtube_connector = YouTubeConnector()
        self.drive_connector = DriveConnector()
        self.drive_alperen_video_folder_id = "1IVyRmVxTdFijHnPZfKrkAWxuq9EaiW4S"
        self.local_temp_folder = repo_path + "/Data"


    def select_content(self) -> tuple:
        """
        Find a random content which is in drive but not in YouTube.
        """
        drive_folders = self.drive_connector.get_folders(self.drive_alperen_video_folder_id)
        city_names_drive = [folder["name"] for folder in drive_folders]

        youtube_videos = self.youtube_connector.get_videos()
        city_names_youtube = [video[42:] for video in youtube_videos]

        city_names = list(set(city_names_drive) - set(city_names_youtube))
        if "sesler" in city_names:
            city_names.remove("sesler")
        selected = random.choice(city_names)

        return selected, drive_folders[city_names_drive.index(selected)]['id']


    def clear_temp_folder(self) -> None:
        """
        Clear the temporary folder.
        """
        if os.path.exists(self.local_temp_folder):
            os.system(f"rm -rf {self.local_temp_folder}/")


    def upload_content(self) -> bool:
        """
        Find a content folder to upload to YouTube:
            1. Get the list of folders in the Google Drive.
            2. Get the list of videos in the YouTube channel.
            3. Find a random content which is in drive but not in YouTube.
        Download the content folder from Google Drive.
        Upload it to YouTube.
        """
        # Clear the temporary folder
        print("Clearing the temporary folder...")
        self.clear_temp_folder()

        # Find a content folder to upload to YouTube
        print("Finding a content folder to upload to YouTube...")
        city_name, folder_id = self.select_content()

        # Download the content folder from Google Drive
        print(f"{city_name} content is downloading from drive...")
        self.drive_connector.download_folder(folder_id, self.local_temp_folder)

        # Video upload
        print(f"{city_name} video is uploading to YouTube...")
        self.youtube_connector.upload_video(city_name)

        if testing_cred:
            print("Testing Done")
            exit(1)

        # Shorts upload
        print(f"{city_name} shorts are uploading to YouTube...")
        self.youtube_connector.upload_shorts()

        return True


helper = Helper()
helper.upload_content()
