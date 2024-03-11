import random
import json
import pickle
import numpy as np
import nltk

from nltk.stem import WordNetLemmatizer
from keras.models import load_model
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('D:/PychrmProjects/chat_with_qa/app/utils/intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.keras')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    CONFIDENCE_THRESHOLD = 0.5
    results = [[i, r] for i, r in enumerate(res) if r > CONFIDENCE_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result, tag

print("GO! Bot is running!")

def user_msg(msg):
    message = msg
    ints = predict_class(message)
    if not ints:
        return "I'm still learning! Soon I will able to give answer related to this question", None
    else:
        response, tag = get_response(ints, intents)
        return response, tag
