#coding=utf8
import sys, collections

from tornado.gen import Future

TRANSLATE = 'Chinese'
TRANSLATION = {}

class NotDict(collections.MutableMapping):
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))
    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]
    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value
    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]
    def __iter__(self):
        return iter(self.store)
    def __len__(self):
        return len(self.store)
    def __keytransform__(self, key):
        return key

class ReturnValue(NotDict, Future):
    def __init__(self, returnValueDict={}):
        # make returnvalue yieldable
        NotDict.__init__(self, **returnValueDict)
        Future.__init__(self)
        self.set_result(self)
        # init
        self._wrap_result = None
        if TRANSLATE:
            self['rawmsg'] = self.get('errmsg', '')
            self['errmsg'] = \
                TRANSLATION[TRANSLATE].get(self.get('errcode', '')) \
                or self.get('errmsg', u'没有errmsg')
            if not self['rawmsg']: self['rawmsg'] = self['errmsg']
    def __nonzero__(self):
        return self.get('errcode', -1) == 0
    def __bool__(self):
        return self.__nonzero__()
    def __str__(self):
        return '{%s}' % ', '.join(
            ['%s: %s' % (repr(k),repr(v)) for k,v in self.items()])
    def __repr__(self):
        return '<ItchatmpReturnValue: %s>' % self.__str__()

