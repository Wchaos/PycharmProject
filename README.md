# Scrapy使用详解
﻿                                                               ——by 王超

---

##**第一部分 scrapy入门**

###**创建scrapy项目**
使用命令行创建一个scrapy项目
>
>     scrapy startproject [projectname]

该命令会在当前目录创建一个名为`projecname`的目录，里面内容如下：
​  
>
>        projectname/
>            scrapy.cfg
>            projectname/
>               __init__.py
>               items.py
>               pipelines.py
>               middlewares.py
>               settings.py
>               spiders/
>                   __init__.py
>                   ...

各文件介绍：

-  scrapy.cfg  项目配置文件，一般不需要修改 
-  items.py  定义需要提取的数据字段，是这些字段的临时容器
-  pipeline.py  项目管道，用于定义采集到的item的保存方法
-  middlewares.py 中间件文件，自定义的下载中间件和爬虫中间件
-  settings.py 项目设置文件，用于定义一些参数和挂载组件（比如中间件和项目管道，均需在此激活，才能使用）
-  spiders文件夹，自定义的爬虫文件放在此文件夹下

###**定义Item**
Item是保存爬取到的数据的容器。代表着你要从网页中提取的字段信息。
用法：定义一个Item类

>
>```python
> from scrapy import Item, Field
> class DmozItem(Item):
>     title = Field()
>     link = Field()
>     desc = Field()
>```
>

###**编写爬虫**

爬虫是用户编写的用于解析网页、爬取数据的类。
首先在spiders文件夹下创建一个python文件，在里面自定义一个爬虫类。

#####**Request对象介绍**
爬虫将对url的请求封装成一个`Request`对象，该`Request`对象经过scrapy内置的一些组件（爬虫中间件、引擎、调度器、下载中间件），最终到达下载器。
`Request`对象主要包含了一个请求的各种信息：如请求的url，headers，cookie，callback（回调函数）等。
具体可以查看源码。

#####**Response对象介绍**
下载器处理`Requset`，将返回一个`Response`对象，该对象经过经过scrapy内置的一些组件（下载中间件、引擎、爬虫中间件），最终到达爬虫。
`Response`对象主要包含返回的各种信息，如该返回对应的url、status(http状态码)、body（html页面）、request（对应的request对象）等。
具体可以查看源码。

#####**定义最基本的属性和方法**

自定义的爬虫类必须继承`scrapy.Spider`类，且定义一些属性：

-  `name`: 用于区别Spider。该名字必须唯一，scrapy通过该字段找到相应需要运行的爬虫类。
-  `start_urls`: 种子url，Spider启动时进行爬取的url列表；后续的url则从初始url获取到的数据中提取。
-  `parse()`: `scrapy.Spider`类中默认处理种子url返回值`response`的函数；承担着提取网页中数据字段，生成items以及根据需要进一步爬取的url生成`Request`对象。

示例如下：

>
>```python
> import scrapy
> class DmozSpider(scrapy.Spider):
>     name = "dmoz"
>     allowed_domains = ["dmoz.org"]
>     start_urls = [
>           "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
>          "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
>     ]
>
>    def parse(self, response):
>        """下面是处理response，爬取数据的代码"""
>```

说明：

-  spider中，`start_urls`和`parse`是通过一个`start_request()`方法连接的，该方法根据`start_urls`中的url构造以`parse()`为回调函数的`Request`对象。
-  可以通过在自定义类中重写`start_request()`方法，而改变这边这种固定模式，但是这种流程思想是不变的。

#####**解析数据**

从html网页中解析出数据的方法有很多，用的较多的是：正则表达式、BeautifulSoup和xpath。一般xpath为主，其他两个为辅。
示例如下：
>
>```python
> def parse(self, response):
>     for sel in response.xpath('//ul/li'):
>         title = sel.xpath('a/text()').extract()
>         link = sel.xpath('a/@href').extract()
>         desc = sel.xpath('text()').extract()
>         print title, link, desc
>```

#####**使用Item**

