#!/usr/bin/python

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from sklearn import linear_model
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve
from sklearn.model_selection import train_test_split

## loading data set 1
df = pd.read_csv("week4.csv",comment='#',header=None, nrows=1977)
X1_s1 = df.iloc[:,0]
X2_s1 = df.iloc[:,1]
X_s1 = np.column_stack((X1_s1, X2_s1))
y_s1 = df.iloc[:,2]
## 80/20 (train/test) split of data 
X_s1_train, X_s1_test, y_s1_train, y_s1_test = train_test_split(X_s1, y_s1, test_size=0.2)

## loading data set 2
df = pd.read_csv("week4.csv",comment='#',header=None, skiprows=1979)
X1_s2 = df.iloc[:,0]
X2_s2 = df.iloc[:,1]
X_s2 = np.column_stack((X1_s2, X2_s2))
y_s2 = df.iloc[:,2]
## 80/20 (train/test) split of data 
X_s2_train, X_s2_test, y_s2_train, y_s2_test = train_test_split(X_s2, y_s2, test_size=0.2)


## function to plot a given set of target values (training or predictions)
def plot_target_values(data_set, output_type, y_new, classifier, Q, C, KNN):
    ##
    ## assign data based on the specified set
    if data_set == 1:
        X1 = X_s1[:,0]
        X2 = X_s1[:,1]
    else:
        X1 = X_s2[:,0]
        X2 = X_s2[:,1]
    ##
    ## init temp arrays for splitting features for each target value
    a = []
    b = []
    c = []
    d = []
    ##
    ## iterate through the target values
    for i, val in enumerate(y_new):
        ##
        ## if target value is a +1
        if val == 1:
            ##
            ## append X1 and X2 feature value to temp arrays
            a.append(X1[i])
            b.append(X2[i])
        ##
        ## else if target value is a -1
        elif val == -1:
            ##
            ## append X1 and X2 feature value to temp arrays
            c.append(X1[i])
            d.append(X2[i])
        ##
    ##
    ## plot for specified data type
    if output_type == 'train':
        plt.title('Training Data')
        plt.scatter(a, b, s=30, color='red', marker='d', label='Training (+1)')
        plt.scatter(c, d, s=30, color='black', marker='x', label='Training (-1)')
    elif output_type == 'pred':
        plt.title(f'{classifier} Predictions (Q={Q}, C={C}, KNN={KNN})')
        plt.scatter(a, b, s=5, color='blue', marker='o', label='Predictions (+1)')
        plt.scatter(c, d, s=30, color='green', marker='+', label='Predictions (-1)')
    elif output_type == 'dummy_freq':
        plt.title(f'Baseline Classifier (Most Frequent)')
        plt.scatter(a, b, s=5, color='blue', marker='o', label='Predictions (+1)')
        plt.scatter(c, d, s=30, color='green', marker='+', label='Predictions (-1)')
    else:
        plt.title(f'Baseline Classifier (Random)')
        plt.scatter(a, b, s=5, color='blue', marker='o', label='Predictions (+1)')
        plt.scatter(c, d, s=30, color='green', marker='+', label='Predictions (-1)')
    ##
    ## set labels
    plt.xlabel('X_1')
    plt.ylabel('X_2')
    plt.legend(loc=2)


