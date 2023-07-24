import mysql.connector
import configparser
from instagrapi.mixins.media import MediaMixin
from instagrapi.types import Media, User, UserShort

CONFIG_PATH = './config.ini'

class dbMannager:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        db_host = config.get('Database', 'host')
        db_username = config.get('Database', 'username')
        db_password = config.get('Database', 'password')
        db_database = config.get('Database', 'database')
        self.conn = mysql.connector.connect(
            host = db_host,
            user = db_username,
            password = db_password,
            database = db_database
        )
        
    def disconnect(self):
        if self.conn:
            self.conn.close()
        
    def updateUserInfo(self, User: User, amount: int =5):
        mediaMixin = MediaMixin()
        UserName = User.username
        FullName = User.full_name
        UserID = int(User.pk)
        FollowrCount = User.follower_count
        email = User.public_email
        homePageLink = 'https://instagram/' + UserName
        recentlyWorks = mediaMixin.user_medias(UserID, amount)
        
        sqlInsertUsers = 'INSERT INTO %s VALUES (%s, %s, %s, %s, %s, %s)'
        sqlInsertUser_posts = 'INSERT INTO %s VALUES (%s, %s, %s, %s, %s, %s)'
        
        cursor = self.conn.cursor()
        # 添加红人
        cursor.execute(sqlInsertUsers, ('users', UserID, UserName, homePageLink, FollowrCount, email, FullName))
        # 最近更新
        for media in recentlyWorks:
            mediaUser = media.user.username
            mediaUrl = 'http://instagram/p/' + media.code
            likeCount = media.like_count
            meidaUserID = int(media.user.pk)
            commentCount = media.comment_count
            mediaTime = media.taken_at.strftime("%Y-%m-%d")
            cursor.execute(sqlInsertUser_posts, ('user_posts', mediaUser, mediaUrl, likeCount, meidaUserID, commentCount, mediaTime))
        
        
        