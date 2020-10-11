import os
import glob
import json
import re


def get_file_extensions_by_album(album):
    assert os.path.isdir(album)
    files = os.listdir(album)
    extensions = []
    for file in files:
        match = re.match(r".*\.(.*)$", file)
        if match:
            extension = match.group(1)
            extension = extension.lower()
            if not extension in extensions:
                extensions.append(extension)
    return extensions


def get_file_extensions_by_albums(path_to_albums):
    album_names = get_album_names(path_to_albums)
    extensions = []
    for album_name in album_names:
        album_path = os.path.join(path_to_albums, album_name)
        try:
            extensions_in_album = get_file_extensions_by_album(album_path)
        except AssertionError:
            continue
        for extension in extensions_in_album:
            if not extension in extensions:
                extensions.append(extension)
    return extensions


def contains_extension(directory, extension):
    lst = glob.glob1(directory, extension)
    if len(lst) > 0:
        return True
    else:
        return False


def contains_photos(directory):
    extensions = ["jpg", "png", "jpeg"]
    for extension in extensions:
        if contains_extension(directory, "*." + extension):
            return extension, True
        extension = extension.upper()
        if contains_extension(directory, "*." + extension):
            return extension, True
    return "", False

def contains_videos(directory):
    extensions = ["mpg", "avi", "mp4", "mts", "3gp"]
    for extension in extensions:
        if contains_extension(directory, "*." + extension):
            return extension, True
        extension = extension.upper()
        if contains_extension(directory, "*." + extension):
            return extension, True
    return "", False


def get_album_dictionary(path):

    album_dict = {}
    album_dict["albums"] = {}

    image_extensions = ["jpg", "png", "jpeg"]
    video_extensions = ["mpg", "avi", "mp4", "mts", "3gp"]
    ignore_files = ["ini", "db", "dat", "tif", "thm", "ini", "bmp", "scn", "zip", "store", "mcf", "mcf~"]

    def get_album_names_rec(album_path):

        album_name = os.path.basename(album_path)
        _, has_photos = contains_photos(album_path)
        _, has_videos = contains_videos(album_path)
        extensions = []
        album_dict["albums"][album_name] = None

        if has_photos or has_videos:
            album_dict["albums"][album_name] = {
                "full_path": album_path,
                "images": 0,
                "videos": 0,
                "other": 0,
            }

        files_n_folders = sorted(os.listdir(album_path))
        for file_o_folder in files_n_folders:

            file_o_folder_path = os.path.join(album_path, file_o_folder)

            # Case where the item is a folder
            if os.path.isdir(file_o_folder_path):
                get_album_names_rec(file_o_folder_path)

            # Case where the item is a file
            if os.path.isfile(file_o_folder_path):
                match = re.match(r".*\.(.*)$", file_o_folder_path)
                if match:
                    extension = match.group(1)
                    extension = extension.lower()
                    if not extension in extensions:
                        extensions.append(extension)

                    if album_dict["albums"][album_name]:
                       if extension in image_extensions:
                           album_dict["albums"][album_name]["images"] += 1
                       if extension in video_extensions:
                           album_dict["albums"][album_name]["videos"] += 1
                       if extension in ignore_files:
                           album_dict["albums"][album_name]["other"] += 1

        if album_dict["albums"][album_name]:
            album_dict["albums"][album_name]["extensions"] = extensions

    get_album_names_rec(path)

    return album_dict


def create_album_created_status(p):
    album_names, extensions = get_album_names(p)
    album_created_dict = {}
    album_created_dict["albums"] = []
    for album_name in album_names:
        album_created_dict["albums"].append(
            {"name": str(album_name),
             "status": "not transferred"})

    json.dump(album_created_dict, open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "albums.json"), "w", encoding='utf8'), ensure_ascii=False)


if __name__ == '__main__':
    path_to_albums = "/media/simon/VERBATIM/Backup af billeder 14022018"

    album_dict = get_album_dictionary(path_to_albums)