提取到数据之后，将数据放入之前创建好的Item类的对象中保存，之后返回这些item，框架会将item送入ItemPipeline中处理。
示例如下：
>
>```python
> def parse(self, response):
>    for sel in response.xpath('//ul/li'):
>        item = DmozItem()
>        item['title'] = sel.xpath('a/text()').extract()
>        item['link'] = sel.xpath('a/@href').extract()
>        item['desc'] = sel.xpath('text()').extract()
>        yield item
>```

说明：

-  yield不理解的话，可以暂且理解为return（不过当然是不一样的）


#####**追踪链接**

一个页面上除了有我们需要的信息，还有一些链接也是有价值的，它们经常能链接到下一页的信息，或者某个条目的详情。
示例爬取下一页信息：
>
>```python
> def parse(self, response):
>     for sel in response.xpath('//ul/li'):
>         item = DmozItem()
>          #提取数据存入item
>          yield item
>     next_page = response.xpath('下一页的xpath路径').extract_first()
>     if next_page:    
>         #next_page如为相对路径，请补为绝对路径
>         yield Request（url=next_page，callback=self.parse）
>```

说明：

-  因下一页页面布局一般与当前页面相同，所以回调函数是自身；
-  如果提取的链接是其他的页面，需要单独为该页面编写解析函数，则最后一行`Request`对象中的回调函数则相应调整。       

#####**一个完整的爬虫类示例**

>
>```python
> import scrapy
> from tutorial.items import DmozItem
>
> class DmozSpider(scrapy.Spider):
>     name = "dmoz"
>     allowed_domains = ["dmoz.org"]
>     start_urls = [
>         "http://www.dmoz.org/Computers/Programming/Languages/Python/",
>     ]
>     
>     def parse(self, response):
>         """种子url对应的Request对象的回调方法，提取后续url，生成请求"""
>         for href in response.css("ul.directory.dir-col > li > a::attr('href')"):#提取url
>             url = response.urljoin(response.url, href.extract()) #拼接成绝对地址
>             yield scrapy.Request(url, callback=self.parse_dir_contents) #生成请求
>
>    def parse_dir_contents(self, response):
>        """回调方法，解析数据，返回item"""
>        for sel in response.xpath('//ul/li'):
>            item = DmozItem()
>            item['title'] = sel.xpath('a/text()').extract()
>            item['link'] = sel.xpath('a/@href').extract()
>            item['desc'] = sel.xpath('text()').extract()
>            yield item
>```

###**保存爬取的数据**

#####**命令行设置法**
保存文件最简单的方式是在启动时添加参数`-o 文件名.json`。示例如下：

>
>     scrapy crawl dmoz -o items.json 

该命令将采用JSON格式对爬取的数据进行序列化，生成items.json文件。
还可以是其他格式文件，详见scrapy内置的`Feed exports`说明文档。此法一般不用，不细讲。

#####**编写pipeline方法**

保存items到MongoDB示例：

>
>```python
> import pymongo
> class MongoPipeline(object):
> 
>     collection_name = 'scrapy_items'
>     
>     def __init__(self, mongo_uri, mongo_db):
>         self.mongo_uri = mongo_uri
>         self.mongo_db = mongo_db
>     
>     @classmethod
>     def from_crawler(cls, crawler):
>         return cls(
>             mongo_uri=crawler.settings.get('MONGO_URI'),
>             mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
>         )
>     
>     def open_spider(self, spider):
>         self.client = pymongo.MongoClient(self.mongo_uri)
>         self.db = self.client[self.mongo_db]
>     
>     def close_spider(self, spider):
>         self.client.close()
>     
>     def process_item(self, item, spider):
>         self.db[self.collection_name].insert(dict(item))
>         return item
>```

说明：

-  此示例演示比较详细，几乎涵盖了框架中默认pipeline类所具有的全部方法。以上四个方法的调用都内置在框架中。
-  类初始化时，先调用`from_crowler`从设置中读取数据库（地址&端口、数据库名）信息，然后调用`__init__`构造函数初始化。
-  spider启动时。调用`open_spider`连接数据库。
-  spider运行时，调用`process_item`方法处理经过该项目管道的item，此处为存入MongoDB数据库。也可以存入MySQL，或者存为Json文件，看代码怎么写。
-  spider关闭时，关闭数据库连接。

#####**启用一个Item Pipeline组件**

