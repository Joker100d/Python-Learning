# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors


class LagouMysqlPipeline(object):
    # 写入 Mysql
    def __init__(self):
        self.conn = MySQLdb.connect(
            'localhost', 'root', 'root', 'scrapyspider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = '''
            INSERT INTO Lagou_API(position_name,exp_lvl,edu_lvl,position_type,position_id,position_url,finance_stage,industry_field,company_name,work_city,salary,position_advantage,publish_date,company_attr,skill_label)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        self.cursor.execute(
            insert_sql, (item['position_name'], item['exp_lvl'], item['edu_lvl'], item['position_type'], item['position_id'], item['position_url'], item['finance_stage'], item['industry_field'], item['company_name'], item['work_city'], item['salary'], item['position_advantage'], item['publish_date'], item['company_attr'], item['skill_label']))
        self.conn.commit()


class LagouTwistedPipeline(object):
     # 初始化时 调用settings里面的配置
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
    # 实例化twisted异步容器
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入异步化
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        # 处理异步插入异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行insert
        insert_sql = '''
            INSERT INTO Lagou_API(position_name,exp_lvl,edu_lvl,position_type,position_id,position_url,finance_stage,industry_field,company_name,work_city,salary,position_advantage,publish_date,company_attr,skill_label)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        cursor.execute(
            insert_sql, (item['position_name'], item['exp_lvl'], item['edu_lvl'], item['position_type'], item['position_id'], item['position_url'], item['finance_stage'], item['industry_field'], item['company_name'], item['work_city'], item['salary'], item['position_advantage'], item['publish_date'], item['company_attr'], item['skill_label']))
