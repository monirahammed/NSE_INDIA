#Author : Moniruddin Ahammed
#Email : monirahammed@gmail.com




import urllib
import re
import requests
import tempfile
import sys
import threading
import time

import mechanize
import calendar
import os.path

#import mysql.connector
import MySQLdb as db
import datetime
import pprint

import zipfile



pp=pprint.PrettyPrinter(indent=4)

dirPath='/home/monir/stockData'
nseDataURL='http://www.nseindia.com/products/content/equities/equities/homepage_eq.htm';
nseDailyDeliveryDataURL='http://www.nseindia.com/archives/equities/mto/MTO_13072015.DAT'
dailyBhavCopy='http://www.nseindia.com/content/historical/EQUITIES/2015/JUL/cm10JUL2015bhav.csv.zip'
date=time.strftime("%d-%m-%Y")
bulkDealsURL='http://www.nseindia.com/content/equities/bulk.csv'
blockDealsURL='http://www.nseindia.com/content/equities/block.csv'


monthNumIndex={}



def getMonthHahs():
    month={}
    for k,v in enumerate(calendar.month_abbr):
        if k==0:
            continue
        month[v.upper()]=k
        monthNumIndex[k]=v.upper()


#    print monthNumIndex
    return month







def getBrowserAgent():
    ua='User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
    br=mechanize.Browser()
    br.addheaders = [('User-Agent', ua), ('Accept', '*/*')]
    br.set_debug_http(True)
    br.set_debug_responses(True)
    br.set_handle_robots(False)
    br.set_handle_equiv(False)
    return br



def getDailyDeliveryFile(url,fileName):
    print "fetching URL: ", url
    br=getBrowserAgent()
    try:
        br.open(url)
        f=open(fileName,'wb');
        f.write(br.response().read())
        f.close()
    except Exception as e:
            print "Exception Can not fetch URL:", str(e)
            br.close()
            return 0
    br.close()
    return fileName



def getFileName(fileName):
    fileWithPath=dirPath+'/'+fileName +'.' + date
    print "File: " , fileWithPath
    return fileWithPath
    
    

def getMysqlDate(date):
    match=re.search('(\d+)-(\w+)-(\d+)',date)
    if match:
        print match.group(1)
        print match.group(2)
        print match.group(3)
        strDate=str(match.group(3))+'-'+str(month[match.group(2)]) +'-' + str(match.group(1))
        return strDate





def processDailyDevliveryFile(fileName):
    print fileName
    if os.path.exists(fileName) == False:
        return 
    outputFile=fileName + '.' + 'output'
    out=open(outputFile,'wb')
    regex='Trade Date <(.*?)>,Settlement Type <N>,Settlement No .*?,Settlement Date <(.*?)>'
    found=0
    found2=0
    tradeDate,settlementDate=0,0

    with open(fileName) as f:
        for line in f:
            if found == 0 :
                match=re.search(regex, line)
                if match:
                    print "found : ", match.group()
                    print "Match : " , match.group(1) , match.group(2)
                    tradeDate=getMysqlDate(match.group(1))
                    settlementDate=getMysqlDate(match.group(2))
                    found=1
                    next

            elif found2 == 0 :
                match=re.search('Record Type', line)
                if match:
                    found2=1
            
            else:
                #out.write(line +','+ tradeDate +','+ settlementDate)
                #print line
                a=line.strip('\n')
                out.write(a +','+ tradeDate +','+ settlementDate + "\n")

    return outputFile

                
                



def getDatabaseConnection():
	try:
	        con=db.connect("localhost","monir","passwd","StockInformation",local_infile = 1)
	except Exception, err:
		print "Can not connect , Error Message is:", str(err)

        return con



def loadDataFile(fileName, tableName,ignoreLines):
    if os.path.exists(fileName) == False:
        return 

    con=getDatabaseConnection()
    cursor=con.cursor()
    sql="LOAD DATA LOCAL INFILE '"+fileName +"' INTO TABLE "+ tableName + " FIELDS TERMINATED BY ','";
    if ignoreLines != 0:
        sql=sql + ' IGNORE ' + str(ignoreLines) + ' LINES  SET tradeDate=CURRENT_DATE ;'
    else:
        sql= sql + " ;";

    print sql
    try:
        cursor.execute(sql)
        print cursor.messages
        print con.stat()
        print con.info()
        print con.warning_count()
        con.commit()
    except Exception , err:
        con.rollback()
        print "*************** Error Can not load the file :", sql , str(err)
    finally:
        con.close()




