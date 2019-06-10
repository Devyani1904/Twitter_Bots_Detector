#Twitter Database
import DataBase

#Twitter API
# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the tweepy library
import tweepy

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '1106237485225558016-T5ngrObrWbpytXJ7d46DaRnuKsK7to'
ACCESS_SECRET = 'p4VFkgRa13HWFS6qcgWj3hBgzCYoTFPjbicBWnbad96Rr'
CONSUMER_KEY = 'oQhoEEKnCFbZPTt4aPdf0poiv'
CONSUMER_SECRET = '6hWgXNG7TgwOCIm5or2QXxA55sHZwwA0QWPasitIxxCTBNVZvE'

# Setup tweepy to authenticate with Twitter credentials:
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
api.verify_credentials()

#DateTime library
from datetime import datetime, timedelta
from flask_mysqldb import MySQLdb




def submitUser(screen_name):
    if screen_name[0] == "@":
        screen_name = screen_name[1:]
    myUser = api.get_user(screen_name)
    dbUser = DataBase.selectUserId(screen_name)
    dbFollowers = DataBase.selectSavedFollowersCount(screen_name)
    insertFollowers = True
    if not dbUser:
        DataBase.insertUser(myUser)
    else:
        if dbFollowers:
            insertFollowers = False

    #get info on API limit
    if insertFollowers:
        #get 200 followers per request and limit it to a maximum of 200 (we don't want to get to the API limit)
        followers = tweepy.Cursor(api.followers, screen_name=screen_name, count=200).items(400)

        for follower in followers:
            try:
                DataBase.insertFollower(myUser, follower)
            except MySQLdb.IntegrityError:
                pass
            except:
                print("Database error")
    
    if False:
        DataBase.calculateFollowerMatrix(screen_name)



def getUserInfo(screen_name):
    dbUser = DataBase.selectUserInfo(screen_name)
    if dbUser:        
        UserInfo = {
                'Screen_Name': dbUser['Screen_Name'],
                'Name': dbUser['Name'],
                'Description': dbUser['Description'],
                'followers_count': dbUser['Followers_Count'],
                'friends_count': dbUser['Friends_Count'],
                'statuses_count': dbUser['Statuses_Count'],
                'favourites_count': dbUser['Favourites_Count'],
                'Profile_Image_Url': dbUser['Profile_Image_Url'].replace("normal", "400x400")
            }
    else:
        UserInfo = None
    return UserInfo

def insertMatrixInfo(screen_name):
    DataBase.calculateFollowerMatrix(screen_name)

def getPercentagesInfo(screen_name):
    dbUser = DataBase.selectUserId(screen_name)
    id = dbUser["idUser"]
    print (id)
    followerMatrix = DataBase.selectMatrixResults(id)
    genuine = followerMatrix['Genuine']
    suspicious = followerMatrix['Suspicious']
    bots = followerMatrix['Bots']
    totalUsers = genuine + suspicious + bots
    MatrixInfo = {
        'genuine': round(safeDivision(genuine,totalUsers) * 100,2),
        'suspicious': round(safeDivision(suspicious,totalUsers)  * 100,2),
        'bots': round(safeDivision(bots,totalUsers)  * 100,2),
    }
    return MatrixInfo

def safeDivision (x,y):
    if y:
        return x/y
    else:
        return 0

def deleteMatrixInfo(screen_name):
    dbUser = DataBase.selectUserId(screen_name)
    id = dbUser["idUser"]
    DataBase.deleteFollowerMatrix(id)


def getFollowersExampleInfo(screen_name, type):
    rows = {}
    FollowersInfo = []   
    dbUser = DataBase.selectUserId(screen_name)
    id = dbUser["idUser"]  
    rows = {}
    FollowersInfo = []  
    if type == "genuine":
        rows = DataBase.selectGenuineExamples(id)
    elif type == "suspicious":
        rows = DataBase.selectSuspiciousExamples(id)
    elif type == "bot":
        rows = DataBase.selectBotsExamples(id)
    if rows: 
        dbUser = rows[0] 
        FollowersInfo.append ( {
                'Screen_Name': dbUser['Screen_Name'],
                'Name': dbUser['Name'],
                'Description': dbUser['Description'],
                'followers_count': dbUser['Followers_Count'],
                'friends_count': dbUser['Friends_Count'],
                'statuses_count': dbUser['Statuses_Count'],
                'favourites_count': dbUser['Favourites_Count'],
                'Profile_Image_Url': dbUser['Profile_Image_Url'].replace("normal", "400x400")
        })
        dbUser = rows[1]   
        FollowersInfo.append( {
                'Screen_Name': dbUser['Screen_Name'],
                'Name': dbUser['Name'],
                'Description': dbUser['Description'],
                'followers_count': dbUser['Followers_Count'],
                'friends_count': dbUser['Friends_Count'],
                'statuses_count': dbUser['Statuses_Count'],
                'favourites_count': dbUser['Favourites_Count'],
                'Profile_Image_Url': dbUser['Profile_Image_Url'].replace("normal", "400x400")
        })
    return FollowersInfo