## function to get predictions for a model and plot them
def get_predictions_and_plot(fig, data_set, classifier, Q, C, KNN):
    ##
    ## assign data base specified set
    print(f'Data Set {data_set}')
    if data_set == 1:
        X = X_s1
        X_train = X_s1_train
        y_train = y_s1_train
        y = y_s1
        X_test = X_s1_test
        y_test = y_s1_test
    else:
        X = X_s2
        X_train = X_s2_train
        y_train = y_s2_train
        y = y_s2
        X_test = X_s2_test
        y_test = y_s2_test
    ##
    ## obtain specified degree of polynomial features for training, testing, plotting
    X_train_poly = PolynomialFeatures(Q).fit_transform(X_train)
    X_test_poly = PolynomialFeatures(Q).fit_transform(X_test)
    X_poly = PolynomialFeatures(Q).fit_transform(X)
    ##
    plt.figure(fig)
    ##
    ## if using logistic regression
    if classifier == 'logreg':
        ##
        ## train logreg classifier with given hyperparams
        model = LogisticRegression(C=C, penalty='l1', solver='saga', max_iter=90000).fit(X_train_poly, y_train)
        ##
        ## obtain values for false positive rates and ture positive rates
        fpr, tpr, _ = roc_curve(y_test, model.predict_proba(X_test_poly)[:,1])
        ##
        ## get classifier predictions on test data
        y_test_pred = model.predict(X_test_poly)
        ##
        ## get classifier predictions on all-data
        y_pred = model.predict(X_poly)
        ##
        ## plot all-data predictions against original dataset
        plot_target_values(data_set, 'train', y, 'N/A', 'N/A', 'N/A', 'N/A')
        plot_target_values(data_set, 'pred', y_pred, 'Logistic Regression', Q, C, KNN)
        print(f'Logistic Regression (Q={Q}, C={C})')
        ##
    ##
    ## else using k nearest neighbours
    else:
        ##
        ## generate knn classifier with given hyperparams
        model = KNeighborsClassifier(n_neighbors=KNN, weights='uniform').fit(X_train_poly, y_train)
        ##
        ## obtain values for false positive rates and ture positive rates
        fpr, tpr, _ = roc_curve(y_test, model.predict_proba(X_test_poly)[:,1])
        ##
        ## get classifier predictions on test data
        y_test_pred = model.predict(X_test_poly)
        ##
        ## get classifier predictions on all-data
        y_pred = model.predict(X_poly)
        ##
        ## plot all-data predictions against original dataset
        plot_target_values(data_set, 'train', y, 'N/A', 'N/A', 'N/A', 'N/A')
        plot_target_values(data_set, 'pred', y_pred, 'K-Nearest-Neighbours', Q, C, KNN)
        print(f'K-Nearest-Neighbours (Q={Q}, KNN={KNN})')
        ##
    ##
    ## print the classifier prediction error and confusion matrix
    print(f'Prediction MSE = {mean_squared_error(y_test, y_test_pred)}')
    print('Confusion Matrix:\n', confusion_matrix(y_test, y_test_pred), '\n')
    ##
    return (fpr, tpr)


## function to get predictions for a model and plot them
def get_baseline_and_plot(fig, data_set, dummy_type):
    ##
    ## assign data base specified set
    print(f'Data Set {data_set}')
    if data_set == 1:
        X = X_s1
        X_train = X_s1_train
        y_train = y_s1_train
        y = y_s1
        X_test = X_s1_test
        y_test = y_s1_test
    else:
        X = X_s2
        X_train = X_s2_train
        y_train = y_s2_train
        y = y_s2
        X_test = X_s2_test
        y_test = y_s2_test
    ##
    plt.figure(fig)
    ##
    ## if getting baseline classifier that gets most frequent
    if dummy_type == 'frequent':
        ##
        ## train dummy classifier on training data
        dummy = DummyClassifier(strategy='most_frequent').fit(X_train, y_train)
        ##
        ## obtain values for false positive rates and ture positive rates
        fpr, tpr, _ = roc_curve(y_test, dummy.predict_proba(X_test)[:,1])
        ##
        ## get baseline target values on test data
        y_test_dummy = dummy.predict(X_test)
        ##
        ## get baseline target values on all-data
        y_dummy = dummy.predict(X)
        ##
        ## plot baseline predictions against original dataset
        plot_target_values(data_set, 'train', y, 'N/A', 'N/A', 'N/A', 'N/A')
        plot_target_values(data_set, 'dummy_freq', y_dummy, 'N/A', 'N/A', 'N/A', 'N/A')
        ##
        ## print the classifier prediction error
        print(f'Most Frequent Baseline MSE = {mean_squared_error(y_test, y_test_dummy)}')
    ##
    ## else get baseline classifier that gets random values
    else:
        ##
        ## train dummy classifier on training data
        dummy = DummyClassifier(strategy='uniform').fit(X_train, y_train)
        ##
        ## obtain values for false positive rates and ture positive rates
        fpr, tpr, _ = roc_curve(y_test, dummy.predict_proba(X_test)[:,1])
        ##
        ## get baseline target values on test data
        y_test_dummy = dummy.predict(X_test)
        ##
        ## get baseline target values on all-data
        y_dummy = dummy.predict(X)
        ##
        ## plot baseline predictions against original dataset
        plot_target_values(data_set, 'train', y, 'N/A', 'N/A', 'N/A', 'N/A')
        plot_target_values(data_set, 'dummy_rand', y_dummy, 'N/A', 'N/A', 'N/A', 'N/A')
        ##
        ## print the classifier prediction error
        print(f'Random Baseline MSE = {mean_squared_error(y_test, y_test_dummy)}')
    ##
    ## print confusion matrix
    print('Confusion Matrix:\n', confusion_matrix(y_test, y_test_dummy), '\n')
    ##
    return (fpr, tpr)


