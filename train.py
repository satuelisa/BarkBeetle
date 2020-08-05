# basado en https://gogul09.github.io/software/image-classification-python
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler

from sklearn.model_selection import train_test_split, cross_val_score

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold, StratifiedKFold

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

from collections import defaultdict
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import mahotas
import cv2
import os

from sys import argv

fixed_size = tuple((76, 76)) # sample dimension

def metrics(model, testData, testLabels): # debug method
    correct = 0
    predict = []
    for (data, label) in zip(testData, testLabels):
        assigned = model.predict(data.reshape(1,-1))[0]
        print(label, assigned)
        predict.append(assigned)
        if label == assigned:
            correct += 1
    print('#', 100 * correct / len(testLabels), '% correct')
    print(confusion_matrix(testLabels, predict))
    print(classification_report(testLabels, predict))

def evaluate(postfix, model, testData, testLabels):
    for (data, label) in zip(testData, testLabels):
        assigned = model.predict(data.reshape(1,-1))[0]
        print('output', label, assigned, postfix)

def fd_hu_moments(image): # Hu moments
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    feature = cv2.HuMoments(cv2.moments(image)).flatten()
    return feature

def fd_haralick(image): # Haralick texture
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    haralick = mahotas.features.haralick(gray).mean(axis=0)
    return haralick

def fd_histogram(image, bins = 10): # a binned color histogram 
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist  = cv2.calcHist([image], [0, 1, 2], None, [bins, bins, bins], [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    return hist.flatten()

targets = ['green', 'yellow', 'red', 'leafless']
kinds = ['squares', 'original', 'enhanced', 'thresholded', 'automaton']
results = []
models = None
flight = '' if 'all' in argv else argv[1]

for kind in kinds:
    labels = []
    features = []
    for label in targets:
        listing = list(os.scandir(f'individual/{kind}/{label}'))
        for entry in listing:
            if entry.path.endswith('.png') and entry.is_file() and flight in entry.path:
                filename = entry.path
                image = cv2.imread(filename)
                image = cv2.resize(image, fixed_size)
                fv_hu_moments = fd_hu_moments(image)
                fv_haralick = fd_haralick(image)
                fv_histogram  = fd_histogram(image)
                global_feature = np.hstack([fv_histogram, fv_haralick, fv_hu_moments])
                labels.append(label)
                features.append(global_feature)
    print(len(features))
    scaler = MinMaxScaler(feature_range = (0, 1))
    rescaled_features = scaler.fit_transform(features) 
    (trainData, testData, trainLabels, testLabels) = train_test_split(np.array(rescaled_features),
                                                                      np.array(labels),
                                                                      test_size = 0.3) # 30 % for testing
    models = [('Linear Discriminant Analysis', LinearDiscriminantAnalysis()),
              ('K Nearest Neighbors', KNeighborsClassifier()),
              ('Decision Tree', DecisionTreeClassifier()),
              ('Random Forest', RandomForestClassifier(10)),
              ('Gaussian Naive Bayes', GaussianNB()),
              ('Support Vector Machine', SVC())]

    for (modelLabel, model) in models:
        if flight != '': # specific case study
            model.fit(trainData, trainLabels) 
            evaluate(' '.join([flight, kind, modelLabel]), model, testData, testLabels)
        else: # comparative study with 70 % of the data
            kfold = KFold(n_splits = 10) # cross-validation
            for score in cross_val_score(model, trainData, trainLabels, cv = kfold, scoring = 'accuracy'):
                results.append([kind, modelLabel, score])

if flight == '': # the comparative study
    detmet = float(argv[2])
    evaluation = pd.DataFrame(results, columns = ['kind', 'model', 'accuracy'])        
    fig, axs = plt.subplots(len(models), 1, figsize = (8, 13))
    avg = np.mean(evaluation.accuracy)
    print(avg) 
    pos = 0
    for model in [m[0] for m in models]:
        ax = axs[pos]
        ax.violinplot(dataset = [evaluation[evaluation.kind == 'squares']["accuracy"].values,
                                 evaluation[evaluation.kind == 'original']["accuracy"].values,
                                 evaluation[evaluation.kind == 'enhanced']["accuracy"].values,
                                 evaluation[evaluation.kind == 'thresholded']["accuracy"].values,
                                 evaluation[evaluation.kind == 'automaton']["accuracy"].values],
                      showmeans = True)
        ax.set_title(model)
        ax.axhline(y = avg, c ="red", linewidth = 2, zorder = 0) # average
        ax.axhline(y = detmet, c ="black", linewidth = 2, zorder = 0) # deterministic method
        if pos == len(models) - 1: # show ticks on the bottom only
            ax.set_xticklabels([''] + kinds, rotation = 0)
        pos += 1
    plt.setp([a.get_xticklabels() for a in axs[:-1]], visible=False)
    plt.tight_layout()
    plt.savefig(f'ml.png')


