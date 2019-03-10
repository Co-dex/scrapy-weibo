# -*- coding: utf-8 -*-
import re
from scrapy import Spider, FormRequest, Request
from weibo.items import WeiboItem
import logging


class lianghuiSpider(Spider):
    name = '感冒'
    allowed_domains = ['weibo.cn']
    search_url = 'https://weibo.cn/search/mblog'
    max_page = 100
    logger = logging.getLogger(__name__)
    keyword = ""

    def start_requests(self):
        self.keyword = self.name
        url = '{url}?keyword={keyword}'.format(url=self.search_url, keyword=self.keyword)
        for page in range(1, self.max_page + 1):
            data = {
                'mp': str(self.max_page),
                'page': str(page)
            }
            yield FormRequest(url, callback=self.parse_index, formdata=data)

    def parse_index(self, response):
        weibos = response.xpath('//div[@class="c" and contains(@id, "M_")]')
        for weibo in weibos:
            is_forward = bool(weibo.xpath('.//span[@class="cmt"]').extract_first())
            if is_forward:
                detail_url = weibo.xpath('.//a[contains(., "原文评论[")]//@href').extract_first()
            else:
                detail_url = weibo.xpath('.//a[contains(., "评论[")]//@href').extract_first()
            yield Request(detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        print('-----parse_detail------')
        collection = self.name  # collection 名称赋值
        print("Collection Name: ", collection)
        id = re.search('comment/(.*?)\?', response.url).group(1)
        url = response.url
        content = ''.join(response.xpath('//div[@id="M_"]//span[@class="ctt"]//text()').extract())
        print(id, url, content)
        comment_count = response.xpath('//span[@class="pms"]//text()').re_first('评论\[(.*?)\]')
        forward_count = response.xpath('//a[contains(., "转发[")]//text()').re_first('转发\[(.*?)\]')
        like_count = response.xpath('//a[contains(., "赞[")]//text()').re_first('赞\[(.*?)\]')
        print('转发： {} 评论： {} 赞： {}'.format(comment_count, forward_count, like_count))
        posted_at = response.xpath('//div[@id="M_"]//span[@class="ct"]//text()').extract_first(default=None)
        user = response.xpath('//div[@id="M_"]/div/a/text()').extract_first(default=None)
        print(posted_at, user)
        weibo_item = WeiboItem()
        for field in weibo_item.fields:
            try:
                weibo_item[field] = eval(field)
            except NameError:
                self.logger.debug('Field No Defined!' + field)
        yield weibo_item

    def parse(self, response):
        pass
