'''Trains and evaluate a simple MLP
on the Reuters newswire topic classification task.
'''
from __future__ import print_function

import numpy as np
from tensorflow import keras
from tensorflow.keras.datasets import reuters
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

import CNN_NLP as cn

max_words = 10000
batch_size = 32
epochs = 5
max_title_len = 20

number_tickers = 30
print("Loading first", number_tickers, "tickers")
tickers = cn.getAllTickers()[0:number_tickers]
tickToInd = {tick:num for num, tick in enumerate(tickers)}
indToTick = {num:tick for num, tick in enumerate(tickers)}



print('Loading data...')
(x_traino, y_train), (x_testo, y_test) = reuters.load_data(num_words=max_words,
                                                         test_split=0.2)

my_x_train = []
my_y_train = []
t = Tokenizer(num_words = max_words)
for year in [2017]:
    dates = []
    for month in range(1, 13):
        print(month)
        for day in range(1, 28):
            date = [day, month, year]
            my_x_train.append(cn.getKaggleTitles(date))
            dates.append(date)
    my_y_train.append(list(map(lambda x: map(lambda y: y[1]/10.0, x),
                      cn.getSentiment(dates, tickers))))
                        # Fetch sentiment vals and normalise"""

t.fit_on_texts([i for i in my_x_train])
my_x_train1 = [t.texts_to_sequences(i) for i in my_x_train]
my_x_train2 = [pad_sequences(i, max_title_len) for i in my_x_train1]
maxTitles = max(map(len, my_x_train2))

raise Exception()


print(len(x_traino), 'train sequences')
print(len(x_testo), 'test sequences')

num_classes = np.max(y_train) + 1
print(num_classes, 'classes')

print('Vectorizing sequence data...')
tokenizer = Tokenizer(num_words=max_words)
x_train = tokenizer.sequences_to_matrix(x_traino, mode='binary')
x_test = tokenizer.sequences_to_matrix(x_testo, mode='binary')
print('x_train shape:', x_train.shape)
print('x_test shape:', x_test.shape)

print('Convert class vector to binary class matrix '
      '(for use with categorical_crossentropy)')
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)
print('y_train shape:', y_train.shape)
print('y_test shape:', y_test.shape)

print('Building model...')
model = Sequential()
model.add(Dense(512, input_shape=(max_words,)))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_split=0.1)
score = model.evaluate(x_test, y_test,
                       batch_size=batch_size, verbose=1)
print('Test score:', score[0])
print('Test accuracy:', score[1])
