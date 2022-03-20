import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display
#import gc
pd.options.mode.chained_assignment = None

#settings in a dictonary format


testid1 = {
    "referencecolname" : [],
    "normalizedrefcolumns" : [],
    "normalizedcolumns" : [],
    "calresultcolumn" : [],
    "normalizedlookup" : [],
    "columntodisplay" :['SBV', 'TargSBV',  'Time', 'Date','TargTemp',
       'OvenTemp','ToolTemp', 'SubbusV', 'SubbusI', '3.6V', '11V', '6.8V',
       'DAC_0.0V', 'DAC_1.4V', 'DAC_2.2V', 'DAC_2.8V', 'DAC_4.3V','result'],
    "transpose" : True,
    "columntoplot" :[],
    "yrange" : [],
    "xlabel" : [],
    "xreverse" : False
}

testid2= {
    "referencecolname" : 'InFrequency',
    "normalizedrefcolumns" : ['ExPhase','StPhase'],
    "normalizedcolumns" : ['NormalizedExPhase','NormalizedStPhase'],
    "calresultcolumn" : [],
    "normalizedlookup" : 2000000,
    "columntodisplay" :['InFrequency','ExPhase','StPhase','NearAGC',
                      'FarAGC','NormalizedExPhase','NormalizedStPhase','result'],
    "transpose" : False,
    "columntoplot" :['NormalizedExPhase','NormalizedStPhase','high','low'],
    "yrange" : [-0.5, 0.5],
    "xlabel" : 'InFrequency',
    "xreverse" : False
}

testid3= {
    "referencecolname" : 'InFrequency',
    "normalizedrefcolumns" : ['ExPhase','StPhase'],
    "normalizedcolumns" : ['NormalizedExPhase','NormalizedStPhase'],
    "calresultcolumn" : [],
    "normalizedlookup" : 1000000,
    "columntodisplay" :['InFrequency','NearAGC','FarAGC',
                        'NearRMS','FarRMS',
                        'NormalizedExPhase','NormalizedStPhase','result'],
    "transpose" : False,
    "columntoplot" :['NormalizedExPhase','NormalizedStPhase','high','low'],
    "yrange" : [-0.5, 0.5],
    "xlabel" : 'InFrequency',
    "xreverse" : False
}

testid4= {
    "referencecolname" : 'InAmp',
    "normalizedrefcolumns" : ['ExPhase','StPhase'],
    "normalizedcolumns" : ['NormalizedExPhase','NormalizedStPhase'],
    "calresultcolumn" : [],
    "normalizedlookup" : -65,
    "columntodisplay" :['InFrequency','NearAGC','FarAGC',
                        'NearRMS','FarRMS',
                        'NormalizedExPhase','NormalizedStPhase','result'],
    "transpose" : False,
    "columntoplot" :['NormalizedExPhase','NormalizedStPhase','high','low'],
    "yrange" : [-1, 1],
    "xlabel" : 'InAmp',
    "xreverse" : True
}

testid5= {
    "referencecolname" : 'InAmp',
    "normalizedrefcolumns" : ['ExPhase','StPhase'],
    "normalizedcolumns" : ['NormalizedExPhase','NormalizedStPhase'],
    "calresultcolumn" : [],
    "normalizedlookup" : -75,
    "columntoplot" :['NormalizedExPhase','NormalizedStPhase','high','low'],
    "columntodisplay" :['InAmp','ExPhase','StPhase','NearAGC',
                      'FarAGC','NormalizedExPhase','NormalizedStPhase','result'],
    "transpose" : False,
    "yrange" : [-1, 1],
    "xlabel" : 'InAmp',
    "xreverse" : True
}

testid6= {
    "referencecolname" : 'InAmp',
    "normalizedrefcolumns" : ['NearRMS','FarRMS'],
    "normalizedcolumns" : ['CorrectedNearRMS','CorrectedFarRMS'],
    "calresultcolumn" : ['Ratio'],
    "normalizedlookup" : -65,
    "columntodisplay" : ['InAmp', 'NearRMS', 'FarRMS', 
                       'CorrectedNearRMS', 'CorrectedFarRMS','result'],
    "transpose" : False,
    "columntoplot" :['CorrectedNearRMS', 'CorrectedFarRMS','high','low'],
    "yrange" : [-1, 1],
    "xlabel" : 'InAmp',
    "xreverse" : True
}

