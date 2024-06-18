"""
This code includes the functions which are related to the Google Drive API.
These are mainly; connect_drive, get_files, get_folders, download_folder
"""

import os
import io
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


class DriveConnector:
    def __init__(self) -> None:
        # If modifying these scopes, delete the file token.pickle.
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.service = self.connect_drive()


    def connect_drive(self) -> object:
        """
        Connects to the Google Drive API.
        :return: The Google Drive API service object.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token_drive.json"):
            creds = Credentials.from_authorized_user_file("token_drive.json", self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "token_drive.json", self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token_drive.json", "w") as token:
                token.write(creds.to_json())

        try:
            service = build('drive', 'v3', credentials=creds)
        except Exception as e:
            print(f"An error occurred: {e}")
            service = None
        return service


    def get_files(self, folder_id) -> list:
        """
        Lists the files in the Google Drive folder.
        :return: The list of files in the folder.
        """
        results = self.service.files().list(
            q=f"'{folder_id}' in parents and trashed=false and mimeType!='application/vnd.google-apps.folder'",
            fields="nextPageToken, files(id, name)",
        ).execute()
        items = results.get("files", [])
        return items


    def get_folders(self, folder_id) -> list:
        """
        Lists the folders in the Google Drive folder.
        :return: The list of folders in the folder.
        """
        results = self.service.files().list(
            q=f"'{folder_id}' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'",
            fields="nextPageToken, files(id, name)",
        ).execute()
        items = results.get("files", [])
        return items


    def download_folder(self, folder_id, destination) -> None:
        """
        Downloads the files in the Google Drive folder.
        :param folder_id: The ID of the folder to download.
        :param destination: The path to the destination folder.
        """
        if not os.path.exists(destination):
            os.makedirs(destination)
        files = self.get_files(folder_id)
        for file in files:
            file_id = file["id"]
            file_name = file["name"]
            request = self.service.files().get_media(fileId=file_id)
            fh = io.FileIO(f"{destination}/{file_name}", "wb")
            downloader = io.BytesIO()
            downloader.write(request.execute())
            fh.write(downloader.getvalue())
            fh.close()
            downloader.close()
        folders = self.get_folders(folder_id)
        for folder in folders:
            folder_id = folder["id"]
            folder_name = folder["name"]
            new_destination = f"{destination}/{folder_name}"
            self.download_folder(folder_id, new_destination)

