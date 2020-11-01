import json
from utils import *

IMAGE_EXTENSIONS = ["jpg", "png", "jpeg"]
VIDEO_EXTENSION = ["mpg", "avi", "mp4", "mts", "3gp"]
ignore_files = ["ini", "db", "dat", "tif", "thm", "ini", "bmp", "scn", "zip", "store", "mcf", "mcf~"]
NOT_TRANSFERRED = "NOT_TRANSFERRED"
TRANSFERRED = "TRANSFERRED"
FAILED = "FAILED"


def create_album_dictionary(directory):
    """
    directory: path to a directory containing albums with images/videos
    returns: a dictionary with the name of each folder containing images and/or videos
    e.g.
    {"album_name":
        {
        "full_path": album_path,
        "images": 0,
        "videos": 0,
        "other": 0,
        "status": "not_transferred"
        }
    }
    """
    dict = {}

    def create_album_dictionary_rec(sub_directory):

        album_name = os.path.basename(sub_directory)
        has_photos = contains_photos(sub_directory)
        has_videos = contains_videos(sub_directory)
        extensions = []

        if has_photos or has_videos:
            dict[album_name] = {
                "full_path": sub_directory,
                "images": 0,
                "videos": 0,
                "other": 0,
                "status": NOT_TRANSFERRED
            }

        files_n_folders = sorted(os.listdir(sub_directory))
        for file_o_folder in files_n_folders:

            file_o_folder_path = os.path.join(sub_directory, file_o_folder)

            # Case where the item is a folder
            if os.path.isdir(file_o_folder_path):
                create_album_dictionary_rec(file_o_folder_path)

            # Case where the item is a file
            if os.path.isfile(file_o_folder_path):
                match = re.match(r".*\.(.*)$", file_o_folder_path)
                if match:
                    extension = match.group(1)
                    extension = extension.lower()
                    if not extension in extensions:
                        extensions.append(extension)

                    if has_photos or has_videos:
                        if extension in IMAGE_EXTENSIONS:
                            dict[album_name]["images"] += 1
                        if extension in VIDEO_EXTENSION:
                            dict[album_name]["videos"] += 1
                        if extension in ignore_files:
                            dict[album_name]["other"] += 1

        if has_photos or has_videos:
            dict[album_name]["extensions"] = extensions

    create_album_dictionary_rec(directory)
    return dict


if __name__ == '__main__':
    path_to_albums = "/home/simon/Desktop/Backup af billeder 14022018"
    album_dict = create_album_dictionary(path_to_albums)
    save_fn = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/albums_test.json")
    save_file = open(save_fn, "w", encoding='utf8')
    json.dump(album_dict, save_file, indent="\t", ensure_ascii=False)