testid7= {
    "referencecolname" : 'InAmp',
    "normalizedrefcolumns" : ['NearRMS','FarRMS'],
    "normalizedcolumns" : ['CorrectedNearRMS','CorrectedFarRMS'],
    "calresultcolumn" : ['Ratio'],
    "normalizedlookup" : -75,
    "columntodisplay" : ['InAmp', 'NearRMS', 'FarRMS', 
                       'CorrectedNearRMS', 'CorrectedFarRMS','result'],
    "transpose" : False,
    "columntoplot" :['CorrectedNearRMS', 'CorrectedFarRMS','high','low'],
    "yrange" : [-1, 1],
    "xlabel" : 'InAmp',
    "xreverse" : True
}

testid8= {
    "referencecolname" : 'InPhase',
    "normalizedrefcolumns" : ['ExPhase','StPhase'],
    "normalizedcolumns" : ['NormalizedExPhase','NormalizedStPhase'],
    "calresultcolumn" : [],
    "normalizedlookup" : 0,
    "columntodisplay" :['InPhase','ExPhase','StPhase',
                        'NormalizedExPhase','NormalizedStPhase','result'],
    "transpose" : False,
    "columntoplot" :['NormalizedExPhase', 'NormalizedStPhase','high','low'],
    "yrange" : [-1, 1],
    "xlabel" : 'InPhase',
    "xreverse" : False
}

testid9= {
    "referencecolname" : 'InPhase',
    "normalizedrefcolumns" : ['ExPhase','StPhase'],
    "normalizedcolumns" : ['NormalizedExPhase','NormalizedStPhase'],
    "calresultcolumn" : [],
    "normalizedlookup" : 0,
    "columntodisplay" :['InPhase','ExPhase','StPhase',
                        'NormalizedExPhase','NormalizedStPhase','result'],
    "transpose" : False,
    "columntoplot" :['NormalizedExPhase', 'NormalizedStPhase','high','low'],
    "yrange" : [-1, 1],
    "xlabel" : 'InPhase',
    "xreverse" : False
}

testid10= {
    "referencecolname" : 'InFrequency',
    "normalizedrefcolumns" : ['ExPhase','StPhase'],
    "normalizedcolumns" : ['NormalizedExPhase','NormalizedStPhase'],
    "calresultcolumn" : [],
    "normalizedlookup" : 2000000,
    "columntodisplay" :['InFrequency','ExPhase','StPhase','result'],
    "transpose" : False,
    "columntoplot" :[],
    "yrange" : [-0.5, 0.5],
    "xlabel" : 'InFrequency',
    "xreverse" : False
}

testid11= {
    "referencecolname" : 'InFrequency',
    "normalizedrefcolumns" : ['ExPhase','StPhase'],
    "normalizedcolumns" : ['NormalizedExPhase','NormalizedStPhase'],
    "calresultcolumn" : [],
    "normalizedlookup" : 1000000,
    "columntodisplay" :['InFrequency','ExPhase','StPhase','result'],
    "transpose" : False,
    "columntoplot" :[],
    "yrange" : [-0.5, 0.5],
    "xlabel" : 'InFrequency',
    "xreverse" : False
}

testid12= {
    "referencecolname" : 'InFrequency',
    "normalizedrefcolumns" : ['ExPhase','StPhase'],
    "normalizedcolumns" : ['NormalizedExPhase','NormalizedStPhase'],
    "calresultcolumn" : [],
    "normalizedlookup" : 2000000,
    "columntodisplay" :['InFrequency','NearAGC','FarAGC','result'],
    "transpose" : False,
    "columntoplot" :[],
    "yrange" : [-0.5, 0.5],
    "xlabel" : 'InFrequency',
    "xreverse" : False
}

