# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from CrawlSpider.items import CrawlspiderItem
import re

class CfSpider(CrawlSpider):
    name = 'cf'
    allowed_domains = ['circ.gov.cn']
    start_urls = ['http://bxjg.circ.gov.cn/web/site0/tab5240/']

    rules = (
        # 获取详情页url
        # follow=False表示不跟随，只提取当前页面的url。当没有callback的时候follow默认为True,当callback存在的时候follow默认为False
        # crawlspider可以自动将url补充完整
        Rule(LinkExtractor(allow=r'/web/site0/tab5240/info\d+\.htm'), callback='parse_item', follow=False),
        # 获取下一页url
        Rule(LinkExtractor(allow=r'http://bxjg.circ.gov.cn/web/site0/tab5240/module14430/page\d+\.htm'), follow=True)
    )
        # parse函数是用来提取链接的所以不能重写parse函数
    def parse_item(self, response):
        item = CrawlspiderItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        item['title'] = re.findall("<!--TitleStart-->(.*?)<!--TitleEnd-->",response.body.decode())[0]
        item['publish_date'] = re.findall("发布时间：(20\d{2}-\d{2}-\d{2})",response.body.decode())[0]
        yield item
