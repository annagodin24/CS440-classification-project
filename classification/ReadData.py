import random
from scipy.spatial import distance
import Image
import Bayes
import numpy as geek
import NearestNeighbor


def read_data(file_name, type):
    if type == "digit":
        image_size = 28
    else:
        image_size = 70

    numbers = []
    with open(file_name) as fp:
        line = fp.readline()
        count_rows = 0
        image = []
        while line:
            row = []
            for c in line:
                if c == ' ':
                    row.append('0')
                else:
                    row.append('1')
            row.pop(len(row) - 1)
            image.append(row)

            count_rows += 1
            if count_rows == image_size:
                count_rows = 0
                numbers.append(image)
                # for irow in image:
                #     print(irow)
                # print("\n")
                image = []
            line = fp.readline()
    return numbers


def read_labels(file_name):
    labels = []
    with open(file_name) as fp:
        line = fp.readline()
        # print(line)
        while line:
            line = line[:-1]
            labels.append(line)
            line = fp.readline()
    return labels


def extract_features(data, data_labels):
    image_info = []
    index = 0
    count = 0
    for image in data:
        features = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        for row in range(len(image)):
            r = (len(image) / 3)
            a = r
            b = 2*r
            d = 3*r

            for col in range(len(image[row])):
                c = (len(image[row]) / 3)
                e = c
                f = 2*c
                g = 3*c

                if image[row][col] == '1':  # if black pixel

                    if row <=a and col <=e:  # Quadrant 1
                        features[0] += 1

                    elif row>a and row<=b  and col<=e:  # Quadrant 2
                        features[1] += 1

                    elif row>b and row<=d  and col <=e:  # Quadrant 3
                        features[2] += 1

                    elif row <=a and col>e and col<=f:  # Quadrant 4
                        features[3] += 1

                    elif row>a and row<=b  and col>e and col<=f :  # Quadrant 5
                        features[4] += 1

                    elif row>b and row<=d  and col>e and col<=f :  # Quadrant 6
                        features[5] += 1

                    elif row <=a and col>f and col<=g:  # Quadrant 7
                        features[6] += 1

                    elif row>a and row<=b  and col>f and col<=g :  # Quadrant 8
                        features[7] += 1

                    elif row>b and row<=d  and col>f and col<=g:  # Quadrant 9
                        features[8] += 1

                    else:
                        continue

        image_info.append(Image.Image(data_labels[index], features))
        index = index + 1
    return image_info

def extract_features_Matrix(data, data_labels):
    image_info = []
    index = 0
    count = 0
    for image in data:
        features = geek.empty([3, 3])
        features.fill(0)

        for row in range(len(image)):
            r = (len(image) / 3)
            a = r
            b = 2*r
            d = 3*r

            for col in range(len(image[row])):
                c = (len(image[row]) / 3)
                e = c
                f = 2*c
                g = 3*c

                if image[row][col] == '1':  # if black pixel

                    if row <=a and col <=e:  # Quadrant 1
                        features[0][0] += 1

                    elif row>a and row<=b  and col<=e:  # Quadrant 2
                        features[0][1] += 1

                    elif row>b and row<=d  and col <=e:  # Quadrant 3
                        features[0][2] += 1

                    elif row <=a and col>e and col<=f:  # Quadrant 4
                        features[1][0] += 1

                    elif row>a and row<=b  and col>e and col<=f:  # Quadrant 5
                        features[1][1] += 1

                    elif row>b and row<=d  and col>e and col<=f:  # Quadrant 6
                        features[1][2] += 1

                    elif row <=a and col>f and col<=g:  # Quadrant 7
                        features[2][0] += 1

                    elif row>a and row<=b  and col>f and col<=g:  # Quadrant 8
                        features[2][1] += 1

                    elif row>b and row<=d  and col>f and col<=g:  # Quadrant 9
                        features[2][2] += 1

                    else:
                        continue

        image_info.append(Image.Image(data_labels[index], features))
        index = index + 1
    return image_info
# main
train_digit_image = "data/digitdata/trainingimages"
train_face_image = "data/facedata/facedatatrain"
train_digit_label = "data/digitdata/traininglabels"
train_face_label = "data/facedata/facedatatrainlabels"
train_digit_image_list = read_data(train_digit_image, "digit")
train_face_image_list = read_data(train_face_image, "face")
train_digit_labels_list = read_labels(train_digit_label)
train_face_labels_list = read_labels(train_face_label)

test_digit_image = "data/digitdata/testimages"
test_face_image = "data/facedata/facedatatest"
test_digit_label = "data/digitdata/testlabels"
test_face_label = "data/facedata/facedatatestlabels"
test_digit_image_list = read_data(test_digit_image, "digit")
test_face_image_list = read_data(test_face_image, "face")
test_digit_labels_list = read_labels(test_digit_label)
test_face_labels_list = read_labels(test_face_label)

#training
training_image_info_list = extract_features(train_digit_image_list, train_digit_labels_list)
training_face_info_list = extract_features(train_face_image_list, train_face_labels_list)

training_image_info_list_KN = extract_features_Matrix(train_digit_image_list, train_digit_labels_list)
training_face_info_list_KN = extract_features_Matrix(train_face_image_list, train_face_labels_list)

#testing
testing_image_info_list = extract_features(test_digit_image_list, test_digit_labels_list)
testing_face_info_list = extract_features(test_face_image_list, test_face_labels_list)

testing_image_info_list_KN = extract_features_Matrix(test_digit_image_list, test_digit_labels_list)
testing_face_info_list_KN = extract_features_Matrix(test_face_image_list, test_face_labels_list)


guess = []
#guess = Bayes.naive_bayes_face_training(training_face_info_list,testing_face_info_list,9)
#guess = Bayes.naive_bayes_digit_training(training_image_info_list,testing_image_info_list,9)
guess = NearestNeighbor.nearest_neighbor(training_image_info_list_KN,testing_image_info_list_KN)
#guess = NearestNeighbor.nearest_neighbor(training_face_info_list_KN,testing_face_info_list_KN)


count = 0
flag = True

if(flag == False):
    for i in range(len(guess)):
        if(guess[i] == test_face_labels_list[i]):
            count +=1

    print count
    print len(guess)

if(flag == True):
    count = 0
    for i in range(len(guess)):
        if(guess[i] == test_digit_labels_list[i]):
           count +=1

    print count
    print len(guess)
