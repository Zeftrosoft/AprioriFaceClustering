# USAGE
# python encode_faces.py --dataset dataset --encodings encodings.pickle
import os
import cv2
import pickle
import argparse
import face_recognition
from imutils import paths


# import the necessary packages
# construct the argument parser and parse the arguments
class Encode:
    def pickle(self, dataset, pickle_path):
        ap = argparse.ArgumentParser()
        ap.add_argument("-d", "--detection-method", type=str, default="cnn",
                        help="face detection model to use: either `hog` or `cnn`")
        args = vars(ap.parse_args())

        # grab the paths to the input images in our dataset, then initialize
        # out data list (which we'll soon populate)
        print("[INFO] quantifying faces...")
        imagePaths = list(paths.list_images(dataset))
        data = []

        # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            print("[INFO] processing image {}/{}".format(i + 1,
                                                        len(imagePaths)))
            print(imagePath)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(
                rgb, model=args["detection_method"])

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            # build a dictionary of the image path, bounding box location,
            # and facial encodings for the current image
            d = [{"imagePath": imagePath, "loc": box, "encoding": enc}
                for (box, enc) in zip(boxes, encodings)]
            data.extend(d)

        # dump the facial encodings data to disk
        print("[INFO] serializing encodings...")
        f = open(pickle_path, "wb")
        f.write(pickle.dumps(data))
        f.close()
