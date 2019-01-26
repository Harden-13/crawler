##### XPATH

有其中类型的节点：元素，属性，文本，命名空间，处理指令，注释以及文档（根）节点

```
<bookstore>
  <book>
    <title lang="en">Harry Potter</title>
    <author>J K. Rowling</author>
    <year>2005</year>
    <price>29.99</price>
  </book>
</bookstore>
注解
<bookstore> (root element node)
<author>J K. Rowling</author> (element node)
lang="en" (attribute node)
```

```
/	从根节点开始找
//	从当前节点的开始的任意曾找
.	当前节点
..	当前节点的父节点
@	选择属性
*	匹配任意元素的节点
@*	匹配任意属性节点
node()	匹配任意类型的节点
text()	匹配text类型的节点
```

##### lxml

lxml是python下功能丰富的xml，html解析库，性能非常好，是对libxml2和libslt的封装

```
from lxml import etree

#使用etree构建html
root = etree.Element('html')
print(type(root))
print(root.tag)

body = etree.Element('body')
root.append(body)
print(etree.tostring(root))

sub = etree.SubElement(body,'child1')
sub = etree.SubElement(body,'child2').append(etree.Element('child21'))
print(etree.tostring(root,pretty_print=True).decode())
```

##### etree还提供了2个有用的函数

etree.HTML(text)解析到html文档，返回根节点

node.xpath(''xpath路径'')对节点使用xpath语法

```
from lxml import etree
import requests

url = 'https://movie.douban.com/'
ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

with requests.get(url,headers={'User-agent':ua}) as response:
    content = response.text
    html = etree.HTML(content)
    title = html.xpath("//div[@class='billboard-bd']//tr/td/a/text()")
    for t in title:
        print(t)
```

##### jsonpath

```
xpath	jsonpath	describe
/		$			根元素
.		@			当前元素
/		.or[]		获取子节点
//		..			任意层次
*		*			通配符，任意匹配节点
[]		[]			下表操作
[]		?()			过滤

```

```
import requests
from jsonpath import jsonpath
import json

ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&page_limit=10&page_start=0"

response =requests.get(url,headers={'User-agent':ua})
with response:
    text = response.text
    js =json.loads(text)
    rs1 = jsonpath(js,'$..title')
    print(rs1)
    
    rs2 = jsonpath(js,'$..subjects[?(@.rate>"8")]')
    
    rs3 = jsonpath(js,'$..subjects[?(@.rate>"8")].title')
    print(rs3)
```



