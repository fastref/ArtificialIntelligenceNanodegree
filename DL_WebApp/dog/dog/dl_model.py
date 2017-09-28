from keras.models import model_from_json
import os


class ModelHandling(object):
    """Class for loading and saving Keras models"""

    def __init__(self):
        pass

    def load_model(self, json_path, weight_path):
        try:
            model = model_from_json(open(json_path).read())
            model.load_weights(weight_path)
            return model
        except Exception as e:
            raise Exception("Loading model/weights failed")


    def save_model(self, model, json_path, weight_path):
        json = model.to_json()
        with open(json_path, 'w') as f:
            f.write(json)
        model.save_weights(weight_path)


class WebPrediction(object):

    def __init__(self, json_path, weight_path):
        model_handling = ModelHandling()
        self.model = model_handling.load_model(json_path, weight_path)


    def compile_model(self, loss = 'categorical_crossentropy', optimizer = 'rmsprop', **kwargs):
        self.model.compile(loss=loss, optimizer=optimizer, **kwargs)


    def predict(self, image_file):
        img = image.load_img(image_file, target_size=(299, 299))

        return self.model.predict(X_input)
