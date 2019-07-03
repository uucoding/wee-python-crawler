#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import json
import re
import time
import multiprocessing

from com.weecoding.crawler.web.lagou.lagou_sql_operate import lagouSqlOperate
from com.weecoding.crawler.request.request import CrawlerRequest
from com.weecoding.crawler.utils.string_utils import StringUtils


class LagouCrawler:
    '''
        拉钩爬虫
    '''
    def __init__(self):
        # 自定义请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        # 城市信息 list
        self.city_list = ''
        # 岗位信息 list
        self.work_type_list = ''
        #获取基础的爬虫请求
        self.crawler_request = CrawlerRequest()
        #异常类别数据：work_type:city_list
        self.except_data = {}

    #获取所有的岗位
    def crawler_work_type_list(self):
        '''
            获取所有岗位类型
        :return:
        '''
        work_type_url = "https://www.lagou.com/"
        result = self.crawler_request.get(url=work_type_url, clear_cookie=True)
        work_type_regx = re.compile(r'<a href="https://www\.lagou\.com/zhaopin/.*" data-lg-tj-id=".*" data-lg-tj-no=".*" data-lg-tj-cid=".*".*>(.*)</a>')
        # 使用正则表达式获取匹配的城市列表: 存在重复数据需要做一次去重
        self.work_type_list = list(set(work_type_regx.findall(result)))

    def crawler_city_list(self):
        '''
            获取所有的城市
        :return:
        '''
        #获取城市的URL
        city_url = "https://www.lagou.com/jobs/allCity.html"
        #获取全部城市的网页信息 : 此处获取之后需要清除cookie，后面的请求不能携带此请求设置的cookie
        result = self.crawler_request.get(url=city_url, clear_cookie= True)
        # 分析网页，构造获取城市的正则匹配
        city_regx = re.compile(r'https://www\.lagou\.com/.*/">(.+)</a>')
        # 使用正则表达式获取匹配的城市列表: 存在重复数据需要做一次去重
        self.city_list = list(set(city_regx.findall(result)))


    def crawler_job_info(self, work_type, city):
        '''
            爬取工作岗位信息
        :param work_type: 工作岗位类型
        :param city:        城市
        :param total_page: 总计页码
        :return:
        '''
        #初始化cookie，并获取页码
        total_page = self.__crawler_set_cookie(work_type=work_type, city=city)
        print("【%s】【%s】岗位信息，共计【%s】页" % (city, work_type, total_page))
        if total_page != 'exception':
            for page in range(1, int(total_page) + 1):
                print("【%s】爬取【%s】岗位,第【%s】页" % (city, work_type, page))
                # 组装获取job的url
                job_url = StringUtils.formart_temp(
                    "https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false",city)
                # 组装referer URL
                referer_url = StringUtils.formart_temp(
                    "https://www.lagou.com/jobs/list_{}?city={}&cl=false&fromSearch=true&labelWords=&suginput=", work_type, city)
                # referer的url需要编码
                self.headers['Referer'] = referer_url.encode();
                # 获取招聘信息: 此处可能会产生错误，所以需要重试机制
                while (True):
                    try:
                        data = {
                            "pn": page,
                            "kd": work_type
                        }
                        result = self.crawler_request.post(url=job_url, data=data, headers=self.headers)
                        #文本转成json
                        json_result = json.loads(result)
                        #获取工作信息
                        if json_result['content']:
                            if json_result['content']['positionResult']:
                                if json_result['content']['positionResult']['result']:
                                    json_job_list = json_result['content']['positionResult']['result']
                                    for json_job in json_job_list:
                                        lagouSqlOperate.save(json_job, work_type)
                        else:
                            print("【%s】暂无【%s】岗位信息"%(city, work_type))
                    except:
                        print("请求岗位异常：重新加载cookie")
                        self.__retry_init_cookie(work_type=work_type, city=city)
                        continue
                    if "您操作太频繁,请稍后再访问" in result:
                        print("操作频繁：重新加载cookie")
                        self.__retry_init_cookie(work_type=work_type, city=city)
                        continue
                    break
        else:
            #获取当前类别下的有问题的城市
            city_list = self.except_data.get(work_type)
            #如果城市不存在，初始化
            if city_list:
                city_list = []
            #存储有问题的数据：用来追溯
            city_list.append(city)
            self.except_data[work_type] = city_list;

    def __crawler_set_cookie(self, work_type, city):
        '''
            获取cookie 和页码
        :param work_type: 工作类型：python 、java 等
        :param city: 城市
        :return:
        '''
        count = 0
        while (True):
            print("初始化cookie")
            #构建获取cookie的url
            init_cookie_url = StringUtils.formart_temp("https://www.lagou.com/jobs/list_{}?city={}", work_type, city)
            #发送请求：获取cookie、获取页面页码
            result = self.crawler_request.get(url=init_cookie_url)
            #设置获取页码的正则
            job_page_total_number_regx = re.compile(r'<span class="span\stotalNum">(\d+)</span>')
            #获取页码
            try:
                #网络问题 or 重定向 会导致拉钩页面获取不到页码，此时会抛出异常，需要重试
                job_page_total_number = job_page_total_number_regx.search(result).group(1)
            except:
                count += 1
                if count == 2:
                    # 匹配异常，返回exception
                    return 'exception'
                # 重新初始化cookie
                print("获取页码异常：重新初始化cookie")
                self.__retry_init_cookie(work_type, city)
                continue
            else:
                return job_page_total_number

    def __retry_init_cookie(self, work_type, city):
        '''
            重试：初始化cookie
        :param work_type:
        :param city:
        :return:
        '''
        # 清除cookie信息
        self.crawler_request.session.cookies.clear()
        # 重新设置cookie
        self.__crawler_set_cookie(work_type=work_type, city=city)
        # 休息10s后重新发送请求
        time.sleep(10)

if __name__ == '__main__':
    lagouCrawler = LagouCrawler()
    #获取城市信息
    lagouCrawler.crawler_city_list()
    #抓取工作类别
    lagouCrawler.crawler_work_type_list()
    # 引入多进程,加速抓取
    processPool = multiprocessing.Pool(4)
    # 爬取所有类别的所有信息
    # for work_type in lagouCrawler.work_type_list:
    #     for city in lagouCrawler.city_list:
    #         print('开始爬取【%s】=【%s】岗位信息' %(city, work_type))
    #         # 使用非阻塞方法
    #         processPool.apply_async(lagouCrawler.crawler_job_info, args=(work_type, city))
    for city in lagouCrawler.city_list:
        print('开始爬取【%s】=>【%s】岗位信息!' % (city, 'Java'))
        # 使用非阻塞方法
        processPool.apply_async(lagouCrawler.crawler_job_info, args=('Java', city))
        break
    processPool.close()
    processPool.join()
    #输出问题数据
    print(lagouCrawler.except_data)




