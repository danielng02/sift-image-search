from flask import Flask, render_template, request, jsonify
import cv2
import os
import numpy as np
from tinydb import TinyDB, Query

app = Flask(__name__)

class ProcessedImage:
  def __init__(self, path, name, descriptors, image):
    self.path = path
    self.name = name
    self.descriptors = descriptors
    self.image = image
class ImageMatch:
  def __init__(self, score, image1, image2, same):
    self.score = score
    self.image1 = image1
    self.image2 = image2
    self.same = same

def object_to_dict(obj):
    obj_dict = {}
    for attr in vars(obj):
        if attr != 'image' and attr != 'descriptors':
            value = getattr(obj, attr)
            if isinstance(value, ProcessedImage):
                value = object_to_dict(value)
            obj_dict[attr] = value
    return obj_dict

def processImageDirectory(path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    images = []

    obj = os.scandir(path)

    for entry in obj:
        if entry.is_file():
            if any(entry.name.lower().endswith(ext) for ext in image_extensions):
                processed_image = processImage(path, entry.name)
                images.append(processed_image)
    return images

def processImage(path, name):
    sift = cv2.SIFT_create()

    img = cv2.imread(path + '/' + name)

    keypoints, descriptors = sift.detectAndCompute(img, None)
    return ProcessedImage(path, name, descriptors, img)

def knnMatchGoodDescriptors(image1, image2, k = 2, range_ratio = 0.75):
    bf = cv2.BFMatcher()

    knn_matches = bf.knnMatch(image1.descriptors, image2.descriptors, k)
    good = []

    for match_list in knn_matches:
        pass_test = True
        for i in range(1, k):
            if match_list[0].distance >= range_ratio * match_list[i].distance:
                pass_test = False
                break
        if pass_test:
            good.append(match_list[0])


    return good

def matchImages(directory1, directory2, k = 2, range_ratio = 0.75):
    image_matches = []

    for image1 in directory1:
        for image2 in directory2:

            if np.array_equal(image1.image, image2.image):
                image_match = ImageMatch(0, image1, image2, True)
                image_matches.append(image_match)
                continue

            good = knnMatchGoodDescriptors(image1, image2, k, range_ratio)

            image_match = ImageMatch(len(good), image1, image2, False)
            image_matches.append(image_match)

    return image_matches

def saveItemsToDb(db, items):
    for item in items:
        item_dict = object_to_dict(item)
        db.insert(item_dict)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load', methods=['POST'])
def load():
    try:
        matchesDb = TinyDB('matches_db.json')
        matchesDb.truncate();

        data = request.get_json()

        processed_img1 = processImageDirectory(data["path1"])
        processed_img2 = processImageDirectory(data["path2"])

        if not processed_img1 or not processed_img2:
            return jsonify(message="No images found"), 400

        matches = matchImages(processed_img1, processed_img2, int(data["kNN"]), float(data["range"]))
        saveItemsToDb(matchesDb, matches)

        return jsonify(message="Images processed and saved successfully"), 200
    except Exception as e:
        return jsonify(message=str(e)), 500

if __name__ == '__main__':
    app.run()