TRANSLATION = {
    'Chinese': {
        -10001: u'参数中所有非ascii字符串需要用Unicode形式传递，如：u"中文"',
        -10002: u'文件读取失败，请以"rb"打开文件并作为参数传入',
        -10003: u'传入参数有误',
        -10004: u'文件无法读取，请检查文件位置与权限',
        -10005: u'返回值不合法',
        -1: u'系统繁忙，此时请开发者稍候再试',
        0: u'请求成功',
        40001: u'获取access_token时AppSecret错误，或者access_token无效。请开发者认真比对AppSecret的正确性，或查看是否正在为恰当的公众号调用接口',
        40002: u'不合法的凭证类型',
        40003: u'不合法的OpenID，请开发者确认OpenID（该用户）是否已关注公众号，或是否是其他公众号的OpenID',
        40004: u'不合法的媒体文件类型',
        40005: u'不合法的文件类型',
        40006: u'不合法的文件大小',
        40007: u'不合法的媒体文件id',
        40008: u'不合法的消息类型',
        40009: u'不合法的图片文件大小',
        40010: u'不合法的语音文件大小',
        40011: u'不合法的视频文件大小',
        40012: u'不合法的缩略图文件大小',
        40013: u'不合法的AppID，请开发者检查AppID的正确性，避免异常字符，注意大小写',
        40014: u'不合法的access_token，请开发者认真比对access_token的有效性（如是否过期），或查看是否正在为恰当的公众号调用接口',
        40015: u'不合法的菜单类型',
        40016: u'不合法的按钮个数',
        40017: u'不合法的按钮个数',
        40018: u'不合法的按钮名字长度',
        40019: u'不合法的按钮KEY长度',
        40020: u'不合法的按钮URL长度',
        40021: u'不合法的菜单版本号',
        40022: u'不合法的子菜单级数',
        40023: u'不合法的子菜单按钮个数',
        40024: u'不合法的子菜单按钮类型',
        40025: u'不合法的子菜单按钮名字长度',
        40026: u'不合法的子菜单按钮KEY长度',
        40027: u'不合法的子菜单按钮URL长度',
        40028: u'不合法的自定义菜单使用用户',
        40029: u'不合法的oauth_code',
        40030: u'不合法的refresh_token',
        40031: u'不合法的openid列表',
        40032: u'不合法的openid列表长度',
        40033: u'不合法的请求字符，不能包含\\uxxxx格式的字符',
        40035: u'不合法的参数',
        40038: u'不合法的请求格式',
        40039: u'不合法的URL长度',
        40050: u'不合法的分组id',
        40051: u'分组名字不合法',
        40117: u'分组名字不合法',
        40118: u'media_id大小不合法',
        40119: u'button类型错误',
        40120: u'button类型错误',
        40121: u'不合法的media_id类型',
        40132: u'微信号不合法',
        40137: u'不支持的图片格式',
        40155: u'请勿添加其他公众号的主页链接',
        41001: u'缺少access_token参数',
        41002: u'缺少appid参数',
        41003: u'缺少refresh_token参数',
        41004: u'缺少secret参数',
        41005: u'缺少多媒体文件数据',
        41006: u'缺少media_id参数',
        41007: u'缺少子菜单数据',
        41008: u'缺少oauth code',
        41009: u'缺少openid',
        42001: u'access_token超时，请检查access_token的有效期，请参考基础支持-获取access_token中，对access_token的详细机制说明',
        42002: u'refresh_token超时',
        42003: u'oauth_code超时',
        42007: u'用户修改微信密码，accesstoken和refreshtoken失效，需要重新授权',
        43001: u'需要GET请求',
        43002: u'需要POST请求',
        43003: u'需要HTTPS请求',
        43004: u'需要接收者关注',
        43005: u'需要好友关系',
        43019: u'需要将接收者从黑名单中移除',
        44001: u'多媒体文件为空',
        44002: u'POST的数据包为空',
        44003: u'图文消息内容为空',
        44004: u'文本消息内容为空',
        45001: u'多媒体文件大小超过限制',
        45002: u'消息内容超过限制',
        45003: u'标题字段超过限制',
        45004: u'描述字段超过限制',
        45005: u'链接字段超过限制',
        45006: u'图片链接字段超过限制',
        45007: u'语音播放时间超过限制',
        45008: u'图文消息超过限制',
        45009: u'接口调用超过限制',
        45010: u'创建菜单个数超过限制',
        45011: u'API调用太频繁，请稍候再试',
        45015: u'回复时间超过限制',
        45016: u'系统分组，不允许修改',
        45017: u'分组名字过长',
        45018: u'分组数量超过上限',
        45047: u'客服接口下行条数超过上限',
        45056: u'创建的标签数过多，请注意不能超过100个',
        45057: u'该标签下粉丝数超过10w，不允许直接删除',
        45058: u'不能修改0/1/2这三个系统默认保留的标签',
        45059: u'有粉丝身上的标签数已经超过限制', 
        45157: u'标签名非法，请注意不能和其他标签重名',
        45158: u'标签名长度超过30个字节',
        45159: u'非法的tag_id',
        46001: u'不存在媒体数据',
        46002: u'不存在的菜单版本',
        46003: u'不存在的菜单数据',
        46004: u'不存在的用户',
        47001: u'解析JSON/XML内容错误',
        48001: u'api功能未授权，请确认公众号已获得该接口，可以在公众平台官网-开发者中心页中查看接口权限',
        48002: u'粉丝拒收消息（粉丝在公众号选项中，关闭了“接收消息”）',
        48004: u'api接口被封禁，请登录mp.weixin.qq.com查看详情',
        48005: u'api禁止删除被自动回复和自定义菜单引用的素材',
        48006: u'api禁止清零调用次数，因为清零次数达到上限',
        49003: u'传入的openid不属于此AppID',
        50001: u'用户未授权该api',
        50002: u'用户受限，可能是违规后接口被封禁',
        61451: u'参数错误(invalid parameter)',
        61452: u'无效客服账号(invalid kf_account)',
        61453: u'客服帐号已存在(kf_account exsited)',
        61454: u'客服帐号名长度超过限制(仅允许10个英文字符，不包括@及@后的公众号的微信号)(invalid   kf_acount length)',
        61455: u'客服帐号名包含非法字符(仅允许英文+数字)(illegal character in     kf_account)',
        61456: u'客服帐号个数超过限制(10个客服账号)(kf_account count exceeded)',
        61457: u'无效头像文件类型(invalid   file type)',
        61450: u'系统错误(system error)',
        61500: u'日期格式错误',
        65301: u'不存在此menuid对应的个性化菜单',
        65302: u'没有相应的用户',
        65303: u'没有默认菜单，不能创建个性化菜单',
        65304: u'MatchRule信息为空',
        65305: u'个性化菜单数量受限',
        65306: u'不支持个性化菜单的帐号',
        65307: u'个性化菜单信息为空',
        65308: u'包含没有响应类型的button',
        65309: u'个性化菜单开关处于关闭状态',
        65310: u'填写了省份或城市信息，国家信息不能为空',
        65311: u'填写了城市信息，省份信息不能为空',
        65312: u'不合法的国家信息',
        65313: u'不合法的省份信息',
        65314: u'不合法的城市信息',
        65316: u'该公众号的菜单设置了过多的域名外跳（最多跳转到3个域名的链接）',
        65317: u'不合法的URL',
        9001001: u'POST数据参数不合法',
        9001002: u'远端服务不可用',
        9001003: u'Ticket不合法',
        9001004: u'获取摇周边用户信息失败',
        9001005: u'获取商户信息失败',
        9001006: u'获取OpenID失败',
        9001007: u'上传文件缺失',
        9001008: u'上传素材的文件类型不合法',
        9001009: u'上传素材的文件尺寸不合法',
        9001010: u'上传失败',
        9001020: u'帐号不合法',
        9001021: u'已有设备激活率低于50%，不能新增设备',
        9001022: u'设备申请数不合法，必须为大于0的数字',
        9001023: u'已存在审核中的设备ID申请',
        9001024: u'一次查询设备ID数量不能超过50',
        9001025: u'设备ID不合法',
        9001026: u'页面ID不合法',
        9001027: u'页面参数不合法',
        9001028: u'一次删除页面ID数量不能超过10',
        9001029: u'页面已应用在设备中，请先解除应用关系再删除',
        9001030: u'一次查询页面ID数量不能超过50',
        9001031: u'时间区间不合法',
        9001032: u'保存设备与页面的绑定关系参数错误',
        9001033: u'门店ID不合法',
        9001034: u'设备备注信息过长',
        9001035: u'设备申请参数不合法',
        9001036: u'查询起始值begin不合法',
    },
}
