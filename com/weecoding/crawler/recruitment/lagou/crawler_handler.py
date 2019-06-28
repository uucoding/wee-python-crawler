#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import re
import time
import multiprocessing

from com.weecoding.crawler.request.request import CrawlerRequest

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

    #获取所有的岗位
    def crawler_work_type_list(self):
        # todo 等待完善
        pass

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
        if total_page != 'exception':
            for page in range(1, int(total_page) + 1):
                # 组装获取job的url
                job_url = self.crawler_request.search_url(
                    "https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false",
                    [city])
                # 组装referer URL
                referer_url = self.crawler_request.search_url(
                    "https://www.lagou.com/jobs/list_{}?city={}&cl=false&fromSearch=true&labelWords=&suginput=",
                    [work_type, city])
                # referer的url需要编码
                self.headers['Referer'] = referer_url.encode();
                # 获取招聘信息: 此处可能会产生错误，所以需要重试机制
                while (True):
                    try:
                        result = self.crawler_request.post(url=job_url, headers=self.headers)
                        print(result)
                    except:
                        print("请求异常：准备重试")
                        self.__retry_init_cookie(work_type=work_type, city=city)
                        continue
                    if "您操作太频繁,请稍后再访问" in result:
                        print("操作频繁：准备重试")
                        self.__retry_init_cookie(work_type=work_type, city=city)
                        continue
                    break

    def __crawler_set_cookie(self, work_type, city):
        '''
            获取cookie 和页码
        :param work_type: 工作类型：python 、java 等
        :param city: 城市
        :return:
        '''
        #构建获取cookie的url
        init_cookie_url = self.crawler_request.search_url("https://www.lagou.com/jobs/list_{}?city={}", [work_type, city])
        #发送请求：获取cookie、获取页面页码
        result = self.crawler_request.get(url=init_cookie_url)
        #设置获取页码的正则
        job_page_total_number_regx = re.compile(r'<span class="span\stotalNum">(\d+)</span>')

        #获取页码
        try:
            job_page_total_number = job_page_total_number_regx.search(result).group(1)
        except:
            #匹配异常，返回exception
            return 'exception';
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
    #引入多进程
    processPool = multiprocessing.Pool(3)
    #
    for city in lagouCrawler.city_list:
        processPool.apply_async(lagouCrawler.crawler_job_info, args=('python', '北京'))
        break;
    processPool.close()
    processPool.join()
