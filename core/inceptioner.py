from keras.applications.inception_v3 import InceptionV3, preprocess_input, decode_predictions
from keras.preprocessing import image
import numpy as np
import os
from configuration.instance import config


class Inceptioner:
    def __init__(self):
        self.model = InceptionV3(weights=None)
        self.model.load_weights(config.model_path)


    def predict(self, img_path):
        img = image.load_img(img_path, target_size=(299, 299))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = self.model.predict(x)
        decoded = decode_predictions(preds)[0][0]
        res = {
            'prediction': decoded[1],
            'confidence': decoded[2]
        }
        return res


if __name__ == '__main__':
    pass