#Author: Anthony Barbosa
#Description: This script is fired when a webhook is receieved by the webhook listener in the Flask Application.
# The Script extracts useful data from the webhooks JSON message and stores it into a SQL database

import json
import time
import cloudways as cloudways #The Database 


def addCall(path):

    ## Functions-----------------------------------------------------------

    #Converts Unix Timestamp to normal time
    def epoch2normal(date):
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date))
        return date

    #Formats the date to our liking
    def dateCleanUp(date):
        date = date.replace("T", " ")
        date = date[:19]
        return date

    #Removed any weird characters in phone numnbers 
    def normalizeNumber(number):
        try:
            number = number.replace("+1","")
            number = number.replace("+","")
            number = number.replace(" ","")
            number = number.replace("-","")
            number = number.replace("(","")
            number = number.replace(")","")
            return number
        except:
            return number

    
    with open(path, "r") as f:
        data = json.load(f)
        data = (data['data'])


        
    #Data we would like to gather
    id = data['id']
    direction = data['direction']
    missedCallReason = data['missed_call_reason']
    duration = epoch2normal(data['duration'])
    started = (data['started_at'])
    answered = (data['answered_at'])
    ended = (data['ended_at'])
    try:
        started = epoch2normal(started)
    except:
        started = dateCleanUp(started)
    try:
        answered = epoch2normal(answered)
    except:
        answered = dateCleanUp(answered)

    try:
        ended = epoch2normal(ended)
    except:
        ended = dateCleanUp(ended)

    if(data['recording'] == None):
        leftVoiceMail = False
    else:
        leftVoiceMail = True

    phone = data['raw_digits']
    phoneNormalized = normalizeNumber(phone)

    #Contact info
    try:
        callerId = data['contact']['id']
        firstName = data['contact']['first_name']
        lastName = data['contact']['last_name']
    except:
        callerId = " "
        firstName = " "
        lastName = " "

    #Store info
    propelId = data['number']['id']
    propelName = data['number']['name']
    propelNumber = normalizeNumber(data['number']['digits'])

    ## ADD TO DB ------------------------------------------------------------------------

    QUERY_CALLS =  '''
        SELECT *
        FROM `BI_AC_CALLS`
        ORDER BY STARTED DESC

        '''
    DATA_CALLS = cloudways.GET_SQL_DATA(QUERY_CALLS)

    data = (id, started, answered, ended, duration, leftVoiceMail, missedCallReason, direction, phone, phoneNormalized, callerId, firstName, lastName, propelId, propelName, propelNumber)
    DATA_CALLS.loc[-1] = data

    #Insert DF to DB
    cloudways.INSERT_VALUES_SQL(DATA_CALLS,'BI_AC_CALLS', create_table = True, drop_table = True)

   
        

addCall("log.json")


