import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import os, urllib
import datafileconfig as dfc

def main():
    # Render the readme as markdown using st.markdown.
    readme_text = st.markdown(get_file_content_as_string("read.me"))
    # Download external dependencies.
    for filename in EXTERNAL_DEPENDENCIES.keys():
        download_file(filename)
        limit_all = pd.read_csv(filename)
        limit_all.columns = limit_all.columns.str.strip().str.lower()
        if not(all(x in dfc.limit_columns for x in limit_all.columns)):
            errorstr = "Limit columns were not found!"
            raise ValueError(errorstr)
        
        limit_all['testname']=limit_all['testname'].astype('string')
        limit_all['refcol']=limit_all['refcol'].str.strip().str.lower()
        limit_all['checkcol']=limit_all['checkcol'].astype(str)
        limit_all['checkcol']=limit_all['checkcol'].str.strip().str.lower()

        limit_testnames = limit_all['testname'].unique()
        limit_testids = limit_all['testid'].unique()
        limit_temperatures = limit_all['targtemp'].unique()
        limit_testidandname = limit_all[['testname','testid']].drop_duplicates()
        limit_testidandtype =  limit_all[['testid','testtype']].drop_duplicates()
    # Once we have the dependencies, add a selector for the app mode on the sidebar.
    #st.sidebar.title("What to do")
    app_mode = st.sidebar.selectbox("Select RUN to run",
        ["Show instructions", "Run the app"])
    if app_mode == "Show instructions":
        st.sidebar.success('To continue select "Run the app".')
    elif app_mode == "Run the app":
        uploadedFile = st.sidebar.file_uploader("Upload CSV data", type=['csv'], accept_multiple_files=False, key="fileUploader")
        if uploadedFile is not None:
            data_all = pd.read_csv(uploadedFile, error_bad_lines=True, warn_bad_lines=False, sep=',', quotechar='"')
            data_all.columns = data_all.columns.str.strip()

            if ((data_all.shape[1] != 34) | (data_all.shape[0] <= 2) | (dfc.columnset.issubset(data_all.columns) == False)):
                st.error('CSV structure not recognized!')
            else:
                st.sidebar.success('Data file is recognized!')
                readme_text.empty()
                #if run_the_app():

                data_all.columns = data_all.columns.str.strip().str.lower()
                data_runs = data_all['runnumber'].unique()
                data_segments = data_all['segment'].unique()
                data_lastrun = data_runs[len(data_runs)-1]
                data_rundf = data_all.loc[data_all['runnumber']==data_lastrun]
                
                data_temperatures = data_all['targtemp'].unique()
                data_testtypes = data_rundf['testtype'].unique()
                data_testids = data_rundf['testid'].unique()
                data_segmentandtemp =data_rundf[['segment','targtemp']].drop_duplicates()
                del data_all
                del data_segments
                del data_runs
                
                # Compare Data and Limits and get the coverage            
                temperatures_can_check = dfc.comparelimitdata(limit_temperatures, data_temperatures) 
                segments_can_check = data_segmentandtemp.loc[
                                data_segmentandtemp['targtemp'].isin(temperatures_can_check)]
                #testids_can_check = dfc.comparelimitdata(limit_testids, data_testids)

                if len(temperatures_can_check) == 0:
                    errorstr = "No Temperature can be verified!"
                    raise ValueError(errorstr)

                #if len(testids_can_check) == 0:
                #    errorstr = "No testid can be verified!"
                #    raise ValueError(errorstr)
                #else:
                #   testnames_can_check = limit_testidandname.loc[
                #       limit_testidandname['testid'].isin(testids_can_check)]['testname']

                #lastrun = df['RunNumber'].unique()[-1]
                #st.write('Plotting for RUN :',data_lastrun)
                del data_lastrun
                #powertest = data_rundf.loc[(data_rundf['testtype'] == 1) & (data_rundf['testid'] == 1)]
                #st.write(powertest)
                #dfc.plot_quicktest(powertest)
                
                #get summary first
                seglist = segments_can_check['segment']
                #resultlist= pd.DataFrame([],columns=seglist,index=testnames_can_check)
                resultlist= pd.DataFrame([],columns=seglist,index=limit_testnames)
                fullfaildata = pd.DataFrame([])
                segcount = 0
                for eachsegment in segments_can_check['segment']:
                    testcount = 0
                    for thistestid in limit_testids:
                        eachtestname = limit_testidandname.loc[limit_testidandname['testid']==thistestid]['testname']
                        #print(eachtestname)
                        #thistestid = int(limit_testidandname.loc[
                        #    limit_testidandname['testname']==eachtestname,'testid'])
                        thistargtemp =  int(data_segmentandtemp.loc[
                            data_segmentandtemp['segment']==eachsegment,'targtemp'])
                        thistesttype =  int(limit_testidandtype.loc[
                            limit_testidandtype['testid']==thistestid,'testtype'])
                        thislimit = dfc.getthislimit(limit_all, eachtestname, thistargtemp)
                        thisdata = dfc.getthisdata(data_rundf, eachsegment,thistestid,thistesttype)
                        checkcols = thislimit['checkcol'].unique()
                        refcolumns = thislimit['refcol'].unique()
                        refcolumn = refcolumns[0]
                        testresult, finalresult, faildata = dfc.checkdata(checkcols, refcolumn, thislimit, thisdata)
                        resultstr = ""
                        if testresult: 
                            resultstr = "pass"
                        else: 
                            resultstr = "fail"
                        resultlist.loc[eachtestname,eachsegment] = resultstr
                                        
                st.sidebar.table(resultlist.style.set_table_styles(dfc.tablestyles).set_caption("Overall Result").apply(dfc.redcellfail,axis=None))

                temperaturetoselect = pd.Series(["All"]) \
                    .append(data_segmentandtemp['segment'].astype(str)+ "-" + \
                            data_segmentandtemp['targtemp'].astype(str)).tolist()
                testtoselect = pd.Series(["ALL", "QuickTest"]) \
                    .append(testnames_can_check).tolist()
                #st.write(testtoselect)

                with st.sidebar.form("my_form"):
                    temperatureselector = st.selectbox("Chose temperature", temperaturetoselect)
                    testselector = st.selectbox("Choose the test",testtoselect)
                    submitted = st.form_submit_button("Submit")
                
                if submitted:
                    readme_text.empty()
                    selectedtemperature = temperaturetoselect.index(temperatureselector)
                    selectedtest =  testtoselect.index(testselector)
                    #readme_text = st.write("temp", selectedtemperature, \
                    #           "test", selectedtest) 
                    
                    if (temperaturetoselect.index(temperatureselector)==0):
                        segments = data_segmentandtemp['segment']
                    else:
                        segments = [data_segmentandtemp.iloc[selectedtemperature-1,[0]][0]]
                    #st.write("segments selected",segments)
                
                    if (selectedtest==1):
                        quicktest = data_rundf.loc[(data_rundf['testtype'] == 1) & (data_rundf['testid'] == 1)]
                        #st.write(powertest)
                        dfc.plot_quicktest(quicktest)
                    else: 
                        if (selectedtest==0): 
                            tests = testnames_can_check
                        else: 
                            tests = [testselector]
                        #st.write("tests selected",tests)
                        resultlist= pd.DataFrame([],columns=segments,index=tests)
                        fullfaildata = pd.DataFrame()
                        segcount = 0
                        for eachsegment in segments:
                            testcount = 0
                            for eachtestname in tests:
                                #print(eachtestname)
                                thistestid = int(limit_testidandname.loc[
                                    limit_testidandname['testname']==eachtestname,'testid'])
                                thistargtemp =  int(data_segmentandtemp.loc[
                                    data_segmentandtemp['segment']==eachsegment,'targtemp'])
                                st.write(eachtestname, " - segment ", eachsegment, " ", thistargtemp , " degC")
                                thistesttype =  int(limit_testidandtype.loc[
                                    limit_testidandtype['testid']==thistestid,'testtype'])
                                thislimit = dfc.getthislimit(limit_all, eachtestname, thistargtemp)
                                thisdata = dfc.getthisdata(data_rundf, eachsegment,thistestid,thistesttype)
                                checkcols = thislimit['checkcol'].unique()
                                refcolumns = thislimit['refcol'].unique()
                                #st.write("refcolumns", refcolumns)
                                if refcolumns.shape[0]==0:
                                    refcolumn = pd.DataFrame
                                else:
                                    refcolumn = refcolumns[0]
                                testresult, finalresult, faildata = dfc.checkdata(checkcols, refcolumn, 
                                                                            thislimit, thisdata)
                                resultstr = ""
                                if testresult: 
                                    resultstr = "pass"
                                else: 
                                    resultstr = "fail"
                                resultlist.loc[eachtestname,eachsegment] = resultstr
                                if fullfaildata.shape[0]==0:
                                    fullfaildata = faildata
                                else:
                                    #print("merge")
                                    fullfaildata = fullfaildata.append(faildata)
                                    fullfaildata.reset_index()
                                    #print(thistargtemp, "degC",eachtestname, resultstr)
                                displayresult = dfc.displaydata(thisdata, thistestid, refcolumn, finalresult)
                                if displayresult.shape[0] > 0: 
                                    if thistestid != 1:
                                        readme_text = st.table(displayresult.style.set_table_styles(dfc.tablestyles).apply(dfc.redrowfail,axis=1))
                                    else: 
                                        displayresult= displayresult.astype('string')
                                        readme_text = st.table(displayresult.style \
                                            .set_table_styles(dfc.tablestyles) \
                                            .set_caption(eachtestname) \
                                            .apply(dfc.redcellfail,axis=None))
                                    readme_text = dfc.plotdata(eachsegment, displayresult, thistestid, eachtestname, refcolumns)
                        
                        readme_text =st.table(resultlist.style.set_table_styles(dfc.tablestyles).set_caption("Overall Result").apply(dfc.redcellfail,axis=None))
                        fullfaildata = fullfaildata.dropna(axis='columns')
                        if fullfaildata.shape[0] > 0:
                            readme_text =st.table(fullfaildata.style.set_table_styles(dfc.tablestyles).set_caption("Fail Data"))


