import glob
import os
import re


def _contains_extension(directory, extension):
    lst = glob.glob1(directory, extension)
    if len(lst) > 0:
        return True
    else:
        return False


def contains_photos(directory):
    extensions = ["jpg", "png", "jpeg"]
    for extension in extensions:
        if _contains_extension(directory, "*." + extension):
            return True
        extension = extension.upper()
        if _contains_extension(directory, "*." + extension):
            return True
    return False


def contains_videos(directory):
    extensions = ["mpg", "avi", "mp4", "mts", "3gp"]
    for extension in extensions:
        if _contains_extension(directory, "*." + extension):
            return True
        extension = extension.upper()
        if _contains_extension(directory, "*." + extension):
            return True
    return False


# Finds unique file extensions in directory
def get_file_extensions_in_dir(directory):
    assert os.path.isdir(directory)
    files = os.listdir(directory)
    extensions = []
    for file in files:
        match = re.match(r".*\.(.*)$", file)
        if match:
            extension = match.group(1)
            extension = extension.lower()
            if not extension in extensions:
                extensions.append(extension)
    return extensions
