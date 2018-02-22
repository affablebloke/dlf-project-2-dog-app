from glob import glob

import numpy as np

import cv2
from extract_bottleneck_features import *
from keras.applications.resnet50 import (ResNet50, decode_predictions,
                                         preprocess_input)
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Sequential
from keras.preprocessing import image
from keras.utils import np_utils
from sklearn.datasets import load_files

print('Loading bottleneck features...')
bottleneck_features = np.load('/bottleneck_features/DogResnet50Data.npz')
train_Resnet50 = bottleneck_features['train']
valid_Resnet50 = bottleneck_features['valid']
test_Resnet50 = bottleneck_features['test']

# define function to load train, test, and validation datasets
def load_dataset(path):
    data = load_files(path)
    dog_files = np.array(data['filenames'])
    dog_targets = np_utils.to_categorical(np.array(data['target']), 133)
    return dog_files, dog_targets

# load list of dog names
dog_names = [item[20:-1] for item in sorted(glob("/dogImages/train/*/"))]

# print statistics about the dataset
print('There are %d total dog categories.' % len(dog_names))

_ResNet50_model = ResNet50(weights='imagenet')

def load_model():
    model = Sequential()
    model.add(GlobalAveragePooling2D(
        input_shape=train_Resnet50.shape[1:]))
    model.add(Dense(133, activation='softmax'))
    model.load_weights('/saved_models/weights.best.Resnet50.hdf5')
    return model


def path_to_tensor(img):
    # loads RGB image as PIL.Image.Image type
    # img = image.load_img(img_path, target_size=(224, 224))
    # convert PIL.Image.Image type to 3D tensor with shape (224, 224, 3)
    x = image.img_to_array(img)
    # convert 3D tensor to 4D tensor with shape (1, 224, 224, 3) and return 4D tensor
    return np.expand_dims(x, axis=0)


def Resnet50_predict_breed(img):
    model = load_model()
    # extract bottleneck features
    bottleneck_feature = extract_Resnet50(path_to_tensor(img))
    predicted_vector = model.predict(bottleneck_feature)
    # return dog breed that is predicted by the model
    return dog_names[np.argmax(predicted_vector)]


def paths_to_tensor(img_paths):
    list_of_tensors = [path_to_tensor(img_path) for img_path in img_paths]
    return np.vstack(list_of_tensors)


def ResNet50_predict_labels(img):
    img = preprocess_input(path_to_tensor(img))
    return np.argmax(_ResNet50_model.predict(img))


def dog_detector(img):
    prediction = ResNet50_predict_labels(img)
    return ((prediction <= 268) & (prediction >= 151))


def face_detector(img):
    # extract pre-trained face detector
    face_cascade = cv2.CascadeClassifier(
        '/haarcascades/haarcascade_frontalface_alt.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    return len(faces) > 0


def fix_breed_name(breed):
    return breed.replace('_', ' ').replace('.', '')


def dog_classifier(img):
    # cv_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if(dog_detector(img)):
        return {'is_dog': True, 'breed': fix_breed_name(Resnet50_predict_breed(img))}
    elif(face_detector(img)):
        return {'is_dog': False, 'breed': fix_breed_name(Resnet50_predict_breed(img))}
    else:
        raise Exception("The image provided does not resemble a human or dog!")
