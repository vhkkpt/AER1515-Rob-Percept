import os, cv2
import numpy as np
from constants import *

# SIFT feature extraction
def extract_sift_features(image_paths):
    sift = cv2.SIFT_create(nfeatures=NO_FEATURES)
    descriptors = []

    for image_path in image_paths:
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, des = sift.detectAndCompute(gray, None)
        descriptors.append(des)

    return descriptors

# Feature encoding
def build_features(kmeans, descriptors):
    features = []

    for des in descriptors:
        histogram = np.zeros(len(kmeans.cluster_centers_))
        cluster_result = kmeans.predict(des)

        for i in cluster_result:
            histogram[i] += 1
        features.append(histogram)

    return features

# Dataset info extraction
def load_image_info_list(dataset_path):
    image_info_list = []

    for city_folder in os.listdir(dataset_path):
        city_folder_path = os.path.join(dataset_path, city_folder)

        for image_file in os.listdir(city_folder_path):
            parts = image_file.split('_')

            if len(parts) > 8:
                parts = parts[:7] + ['_'.join(parts[7:])]

            (city, place_id, year, month, bearing, latitude,
                longitude, panoid) = parts
            panoid = panoid.split('.')[0]

            image_info_list.append({
                K_CITY: city,
                K_PLACEID: place_id,
                K_YEAR: year,
                K_MONTH: month,
                K_BEARING: bearing,
                K_LATITUDE: latitude,
                K_LONGITUDE: longitude,
                K_PANOID: panoid,
                K_FILE: image_file,
                K_PATH: os.path.join(city_folder_path, image_file)
            })

    return image_info_list