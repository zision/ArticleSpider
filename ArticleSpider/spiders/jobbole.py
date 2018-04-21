# -*- coding: utf-8 -*-
import re
from urllib import parse
import scrapy
from scrapy import Request


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        '''
        1. 获取文章列表页中的文章url并交给scrapy进行解析
        2. 获取下一页的url并交给scrapy进行下载
        '''

        # 解析所有文章页的url进行下载与解析
        post_urls = response.css("#archive .floated-thumb .post-thumb a::attr(href)").extract()
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)

        # 提取下一页并交给scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)


    def parse_detail(self, response):
        # 提取文章的具体字段
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
