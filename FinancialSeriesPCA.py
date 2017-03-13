# -*- coding: utf-8 -*-
"""
Allows the user to perform an iterated PCA routine. Aimed at 1d time series data. 
@author: BVasudevan
"""
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

class FinancialSeriesPCA(): 
    
    df = pd.ExcelFile('GSWISS.xlsx')
    data=df.parse(0)
    data.index=data['Date']
    data.drop('Date',axis=1,inplace = True)
     
    for i in range(1,5):
       sheet_data=df.parse(i)
       sheet_data.index=sheet_data['Date']
       sheet_data.drop('Date', axis = 1, inplace = True)
       data = pd.concat([data, sheet_data],axis=1,join='outer')

    data=data.dropna()
    date_index=data.index
    global tenors
    tenors = data.columns.values
    data=np.array(data)
       
    def pca_routine(X):
        """Assign and define PCA"""
        
        pca=PCA(n_components=4)
        X_pca = pca.fit(X)
        percentageExplainedRatio_X= X_pca.explained_variance_ratio_
        eigenVectorsCovariance_X = X_pca.components_
        eigenVectorsCovariance_X = np.matrix(eigenVectorsCovariance_X)
        eigenVectorsCovariance_X = eigenVectorsCovariance_X.T
        return eigenVectorsCovariance_X, percentageExplainedRatio_X

    def p_PCA(n,X): #n= size of partitions,X = data
        """To partition the samples & eigenvector matrices"""
        loadings = []
        scores = []
        y=X.shape[0]
        x=0
        while x<y:
            data_amend = X[x:x+n]
            loadings.append(FinancialSeriesPCA.pca_routine(data_amend)[0])
            scores.append(FinancialSeriesPCA.pca_routine(data_amend)[1])
            x = x+n
        
        return loadings, scores
        
        
    def isolate_component_series(X):
        """Generates 10 series of zero coupon rates by tenor."""
        c_1,c_2,c_3,c_4,c_5,c_6,c_7,c_8,c_9,c_10 = ([] for i in range(10))
        component_series = [c_1,c_2,c_3,c_4,c_5,c_6,c_7,c_8,c_9,c_10]
        
        for i in range(0,len(X)-1):
            for j in range(0,4):
                component_series[j].append(X[i][j,0])
        
        global comp_series
        comp_series = []
        for i in range(0,len(component_series)-1):
            comp_series.append(pd.DataFrame(component_series[i]))
        return component_series
            
    def main(n):
        loadings = FinancialSeriesPCA.p_PCA(n,FinancialSeriesPCA.data)[0]
        scores = FinancialSeriesPCA.p_PCA(n,FinancialSeriesPCA.data)[1]
        return loadings, scores 
        
        
        
        
        