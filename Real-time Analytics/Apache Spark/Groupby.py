# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import findspark
import pyspark
findspark.init()
findspark.find()
from pyspark.sql import SparkSession

spark = SparkSession.builder.master('spark://172.27.80.1:7077').appName('GroupBy').getOrCreate()

spark

df = spark.read.csv('file:///C:/pythonworks/210714/sales_info.csv', inferSchema=True, header=True)

df.head(2)

df.printSchema()

df.groupBy('Company')

#mean, max, sum,max, count 등 groupby 모두 가능
df.groupBy('Company').mean().show()

df.groupBy('Company').max().show()

# [사용자 정의함수 aggregation = agg]

df.agg({'Sales':'max'}).show()

grouped = df.groupBy('company')

grouped.agg({'Sales':'max'}).show()

#spark 제공 함수 사용 모듈 -> 실제 spark 이용시 쓰는게 잘 된다
from pyspark.sql.functions import countDistinct, avg, stddev

#중복값 제거하고 고유값 갯수
df.select(countDistinct('Sales')).show()

#alias = col이름 재정의 가능
df.select(countDistinct('Sales').alias('Distinct Sales')).show()

#sales 평균
df.select(avg('Sales').alias('avg Sales')).show()

#소숫점 자릿수 지정
from pyspark.sql.functions import format_number

sales_std = df.select(stddev('Sales').alias('std'))

#자릿수 김
sales_std.show()

#소숫점 3자리까지 지정 -> 실무에선 도메인 전문가와 협의
sales_std.select(format_number('std',3)).show()

#오름차순 default
df.orderBy('Sales').show()

#desc시 col자체에 정렬을 걸로 orderby에 넣어야됨
df.orderBy((df['Sales']).desc()).show()
