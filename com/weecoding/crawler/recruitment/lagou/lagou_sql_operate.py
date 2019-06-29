#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import time

from com.weecoding.crawler.recruitment.lagou.lagou_position import LagouPosition
from com.weecoding.crawler.utils.sql_utils import DBSession
from com.weecoding.crawler.utils.string_utils import StringUtils


class LagouSqlOperate:

    def __init__(self):
        # 获取操作数据库的session
        self.sql_session = DBSession()

    def save(self, job_json):
        # 获取当前时间
        now = time.strftime("%Y-%m-%d", time.localtime())
        # 判断是否有重复，有就不抓
        result = self.sql_session.query(LagouPosition).filter(LagouPosition.create_time == now,
                                                              LagouPosition.position_id == job_json[
                                                                  'positionId']).first()
        if result:
            print("当前岗位信息已经存在：%s:%s:%s:%s" % (
            job_json['city'], job_json['companyShortName'], job_json['positionName'], job_json['positionId']))
            return
        else:
            #构建数据
            data = self.create_lagou_position(job_json, now)
            # 插入数据、并提交
            self.sql_session.add(data)
            self.sql_session.commit()
            print("新增岗位:%s"%job_json['positionId'])

    def create_lagou_position(self, job_json, now):
        '''
            构建待提交数据
        :param job_json:
        :param now:
        :return:
        '''
        # 插入新数据
        data = LagouPosition(
            # 岗位ID,网站提供
            position_id=job_json['positionId'],
            # 公司全称
            company_full_name=job_json['companyFullName'],
            # 公司简称
            company_short_name=job_json['companyShortName'],
            # 业务方向
            industry_field=job_json['industryField'],
            # 公司类型
            finance_stage=job_json['financeStage'],
            # 所在城市
            city=job_json['city'],
            # 公司所在区
            district=job_json['district'],
            # 经度
            longitude=job_json['longitude'],
            # 纬度
            latitude=job_json['latitude'],
            # 公司规模
            company_size=job_json['companySize'],
            # 公司福利标签
            company_label_list=StringUtils.join(job_json['companyLabelList']),
            # 岗位名称
            position_name=job_json['positionName'],
            # 岗位性质
            job_nature=job_json['jobNature'],
            # 工作年限
            work_year=job_json['workYear'],
            # 岗位标签
            position_advantage=job_json['positionAdvantage'],
            # 工资
            salary=job_json['salary'],
            # 学历
            education=job_json['education'],
            # 创建时间
            create_time=now,
        )
        return data

#实例对象
lagouSqlOperate = LagouSqlOperate()
