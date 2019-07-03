#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base();

# 初始化数据库的连接
engine = create_engine("mysql+pymysql://root:123456@localhost:3306/crawler?charset=utf8")

#创建一个session, 用于操作数据库
DBSession = sessionmaker(bind=engine)

