import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import keras


# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    # containers for input/output pairs
    X = [series[i:(i + window_size)] for i in range(0, len(series) - window_size)]
    y = series[window_size:]

    # reshape each 
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)

    return X,y


def build_part1_RNN(window_size):
    model = Sequential()
    model.add(LSTM(5, input_shape=(window_size, 1)))
    model.add(Dense(1))
    return model


def cleaned_text(text):
    import string
    punctuation = ['!', ',', '.', ':', ';', '?']
    allowed_chars = list(string.ascii_letters) + punctuation + list(' ')
    chars_in_text = set(text)
    chars_to_remove = [c for c in chars_in_text if c not in allowed_chars]
    
    for punct in chars_to_remove:
        text = text.replace(punct, '')
    
    return text

def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = [text[i:(i + window_size)] for i in range(0, len(text) - window_size, step_size)]
    outputs = [text[i + window_size] for i in range(0, len(text) - window_size, step_size)]
    
    return inputs, outputs

# TODO build the required RNN model: 
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
def build_part2_RNN(window_size, num_chars):
    model = Sequential()
    model.add(LSTM(200, input_shape = (window_size, num_chars)))
    model.add(Dense(num_chars, activation='softmax'))
    return model
