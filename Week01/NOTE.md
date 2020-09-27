# 初始

> 特点：  
	1. 语法简单
	2. 高级编程语言，接近人脑的思维方式
	3. 即支持面向过程、又支持面向对象
	4. 跨平台的。可以在windows和linux上都能运行
	5. 第三方模块非常丰富：TerserFlow
	6. 应用领域广：自动化运维、数据挖掘、深度学习、爬虫

> 学习方法 之 学会提问：  
	1. 推荐书《提问的智慧》： [ https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/master/README-zh_CN.md](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/master/README-zh_CN.md) 
	2. Python 3.7.7 官方文档（中文）： [ https://docs.python.org/zh-cn/3.7/](https://docs.python.org/zh-cn/3.7/) 
		* 更新的内容
		* 教程
		*  [标准库参考](https://docs.python.org/zh-cn/3.7/library/index.html) 
	3. GitHub 搜索帮助： [ https://help.github.com/cn/github/searching-for-information-on-github](https://help.github.com/cn/github/searching-for-information-on-github) 
	4. PEP8： [ https://www.python.org/dev/peps/pep-0008/](https://www.python.org/dev/peps/pep-0008/) 
	5. Google Python Style Guides： [ http://google.github.io/styleguide/pyguide.html](http://google.github.io/styleguide/pyguide.html) 

# 安装
查找python的位置：
![](&&&SFLOCALFILEPATH&&&46D61FFE-DF7C-4664-B7D0-CA65933008C0.png)

```bash
python -V # 查看python的版本号; 注意是大v不是小v，小v是一堆信息。我这output：Python 2.7.16
```
> 去官网下载其他包  
官网地址：https://www.python.org/downloads/
安装成功后文件会存在：/System/Library/Frameworks/Python.framework 和
/usr/bin/python

> 多个python共存的情况下，指定优先执行的顺序  
通过修改$PATH的内容，将其版本提前。
命令`which python`, `which python3`

方式一：临时方式
![](&&&SFLOCALFILEPATH&&&4A218753-6890-4D74-85CE-CF9492D16079.png)
在fish终端，使用`set`而不是 `export`
```bash
⋊> ~ set PATH /Users/pomelo-lxq/.yarn/bin /usr/local/bin /usr/bin /bin /usr/sbin /sbin /Library/Apple/usr/bin
⋊> ~ set PATH /usr/local/bin/python3 $PATH           13:31:56
⋊> ~ echo $PATH                                      13:31:56
/usr/local/bin/python3 /Users/pomelo-lxq/.yarn/bin /usr/local/bin /usr/bin /bin /usr/sbin /sbin /Library/Apple/usr/bin
```

方式二：长期方式
没太懂...
将命令的搜索路径粘贴到该文件：`vim /etc/bashrc`

![](&&&SFLOCALFILEPATH&&&A6A6425A-63C7-4B2A-B666-C19E00A782CC.png)

## 配置pip源
pip用于安装第三方模块，是包管理工具。
```bash
⋊> ~ pip3 -V                                                                                                                  
pip 20.1.1 from /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pip (python 3.7)
```

> 如何安装和校验某个包  
`pip3 install requests`
校验是否安装成功：
```
⋊> ~ python3                                                                                                                 
Python 3.7.9 (v3.7.9:13c94747c7, Aug 15 2020, 01:31:08)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import requests
```
没有报错 说明安装成功。

> 更换为国内源  
	* 临时 `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package`
	* 长期 `pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple`

常用 pip 源地址：
	* 豆瓣： [ https://pypi.doubanio.com/simple/](https://pypi.doubanio.com/simple/) 
	* 清华： [ https://mirrors.tuna.tsinghua.edu.cn/help/pypi/](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/) 
	* 中科大： [ https://pypi.mirrors.ustc.edu.cn/simple/](https://pypi.mirrors.ustc.edu.cn/simple/) 
	* 阿里云： [ https://mirrors.aliyun.com/pypi/simple/](https://mirrors.aliyun.com/pypi/simple/) 

> freeze用于包迁移  
A环境迁移到B环境，可以保留原来的依赖。
	1. 在A环境生成requirements.txt文件： `pip3 freeze > requirements.txt`
	2. 在B环境克隆A环境: `pip3 install -r requirements.txt`
pip也可以根据某个文件安装指定的包列表

# 虚拟环境
> 为了解决什么问题？  
不同项目需要不同版本的同类包，虚拟环境用于隔离
> 是什么？  
用于创建和管理虚拟环境的模块称为  [venv](https://docs.python.org/zh-cn/3.7/library/venv.html#module-venv) 
> 创建  
```bash
python3 -m venv venv01 # 创建venv01虚拟环境, 会装在/tmp/下
source venv01/bin/activate # 让这个环境的包生效
# 生效后再这个环境装包
```

Record：source的时候出了问题：
![](&&&SFLOCALFILEPATH&&&188669D7-F662-4930-B717-CDC4350C9434.png)
切换成bash: `bash --login`就可以了。
![](&&&SFLOCALFILEPATH&&&6F98017B-D4EA-40C4-84FF-018AFC5AD9E8.png)


# IDE
pylint 检测语法
pep8 检测美观
autopep8 VSCode 语法和美观都会帮你检测和调整
