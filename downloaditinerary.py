from __future__ import print_function
import pickle
import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaIoBaseDownload
import service

def findFile(name):
    """Finds the itinerary Google Doc with NAME.
    """
    page_token = None
    while True:
        response = service.create_service().files().list(q="name='" + name + "'",
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)',
                                              pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
            return file

def downloadFile(file, mimeType, filepath):
    """Downloads the itinerary as a plain text file.
    """
    request = service.create_service().files().export_media(fileId=file.get('id'),
                                                 mimeType=mimeType)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())

itinerary = findFile("2020 Pac-12 Championships Itinerary")
downloadFile(itinerary,'text/plain', itinerary.get('name'))
