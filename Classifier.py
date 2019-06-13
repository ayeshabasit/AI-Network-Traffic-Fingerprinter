import os
import extractFeatures
import numpy as np
from  sklearn.ensemble import RandomForestClassifier
from  sklearn import svm
from optparse import OptionParser
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support as results
from sklearn.metrics import accuracy_score

def getFeaturesAndLabels(rootdir, samplingRate):

    x = []
    y = []
    totalFileCount = 0
    count = 0
    for fileData in os.walk(rootdir):
        if count > 0:
            files = os.listdir(fileData[0])
            fileCount = len(files)
            totalFileCount += fileCount
            for file in files:
                tmps = file.lower()
                y += [''.join(i for i in tmps if ((not i.isdigit()) and i != " " and i != "." and i != "-" and i != ":"))] # Getting labels, removing digits, dots, and lowercase-ing
                filepath = os.path.join(fileData[0],file)
                x += [extractFeaturesArray.main(filepath, samplingRate)]
        count+=1


    Xtemp = np.full((totalFileCount,3,samplingRate,16), -1) # make a final feature vector of dimensions [Number of files x 3 x samples x 16]
    X = np.full((totalFileCount, 3*samplingRate*16), -1)


    Y = np.chararray((totalFileCount), itemsize = 40)
    Y[:] = '000000000000000000000000000000000000000000000000000000000000'


    for a in range(totalFileCount): # Copying from small x to big X because x is a list and X is an array
        Y[a] = y[a]
        for b in range(len(x[a][1])):
            Xtemp[a][0][b] = x[a][0][b]
            Xtemp[a][1][b] = x[a][1][b]
            Xtemp[a][2][b] = x[a][2][b]


    for a in range(totalFileCount):
        temp = np.hstack(Xtemp[a]) # flattens the 2-D arrays for each file into 1-D arrays so that sklearn's svm algorithm can work
        X[a] = np.hstack(temp)

    return (X,Y)



def Train(dir, samples):

    X, y = getFeaturesAndLabels(dir, samples)
    clf = RandomForestClassifier(n_estimators = 100)
#    clf = svm.SVC(decision_function_shape='ovo')
    clf.fit(X, y)

    labels = []
    for i in y:
        if(i not in labels):
            labels += [i]

    return clf, labels

def Test(dir, samples, clf, labels):
    Accuracy = 0
    Precision = 0
    Recall = 0

    Xt, yt = getFeaturesAndLabels(dir, samples)
    yPred = np.chararray((len(Xt)), itemsize = 40)
    yPred[:] = '000000000000000000000000000000000000000000000000000000000000'

    for i in range(len(Xt)):
        yPred[i] = str(clf.predict([Xt[i]])[0])

    confusionMatrix = confusion_matrix(yt, yPred, labels)
    print "Yt = "
    print yt
    Precision, Recall, FbetaScore, support = results(yt, yPred, average='macro')
    Accuracy = accuracy_score(yt, yPred)

    print "Actual: "
    print yt
    print "Predicted: "
    print yPred

    return (confusionMatrix, Accuracy, Precision, Recall)

#def pickleClassifier(clf):

def main():
    # Getting command line options
    parser = OptionParser()
    parser.add_option("-s", "--samples", dest="Samples",
                  help="number of samples from total number of packets in each file")
    parser.add_option("-t", "--training", dest="TrainingDataDir",
                  help="Name of directory which has training data")
    parser.add_option("-e", "--testing", dest="TestingDataDir",
                  help="Name of directory with testing data")
    (options, args) = parser.parse_args()
    samples = int(options.Samples)


    clf, labels = Train('./'+options.TrainingDataDir, samples) # Training
    print "DONE TRAINING NOW TESTING"

    confusionMatrix, Accuracy, Precision, Recall = Test('./'+options.TestingDataDir, samples, clf, labels) # Testing

    print "Accuracy = " + str(Accuracy)
    print "Precision = " + str(Precision)
    print "Recall = " +  str(Recall)
    print "Confusion Matrix = "
    print confusionMatrix


if __name__ == "__main__":
    main()
