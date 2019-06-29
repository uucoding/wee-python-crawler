#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
from com.weecoding.crawler.utils.string_utils import StringUtils


class AbuyunProxy(object):
    def __init__(self):
        pass

    @staticmethod
    def get_ip():
        '''
            获取一个阿布云的代理ip：模版参数依次为：通行证书、密钥、主机、端口
            购买后可见/新用户可以体验
        :return:
        '''
        proxy_info = StringUtils.formart_temp("http://{}:{}@{}:{}", 'HA22492FSA106HND', '2A3CA7CC95E19B2A', 'http-dyn.abuyun.com', '9020')
        proxy = {
            'http': proxy_info,
            'https': proxy_info
        }
        return proxy
