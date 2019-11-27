from google_images_download import google_images_download
import os, shutil


def get_image_url(city_name):
    response = google_images_download.googleimagesdownload()
    arguments = { "keywords": city_name, "limit": 1 }
    paths = response.download(arguments)
    return paths[0][city_name][0]


def delete_photo():
    folder = './downloads'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)