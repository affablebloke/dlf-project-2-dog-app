import numpy as np

from keras import applications
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator


class BottleneckFeatureExtractor(object):
    """
    Bottleneck features are the last activation maps before the fully-connected layers.
    https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html
    https://github.com/udacity/aind2-cnn/blob/master/transfer-learning/bottleneck_features.ipynb
    """

    def __init__(self, model_name='resnet50', weights='imagenet'):
        # These could be dependency injected
        self.dependency_map = {
            'resnet50': {'model': applications.resnet50.ResNet50, 'preprocess_input': applications.resnet50.preprocess_input},
            'vgg16': {'model': applications.vgg16.VGG16, 'preprocess_input': applications.vgg16.preprocess_input},
            'vgg19': {'model': applications.vgg19.VGG19, 'preprocess_input': applications.vgg19.preprocess_input},
            'xception': {'model': applications.xception.Xception, 'preprocess_input': applications.Xception.preprocess_input},
            'inceptionv3': {'model': applications.inception_v3.InceptionV3, 'preprocess_input': applications.InceptionV3.preprocess_input}
        }
        dependency = self.dependency_map.get(model_name.lower())
        self.model = dependency.get('model')(
            weights='imagenet', include_top=False)
        self.preprocess_input = dependency.get('preprocess_input')
        self.datagen = image.ImageDataGenerator(
            rotation_range=40,
            width_shift_range=0.2,
            height_shift_range=0.2,
            rescale=1./255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest')

    def run(self, saved_file_name, train_dir, validation_dir, train_size, validation_size, batch_size=16):
        generator = self.datagen.flow_from_directory(
                train_dir,
                target_size=(224, 224),  # these architectures trained on imagenet expect 224x224
                batch_size=batch_size,
                class_mode='categorical')
        bottleneck_features_train = self.model.predict_generator(generator, train_size)
        generator = self.datagen.flow_from_directory(
                validation_dir,
                target_size=(224, 224),
                batch_size=batch_size,
                class_mode='categorical')
        bottleneck_features_validation = self.model.predict_generator(generator, validation_size)
        np.savez('{0}_bottleneck_features.npy'.format(saved_file_name), train=bottleneck_features_train, validate=bottleneck_features_validation)