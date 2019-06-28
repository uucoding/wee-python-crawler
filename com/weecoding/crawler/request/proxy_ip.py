#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import re
from urllib3.exceptions import InsecureRequestWarning

import requests


#关闭ssl校验后，会有⚠️信息，此处可以消除⚠️
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class ProxyIpPool(object):
    '''
        组装代理ip线程池
    '''
    def __init__(self):
        #ip池
        self.ip_port_pool = []
        #ip
        self.ip_list = ''
        #端口号
        self.port_list = ''
        # 请求默认的头信息
        self.default_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def get_can_use_proxy_ip(self):
        '''
            取出一个可用的代理ip, 拿不到ip代理池会重新初始化重试2次，找不到合适的代理直接退出,使用本地ip爬取数据
        :return:
        '''
        count = 0
        while (True):
            #重试2次，找不到合适的代理直接退出
            if count == 3:
                print("找不到合适的代理，启用本地ip进行爬取")
                return {}
            # 如果代理不存在，先初始化代理
            if len(self.ip_port_pool) == 0:
                self.__crawler_proxy_ip()
                print(self.ip_port_pool)
                count = count + 1
                continue;
            else:
                #遍历: 倒序可删除，但ip池中后面的ip不稳定，前面的稳定，故而正序遍历
                for index in range(len(self.ip_port_pool)):#range(len(self.ip_port_pool) - 1, -1, -1):
                    #会主动删除，但是正序删除会丢数据，为了避免数组越界，加上if拦截
                    if index > len(self.ip_port_pool) - 1:
                        #超过数组长度，跳出循环，重新再试
                        break
                    proxy = {
                        'http': "http://" + self.ip_port_pool[index],
                        'https': "http://" + self.ip_port_pool[index]
                    }
                    # 测试ip是否可用：如果可用跳出直接使用，否则重试
                    try:
                        # 校验代理是否可用
                        response = requests.get(url="http://www.baidu.com", verify=False, proxies=proxy, timeout=6, headers=self.default_headers)
                        # 如果状态码是200则表示代理可用：返回代理
                        if 200 == response.status_code:
                            print(proxy)
                            return proxy
                        else:
                            # 删除不可用的ip
                            self.ip_port_pool.pop(index)
                            continue
                    except:
                        #删除不可用的ip
                        self.ip_port_pool.pop(index)
                        continue
                    break

    def __crawler_proxy_ip(self):
        '''
            爬取代理ip（只获取第一页，越往后ip越不稳定）：https://www.xicidaili.com/nn/1
        :return:
        '''
        proxy_ip_url = 'https://www.xicidaili.com/nn/1';

        #获取响应数据
        response = requests.get(url=proxy_ip_url, headers=self.default_headers)
        #获取响应内容
        result = response.text;
        #获取所有的ip
        proxy_ip_regx = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')
        self.ip_list = proxy_ip_regx.findall(result)
        #获取所有的端口号
        proxy_port_regx = re.compile(r'<td>(\d+)</td>')
        self.port_list = proxy_port_regx.findall(result)
        # ip和端口号是一一对应的
        if len(self.ip_list) == len(self.port_list):
            for index in range(len(self.ip_list)):
                self.ip_port_pool.append(self.ip_list[index] + ':' + self.port_list[index])
        return

if __name__ == '__main__':
    proxyip = ProxyIpPool()
    print(proxyip.get_can_use_proxy_ip())


