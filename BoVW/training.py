import cv2, os, sys, pickle
import numpy as np
from sklearn.svm import SVC
from constants import *
from functions import (
    load_image_info_list, extract_sift_features, build_features
)

# from sklearn.cluster import KMeans
from cuml.cluster import KMeans

# Vocabulary building
def build_vocabulary(descriptors, k):
    kmeans = KMeans(n_clusters=k, random_state=0, n_init=3, tol=1e-4)
    kmeans.fit(np.vstack(descriptors))

    return kmeans

# Classifier training
def train_classifier(features, labels):
    classifier = SVC(kernel='linear')
    classifier.fit(features, labels)

    return classifier

def main():
    try:
        image_path = sys.argv[1]
    except:
        print('Invalid argv! Expected: training_set_path')

    print('Read training set list')

    training_list = load_image_info_list(os.path.join(image_path, 'training'))
    image_paths = [i[K_PATH] for i in training_list]

    print(f'Training size: {len(training_list)}')

    descriptors = extract_sift_features(image_paths)
    sift_size = 0

    for i in range(len(descriptors)):
        if descriptors[i] is None:
            print('Error: no features were found in', training_list[i][K_FILE])
            exit(0)
        sift_size += len(descriptors[i])

    print('SIFT size: {}'.format(sift_size))
    print('Build vocabulary')

    kmeans = build_vocabulary(descriptors,k=NO_CLUSTERS)

    with open(F_KMEANS, 'wb') as file:
        pickle.dump(kmeans, file)

    print('Build features')

    features = build_features(kmeans, descriptors)

    print('Train classifier')

    labels = [f'{i[K_CITY]}_{i[K_PLACEID]}' for i in training_list]
    classifier = train_classifier(features, labels)

    with open(F_CLASSIFIER, 'wb') as file:
        pickle.dump(classifier, file)

    print('Training completed')

if __name__ == '__main__':
    main()