def run_the_app():
    # To make Streamlit fast, st.cache allows us to reuse computation across runs.
    # In this common pattern, we download data from an endpoint only once.
    #@st.cache
    return True
    
    st.write("main")

# Download a single file and make its content available as a string.
@st.cache(show_spinner=False)
def get_file_content_as_string(path):
    url = 'https://raw.githubusercontent.com/morrise/limit/main/' + path
    #url = 'http://localhost:8501/' + path
    response = urllib.request.urlopen(url)
    return response.read()#.decode("utf-8")

# This file downloader demonstrates Streamlit animation.
def download_file(file_path):
    # Don't download the file twice. (If possible, verify the download using the file length.)
    if os.path.exists(file_path):
        if "size" not in EXTERNAL_DEPENDENCIES[file_path]:
            return
        elif os.path.getsize(file_path) == EXTERNAL_DEPENDENCIES[file_path]["size"]:
            return

    # These are handles to two visual elements to animate.
    weights_warning, progress_bar = None, None
    try:
        weights_warning = st.warning("Downloading %s..." % file_path)
        progress_bar = st.progress(0)
        with open(file_path, "wb") as output_file:
            with urllib.request.urlopen(EXTERNAL_DEPENDENCIES[file_path]["url"]) as response:
                length = int(response.info()["Content-Length"])
                counter = 0.0
                MEGABYTES = 2.0 ** 20.0
                while True:
                    data = response.read(8192)
                    if not data:
                        break
                    counter += len(data)
                    output_file.write(data)

                    # We perform animation by overwriting the elements.
                    weights_warning.warning("Downloading %s... (%6.2f/%6.2f MB)" %
                        (file_path, counter / MEGABYTES, length / MEGABYTES))
                    progress_bar.progress(min(counter / length, 1.0))

    # Finally, we remove these visual elements by calling .empty().
    finally:
        if weights_warning is not None:
            weights_warning.empty()
        if progress_bar is not None:
            progress_bar.empty()


# Path to the Streamlit public S3 bucket

# External files to download.
EXTERNAL_DEPENDENCIES = {
    "yolov3.weights": {
        "url": "https://raw.githubusercontent.com/morrise/limit/main/EwrSolarSetLimit_TrialMar2022.csv",
        "size": 61490
    }
}




if __name__ == "__main__":
    main()
