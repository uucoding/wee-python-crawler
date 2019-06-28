#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import requests
from urllib3.exceptions import InsecureRequestWarning

from com.weecoding.crawler.request.proxy_ip import ProxyIpPool


#关闭ssl校验后，会有⚠️信息，此处可以消除⚠️0
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class CrawlerRequest(ProxyIpPool):
    '''
        爬虫的相关请求设置
    '''
    def __init__(self):
        super(CrawlerRequest, self).__init__()
        #使用session设置相关的cookie
        self.session = requests.session()

    def get(self, url, clear_cookie=False, **headers):
        '''
            get请求
        :param url:  请求的url
        :param headers:   请求的头信息
        :return:
        '''
        return self.__request(method='GET', url=url, clear_cookie=clear_cookie, **headers)

    def post(self, url, data=None, clear_cookie=False, **headers):
        '''
            post请求
        :param url:  请求的url
        :param data: 请求的参数
        :param headers:   请求的头信息
        :return:
        '''
        return self.__request(method='POST', url=url, data=data, clear_cookie=clear_cookie, **headers)

    def search_url(self, formart_url, search_key):
        '''
        模版url的转化
        :param formart_url: 模版URL 使用{}设置模版
        :param search_key:  需要替换模版的变量 - 集合形式
        :return:
        '''
        return formart_url.format(*search_key)


    def __request(self, method, url, data=None, clear_cookie=False, **headers):
        '''
            通用请求设置:对外不可见
        :param method: 请求的方法
        :param url:    请求的url
        :param data:   请求的参数
        :param clear_cookie:   是否清除cookie，默认不清除
        :param headers:   请求的头信息
        :return:
        '''
        #如果请求头不存在，那么设置为默认请求头
        if headers == {}:
            headers = {
                "headers": self.default_headers
            }
        #设置阿布云代理（新用户可以免费适用一小时）
        # proxy_info = self.search_url("http://{}:{}@{}:{}", ['HH61OT5D4ZAZ8MZD', '93FB7F6730FB318E', 'http-dyn.abuyun.com', '9020'])
        # proxy = {
        #     'http': proxy_info,
        #     'https': proxy_info
        # }
        #获取代理ip配置
        proxy = self.get_can_use_proxy_ip()
        # proxy = {}
        #如果代理为空，表示代理不存在，那么使用本地
        if proxy == {}:
            use_proxies = False
        else:
            use_proxies = True
            # 代理不稳定：本地不使用代理
            # use_proxies = False
        count = 1
        #出错后重试：允许重试两次,两次不成功返回空字符串
        while(True):
            print("请求【%s】第【%d】次" % (url, count))
            if count == 3:
                return ''
            try:
                # 判断请求方式
                if method == 'GET':
                    # verify = False关掉ssl校验
                    if use_proxies:
                        response = self.session.get(url=url, verify=False, proxies=proxy, timeout=6, **headers)
                        print(response)
                    else:
                        response = self.session.get(url=url, verify=False, timeout=6, **headers)
                elif method == 'POST':
                    if use_proxies:
                       response = self.session.post(url=url, data=data, verify=False, proxies=proxy, timeout=6, **headers)
                    else:
                        response = self.session.post(url=url, data=data, verify=False, timeout=6, **headers)
                else:
                    print("暂不支持该请求%s" % method)
            except:
                print("=============")
                #重试
                count += 1
                continue
            break
        #清除cookie
        if clear_cookie:
            self.session.cookies.clear()
        #设置编码
        response.encoding = 'urf-8'
        return response.text;


if __name__ == '__main__':
    crawler = CrawlerRequest()
    formart_url = "https://www.lagou.com/jobs/list_{}?city={}"
    url = crawler.search_url(formart_url, ['前端','北京'])
    print(url)