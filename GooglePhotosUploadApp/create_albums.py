import json
import os
import re
import requests
import pickle
import time

import pandas as pd
from create_google_service import service
from script.create_album_dictionary import TRANSFERRED, NOT_TRANSFERRED, IMAGE_EXTENSIONS, VIDEO_EXTENSION


def parse_values(values):
    full_path = values["full_path"]
    images = values["images"]
    videos = values["videos"]
    other = values["other"]
    status = values["status"]
    extensions = values["extensions"]
    return full_path, images, videos, other, status, extensions


def get_images_and_video_files(album_directory):
    files_for_transfer = []
    files = os.listdir(album_directory)
    for file in files:
        fp = os.path.join(album_directory, file)
        if os.path.isfile(fp):
            match = re.match(r".*\.(.*)$", file)
            if match:
                extension = match.group(1)
                extension = extension.lower()
                if extension in IMAGE_EXTENSIONS or extension in VIDEO_EXTENSION:
                    files_for_transfer.append(fp)
    return files_for_transfer


def create_media_item(image_file, token):
    img_name = os.path.basename(image_file)
    upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'

    request_headers = {
        "Authorization": "Bearer " + token,
        "Content-type": 'application/octet-stream',
        'X-Goog-Upload-Protocol': 'raw',
        'X-Goog-Upload-File-Name': img_name
    }

    img = open(image_file, "rb").read()

    start_time = time.time()
    response = requests.post(upload_url, data=img, headers=request_headers)
    print("Post request took", time.time() - start_time)

    media_item = {
        "simpleMediaItem": {
            "fileName": img_name,
            "uploadToken": response.content.decode('utf-8')
        }
    }

    return media_item


if __name__ == '__main__':

    print("WARNING: THIS IS RUN ON TEST ALBUMS!!!")

    # Read the json file with the album names
    albums_fp = "/home/simon/Projects/Week-by-week-learning/GooglePhotosUploadApp/data/albums_test.json"
    albums_file = open(albums_fp, "r", encoding='utf-8')
    dict = json.load(albums_file)
    token = pickle.load(open("token_photoslibrary_v1.pickle", "rb"))

    """
    iterate over each album name and create a photo album 
    """
    for key in dict.keys():
        album_name = key
        album_values = dict[album_name]
        full_path, images, videos, other, status, extensions = parse_values(album_values)

        if status == NOT_TRANSFERRED:
            print("Processing...", album_name)

            # Create the album
            request_body = {
                'album': {
                    'title': album_name,
                    'isWriteable': True
                },
            }
            response = service.albums().create(body=request_body).execute()

            if response:
                album_id = response["id"]
                print("Album id", album_id)

                # Change the status to TRANSFERRED
                dict[album_name]["status"] = TRANSFERRED
                album_path = full_path

                # Extract image and video files
                files_for_transfer = get_images_and_video_files(album_path)

                # TODO: Create MediaItems
                # see: https://developers.google.com/photos/library/reference/rest/v1/mediaItems#MediaItem

                # Add images and video files to album
                mediaItems = []
                for file in files_for_transfer:
                    print("Creating media item for", file)
                    media_item = create_media_item(file, token=token.token)
                    mediaItems.append(media_item)

                upload_request = {
                    "albumId": album_id,
                    "newMediaItems": mediaItems
                }

                upload_response = service.mediaItems().batchCreate(body=upload_request).execute()
                print("Uploaded", len(mediaItems), "media items to", album_name)
                json.dump(dict, open(albums_fp, "w"), indent="\t")
            # TODO: Check that the number of images and videos corresponds to images and videos in the album_values

        else:
            print(album_name, "is already transferred")



#