启用一个编写好的Item Pipeline组件，需要在设置中将其挂载到scrapy项目中：
>
>```python
> ITEM_PIPELINES = {
>    'myproject.pipelines.MongoPipeline': 300,
>    'myproject.pipelines.JsonWriterPipeline': 800,  }
>```

scrapy初始化时，会读取配置文件，从而能够将其中的Item Pipeline组件挂载到项目中。

###**运行爬虫**
使用命令行：
>
>    scrapy crawl 爬虫名

有些时候需要暂停爬虫，之后再从断点续爬。
此时使用如下命令启动：
>
>     scrapy crawl 爬虫名 -s JOBDIR=目录

此时若停止爬虫（按Ctrl-C或者发送一个信号），程序会将爬虫状态保存到该命令设置的目录中；
恢复该爬虫，运行同样的命令即可。


##**第二部分 scrapy进阶**
要理解一部分的内容，最好先对scrapy的源码分析和基本架构有一定了解。

###**用户代理（User-Agent）**

用户代理是指http请求头`headers`中的`User-Agent`字段，服务端通过这个字段判断用户类型（程序、浏览器）。
程序用户类型，如：

-  scrapy默认的`User-Agent`字段是对应的scrapy的版本号；
-  如果用python的urllib模块请求网页，则默认的`User-Agent`字段是对应python版本号；

浏览器用户类型则是与浏览器厂商、内核、版本号有关的一串识别符。如下是谷歌浏览器39.0版本的识别号：

>     Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60
>

我们需要将爬虫程序中的`User-Agent`换成浏览器的`User-Agent`，以伪装成真实浏览器服务端发起请求。

#####**使用settings设置**
在setting.py文件中定义`User-Agent`字段，scrapy内置的`scrapy.downloadermiddlewares.useragent.UserAgentMiddleware`中间件会使用该字段值替换调默认的值。

#####**自定义User-Agent中间件**
我们还可以通过自定义User-Agent下载中间件来更换请求头`headers`中的`User-Agent`字段。
方法如下：

>
>```python
> class UserAgentMiddleware(object):
>     """ 换User-Agent """
>     def process_request(self, request, spider):
>         agent = random.choice(agent_list) #agent_list是一个存放user-agent的列表
>         request.headers["User-Agent"] = agent
>```

说明：

-  agent_list是一个存放user-agent的列表，一般在setting文件或以单独文件中定义好，导入即可。
-  该UserAgentMiddleware需要在settings文件中激活启用。
-  最好关闭内置的`scrapy.downloadermiddlewares.useragent.UserAgentMiddleware`中间件，以免引起冲突。


###**IP代理**
有些服务器会对日志文件进行分析，对访问过于频繁的ip进行限制。
为了防止单一ip爬取被限制，我们可以添加ip代理池。
方法也是使用下载中间件，对每个经过的'Request'对象添加一个ip代理，scrapy下载器会使用该代理ip去对服务器发起请求。
简单用法如下：

>
>```python
> class ProxyMiddleware(object):
>     """ 换IP """
>     def process_request(self, request, spider):
>         ip = random.choice(ip_list)
>         request.meta['proxy'] = ip
>```

说明：

-  ip_list是一个存放代理ip的列表，里面存放的ip格式如下：`http://110.72.32.103:8123`包含代理类型、地址和端口
-  scrapy对http代理的支持是通过内置的`HttpProxyMiddleware`下载中间件支持的，需确保自定义的ip代理中间件执行顺序在其之前，以确保`HttpProxyMiddleware`能从`request.meta`中找到`proxy`属性。

#####**用数据库升级ip代理服务**
ip代理和User-agent不同的是：

-  User-agent是可以认为是不会过期的。
-  而ip是有有效期的。因此使用一个固定的列表来存储ip，是危险的。


使用数据库（一般用redis）来存储ip，之后下载中间件的写法：

-  添加`__init__`构造方法，初始化下载中间件时，创建数据库连接。
-  `process_request`方法改为从数据库中随机读取ip，其余一样。

使用数据库的好处：

- 可以写一个爬虫程序，不断爬取代理ip，测试有用性后添加入数据库
- 一旦发现因为ip，请求失败，可以从数据库删除无效的ip。通过对response的判断或exception的判断来实现。
- 总之，就是可以实现ip池的动态变化，保证ip的有效性。


