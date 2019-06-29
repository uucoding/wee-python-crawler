#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

from sqlalchemy import Integer,String,Float
from sqlalchemy import Column
from com.weecoding.crawler.utils.sql_utils import Base, engine


class LagouPosition(Base):
    '''
        拉钩职位表
    '''
    #表名称
    __tablename__ = 'lagou_position'
    #id,设置为主键和自动增长
    id = Column(Integer,primary_key=True,autoincrement=True)
    #岗位ID,网站提供
    position_id = Column(Integer,nullable=False, comment='岗位ID')
    # 公司全称
    company_full_name = Column(String(length=200), nullable=True, comment='公司全称')
    # 公司简称
    company_short_name = Column(String(length=50), nullable=True, comment='公司简称')
    # 业务方向
    industry_field = Column(String(length=30), nullable=True, comment='业务方向')
    # 公司类型
    finance_stage = Column(String(length=30), nullable=True, comment='公司类型')
    # 所在城市
    city = Column(String(length=10), nullable=True, comment='所在城市')
    # 公司所在区
    district = Column(String(length=20), nullable=True, comment='公司所在区')
    # 经度
    longitude = Column(Float, nullable=True, comment='经度')
    # 纬度
    latitude = Column(Float, nullable=True, comment='纬度')
    # 公司规模
    company_size = Column(String(length=30), nullable=True, comment='公司规模')
    # 公司福利标签
    company_label_list = Column(String(length=200), nullable=True, comment='公司福利标签')
    # 岗位名称
    position_name = Column(String(length=50), nullable=True, comment='岗位名称')
    # 岗位性质
    job_nature = Column(String(length=20), nullable=True, comment='岗位性质')
    # 工作年限
    work_year = Column(String(length=20), nullable=True, comment='工作年限')
    # 岗位标签
    position_advantage = Column(String(length=200), nullable=True, comment='岗位标签')
    # 工资
    salary = Column(String(length=20), nullable=True, comment='工资')
    # 学历
    education = Column(String(length=20), nullable=True, comment='学历')
    # 创建时间
    create_time = Column(String(length=20), nullable=False, comment='创建时间')



if __name__ == '__main__':
    LagouPosition.metadata.create_all(engine)