testid13= {
    "referencecolname" : 'InFrequency',
    "normalizedrefcolumns" : ['ExPhase','StPhase'],
    "normalizedcolumns" : ['NormalizedExPhase','NormalizedStPhase'],
    "calresultcolumn" : [],
    "normalizedlookup" : 1000000,
    "columntodisplay" :['InFrequency','NearAGC','FarAGC','result'],
    "transpose" : False,
    "columntoplot" :[],
    "yrange" : [-0.5, 0.5],
    "xlabel" : 'InFrequency',
    "xreverse" : False
}

testid14= {
    "referencecolname" : 'InAmp',
    "normalizedrefcolumns" : ['ExPhase','StPhase'],
    "normalizedcolumns" : ['NormalizedExPhase','NormalizedStPhase'],
    "calresultcolumn" : [],
    "normalizedlookup" : -65,
    "columntodisplay" :['InFrequency','NearAGC','FarAGC',
                        'NearRMS','FarRMS','result'],
    "transpose" : False,
    "columntoplot" :[],
    "yrange" : [-1, 1],
    "xlabel" : 'InAmp',
    "xreverse" : True
}

testid15= {
    "referencecolname" : 'InAmp',
    "normalizedrefcolumns" : ['ExPhase','StPhase'],
    "normalizedcolumns" : ['NormalizedExPhase','NormalizedStPhase'],
    "calresultcolumn" : [],
    "normalizedlookup" : -75,
    "columntoplot" :['NormalizedExPhase','NormalizedStPhase','high','low'],
    "columntodisplay" :['InFrequency','NearAGC','FarAGC',
                        'NearRMS','FarRMS','result'],
    "transpose" : False,
    "yrange" : [-1, 1],
    "xlabel" : 'InAmp',
    "xreverse" : True
}

columnset = set(['RunNumber', 'Mother_SN', 'Daugther_SN', 'Cycle', 'Segment', 'TestType',
                 'TestID', 'ELS', 'SBV', 'TargSBV', 'Time', 'Date', 'TargTemp',
                 'OvenTemp', 'ToolTemp', 'SubbusV', 'SubbusI', '3.6V', '11V', '6.8V',
                 'DAC_0.0V', 'DAC_1.4V', 'DAC_2.2V', 'DAC_2.8V', 'DAC_4.3V',
                 'InFrequency', 'InAmp', 'InPhase', 'ExPhase', 'StPhase', 'NearAGC',
                 'FarAGC', 'NearRMS', 'FarRMS'])

testnames = ["ALL", "Quick Tests", "Power Test", "2MHz Band Width", "1MHz Band Width",
             "2MHz Phase vs Amplitude", "1MHz Phase vs Amplitude",
             "2MHz Corrected Amplitude", "1MHz corrected amplitude",
             "2MHz Phase Linearity", "1MHz Phase Linearity"]
 
tablestyles = [
    dict(selector="tr:hover",
                props=[("background", "#f7f7f7")]),
    dict(selector="th", props=[("border", "1px solid #0"),
                               ("padding", "1px 1px"),
                               ("text-align", "center"),
                               ("border-collapse", "collapse"),
                               ("text-transform", "uppercase"),
                               ("font-size", "12px")
                               ]),
    dict(selector="td", props=[("border", "1px solid #eee"),
                               ("text-align", "center"),
                               ("padding", "0px 1px"),
                               ("border-collapse", "collapse"),
                               ("font-size", "12px")
                               ]),
    dict(selector="table", props=[
                                    ("font-family" , 'Arial'),
                                    ("margin" , "1px auto"),
                                    ("border-collapse" , "collapse"),
                                    ("border" , "1px solid #eee"),
                                    ("border-bottom" , "2px solid #00cccc"),                                    
                                      ]),
    dict(selector="caption", props=[("caption-side", "top")])
]        
    
test_dict = {1: testid1, 2: testid2, 3: testid3, 
             4: testid4, 5: testid5, 6: testid6, 
             7: testid7, 8: testid8, 9: testid9,
             10: testid10, 11:testid11, 12: testid12,
             13: testid13, 13:testid14, 15: testid15}

limit_columns = ['targtemp','testtype','testid', 
                 'refvalue', 'refcol','checkcol',
                 'high', 'low', 'testname']


# get a part of the limit for each test with 2 keys
# return the limits for one test case
def getthislimit(limit_all, testname, targtemp):
    thislimit = limit_all.loc[(limit_all['testname']==testname)
                            & (limit_all['targtemp']==targtemp)]
    return thislimit

