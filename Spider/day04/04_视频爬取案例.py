import requests
from lxml import etree

url = 'http://tieba.baidu.com/p/6050091945' 
headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}

res = requests.get(url,headers=headers)
res.encoding = 'utf-8'
html = res.text

with open('帖子.html','w') as f:
    f.write(html)


parseHtml = etree.HTML(html)
rList = parseHtml.xpath(
'//div[@class="video_src_wrapper"]/embed/@data-video')

print(rList)

