## function to run cross validation process
def cross_val_model(data_set, classifier, folds, Q, C, KNN):
    ##
    ## assign data based on specified set
    if data_set == 1:
        X = X_s1
        y = y_s1
    else:
        X = X_s2
        y = y_s2
    ##
    ## generate specifed degree of polynomial features for training
    X_poly = PolynomialFeatures(Q).fit_transform(X)
    ##
    ## init mean-squared-error array
    mse=[]
    ##
    ## make k-fold obj
    kf = KFold(n_splits=folds)
    ##
    ## loop through each k-fold split
    for train, test in kf.split(X_poly):
        ##
        ## if using logistic regression
        if classifier == 'logreg':
            ##
            ## generate model with specified hyperparams
            model = LogisticRegression(C=C, penalty='l1', solver='saga', max_iter=90000).fit(X_poly[train], y[train])
        ##
        ## else using k nearest neighbours
        else:
            ##
            ## generate model with specified hyperparams
            model = KNeighborsClassifier(n_neighbors=KNN, weights='uniform').fit(X_poly[train], y[train])
        ##
        ## get pridictions using test part of split
        y_pred = model.predict(X_poly[test])
        ##
        ## get error for predictions and append to error list
        mse.append(mean_squared_error(y[test], y_pred))
    ##
    ## return mean, varience and standard dev error values
    return [np.mean(mse), np.var(mse), np.std(mse)]
    ##
    # print(f'k-fold cross-validation (folds {folds})')
    # print(f'Mean MSE - {np.mean(mse)}')
    # print(f'Var MSE - {np.var(mse)}')
    # print(f'Std MSE - {np.std(mse)}\n')


## function to plot mse vs number of kfolds
def plot_error_vs_folds(fold_range, x_axis_vals, fig, data_set, classifier, Q, C, KNN):
    ##
    ## init mean, var and std arrays
    mean_mse = []
    var_mse = []
    std_mse = []
    ##
    ## for each k-fold value
    for folds in fold_range:
        ##
        ## run cross validation for for specified classifier
        cross_val_results = cross_val_model(data_set, classifier, folds, Q, C, KNN)
        ##
        ## append append mean, var and std error values to arrays
        mean_mse.append(cross_val_results[0])
        var_mse.append(cross_val_results[1])
        std_mse.append(cross_val_results[2])
    ##
    ## add results to errorbar plot
    plt.figure(fig)
    plt.errorbar(x_axis_vals, mean_mse, yerr=var_mse, capsize=5, ecolor='red', label='Mean prediction error with varience')
    plt.title(f'Prediction Error vs Number of K-folds (Q = {Q}, C = {C}, KNN = {KNN})')
    plt.xlabel('Number of K-folds')
    plt.ylabel('Mean Prediction Error')
    plt.legend()


