#!/opt/conda/bin/python3
# -*- coding: utf-8 -*-

import itchatmp
import lib.tuling as tuling
import lib.wechat
import traceback
import settings
from pprint import pprint
import pymongo

itchatmp.update_config(itchatmp.WechatConfig(
    token = settings.WC_CHAT_TOKEN,
    copId = settings.WC_CHAT_CORP_ID,
    appSecret = settings.WC_CHAT_SECRET,
    encryptMode = itchatmp.content.SAFE,
    encodingAesKey = settings.WC_CHAT_AESKEY))

r2d2 = tuling.tuling(settings.TULING)

wc_api = lib.wechat.wechat_corp(settings.WC_CHAT_CORP_ID,\
         settings.WC_CHAT_AGENT_ID,\
         settings.WC_CHAT_SECRET)

@itchatmp.msg_register(itchatmp.content.INCOME_MSG)
def text_reply(msg):
    try:
        print(msg)
        #msg = json.loads(msg)
        if 'MsgType' not in msg:
            return
        if msg['MsgType'] != 'event':
            if 'Content' in msg:
                return r2d2.talk(msg['Content'])
            else:
                return
        if 'EventKey' not in msg:
            return
        if 'FromUserName' not in msg:
            return
        if msg['EventKey'] == 'aqi_now':
            client = pymongo.MongoClient('restheart-dev-mongo', 27017)
            db = client.admin
            cursor = db.env.find({"category":"aqi"}).limit(1).sort("_id", -1)
            for each in cursor:
                data = each['text']
            print(data)
            wc_api.send_text(str(data), msg['FromUserName'])
            return

        #wc_api.post_img('period.png')
        #wc_api.send_img('3m0G3WCRfm8UUvGkhZ4Ob_2H_vWE_UY0r8zbnW9XfffFeusKU41XfpDApNEJQUdju', 'YangBin')

    except Exception:
        traceback.print_exc()

itchatmp.run()
