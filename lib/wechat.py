import requests, json, time, traceback

class wechat_corp(object):
    def __init__(self, corp_id, agent_id, secret):
        self.__corp_id = corp_id
        self.__agent_id = agent_id
        self.__secret = secret

        self.__token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid="\
                + self.__corp_id + "&corpsecret=" + self.__secret
        self.__token = ""
        self.__token_expires_time = time.time()
        self.__token_tolerance = 30

        self.__send_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
        self.__upload_url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token="

    def __get_token(self):
        try:
            if self.__token_expires_time - time.time() < self.__token_tolerance:
                req = requests.post(self.__token_url)
                data = json.loads(req.text)
                self.__token = data["access_token"]
                self.__token_expires_time = time.time() + data["expires_in"]
            print(self.__token)
            print(self.__token_expires_time)
            return True
        except:
            traceback.print_exc()
            return False

    def send_text(self, msg, touser = '', toparty = '', totag = ''):
        self.__get_token()
        send_url = self.__send_url + self.__token
        values = {\
            "touser" : touser,\
            "toparty" : toparty,\
            "totag"   : totag,\
            "msgtype" : "text",\
            "agentid" : self.__agent_id,\
            "text" : {\
                "content" : msg\
                    },\
           "safe":0\
        }
        req = requests.post(send_url, json.dumps(values))
        print(req)
        return True

    def send_img(self, msg = '', touser = '', toparty = '', totag = ''):
        self.__get_token()
        send_url = self.__send_url + self.__token
        values = {\
            "touser" : touser,\
            "toparty" : toparty,\
            "totag"   : totag,\
            "msgtype" : "image",\
            "agentid" : self.__agent_id,\
            "image" : {\
                "media_id" : msg\
                    },\
           "safe":0\
        }
        req = requests.post(send_url, json.dumps(values))
        print(req)
        return True

    def send_text_card(self, title = 'na', msg = 'na', url = '127.0.0.1', btntxt = '', touser = '', toparty = '', totag = ''):
        self.__get_token()
        send_url = self.__send_url + self.__token
        values = {\
	    "touser" : touser,\
            "toparty" : toparty,\
            "totag"   : totag,\
	    "msgtype" : "textcard",
            "agentid" : self.__agent_id,\
	    "textcard" : {
		    "title" : title,
		    "description" : msg,
		    "url" : url,
		    "btntxt":btntxt
		}
	    }
        print(values)
        req = requests.post(send_url, json.dumps(values))
        print(json.dumps(values))
        print(req.text)
        return True
    def post_img(self, msg):
        self.__get_token()
        send_url = self.__upload_url + self.__token + "&type=image"
        files = {'media': open(msg, 'rb')}
        req = requests.post(send_url, files=files)
        print(req.text)
        return req.text


