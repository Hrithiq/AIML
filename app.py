from flask import Flask, render_template, request
import nltk
import datetime
from nltk.stem. lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle

stemmer = LancasterStemmer()
seat_count = 50
    
with open("intents.json") as file:
    data = json.load(file)
with open("data.pickle", "rb") as f:
    words, labels, training, output = pickle.load(f)
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
        return np.array(bag)
    
tf.compact.v1.reset_default_graph()

net= tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)   
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")    
net = tflearn.regression(net)
model= tflearn.DNN(net)
model.load("model.tflearn")

app=Flask(__name__)

@app.route('/get')
def get_bot_response():
    global seat_count
    message =request.args.get('msg')
    if message:

        message=message.lower()

        results=model.predict([bag_of_words (message, words)])[0]

        result_index= np.argmax(results)

        tag=labels[result_index]

        if results[result_index]> 0.5: 
            if tag=="book_table":
                seat_count-=1
                response="Your table has been booked successfully. Remaining tables: "+str(seat_count)

            elif tag == "available_tables":
                response="There are " + str(seat_count)+"tables available at the moment"

            elif tag=="menu":
                day=datetime.datetime.now()
                day=day.strftime("A")
                if day == 0:
                    response = "Chef recommends: Steamed Tofu with Schezwan Peppercorn, Eggplant with Hot Garlic Sauce, Chicken & Chives, Schezwan Style, Diced Chicken with Dry Red Chilli, Schezwan Pepper"
                elif day == 1:
                    response = "Chef recommends: Asparagus Fresh Shitake & King Oyster Mushroom, Stir Fried Chilli Lotus Stem, Crispy Fried Chicken with Dry Red Pepper, Osmanthus Honey, Hunan Style Chicken"

                elif day == 2:
                    response = "Chef recommends: Baby Pokchoi Fresh Shitake Shimeji Straw & Button Mushroom, Mock Meat in Hot Sweet Bean Sauce, Diced Chicken with Bell Peppers & Onions in Hot Garlic Sauce, Chicken in Chilli Black Bean & Soy Sauce"

                elif day == 3:
                    response = "Chef recommends: Eggplant & Tofu with Chilli Oyster Sauce, Corn, Asparagus Shitake & Snow Peas in Hot Bean Sauce, Diced Chicken Plum Honey Chilli Sauce, Clay Pot Chicken with Dried Bean Curd Sheet"

                elif day == 4:
                    response = "Chef recommends: Kailan in Ginger Wine Sauce, Tofu with Fresh Shitake & Shimeji, Supreme Soy Sauce, Diced Chicken in Black Pepper Sauce, Sliced Chicken in Spicy Mala Sauce"

                elif day == 5:
                    response = "Chef recommends: Kung Pao Potato, Okra in Hot Bean Sauce, Chicken in Chilli Black Bean & Soy Sauce, Hunan Style Chicken"

                elif day == 6:
                    response = "Chef recommends: Stir Fried Bean Sprouts & Tofu with Chives, Vegetable Thou Sou, Diced Chicken Plum Honey Chilli Sauce, Diced Chicken in Black Pepper Sauce"
                                
 