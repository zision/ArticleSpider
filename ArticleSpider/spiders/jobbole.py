# -*- coding: utf-8 -*-
import re
from urllib import parse
import scrapy
from scrapy import Request
from ArticleSpider.items import JobBoleArticleItem
from ArticleSpider.utils.common import get_md5


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
        post_nods = response.css("#archive .floated-thumb .post-thumb a")
        for post_nod in post_nods:
            image_url = post_nod.css("img::attr(src)").extract_first("")
            post_url = post_nod.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url":image_url}, callback=self.parse_detail)

        # 提取下一页并交给scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)


    def parse_detail(self, response):
        article_item = JobBoleArticleItem()
        # 提取文章的具体字段
        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        title = response.xpath('//*[@class="entry-header"]/h1/text()').extract_first().strip()
        # extract_first() 相当于 extract()[0]且自带默认空值，不会报错
        # css选择器写法 response.css(".entry-header h1::text").extract_first().strip()
        creat_data = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract_first().replace("·", "").strip()
        # css选择器写法response.css("p.entry-meta-hide-on-mobile::text").extract()[0].replace("·", "").strip()
        dianzan_nums = response.xpath("//div[@class='post-adds']/span[1]/h10[1]/text()").extract_first().strip()
        # css选择器写法response.css(".vote-post-up h10::text").extract_first()
        match_re = re.match('.*?(\d+).*', response.xpath("//div[@class='post-adds']/span[2]/text()").extract_first().strip())
        # css选择器写法response.css(".bookmark-btn::text").extract_first()
        shoucang_nums = '0'
        if match_re:
            shoucang_nums = match_re.group(1)
        match_re = re.match('.*?(\d+).*', response.xpath("//div[@class='post-adds']/a[1]/span[1]/text()").extract_first().strip())
        # css选择器写法response.css('a[href="#article-comment"] span::text').extract_first()
        pinglun_nums = '0'
        if match_re:
            pinglun_nums = match_re.group(1)
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # css选择器写法response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)
        content = response.xpath("//div[@class='entry']").extract_first().strip()
        # css选择器写法response.css("div.entry").extract_first()

        article_item["url_object_id"] = get_md5(response.url)
        article_item["title"] = title
        article_item["url"] = response.url
        article_item["creat_data"] = creat_data
        article_item["front_image_url"] = {front_image_url}
        article_item["dianzan_nums"] = dianzan_nums
        article_item["shoucang_nums"] = shoucang_nums
        article_item["pinglun_nums"] = pinglun_nums
        article_item["tags"] = tags
        article_item["content"] = content

        yield article_item
        pass