## function to plot mse vs polynomial degree (Q)
def plot_error_vs_Q(q_range, x_axis_vals, fig, data_set, classifier, folds, C, KNN):
    ##
    ## init mean, var and std arrays
    mean_mse = []
    var_mse = []
    std_mse = []
    ##
    ## for each Q value
    for Q in q_range:
        ##
        ## run cross validation for specified classifier
        cross_val_results = cross_val_model(data_set, classifier, folds, Q, C, KNN)
        ##
        ## append append mean, var and std error values to arrays
        mean_mse.append(cross_val_results[0])
        var_mse.append(cross_val_results[1])
        std_mse.append(cross_val_results[2])
    ##
    ## add results to errorbar plot
    plt.figure(fig)
    plt.errorbar(x_axis_vals, mean_mse, yerr=var_mse, capsize=5, ecolor='red', label='Mean prediction error with varience')
    plt.title(f'Prediction Error vs Polynomial Degree (Q) (K-folds = {folds}, C = {C}, KNN = {KNN})')
    plt.xlabel('Polynomial Degree (Q)')
    plt.ylabel('Mean Prediction Error')
    plt.legend()


## function to plot mse vs KNN neighbours
def plot_error_vs_KNN(knn_range, x_axis_vals, fig, data_set, classifier, folds, Q, C):
    ##
    ## init mean, var and std lists
    mean_mse = []
    var_mse = []
    std_mse = []
    ##
    ## for each KNN value
    for KNN in knn_range:
        ##
        ## run cross validation for specified classifier
        cross_val_results = cross_val_model(data_set, classifier, folds, Q, C, KNN)
        ##
        ## append append mean, var and std error values to arrays
        mean_mse.append(cross_val_results[0])
        var_mse.append(cross_val_results[1])
        std_mse.append(cross_val_results[2])
    ##
    ## add results to errorbar plot
    plt.figure(fig)
    plt.errorbar(x_axis_vals, mean_mse, yerr=var_mse, capsize=5, ecolor='red', label='Mean prediction error with varience')
    plt.title(f'Prediction Error vs K-Nearest-Neighbours (KNN) (K-folds = {folds}, Q = {Q})')
    plt.xlabel('Number of K-Nearest-Neighbours (KNN)')
    plt.ylabel('Mean Prediction Error')
    plt.legend()


## function to plot mse vs penalty (C)
def plot_error_vs_C(c_range, x_axis_vals, fig, data_set, classifier, folds, Q, KNN):
    ##
    ## init mean, var and std lists
    mean_mse = []
    var_mse = []
    std_mse = []
    ##
    ## for each C value
    for C in c_range:
        ##
        ## run cross validation for specified classifier
        cross_val_results = cross_val_model(data_set, classifier, folds, Q, C, KNN)
        ##
        ## append append mean, var and std error values to arrays
        mean_mse.append(cross_val_results[0])
        var_mse.append(cross_val_results[1])
        std_mse.append(cross_val_results[2])
    ##
    ## add results to errorbar plot
    plt.figure(fig)
    plt.errorbar(x_axis_vals, mean_mse, yerr=var_mse, capsize=5, ecolor='red', label='Mean prediction error with varience')
    plt.title(f'Prediction Error vs Regularisation Penalty Value (C) (K-folds = {folds}, Q = {Q})')
    plt.xlabel('Penalty Value (C)')
    plt.ylabel('Mean Prediction Error')
    plt.legend()



