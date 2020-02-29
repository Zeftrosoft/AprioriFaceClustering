# USAGE
# python cluster.py --encodings encodings.pickle

# import the necessary packages

from sklearn.cluster import DBSCAN
from imutils import build_montages
import numpy as np
import argparse
import pickle
import cv2
import os
from dbhelper import DBHelper
from mlxtend.frequent_patterns import apriori
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder


class Cluster:
    
    def montage(self, pickle_path):
        helper = DBHelper()
        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-j", "--jobs", type=int, default=-1,
                        help="# of parallel jobs to run (-1 will use all CPUs)")
        args = vars(ap.parse_args())

        # load the serialized face encodings + bounding box locations from
        # disk, then extract the set of encodings to so we can cluster on
        # them
        print("[INFO] loading encodings...")
        data = pickle.loads(open(pickle_path, "rb").read())
        data = np.array(data)
        encodings = [d["encoding"] for d in data]
        # print(encodings)
        # cluster the embeddings
        #print("[INFO] clustering...")
        clt = DBSCAN(metric="euclidean", n_jobs=args["jobs"])
        clt.fit(encodings)

        # determine the total number of unique faces found in the dataset
        labelIDs = np.unique(clt.labels_)
        numUniqueFaces = len(np.where(labelIDs > -1)[0])
        # print("[INFO] # unique faces: {}".format(numUniqueFaces))

        # loop over the unique face integers
        for labelID in labelIDs:

            # find all indexes into the `data` array that belong to the
            # current label ID, then randomly sample a maximum of 25 indexes
            # from the set
            print("[INFO] faces for face ID: {}".format(labelID))
            idxs = np.where(clt.labels_ == labelID)[0]
            # print(len(idxs))
            #idxs = np.random.choice(idxs, size=min(4, len(idxs)), replace=False)
            idxs = np.random.choice(idxs, size=len(idxs), replace=False)

            # initialize the list of faces to include in the montage
            faces = []

            # loop over the sampled indexes
            for i in idxs:
                # load the input image and extract the face ROI
                image = cv2.imread(data[i]["imagePath"])  # Saved Image Path
                (top, right, bottom, left) = data[i]["loc"]
                face = image[top:bottom, left:right]
                # force resize the face ROI to 96x96 and then add it to the
                # faces montage list
                face = cv2.resize(face, (96, 96))
                faces.append(face)
                # gettting image name from path
                img_path = data[i]["imagePath"]
                str(img_path)
                image_tuple = img_path.split("\\")
                img_tuple_len = len(image_tuple)
                img_tuple_length = img_tuple_len - 1
                imagefullname = image_tuple[img_tuple_length]
                image_name = imagefullname.split(".")
                image_path = "/dist/image/dataset1/{0}".format(imagefullname)
                invoice_id = helper.getinvoiceid(
                    labelID, image_path, image_name[0])
                if len(invoice_id) <= 0:
                    helper.insert_labelid_image_path_invoiceno(
                        labelID, image_path, image_name[0])

            # create a montage using 96x96 "tiles" with 5 rows and 5 columns
            montage = build_montages(faces, (96, 96), (5, 5))[0]
            montage_image = "montag-{0}.jpg".format(labelID)
            # creating path for storing montage
            montage_path = os.path.join(
                os.getcwd(), "web", "static", "dist", "image", "montage", montage_image)

        # return label_id from invoice table ,if not insert it into user table
            user_id = helper.getuserid(labelID)
            db_montage_path = "/dist/image/montage/{0}".format(montage_image)
            if len(user_id) <= 0:
                helper.insert_labelid_montage(labelID, db_montage_path)
            else:
                helper.update_user(user_id[0][0], db_montage_path)
            # get invoice using labelid
            #invoice = helper.getinvoicesbyuserid(labelID)
            # print(invoice)
            listofitems = helper.getinvoiceitembyuserid(labelID)
            # print(listofitems)
            #alluser = helper.getalluser()
            # print(alluser)
            # show the output montage and store the montage to dist/image/montage path
            title = "Face ID #{}".format(labelID)
            title = "Unknown Faces" if labelID == -1 else title
            #cv2.imshow(title, montage)
            cv2.imwrite(montage_path, montage)
            cv2.waitKey(0)
            