def insertIntoDailyBhavCopy(dateString):
    sqlString="INSERT INTO dailySecurityPriceInfo (ticker, series, openPrice, highPrice , lowPrice , closePrice , lastPrice , previousClosePrice ,tradedQuantity, tradeValue , totalNumberOfTrade , ISIN , tradeDate)  select SYMBOL , SERIES, OPEN , HIGH, LOW, CLOSE , LAST, PREVCLOSE , TOTTRDQTY , TOTTRDVAL , TOTALTRADE , ISIN, STR_TO_DATE(TIMESTAMP,'%d-%b-%Y') from test where TIMESTAMP='" +dateString+"'";
    print sqlString
    con=getDatabaseConnection()
    cursor=con.cursor()

    try:
        cursor.execute(sqlString)
        print cursor.messages
        print con.stat()
        print con.info()
        print con.warning_count()
        con.commit()
    except Exception, err:
        con.rollback()
        print "*************** ERROR : ", str(err)
    finally:
        con.close()



    


def getBulkDealsFile():
    getDailyDeliveryFile(bulkDealsURL ,getFileName('dailyBulkDeals.csv'))
    loadDataFile(getFileName('dailyBulkDeals.csv'),'bulkDeals',1)
    
    

def getBlockDealsFile():
    print "getBlockDealsFile -------------------------"
    getDailyDeliveryFile(blockDealsURL ,getFileName('dailyBlockDeals.csv'))
    loadDataFile(getFileName('dailyBlockDeals.csv'),'blockDeals', 1)



def downloadBhavCopy(url):
    fileName=os.path.basename(url)
    dirName='bhavCopy'
    fileWithDir=dirPath + '/' + dirName + '/' + fileName
    print "URL is ", url , " and file Name " , fileWithDir
    getDailyDeliveryFile(url, fileWithDir)
    return fileWithDir

    
    
def downloadDailyDeliveryCopy(url):
    fileName=os.path.basename(url)
    dirName='deliveryInfo'
    fileWithDir=dirPath + '/' + dirName + '/' + fileName
    print "URL is ", url , " and file Name " , fileWithDir
    fileWithDir=getDailyDeliveryFile(url, fileWithDir)
    return fileWithDir
    
    

def loadDailyDeliverFile(nseDailyDeliveryDataURL):
    #t= '0' +  str(i)
#    nseDailyDeliveryDataURL='http://www.nseindia.com/archives/equities/mto/MTO_'+str(t)+'082015.DAT'
    fileName=downloadDailyDeliveryCopy(nseDailyDeliveryDataURL)
    if fileName == 0: return
    getDailyDeliveryFile(nseDailyDeliveryDataURL,getFileName('dailyDeliveryData.csv'))
    outputFile=processDailyDevliveryFile(fileName)
    loadDataFile(outputFile,'securityDeliveryInfo',0)



def downLoadDailyBhavCopy(url):
    fileName=downloadBhavCopy(url)
    return fileName
    
    
    
    

def unzipFile(inputfile):
    print "----------> unzipingh file " + inputfile
    (dirname, filename) = os.path.split(inputfile)
    print dirname, filename
    zfile=zipfile.ZipFile(inputfile)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    zfile.extractall(dirname)

    
    

def loadDbf2Mysql(inputfile):
    print "inside loaddbf " + inputfile
    cmd='dbf2mysql  -vv -q -h localhost -Ppasswd -Umonir   -d StockInformation  -t test -L '  + inputfile
    if os.system(cmd) != 0:
        print "Can not execute command " , cmd 


    

def doAllDialyBhavCopy(url):
    inFile=downLoadDailyBhavCopy(url)
    if os.path.exists(inFile) == False:
        return False
    unzipFile(inFile)
    loadDbf2Mysql(inFile[:-4])