## ML workflow for Dataset1
##
## plotting scatter of training data
plt.figure(1)
plot_target_values(1, 'train', y_s1, 'N/A', 'N/A', 'N/A', 'N/A')
##
## Logistic Regression predictions before cross validation to tune hyperparams
get_predictions_and_plot(fig=2, data_set=1, classifier='logreg', Q=1, C=1, KNN='N/A')
##
## plot the prediction error vs number of kfolds
fold_range = [2, 5, 10, 25, 50, 100]
x_axis_vals = ['2', '5', '10', '25', '50', '100']
plot_error_vs_folds(fold_range, x_axis_vals, fig=3, data_set=1, classifier='logreg', Q=1, C=1, KNN='N/A')
##
## plot the prediction error vs polynomial degree (Q)
q_range = [1, 2, 3, 4, 5, 6, 7, 8]
x_axis_vals = ['1', '2', '3', '4', '5', '6', '7', '8']
plot_error_vs_Q(q_range, x_axis_vals, fig=4, data_set=1, classifier='logreg', folds=2, C=1, KNN='N/A')
##
## plot the prediction error vs penalty value (C)
c_range = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
x_axis_vals = ['0.001', '0.01', '0.1', '1', '10', '100', '1000']
plot_error_vs_C(c_range, x_axis_vals, fig=5, data_set=1, classifier='logreg', folds=2, Q=5, KNN='N/A')
##
## plot the predictions with tuned hyperparams
(fpr, tpr) = get_predictions_and_plot(fig=6, data_set=1, classifier='logreg', Q=2, C=1, KNN='N/A')
##
## plot the ROC curve for Logistic Regression
plt.figure(14)
plt.plot(fpr, tpr, label='LogReg')
##
##
## KNN predictions before cross validation to tune hyperparams
get_predictions_and_plot(fig=7, data_set=1, classifier='knn', Q=1, C='N/A', KNN=3)
##
## plot the prediction error vs number of kfolds 
fold_range = [2, 5, 10, 25, 50, 100]
x_axis_vals = ['2', '5', '10', '25', '50', '100']
plot_error_vs_folds(fold_range, x_axis_vals, fig=8, data_set=1, classifier='knn', Q=1, C='N/A', KNN=3)
##
## plot the prediction error vs polynomial degree (Q)
q_range = [1, 2, 3, 4, 5, 6, 7, 8]
x_axis_vals = ['1', '2', '3', '4', '5', '6', '7', '8']
plot_error_vs_Q(q_range, x_axis_vals, fig=9, data_set=1, classifier='knn', folds=5, C='N/A', KNN=3)
##
## plot the prediction error vs KNN neighbours (KNN)
knn_range = [2, 5, 10, 20, 35, 50, 75, 100, 200]
x_axis_vals = ['2', '5', '10', '20', '35', '50', '75', '100', '200']
plot_error_vs_KNN(knn_range, x_axis_vals, fig=10, data_set=1, classifier='knn', folds=5, Q=6, C='N/A')
##
## plot the predictions with tuned hyperparams
(fpr, tpr) = get_predictions_and_plot(fig=11, data_set=1, classifier='knn', Q=6, C='N/A', KNN=75)
##
## plot the ROC curve for the KNN
plt.figure(14)
plt.plot(fpr, tpr, label='KNN')
##
## create a random and most freq baseline model and plot predictions
(fpr, tpr) = get_baseline_and_plot(fig=12, data_set=1, dummy_type='frequent')
##
## plot the ROC curve for the most freq baseline classifier
plt.figure(14)
plt.plot(fpr, tpr, label='Baseline (most freq)')
##
## create a random and most freq baseline model and plot predictions
(fpr, tpr) = get_baseline_and_plot(fig=13, data_set=1, dummy_type='random')
##
## plot the ROC curve for the random baseline classifier
plt.figure(14)
plt.plot(fpr, tpr, label='Baseline (random)')
plt.plot([0, 1], [0, 1], color='green', linestyle='--', label='45 degree')
plt.title('ROC Curves for each model on Dataset_1')
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.legend()



