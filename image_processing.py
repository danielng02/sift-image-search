import cv2
import os
import numpy as np

class ProcessedImage:
    def __init__(self, path, name, descriptors, image):
        self.path = path
        self.name = name
        self.descriptors = descriptors
        self.image = image


class ImageMatch:
    def __init__(self, score, image1, image2):
        self.score = score
        self.image1_name = image1.name
        self.image2_name = image2.name
        self.image1_path = image1.path
        self.image2_path = image2.path
    def __hash__(self):
        return hash((self.image1_name, self.image1_path, self.image2_name, self.image2_path))

    def __eq__(self, other):
        if isinstance(other, ImageMatch):
            return (self.image1_name, self.image1_path, self.image2_name, self.image2_path) == (other.image1_name, other.image1_path, other.image2_name, other.image2_path)
        return False
        

def process_image_directory(path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    images = []

    full_path = os.path.abspath(os.path.expanduser(path))
    obj = os.scandir(full_path)

    for entry in obj:
        if entry.is_file():
            if any(entry.name.lower().endswith(ext) for ext in image_extensions):
                processed_image = process_image(full_path, entry.name)
                images.append(processed_image)
    return images

def process_image(path, name):
    sift = cv2.SIFT_create()

    img = cv2.imread(path + '/' + name)

    keypoints, descriptors = sift.detectAndCompute(img, None)
    return ProcessedImage(path, name, descriptors, img)

def knn_match_good_descriptors(image1, image2):
    bf = cv2.BFMatcher()

    matches = bf.knnMatch(image1.descriptors, image2.descriptors, k=2)
    good = []

    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])

    return good

def match_images(directory1, directory2, k=2, range_ratio=0.75):
    image_matches = set()

    for image1 in directory1:
        for image2 in directory2:
            if np.array_equal(image1.image, image2.image):
                continue

            good = knn_match_good_descriptors(image1, image2)

            image_match = ImageMatch(len(good), image1, image2)
            image_matches.add(image_match)
            
    return image_matches