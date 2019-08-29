# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http.cookies import CookieJar
import json
from scrapy.loader import ItemLoader
from Lagou.items import LagouItem, LagouItemLoader


class LagouSpider(CrawlSpider):
    name = 'lagou_2'
    allowed_domains = ['www.lagou.com']
    start_urls = [
        'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=']
    json_api = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'

    def start_requests(self):
        # 访问职位列表首页,获取cookies并通过 cookiejar 传入访问api的函数中
        cookiejar = CookieJar()
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.get_API, meta={'cookiejar': cookiejar})

    def get_API(self, response):
        # api分页 post表单数据
        for pn in range(1, 50):
            postdata = {
                'first': 'false',
                'pn': str(pn),
                'kd': 'Python',
                'sid': 'c4d693012ca840a1ae4bac553cea8f19',
            }
            yield scrapy.FormRequest(url=self.json_api,
                                     formdata=postdata,
                                     meta={
                                         'cookiejar': response.meta['cookiejar'],
                                         'pn': pn,
                                     },
                                     callback=self.parse_item,
                                     dont_filter=True,)

    def parse_item(self, response):
        pn = response.meta['pn']
        print('Json API 第%s开始解析' % pn)

        print(response.text)
        data_list = json.loads(response.text)
        for position in data_list['content']['positionResult']['result']:
            loader = LagouItemLoader(item=LagouItem(), response=response)

            loader.add_value('position_name', position['positionName'])
            loader.add_value('exp_lvl', position['workYear'])
            loader.add_value('edu_lvl', position['education'])
            loader.add_value('position_type', position['jobNature'])
            loader.add_value('position_id', str(position['positionId']))
            loader.add_value(
                'position_url', 'https://www.lagou.com/jobs/' + str(position['positionId']) + '.html')
            loader.add_value('finance_stage', position['financeStage'])
            loader.add_value('industry_field', position['industryField'])
            loader.add_value('company_name', position['companyFullName'])
            loader.add_value('work_city', position['city'])
            loader.add_value('salary', position['salary'])
            loader.add_value('position_advantage',
                             position['positionAdvantage'])
            loader.add_value('publish_date', position['createTime'])
            if position['companyLabelList']:
                loader.add_value('company_attr', position['companyLabelList'])
            else:
                loader.add_value('company_attr', 'None')
            if position['skillLables']:
                loader.add_value('skill_label', position['skillLables'])
            else:
                loader.add_value('skill_label', 'None')

            item = loader.load_item()
            # print(item)
            # break
            yield item

    def show_response(self, response):
        pn = response.meta['pn']
        print('Json API 第%s开始解析' % pn)

        print(response.text)
