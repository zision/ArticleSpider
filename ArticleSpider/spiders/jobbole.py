# -*- coding: utf-8 -*-
import re

import scrapy


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/113744/']

    def parse(self, response):
        title = response.xpath('//*[@class="entry-header"]/h1/text()').extract()[0].strip()
        creat_data = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].replace("·", "").strip()
        dianzan_num = response.xpath("//div[@class='post-adds']/span[1]/h10[1]/text()").extract()[0].strip()
        match_re = re.match('.*(\d+).*', response.xpath("//div[@class='post-adds']/span[2]/text()").extract()[0].strip())
        shoucang_num = '0'
        if match_re:
            shoucang_num = match_re.group(1)
        match_re = re.match('.*(\d+).*', response.xpath("//div[@class='post-adds']/a[1]/span[1]/text()").extract()[0].strip())
        pinglun_num = '0'
        if match_re:
            pinglun_num = match_re.group(1)
        pass
