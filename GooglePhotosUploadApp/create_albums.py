import json
import os
import re
import requests
import pickle
import time

from create_google_service import service
from script.create_album_dictionary import TRANSFERRED, NOT_TRANSFERRED, FAILED, IMAGE_EXTENSIONS, VIDEO_EXTENSION


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

    response = requests.post(upload_url, data=img, headers=request_headers)

    media_item = {
        "simpleMediaItem": {
            "fileName": img_name,
            "uploadToken": response.content.decode('utf-8')
        }
    }

    return media_item


if __name__ == '__main__':

    # print("WARNING: THIS IS RUN ON TEST ALBUMS!!!")

    # Read the json file with the album names
    albums_fp = "/home/simon/Projects/Week-by-week-learning/GooglePhotosUploadApp/data/albums.json"
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
            print("Processing album:", album_name)

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

                # Change the status to TRANSFERRED
                album_path = full_path

                # Extract image and video files
                files_for_transfer = get_images_and_video_files(album_path)

                # Add images and video files to album
                mediaItems = []
                for file_i, file in enumerate(files_for_transfer):
                    print("Processing media item (" + str(file_i + 1) + "/" + str(len(files_for_transfer)) + ":", file)
                    # Create MediaItems
                    # Documentation: https://developers.google.com/photos/library/reference/rest/v1/mediaItems#MediaItem
                    media_item = create_media_item(file, token=token.token)
                    # mediaItems.append(media_item)
                    upload_request = {
                        "albumId": album_id,
                        "newMediaItems": [media_item]
                    }
                    mediaItems.append(media_item)
                    upload_response = service.mediaItems().batchCreate(body=upload_request).execute()

                print("Uploaded", len(mediaItems), "media items to", album_name)
                if len(mediaItems) == dict[album_name]["videos"] + dict[album_name]["images"]:
                    dict[album_name]["status"] = TRANSFERRED
                else:
                    dict[album_name]["status"] = FAILED
                json.dump(dict, open(albums_fp, "w"), indent="\t")

        else:
            print(album_name, "is already transferred")



"""
TODO:

FIX
Processing media item (65/87: /media/simon/VERBATIM/Backup af billeder 14022018/Blandede billeder 2016/20161202_215111.jpg
Processing media item (66/87: /media/simon/VERBATIM/Backup af billeder 14022018/Blandede billeder 2016/20161202_215117.jpg
Processing media item (67/87: /media/simon/VERBATIM/Backup af billeder 14022018/Blandede billeder 2016/20161202_215132.mp4
Processing media item (68/87: /media/simon/VERBATIM/Backup af billeder 14022018/Blandede billeder 2016/20161202_215236.mp4
Processing media item (69/87: /media/simon/VERBATIM/Backup af billeder 14022018/Blandede billeder 2016/20161202_215325.mp4
Processing media item (70/87: /media/simon/VERBATIM/Backup af billeder 14022018/Blandede billeder 2016/20161202_215439.jpg
Traceback (most recent call last):
  File "/home/simon/Projects/Week-by-week-learning/GooglePhotosUploadApp/create_albums.py", line 117, in <module>
    upload_response = service.mediaItems().batchCreate(body=upload_request).execute()
  File "/home/simon/.pyenv/versions/week-by-week/lib/python3.6/site-packages/googleapiclient/_helpers.py", line 134, in positional_wrapper
    return wrapped(*args, **kwargs)
  File "/home/simon/.pyenv/versions/week-by-week/lib/python3.6/site-packages/googleapiclient/http.py", line 907, in execute
    raise HttpError(resp, content, uri=self.uri)
googleapiclient.errors.HttpError: <HttpError 400 when requesting https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate?alt=json returned "Request must contain a valid upload token.">

Process finished with exit code 1
"""