## ML workflow for Dataset2
##
## plotting scatter of training data
plt.figure(15)
plot_target_values(2, 'train', y_s2, 'N/A', 'N/A', 'N/A', 'N/A')
##
## Logistic Regression predictions before cross validation to tune hyperparams
get_predictions_and_plot(fig=16, data_set=2, classifier='logreg', Q=1, C=1, KNN='N/A')
##
## plot the prediction error vs number of kfolds
fold_range = [2, 5, 10, 25, 50, 100, 200]
x_axis_vals = ['2', '5', '10', '25', '50', '100', '200']
plot_error_vs_folds(fold_range, x_axis_vals, fig=17, data_set=2, classifier='logreg', Q=1, C=1, KNN='N/A')
##
## plot the prediction error vs polynomial degree (Q)
q_range = [1, 2, 3, 4, 5]
x_axis_vals = ['1', '2', '3', '4', '5']
plot_error_vs_Q(q_range, x_axis_vals, fig=18, data_set=2, classifier='logreg', folds=10, C=1, KNN='N/A')
##
## plot the prediction error vs penalty value (C)
c_range = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
x_axis_vals = ['0.001', '0.01', '0.1', '1', '10', '100', '1000']
plot_error_vs_C(c_range, x_axis_vals, fig=19, data_set=2, classifier='logreg', folds=10, Q=2, KNN='N/A')
##
## plot the predictions with tuned hyperparams
(fpr, tpr) = get_predictions_and_plot(fig=20, data_set=2, classifier='logreg', Q=2, C=1, KNN='N/A')
##
## plot the ROC curve for Logistic Regression
plt.figure(28)
plt.plot(fpr, tpr, label='LogReg')
##
##
## KNN predictions before cross validation to tune hyperparams
get_predictions_and_plot(fig=21, data_set=2, classifier='knn', Q=1, C='N/A', KNN=1)
##
## plot the prediction error vs number of kfolds 
fold_range = [2, 5, 10, 25, 50, 100]
x_axis_vals = ['2', '5', '10', '25', '50', '100']
plot_error_vs_folds(fold_range, x_axis_vals, fig=22, data_set=2, classifier='knn', Q=1, C='N/A', KNN=3)
##
## plot the prediction error vs polynomial degree (Q)
q_range = [1, 2, 3, 4, 5]
x_axis_vals = ['1', '2', '3', '4', '5']
plot_error_vs_Q(q_range, x_axis_vals, fig=23, data_set=2, classifier='knn', folds=2, C='N/A', KNN=3)
##
## plot the prediction error vs KNN neighbours (KNN)
knn_range = [2, 5, 10, 20, 35, 50, 75, 100]
x_axis_vals = ['2', '5', '10', '20', '35', '50', '75', '100']
plot_error_vs_KNN(knn_range, x_axis_vals, fig=24, data_set=2, classifier='knn', folds=2, Q=1, C='N/A')
##
## plot the predictions with tuned hyperparams
(fpr, tpr) = get_predictions_and_plot(fig=25, data_set=2, classifier='knn', Q=2, C='N/A', KNN=20)
##
## plot the ROC curve for the KNN
plt.figure(28)
plt.plot(fpr, tpr, label='KNN')
#
## create a random and most freq baseline model and plot predictions
(fpr, tpr) = get_baseline_and_plot(fig=26, data_set=2, dummy_type='frequent')
##
## plot the ROC curve for the most freq baseline classifier
plt.figure(28)
plt.plot(fpr, tpr, label='Baseline (most freq)')
##
## create a random and most freq baseline model and plot predictions
(fpr, tpr) = get_baseline_and_plot(fig=27, data_set=2, dummy_type='random')
##
## plot the ROC curve for the random baseline classifier
plt.figure(28)
plt.plot(fpr, tpr, label='Baseline (random)')
plt.plot([0, 1], [0, 1], color='green', linestyle='--', label='45 degree')
plt.title('ROC Curves for each model on Dataset_1')
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.legend()


## display plots
plt.show()