###**cookie池设置**
有些网站的网页需要登录之后才有权限访问，游客身份不能访问。
要爬取这样的页面，我们需要带上请求该页面是需要带上服务端用于识别用户身份和用户登录状态的cookie。
简单用法如下：

>
>```python
> class CookiesMiddleware(object):
>     """ 换cookie """
>     def process_request(self,request,spider):
>         cookie = random.choice(cookies_list)
>         cookie = dict(elem.strip().split('=') for elem in cookie.split(';'))#转换成字典类型
>         request.cookies = cookie
>```

说明：

-  cookie_list也是存放cookie的列表。
-  cookie可以在页面登录之后，在浏览器调试工具中，找到登录之后的请求，找到请求头，直接复制里面的cookie。

#####**用数据库升级cookie服务**
和ip类似，cookie也是有有效期的。所以需要将cookie池做成动态变化的，保证里面存储的cookie一直有效。

中间件的改动，与ip代理类似：

-  在构造函数中，建立数据库连接；
-  `process_request`改为从数据库中随机读取一个cookie。
-  `process_response`方法中对放回response进行判断：如果判断账号被限，则删除该账号的cookie；如果判断账号需要重新登录，则重新登录该账号，更新数据库中该账号的cookie。

#####**模拟登陆**
模拟登陆的主要作用是获取登录之后的cookie。
模拟登陆的常用两种方法（[模拟登陆微博的方法示例](https://www.jianshu.com/p/816594c83c74/ "weibo_login")）：

-  直接法： 分析登录过程，组装服务端完成登录所需的信息，用post方法登录。此法只适用一些简单的网站，复杂网站分析特别麻烦。如下是一个[微博直接登录法的分析过程](https://www.jianshu.com/p/816594c83c74/ "weibo_login_analyse")。
-  selenium法：直接控制浏览器打开登录页面，模拟输入和点击，实现登录。此法比较简便，推荐。

模拟登陆的**难点**是**验证码的识别**
验证码的识别方法：

- 截图，手动输入；不够自动化，但是有些难以识别的验证码，只能采用此法。
- 接入打码平台
- 编写图像处理代码，使用OCR，甚至机器学习、深度学习的方法训练模型来识别。


###**Scrapy+Selenium**

本质： 使用浏览器来代替Scrapy的下载器。
作用： 能够爬取动态页面。
原因： 因为scrapy本身不能执行页面中的js，所以对于动态页面通过js实现的后续数据请求和页面渲染无能为力。
用法如下：
#####**在爬虫类中打开一个浏览器**

>
>```python
> class Spider(Spider):
>     def __init__(self):
>     #初始化时候，给爬虫新开一个浏览器
>     self.browser = webdriver.Chrome()
>     self.browser.maximize_window()
>     super(Spider, self).__init__()
>     dispatcher.connect(self.spider_closed, signals.spider_closed)
>     #第二个参数是信号（spider_closed:爬虫关闭信号，信号量有很多）,
>     #第一个参数是当执行第二个参数信号时候要执行的方法
>       
>     def spider_closed(self, spider):
>         #当爬虫退出的时候关闭chrome
>         print("spider closed")
>         self.browser.quit()
>```
>

#####**添加下载中间件**

>
>```python
> class JavaScriptMiddleware(object):
>     def process_request(self, request, spider):
>         spider.browser.get(request.url)
>         time.sleep(2）#等待页面渲染
>         rendered_body = spider.browser.page_source
>         if r'charset="GBK"' in rendered_body or r'charset=gbk' in rendered_body:
>             coding = 'gbk'
>         else:
>             coding = 'utf-8'
>         #将渲染页面封装成一个Response对象返回
>         return HtmlResponse(url=spider.browser.current_url,\
>                             body=rendered_body, encoding=coding,request=request)
>```

说明：

-  此处使用等待2秒的页面渲染时间是不严谨的，可以通过查找某一动态元素，来确认页面是否渲染完成；
-  当页面需要下拉才能渲染完成时，可以添加模拟下拉的操作。
-  Request请求走到此下载中间件，返回的Response对象会原路返回至引擎。在这之后的下载中间件将不会被执行。需要注意下载中间件的顺序。


###**Selenium的一些操作**

#####**Chrome设置Headless**
无头浏览器是指没有界面的浏览器，这种没有打开界面的操作，运行较快，对爬虫和自动化测试来说比较方便。
之前用的较广的无头浏览器是PhantomJS。
现在PhantomJS已经不再维护了，且谷歌也在Chrome中添加了对无头模式的支持。
设置方法如下（需要Chrome版本号为61以上）：

>
>```python
> chrome_options = webdriver.ChromeOptions()
> chrome_options.add_argument("--headless") #设置headless
> chrome = webdriver.Chrome(chrome_options=chrome_options) #打开一个chrome浏览器
>```

#####**Chrome设置ip代理**

>
>```python
> proxy = "http://222.169.193.162:8099"
> chrome_options.add_argument('--proxy-server={}'.format(proxy)) #设置代理ip
> chrome = webdriver.Chrome(chrome_options=chrome_options) #打开一个chrome浏览器
>```

说明：

- 这个只能在打开浏览器的时候设置代理，暂时还不知道能不能在浏览器运行过程中，换代理ip；
- 如果不能，那只能每次换ip时都打开一个新的浏览器处理请求。

#####**Chrome设置Cookie**
webdriver有`delete_all_cookies`方法和`add_cookie`方法；
其中add_cookie方法，对待已有的字段，不会覆盖更新，而是添加在后面，会导致出现两个相同的字段。所以添加前需调用删除cookie的方法，确保没有该字段了。

>
>```python
> cookie = dict(elem.strip().split('=') for elem in cookie.split(';'))#转换成字典
> browser = webdriver.Chrome() #打开一个浏览器
> browser.get(url=url) #打开一个url，此时未登录
> time.sleep(1)
> browser.delete_all_cookies() #删除cookie
> for key, value in cookie.items():
>     dic = {
>         'name': key,
>         'value': value,
>     }
>     browser.add_cookie(dic) #循环添加cookie中的每一个字段
> browser.get(url=url) #再次打开该url，此时状态为已登录
>```

说明：

-  这里这只是单独的试成功了，添加登录成功的cookie之后，打开的页面也是登录成功的
-  但是加入scrapy框架，频繁删除浏览器cookie，再添加cookie，好像会出一些问题，这块不是很成熟。

###**爬虫的控制**

#####**外部控制**
使用`Telnet`终端可以实现对爬虫进行外部控制，`telnet`是爬虫内置的一个扩展（Extendsion），默认监听端口为6023。具体可以查看[官方文档](http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/telnetconsole.html "Telnet Console")
python可以通过`telnetlib`包实现程序对Telnet终端的控制，从而实现用程序对爬虫的外部控制。
用法如下：
>
>```python
> HOST = “localhost”
> port = “6023”
> tn = telnetlib.Telnet(HOST, port) #连接爬虫中设定的监听地址
> tn.write(b"engine.pause()\n") #暂停引擎
> tn.write(b"engine.unpause()\n") #恢复引擎
> tn.write(b"engine.stop()\n") #停止引擎
>```
>

#####**内部控制**
scrapy 可以在内部实现对爬虫的停止（暂停）操作。

- 通过在spider、爬虫中间件、pipeline中抛出CloseSpider异常来控制spider停止。
>
>```python
> raise CloseSpider("some reasons")
>```

- 通过调用引擎的close_spider()方法
>
>```python
> """在中间件中定义如下方法，获取crawler对象的引用"""
> @classmethod
> def from_crawler(cls, crawler):
> return cls(crawler)
> 
> """执行如下语句即可关闭爬虫"""
> crawler.engine.close_spider(spider,"some reasons")
>```


###**爬虫异常处理**
`Scrapy`需要自己编写代码的组件，可能捕获异常或者抛出异常的有：爬虫、爬虫中间件、项目管道、下载中间件。

#####**爬虫抛出异常**
爬虫抛出异常，[官方文档](http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/spider-middleware.html "spider_mw")上说会依次调用爬虫中间件的`Process_spider_exception`方法处理，但是实践尝试之后没有成功。
处理爬虫抛出的异常，还可以使用扩展（`Extension`）。
用法如下：
>
>```python
> from scrapy import signals
> """自定义扩展类，使用需在设置中激活"""
> class SpiderErrHandleExtension(object):
> 
> @classmethod
> def from_crawler(cls, crawler):
>     return cls(crawler)
>
> def __init__(self,crawler):
>     """将信号和对应函数连接"""
>     crawler.signals.connect(self.spider_error, signal=signals.spider_error)
>
> def spider_error(self, failure, response, spider):
>     exception = failure.value #获取捕获的异常实例
>     if isinstance(exception, myexception): #myexception为需要处理的异常类型
>         """do something"""
>```
>


#####**爬虫中间件抛出异常**
可以在爬虫中间件的`process_spider_input`方法中抛出异常，然后在`process_spider_exception`中捕获这些异常，并进行处理。
如`httperror`中间件中的如下用法：
>
>```python 
> class HttpErrorMiddleware(object):
>     """抛出异常"""
>     def process_spider_input(self, response, spider):
>         if 200 <= response.status < 300:
>             """do something"""
>         else:
>             raise HttpError(response, 'Ignoring non-200 response')
>     """处理异常"""        
>     def process_spider_exception(self, response, exception, spider):
>         if isinstance(exception,HttpError):
>             """do something"""
>```
>
>说明：
>中间件默认方法中的另一的`process_spider_output`方法只能返回`Request`、`dict`或`item`对象，抛出异常或者返回其他值均不会进行处理。

#####**ItemPipeline抛出异常**
项目管道抛出异常，直接抛出抛出内置的`DropItem`和`CloseSpider`均可被内置的`scraper`组件捕捉到，而自动进行丢弃item和关闭spider的相应处理。
项目管道另一可能出现的异常为数据库连接或IO异常，此时可以直接抛出`CloseSpider`异常，并在异常中说明原因即可，不需要自定义异常。因为这两种异常都会导致数据不能存储，爬到的数据白白浪费掉。

#####**下载中间件抛出异常**
与爬虫中间件类似：
使用`process_exception()`来处理下载处理器(`download handler`)或 `process_request()` (下载中间件)中抛出的异常(包括 `IgnoreRequest` 异常)。详见[官方文档](http://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/downloader-middleware.html "downloadmw")
用法示例：

> 与爬虫中间件类似，只不过方法参数变为： `process_exception(request,exception,spider)`

最后，下载中间件中所有未处理的异常，均能走到`Spider`中定义的`Request`的错误回调方法，需在`Request`对象中设定好（`request.errback`）。
用法示例：
>```python
>     class MySpider(Spider):
>
>         """省略其他，构造请求,并在请求中设置错误回调函数"""
>         yield Request（url, callback,errback = self.errorback）
>         
>         """定义错误回调函数"""
>         def errback(self, failure):
>             exception = failure.value
>             if isinstance(exception, myexception): #myexception为需要处理的异常类型
>             """do something"""
>```

###**分布式爬虫**
使用`scrapy-redis`包可以实现简单的分布式爬虫，这个包直接重写了调度和请求队列等一些组件，直接将`Scrapy`中原始的组件替换掉，然后做相应修改就可以了。

#####**修改settings**
将'scrapy-redis'的组件挂载到框架当中，并添加`redis`的一些设置。
>
>```python 
> SCHEDULER = "scrapy_redis.scheduler.Scheduler"
> DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
> SCHEDULER_PERSIST = True
> SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
> REDIS_URL = None  # 一般情况可以省去
> REDIS_HOST = '127.0.0.1'  # redis服务器地址
> REDIS_PORT = 6379
>```
>

#####**爬虫修改**

爬虫做相应修改，继承的父类改为`RedisSpider`,`start_urls`不在需要，爬虫的初始请求改为从redis获取，需设置`redis_key`。
>
>```python 
> from scrapy_redis.spiders import RedisSpider
> class MySpider(RedisSpider):
>     name = "MySpider"
>     redis_key = "myspider:start_urls"
>    
>     def parse(sele,response):
>         """do something"""
>```

打开redis客户端,设置起始键：

> set myspider:start_urls www.***.com

然后，将爬虫程序拷贝到多个计算机运行即可。