#    insertIntoDailyBhavCopy("11-AUG-2015")
    
    
    
month=getMonthHahs()
    
    

#getBlockDealsFile()
#getBulkDealsFile()

#loadDailyDeliverFile(10);
#loadDailyDeliverFile(11);
#    nseDailyDeliveryDataURL='http://www.nseindia.com/archives/equities/mto/MTO_'+str(t)+'082015.DAT'

#downLoadDailyBhavCopy(10)

def loadDailyDeliveryFile():
            monthStr='10'
            nseDailyDeliveryDataURL='http://www.nseindia.com/archives/equities/mto/MTO_'+str(strI)+str(monthStr)+'2015.DAT'
            print nseDailyDeliveryDataURL
            loadDailyDeliverFile(nseDailyDeliveryDataURL)
    


def loadDailyBhavCopyFile():
            monthName='OCT'
            url='http://www.nseindia.com/content/historical/EQUITIES/2015/'+monthName+'/cm' +str(strI)+monthName+'2015bhav.dbf.zip'
            print url
            if doAllDialyBhavCopy(url) == False: return
            dateFormat=strI +'-'+ monthName +'-'+ '2015'
            print dateFormat
            insertIntoDailyBhavCopy(dateFormat)
    


strI='14'
loadDailyDeliveryFile()
loadDailyBhavCopyFile()


def loadPrevioysDeliveryFiles():
    for month in monthNumIndex:
        #print month, monthNumIndex[month]
        monthName=monthNumIndex[month]
        monthStr=str(month)
        if month < 9: continue
        if month < 10 : monthStr='0'+monthStr
        for i in range(1,32):
            strI=str(i)
            if i < 9 : strI='0'+strI;
            nseDailyDeliveryDataURL='http://www.nseindia.com/archives/equities/mto/MTO_'+str(strI)+str(monthStr)+'2015.DAT'
            print nseDailyDeliveryDataURL
            loadDailyDeliverFile(nseDailyDeliveryDataURL)

    


#loadPrevioysDeliveryFiles()

def loadPreviousBhavCopy():
    for month in monthNumIndex:
        print month, monthNumIndex[month]
        if month < 9: continue
        monthName=monthNumIndex[month]
        if monthName == 'JUL': break
        for i in range(1,32):
            strI=str(i)
            if i < 9 : strI='0'+strI;
            url='http://www.nseindia.com/content/historical/EQUITIES/2015/'+monthName+'/cm' +str(strI)+monthName+'2015bhav.dbf.zip'
            print url
            if doAllDialyBhavCopy(url) == False: continue
            dateFormat=strI +'-'+ monthName +'-'+ '2015'
            print dateFormat
            insertIntoDailyBhavCopy(dateFormat)
    


#loadPreviousBhavCopy()

#def loadArchiveBulkDealsFile():
    #    sqlCmd='mysqlimport  --local --fields-enclosed-by='"' --fields-escaped-by=',' --fields-terminated-by=',' --ignore-lines=1 --user=monir --password=passwd StockInformation   /home/monir/Downloads/TestbulkDeals.csv';

    

    
#doAllDialyBhavCopy(11);


#http://www.nseindia.com/content/historical/EQUITIES/2015/JUL/cm24JUL2015bhav.dbf.zip

#
#for i in range(5,10):
#    t= '0' +  str(i)
#    nseDailyDeliveryDataURL='http://www.nseindia.com/archives/equities/mto/MTO_'+t+'082015.DAT'
#    fileName=downloadDailyDeliveryCopy(nseDailyDeliveryDataURL)
#    if fileName == 0: continue 
#    #print br.response().read()
#    getDailyDeliveryFile(nseDailyDeliveryDataURL,getFileName('dailyDeliveryData.csv'))
#    #getDailyDeliveryFile(dailyBhavCopy,getFileName('dailyBhavCopy.zip'))
#    outputFile=processDailyDevliveryFile(fileName)
#    #url='http://www.nseindia.com/content/historical/EQUITIES/2015/AUG/cm' +t+'AUG2015bhav.dbf.zip'
#   # downloadBhavCopy(url)
#
#    loadDataFile(outputFile,'securityDeliveryInfo',0)
#