# get chunk of data, unfortunately, there are two test types
# currently only type 2 is supported
# calculate normalization
# return data with calculated columns
def getthisdata(data_rundf, segment, testid, testtype):
    if (testid>9):
        translatetestid  = testid - 7
    else: 
        translatetestid  = testid
    thisdata = data_rundf.loc[(data_rundf['segment']==segment)
                            & (data_rundf['testid']==translatetestid)
                            & (data_rundf['testtype']==testtype)]
    #st.write("segment",segment,"testid",testid,"testtype",testtype)
    #normalizaion calculation, if not required skip
    xlabel = str(test_dict[testid]['xlabel']).lower()
    refcolumns = [x.lower() for x in 
                  test_dict[testid]['normalizedrefcolumns']]
    normalizedcolumns = [x.lower() for x in 
                         test_dict[testid]['normalizedcolumns']]
    if len(normalizedcolumns) == 0:
        return thisdata
    columntodisplay = [x.lower() for x in 
                       test_dict[testid]['columntodisplay']]
    calresultcolumn = [x.lower() for x in 
                       test_dict[testid]['calresultcolumn']]   
    lookupreference = test_dict[testid]['normalizedlookup']
    #st.write("lookupreference",lookupreference)
    bwcenter = thisdata.loc[thisdata[xlabel]==lookupreference]
    #st.write("bwcenter",bwcenter)
    # do require calculation on data
    for colcount in range (0,len(refcolumns)):
        newcol = str(normalizedcolumns[colcount])
        refcol = str(refcolumns[colcount])
        if (testid in [2,3,4,5]):
            thisdata.loc[:,newcol]=thisdata.loc[:,refcol] \
                            - bwcenter.iloc[0][refcol] 
        elif (testid in [6,7]):
            thisdata.loc[:,newcol]=(thisdata.loc[:,xlabel] - lookupreference)\
                            - thisdata.loc[:,refcol] \
                            + bwcenter.iloc[0][refcol] 
        elif (testid in [8,9]):
            thisdata.loc[:,newcol]=thisdata.loc[:,refcol] \
                            - bwcenter.iloc[0][refcol] \
                            - (thisdata.loc[:,xlabel] - lookupreference) 
        thisdata.loc[:,newcol]=thisdata.loc[:,newcol].round(3) 

    return thisdata

# do the checking of data against limit
# it will result resultdata
def checkdata(checkcols, refcolumn, thislimit, thisdata): 
    testcount = 0
    faildata = pd.DataFrame([])
    currentdata = thisdata.copy(deep=False)
    currentdata.set_index(refcolumn, inplace=True)
    for indcheckcol in checkcols:
        currentlimit = thislimit.loc[thislimit['checkcol']==indcheckcol]
        currentlimit= currentlimit.loc[:, ~currentlimit.columns.isin(['testtype', 
                                            'testid', 'checkcol', 'segment',
                                            'testname','targtemp'])] 
        currentlimit.set_index('refvalue', inplace=True)
        if currentlimit.shape[0] > currentdata.shape[0]:
            errorstr = "data set is smaller!"
            raise ValueError(errorstr)
        newdata = currentlimit.join(currentdata)
        newdata.dropna(how='all',axis=0, inplace=True)
        newdata.loc[:,indcheckcol+'result']= \
                            (newdata.loc[:,indcheckcol]<= newdata.loc[:,'high']) \
                            & (newdata.loc[:,indcheckcol] > newdata.loc[:,'low'] )
        checkpass = newdata.loc[newdata[indcheckcol+'result'] == False].copy()
        checkpass.rename({indcheckcol+'result' : 'result'}, axis=1, inplace=True)
        if faildata.shape[0]==0:
            #print("new")
            faildata = checkpass
        else:
            #print("merge")
            faildata = faildata.append(checkpass)
            faildata.reset_index()
        
        newdata = newdata[[indcheckcol+'result']]
        if testcount == 0:
            resultdata = newdata
            testcount = testcount + 1
        else: 
            #print("check pass 2")
            resultdata = resultdata.join(newdata)
    #print(resultdata)
    finalresult = resultdata.copy()
    finalresult = finalresult.replace(np.nan, True)
    finalresult['result']= finalresult.any(axis=1)
    #print("finalresult", finalresult.all(axis=None))
    testresult =  finalresult.all(axis=None) 
    finalresult['result'] = np.where((finalresult==True).all(axis=1),
                                     "pass","fail")
    finalresult = finalresult['result']
    return testresult, finalresult, faildata
