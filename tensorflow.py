import os
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.utils import np_utils
from keras_preprocessing.sequence import pad_sequences

numpy.random.seed(7)

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

char_to_int = dict((c, i) for i, c in enumerate(alphabet))
int_to_char = dict((i, c) for i, c in enumerate(alphabet))

seq_length = 3
dataX = []
dataY = []
for i in range(0, len(alphabet) - seq_length, 1):
    seq_in = alphabet[i:i + seq_length]
    seq_out = alphabet[i + seq_length]
    dataX.append([char_to_int[char] for char in seq_in])
    dataY.append(char_to_int[seq_out])

print(dataX)

X = numpy.reshape(dataX, (len(dataX), seq_length, 1))

X = X / float(len(alphabet))

y = np_utils.to_categorical(dataY)


model = Sequential()
model.add(LSTM(32,input_shape = (X.shape[1],X.shape[2])))

model.add(Dense(y.shape[1],activation="softmax"))
model.compile(loss = "categorical_crossentropy", optimizer = "adam", metrics= ["accuracy"])

model.fit(X, y, epochs=500, batch_size=len(dataX), verbose=2, shuffle=False)

scores = model.evaluate(X,y,verbose=0)
print("Model Accuracy: %.2f%%" %(scores[1]*100))
#----------------------------------------------------------
for pattern in dataX:

    x = numpy.reshape(pattern, (1, len(pattern), 1))

    x = x / float(len(alphabet))
    prediction = model.predict(x, verbose=0)
    index = numpy.argmax(prediction)
    result = int_to_char[int(index)]
    seq_in = [int_to_char[value] for value in pattern]
    print(seq_in, "->", result)

print("Test a Random Pattern:")
for i in range(0,20):
    pattern_index = numpy.random.randint(len(dataX))
    pattern = dataX[pattern_index]
    x = numpy.reshape(pattern, (1, len(pattern), 1))
    x = x / float(len(alphabet))
    prediction = model.predict(x, verbose=0)
    index = numpy.argmax(prediction)
    result = int_to_char[int(index)]
    seq_in = [int_to_char[value] for value in pattern]
    print(seq_in, "->", result)
























