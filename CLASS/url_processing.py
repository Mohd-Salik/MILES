#Libraries used for data_extraction.py
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score

class Url_processing(object):
    
    def __init__(self):
        super().__init__()
        self.urlData = pd.read_sql_query("SELECT * FROM Url", sqlite3.connect("C:/Users/3400g/Documents/MILES/CLASS/milesDB.db"))
        self.connection = sqlite3.connect("C:/Users/3400g/Documents/MILES/CLASS/milesDB.db")
        self.phishing = self.connection.execute("SELECT URLs FROM URL WHERE URL.Condition='0'").fetchall()
        self.safe = self.connection.execute("SELECT URLs FROM URL WHERE URL.Condition='1'").fetchall()
        self.URL = self.connection.execute("SELECT URLs FROM Url").fetchall()
        self.vector = TfidfVectorizer()

    # Function that trains the data model
    def train(self):
        y = self.urlData["Condition"] 
        urlList = self.urlData["URLs"] 
        x = self.vector.fit_transform(urlList)

        xtrain, xTest, ytrain, yTest = train_test_split(x, y, test_size=0.2, random_state=42)
        return xtrain, xTest, ytrain, yTest

    # Predicting url through logistic regression
    def prediction(self, urlInput):
        xtrain, xTest, ytrain, yTest = self.train()
        regression = LogisticRegression()
        regression.fit(xtrain, ytrain)
        
        # Processing dependent variable 
        url = urlInput.strip().split()
        urlTok = self.vector.transform(url)

        # Comparing dependent variable to our independent data set
        value = regression.predict(urlTok)
        print("PROCESSING: Prediction value\n", value)
        return value

    # Returning the accuracy rate of the data model
    def accuracy(self):
        xtrain, xTest, ytrain, yTest = self.train()
        regression = LogisticRegression()
        regression.fit(xtrain, ytrain)
        accuracy = regression.score(xTest, yTest)
        print("Accuracy: ", accuracy)
        return accuracy

    # Display ROC curve of the data model
    def rocCurve(self):
        xtrain, xTest, ytrain, yTest = self.train()
        regression = LogisticRegression()
        regression.fit(xtrain, ytrain)
        logit_roc_auc = roc_auc_score(yTest, regression.predict(xTest))
        fpr, tpr, thresholds = roc_curve(yTest, regression.predict_proba(xTest)[:,1])
        plt.figure()
        plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
        plt.plot([0, 1], [0, 1],'r--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic')
        plt.legend(loc="lower right")
        plt.savefig('Log_ROC')
        plt.show()
        
    # Display bar graph of the data model
    def graph(self):
        status = ['Phishing Links', 'Safe Links']
        quantity = [len(self.phishing), len(self.safe)]
        ypos = np.arange(len(status))
        plt.title('PHISHING DATA SET VISUALIZATION')
        plt.xlabel('Status')
        plt.ylabel('Quantity')
        plt.bar(ypos, quantity, color=('Red', 'Green'))
        plt.xticks(ypos, status)
        plt.show()

object1 = Url_processing()
# # links = ["https://lnpost-pl.id-226109.site/index.html", 
# #     "www.seaborn.org", 
# #     "www.google.com", 
# #     "https://ngere.rw/wp-content/themes/yensiocjqi/pl.php/", 
# #     "www.msteams.com"]
# # for link in links:
# #     print(link)
# #     object1.prediction(link)
object1.accuracy()
# object1.rocCurve()
# object1.graph()