#del resultdat

# return the result table to display from data and result
def displaydata(thisdata, thistestid, refcolumn, finalresult):
    displayresult = thisdata.copy()
    displayresult.set_index(refcolumn, inplace=True)
    displayresult = displayresult.join(finalresult)
    displayresult['result'] = displayresult['result'].replace(np.nan, "")
    columntodisplay = [x.lower() for x in 
                   test_dict[thistestid]['columntodisplay']]
    if len(columntodisplay) == 0: return pd.Dataframe([])
    if refcolumn in columntodisplay: columntodisplay.remove(refcolumn)
    displayresult = displayresult[columntodisplay]
    if test_dict[thistestid]['transpose']:
        return displayresult.transpose()
    else: 
        return displayresult



# sort and find same set of data common to two array
# to check the data that can be verified by limit
def comparelimitdata(limitarray, dataarray):
    sameset = []
    if len(limitarray) == len(dataarray):
        if ((np.sort(limitarray)) != (np.sort( dataarray))).all():
            sameset = np.array(list(set(np.sort(limitarray)) \
                                    & set(np.sort( dataarray))))
        else: sameset =  limitarray   
    else: sameset = np.array(list(set(np.sort(limitarray)) 
                                & set(np.sort( dataarray))))
    return sameset

# red highligh failed cells
def redrowfail(row):
    #print(row)
    x = row.loc["result"]
    if x == "fail":
        color = 'pink'
    elif x == "pass":
        color = 'lightgreen'
    else:
        color = 'white'
    return ['background-color: %s' % color for r in row]


def redcellfail(x):
    c1='background-color: pink'
    c2=''
    condition=x.eq("fail")
    res=pd.DataFrame(np.where(condition,c1,c2),index=x.index,columns=x.columns)
    return res



def plot_quicktest(powertest):
    leftside = ['oventemp', 'tooltemp', 'subbusi']
    rightside = ['subbusv','11v', '6.8v','dac_0.0v', 'dac_1.4v', 'dac_2.2v', 'dac_2.8v', 'dac_4.3v']
    fig,ax1 = plt.subplots(figsize=(6.5,4))
    ax2 = ax1.twinx()
    for i in leftside:
        ax1.plot(powertest['els'],powertest[i],label=i)
    for i in rightside:
        ax2.plot(powertest['els'],powertest[i],label=i)
    ax1.set_xlabel("ELS")
    ax1.set_ylabel("Temperature (C) / Current (mA)")
    ax2.set_ylabel("Voltage (V)")
    ax2.set_ylim(0,21)
    ax1.legend()
    ax2.legend(loc="right")
    ax1.set_title("QUICK TEST PLOT")
    #fig.tight_layout()
    #pdf.savefig()  # saves the current figure into a pdf page
    plt.show()
    st.pyplot(fig)

# plot the data based on dictionary settings
def plotdata(segment, thisdata, testid, testname, refcolumns):    
    columntoplot = [x.lower() for x in 
                       test_dict[testid]['columntoplot']]  
    if len(columntoplot) != 0:
        yrange = test_dict[testid]['yrange'] 
        xreverse  = test_dict[testid]['xreverse']
        fig,ax1 = plt.subplots(figsize=(6.5,2.5))
        columntoplot = [x for x in columntoplot if x in thisdata.columns]
        for colcount in range (0,len(refcolumns)):
            ax1.plot(thisdata[columntoplot], label=columntoplot)
        if len(yrange) == 2: ax1.set_ylim(yrange[0],yrange[1])
        ax1.legend()
        ax1.grid()
        ax1.set_title(testname)
        if (xreverse): plt.gca().invert_xaxis()
        #pdf.savefig()
        plt.show()
        st.pyplot(fig)
