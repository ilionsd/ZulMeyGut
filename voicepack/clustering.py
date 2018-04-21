# -*- coding: utf-8 -*-

import numpy as np
from sklearn import mixture 
from sklearn import cluster 

def components_number(X, Nfft, samplerate) :
    min_speech_time = 0.1
    min_samples = np.ceil( samplerate * min_speech_time / Nfft).astype(np.int)
    model = cluster.DBSCAN(min_samples=min_samples)
    model.fit(X)
    n_components = len(model.core_sample_indices_)
    return n_components

def gaussian(X, n_components, covariance_type='full') :
    model = mixture.GaussianMixture(n_components=n_components, 
                                    covariance_type=covariance_type)
    model.fit(X)
    return model
    
def bayesian_gaussian(X, n_components_limit, covariance_type='full') :
    model = mixture.BayesianGaussianMixture(n_components=n_components_limit, 
                                            covariance_type=covariance_type)
    model.fit(X)
    return model

def mixture_selection(X, n_components_list, covariance_type_list=['spherical', 'tied', 'diag', 'full'], mixture_type='GM') :
    
    n_components_list = np.asarray(n_components_list)
    covariance_type_list = np.asanyarray(covariance_type_list)
    
    best_bic = np.infty
    best_model = None
    
    for cv_type in covariance_type_list :
        for n_components in n_components_list :
            model = mixture.GaussianMixture(n_components=n_components, covariance_type=cv_type)
            model.fit(X)
            model_bic = model.bic(X)
            if model_bic < best_bic :
                best_bic, best_model = model_bic, model
                
    return best_model

def k_means(X, n_clusters) :
    model = cluster.MiniBatchKMeans(n_clusters=n_clusters)
    model.fit(X)
    return model.cluster_centers_

def mean_shift(X) :
    model = cluster.MeanShift(cluster_all=False)
    model.fit(X)
    return model.cluster_centers_
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    