# -*- coding: utf-8 -*-
import re

import scrapy


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/113744/']

    def parse(self, response):
        title = response.xpath('//*[@class="entry-header"]/h1/text()').extract_first().strip()
        # extract_first() 相当于 extract()[0]且自带默认空值，不会报错
        # css选择器写法 response.css(".entry-header h1::text").extract_first().strip()
        creat_data = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract_first().replace("·", "").strip()
        # css选择器写法response.css("p.entry-meta-hide-on-mobile::text").extract()[0].replace("·", "").strip()
        dianzan_num = response.xpath("//div[@class='post-adds']/span[1]/h10[1]/text()").extract_first().strip()
        # css选择器写法response.css(".vote-post-up h10::text").extract_first()
        match_re = re.match('.*?(\d+).*', response.xpath("//div[@class='post-adds']/span[2]/text()").extract_first().strip())
        # css选择器写法response.css(".bookmark-btn::text").extract_first()
        shoucang_num = '0'
        if match_re:
            shoucang_num = match_re.group(1)
        match_re = re.match('.*?(\d+).*', response.xpath("//div[@class='post-adds']/a[1]/span[1]/text()").extract_first().strip())
        # css选择器写法response.css('a[href="#article-comment"] span::text').extract_first()
        pinglun_num = '0'
        if match_re:
            pinglun_num = match_re.group(1)
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # css选择器写法response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)
        cotent = response.xpath("//div[@class='entry']").extract_first().strip()
        # css选择器写法response.css("div.entry").extract_first()
        pass
