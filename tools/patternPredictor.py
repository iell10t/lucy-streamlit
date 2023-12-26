import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import FinanceDataReader as fdr

class PatternPredictor():
    def __init__(self):
        self.datesToPredict = 10
    
    def getStockData(self, symbol: str):
        self.data = fdr.DataReader(symbol)
        self.close = self.data['Close']
        return self.data
    
    def searchPattern(self, start_date, end_date, threshold=0.95):
        base = self.close[start_date:end_date]
        self.base_norm = (base - base.min()) / (base.max() - base.min())
        self.base = base

        window_size = len(base)
        moving_cnt = len(self.data) - window_size - self.datesToPredict + 1
        cosSimList = self.__cosineSimList(moving_cnt, window_size)
        
        self.window_size = window_size
        cosSimList = cosSimList[cosSimList > threshold]
        return cosSimList
    
    def __cosineSimList(self, moving_cnt, window_size):
        def cosineSimilarity(x, y):
            return np.dot(x, y) / (np.sqrt(np.dot(x, x)) * np.sqrt(np.dot(y, y)))
        
        simList = []

        for i in range(moving_cnt):
            target = self.close[i:i+window_size]
            target_norm = (target - target.min()) / (target.max() - target.min())
            cos_similarity = cosineSimilarity(self.base_norm, target_norm)
            simList.append(cos_similarity)

        return pd.Series(simList).sort_values(ascending=False)

    def plotPattern(self, idx, datesToPredict):
        pattern = self.close[idx:idx+self.window_size+datesToPredict]
        pattern_norm = (pattern - pattern.min()) / (pattern.max() - pattern.min())
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.plot(self.base_norm.values, label='Stock Price', color='black',  alpha=0.5)
        axis.plot(pattern_norm.values[:len(self.base_norm.values)], label='Similar Pattern', color='red', linestyle='solid')
        axis.plot(pattern_norm.values, label='Price Prediction', color='red', linestyle='dashed')
        axis.axvline(x=len(self.base_norm)-1, c='tomato', linestyle='dotted')
        axis.axvspan(len(self.base_norm.values)-1, len(pattern_norm.values)-1, facecolor='yellow', alpha=0.3)
        axis.legend()
        axis.get_yaxis().set_visible(False)
        axis.get_xaxis().set_visible(False)
        
        return fig
    