from flask_mysqldb import MySQLdb

# Configure DB
conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="MyTwitter_bots", charset='utf8mb4')
myCursor = conn.cursor(MySQLdb.cursors.DictCursor)


def insertUser(myUser):
    sql = "INSERT INTO User (idUser, Name, Description, followers_count, friends_count, statuses_count, favourites_count, default_profile, default_profile_image, lang, screen_name, verified, created_at, Profile_Image_Url, protected) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"  
    insertUser = (myUser.id, myUser.name, myUser.description, myUser.followers_count, myUser.friends_count, myUser.statuses_count, myUser.favourites_count, myUser.default_profile, myUser.default_profile_image, myUser.lang, myUser.screen_name, myUser.verified, myUser.created_at, myUser.profile_image_url, myUser.protected)
    myCursor.execute(sql, insertUser)
    conn.commit()


def insertFollower(myUser, myFollower):
    insertUser(myFollower)
    sql = "INSERT INTO UserFollower (idUser, idFollower) VALUES (%s, %s) " % (myUser.id, myFollower.id)
    myCursor.execute(sql)
    conn.commit()


def calculateFollowerMatrix(screen_name):
    args = [screen_name]
    myCursor.callproc('insertMatrixInformation_noTweetTable', args)
    conn.commit()

def selectUserId(screen_name):
    sql = "SELECT idUser FROM USER WHERE screen_name  = '%s'" %(screen_name)
    myCursor.execute(sql)
    return myCursor.fetchone()

def selectUserInfo(screen_name):
    sql = "SELECT * FROM USER WHERE screen_name  = '%s'" %(screen_name)
    myCursor.execute(sql)
    return myCursor.fetchone()

def selectSavedFollowersCount(screen_name):
    sql = "SELECT count(*) FROM UserFollower WHERE idUser  = (SELECT idUser FROM User WHERE Screen_name = '%s')" %(screen_name)
    myCursor.execute(sql)
    return myCursor.fetchone() 


def selectMatrixResults(id):
    sql = "SELECT * FROM "
    sql = sql + "(SELECT count(score) as Genuine FROM Matrix WHERE Score < 3 AND  idFollowing = %s) t1 , " %id
    sql = sql + "(SELECT count(score) as Suspicious FROM Matrix WHERE Score = 3 AND  idFollowing = %s) t2 , " %id
    sql = sql + "(SELECT count(score) as Bots FROM Matrix WHERE Score > 3 AND  idFollowing = %s) t3" %id
    myCursor.execute(sql)
    return myCursor.fetchone() 

def selectGenuineExamples(id):
    # sql = "SELECT * FROM User INNER JOIN (SELECT * FROM Matrix WHERE Score < 3 AND Score >= 0  AND idFollowing = %s ORDER BY Score LIMIT 2) as Matrix ON User.idUser = Matrix.idUser" %id
    sql = "SELECT * FROM User INNER JOIN (SELECT * FROM Matrix WHERE Score < 3 AND Score >= 0  AND idFollowing = %s) as Matrix ON User.idUser = Matrix.idUser WHERE Protected = 0  ORDER BY Score, Name  LIMIT 2" %id
    myCursor.execute(sql)
    return myCursor.fetchall() 

def selectSuspiciousExamples(id):
    # sql = "SELECT * FROM User INNER JOIN (SELECT * FROM Matrix WHERE Score = 3 AND idFollowing = %s ORDER BY Score LIMIT 2) as Matrix ON User.idUser = Matrix.idUser" %id
    sql = "SELECT * FROM User INNER JOIN (SELECT * FROM Matrix WHERE Score = 3  AND idFollowing = %s) as Matrix ON User.idUser = Matrix.idUser WHERE Protected = 0  ORDER BY Score desc  LIMIT 2" %id
    myCursor.execute(sql)
    return myCursor.fetchall() 

def selectBotsExamples(id):
    # sql = "SELECT * FROM User INNER JOIN (SELECT * FROM Matrix WHERE Score > 3 AND Score < 10  AND idFollowing = %s ORDER BY Score desc LIMIT 2) as Matrix ON User.idUser = Matrix.idUser" %id

    sql = "SELECT * FROM User INNER JOIN (SELECT * FROM Matrix WHERE Score > 3 AND Score < 10  AND idFollowing = %s) as Matrix ON User.idUser = Matrix.idUser WHERE Protected = 0  ORDER BY Score desc  LIMIT 2" %id
    myCursor.execute(sql)
    return myCursor.fetchall() 


def deleteUserAndFollowers(idUser):
    sql = "DELETE FROM User WHERE idUser = (SELECT idFollower FROM UserFollower WHERE idUser = %s)" % (idUser)
    myCursor.execute(sql)
    sql = "DELETE FROM UserFollower WHERE idUser = %s" % (idUser)
    myCursor.execute(sql)
    conn.commit()

    deleteUser(idUser)

def deleteUser(idUser):
    sql = "DELETE FROM User WHERE idUser = %s" % (idUser)
    myCursor.execute(sql)
    conn.commit()


def deleteFollowerMatrix(idUser):
    sql = "SET SQL_SAFE_UPDATES = 0;"
    myCursor.execute(sql)
    sql =  "DELETE From Matrix where idFollowing = %s;" %idUser
    myCursor.execute(sql)
    sql =  "SET SQL_SAFE_UPDATES = 1;"
    myCursor.execute(sql)
    conn.commit()
#args = [0]
# outputProcedure = myCursor.callproc('simpleproc', args)
# flash(f'Output of procedure {outputProcedure} !', 'danger')