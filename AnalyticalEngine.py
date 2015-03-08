import pandas as pd
from sklearn import linear_model
import random

class Record(object):
    pass

def data_read_proc(filename, path):
    inputdata = pd.read_csv(path + filename)
    return list(inputdata.columns.values)

def binomial_logit_proc(path, filename, ex_variable, variable_list, target_variable):
    #Data Importing
    data = pd.read_csv(path + filename)

    #Variable Preparation
    variable_list.remove(target_variable)
    for ex_var in ex_variable:
        variable_list.remove(ex_var)
        #if ex_var in dummyvar:
        #    dummyvar.remove(ex_var)
    #for dum_var in dummyvar:
     #   variable_list.remove(dum_var)

    #Dummy Variable dataset Prepartion
    #data = dummyvariable(dataset,variablelist)


    #Data Sampling
    rows = random.sample(data.index, int(round((.3 * data.shape[0]))))
    data1 = data.ix[rows]


    #Model Building
    try:
        logreg = linear_model.LogisticRegression(C=1e5)
        fit = logreg.fit(data1[variable_list], data1[target_variable])
        return fit.summary()
    except:
        print "Error Modeling"
        return "Error"

#Dummy Variable Creation Function.
def dummyvariable(dataset,variablelist):
    r = Record()
    finalprint = ""
    columnlist = list(dataset.columns.values)
    for var in variablelist:
        dyna_var = var+'_rank'
        setattr(r,dyna_var,pd.get_dummies(dataset[var], prefix=var))
        exec("%s %s"%('print',dyna_var+".shape"))
        finalprint = '.join('+dyna_var+'.ix[:,:])'+finalprint
        columnlist.remove(var)
    exec("%s = %s"%('finalset','dataset.ix[:,columnlist]'+finalprint))
    return finalset

