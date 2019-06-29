#!/usr/local/bin/python
# -*- coding: UTF-8 -*-


class StringUtils:
    def __init__(self):
        pass

    @staticmethod
    def formart_temp(temp_str, *args):
        '''
            模版url的转化：参考__main__的示例
        :param temp_str: 模版URL 使用{}设置模版
        :param args:  需要替换模版的变量
        :return:
        '''
        return temp_str.format(*args)

    @staticmethod
    def join(args=[], separator = ','):
        '''
            字符串拼接，默认使用","
        :param args:  待拼接字符串
        :param separator: 分隔符 default ,
        :return:
        '''
        return separator.join(args)

if __name__ == '__main__':
    #测试代码
    result = StringUtils.formart_temp("https://www.lagou.com/jobs/list_{}?city={}",'前端','北京')
    print(result)
    print(StringUtils.join(["a","b"]))