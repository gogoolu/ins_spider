import sys, os
from api.bot import Bot
from instagrapi.mixins.media import MediaMixin
from db.database import dbMannager

bot = Bot()
media_lst = bot.getMedia("love", amount=10)
mediaMixin = MediaMixin()
user_pklst = (bot.getUser(l) for l in media_lst if Bot.getFollower_count(bot.getUser(l)) > 10000)

db = dbMannager()
for user in user_pklst:
    db.updateUserInfo(user)
    
db.disconnect()