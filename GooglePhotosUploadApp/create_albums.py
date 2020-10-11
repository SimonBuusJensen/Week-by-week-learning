import json
import os
import re

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


if __name__ == '__main__':

    print("WARNING: THIS IS RUN ON TEST ALBUMS!!!")

    # Read the json file with the album names
    albums_fp = "/home/simon/Projects/Week-by-week-learning/GooglePhotosUploadApp/data/albums_test.json"
    albums_file = open(albums_fp, "r", encoding='utf-8')
    dict = json.load(albums_file)

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
                'album': {'title': album_name}
            }
            response = service.albums().create(body=request_body).execute()
            if response:
                album_id = response["id"]

                # Change the status to TRANSFERRED
                dict[album_name]["status"] = TRANSFERRED
                album_path = full_path

                # Extract image and video files
                files_for_transfer = get_images_and_video_files(album_path)

                # TODO: Create MediaItems
                # see: https://developers.google.com/photos/library/reference/rest/v1/mediaItems#MediaItem

                # Add images and video files to album
                service.albums().batchAddMediaItems()

                # TODO: Check that the number of images and videos corresponds to images and videos in the album_values



            else:
                print("WARNING: couldn't process", album_name)











#
