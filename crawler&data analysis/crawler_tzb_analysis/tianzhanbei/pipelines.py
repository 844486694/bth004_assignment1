# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os
import MySQLdb.cursors
from twisted.enterprise import adbapi

class TheseusPipeline():
    def __init__(self,dbpool):
        self.dbpool=dbpool

    # pipeline默认调用
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    # 写入数据库中
    def _conditional_insert(self, tx, item):
        # print item['name']
        sql = "insert into theseus_paper(paper,author,url,subject,category,keyword,year,institution,degree) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (item["paper"],item["author"], item["url"],item['subject'],item["cate"],item["keyword"],item["year"]
                  ,item["institution"],item["degree"])
        tx.execute(sql, params)

    #错误处理方法
    def _handle_error(self, failue, item, spider):
        print(failue)

    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
		   2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
		   3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        dbparams = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到




class TianzhanbeiPipeline(object):
    pass
    # def __init__(self):
    #     # csv文件的位置,无需事先创建
    #     store_file = os.path.dirname(__file__) + '/spiders/date.csv'
    #     # 打开(创建)文件
    #     self.file = open(store_file, 'wb')
    #     # csv写法
    #     self.writer = csv.writer(self.file)
    #
    # def process_item(self, item, spider):
    #     # 判断字段值不为空再写入文件
    #     if item['name']:
    #         self.writer.writerow(bytes((item["category"], 'utf-8'),bytes(item['name'], 'utf-8'),bytes( item['origin'], 'utf-8')))
    #     return item
    #
    # def close_spider(self, spider):
    #     # 关闭爬虫时顺便将文件保存退出
    #     self.file.close()


