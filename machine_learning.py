CLASSIFIER_TRESHOLD = 0.2
GENERATIVE_TRESHOLD = 0.6

with open("dialogues.txt") as f:
    data = f.read()
    
dialogues = []

for dialogue in data.split('\n\n'):
    
    replicas = []
    for replica in dialogue.split('\n')[:2]:
        replica = replica[2:].lower()
        replicas.append(replica)
        
    if len(replicas) == 2 and len(replicas[0]) > 1 and len(replicas[1]) > 0:
        dialogues.append(replicas)
        
GENERATIVE_DIALOGUES = dialogues[:5000]

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

X_text = []
y = []

for intent, value in BOT_CONFIG['intents'].items():
    for example in value['examples']:
        X_text.append(example)
        y.append(intent)
        
VECTORIZER = CountVectorizer()
X = VECTORIZER.fit_transform(X_text)

CLF = LogisticRegression()
CLF.fit(X, y)

LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                   intercept_scaling=1, l1_ratio=None, max_iter=100,
                   multi_class='auto', n_jobs=None, penalty='l2',
                   random_state=None, solver='lbfgs', tol=0.0001, verbose=0,
                   warm_start=False)

def get_intent(text):
    probas = CLF.predict_proba(VECTORIZER.transform([text]))
    max_proba = max(probas[0])
    if max_proba >= CLASSIFIER_TRESHOLD:
        index = list(probas[0]).index(max_proba)
        return CLF.classes_[index]

from nltk.metrics.distance import edit_distance

def get_answer_by_generative_model(text):
    text = text.lower()
    
    for question, answer in GENERATIVE_DIALOGUES:
        if abs(len(text) - len(question)) / len(question) < 1 - GENERATIVE_TRESHOLD:
            dist = edit_distance(text, question)
            l = len(question)
            similarity = 1 - dist / l
            if similarity > GENERATIVE_TRESHOLD:
                return answer

import random

def get_response_by_intent(intent):
    responses = BOT_CONFIG['intents'][intent]['responses']
    return random.choice(responses)

def get_failure_phrase():
    phrases = BOT_CONFIG['failure_phrases']
    return random.choice(phrases)

stats = {
    'requests': 0,
    'byscript': 0,
    'bygenerative': 0,
    'stub': 0
}

def generate_answer(text):
    stats['requests'] += 1
    
    # NLU
    intent = get_intent(text)
    
    # Make answer
    
    # by script
    if intent:
        stats['byscript'] += 1
        response = get_response_by_intent(intent)
        return response
    
    # use generative model
    answer = get_answer_by_generative_model(text)
    if answer:
        stats['bygenerative'] += 1
        return answer
    
    stats['stub'] += 1
    failure_phrase = get_failure_phrase()
    return failure_phrase

while True:
    text = input('Введите вопрос: ')
    answer = generate_answer(text)
    print(answer)
