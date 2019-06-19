## python这样发邮件才舒服

发邮件是个很简单的操作，但用编程发邮件就不是那么好操作了。在我还用`perl`的时候，它的模块用起来非常不好用，第三方模块用起来格式有严格的要求，当时花费了几天的时间找到了最优的解决办法，最终用于检测集群CPU温度、硬盘是否快满了等等，还是很方便的（如果有邮箱app推送，几乎是实时监控了）。先看一下`perl`怎么写的吧：
```perl
sub sendMail
{
	my $content = shift @_;
	my $smtpHost = 'smtp.qq.com';
	my $smtpPort = '25';
	 
	my $username = 'xxx@qq.com';
	my $passowrd = 'pw';
	 
	my @to = ('1', '2');
	my $suffix = "\@qq.com";
	my $subject = "我是标题";

	my $message = <<MSG;
      $content
MSG

	my $smtp = Net::SMTP_auth->new($smtpHost, Timeout => 30) or die "Error:连接到$smtpHost失败！";
	$smtp->auth('LOGIN', $username, $passowrd) or die("Error:认证失败！");

#	foreach my $i(@to)
#	{
#		my $x = $i.$suffix;
		my @address = map {my $i = $_.$suffix; $i} @to;
		my $x = join ", ", @address;
		
		$smtp->mail($username);
		$smtp->to(@address);
		$smtp->data();
		$smtp->datasend("To: $x\n"); # strict format
		$smtp->datasend("From: $username\n"); # strict format
		$smtp->datasend("Subject: $subject\n"); # strict format
		$smtp->datasend("Content-Type:text/plain;charset=UTF-8\n"); # strict format
		$smtp->datasend("Content-Trensfer-Encoding:7bit\n\n"); # strict format
		$smtp->datasend($message);
		$smtp->dataend();
#	}
	$smtp->quit();
}
```

看到上面的结论就是麻烦= =！

我们来看看`python`的效果（官网给的例子）：
```python
#!/usr/bin/env python
"""Send the contents of a directory as a MIME message."""
import os
import sys
import smtplib
import mimetypes
from optparse import OptionParser
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
```

更麻烦！！！还没写邮件呢，就先导入一堆的包，要死了。。。

用`python`有一个好处就是第三方模块强大（当然我用`perl`也可以封装起来，但是它的面向对象写法太晦涩了。。。）！所以介绍大家使用`yagmail`！
```python
import yagmail
# SMTP中参数 port 一般不用写端口号
yag = yagmail.SMTP(user='xxx@qq.com', password='pw', host='smtp.qq.com')
yag.send('ooo@qq.com', subject = "我是标题", contents='我是正文', attachments=['我是附件.txt', '我是附件.jpg'])
# 发送多人
# yag.send(['1@qq.com', '2@qq.com'], subject = "我是标题", contents='我是正文', attachments=['我是附件.txt', '我是附件.jpg'])
# 最简发送
# yag.send('ooo@qq.com', "我是标题", ['我是正文', '我是附件.txt', '我是附件.jpg'])
# 抄送
# yag.send(to='ooo@qq.com', cc='xxx@qq.com', subject = "我是标题", contents='我是正文')
```

是不是感觉so easy了~拿起这个轰炸。。。啊不。。。测试一下吧

> github地址：https://github.com/skenoy/smartanalysis
> 本文路径：instance/email


![](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9pLEwFgUObcImwB175s3Nm5eXowgRhE68Nq10K66oBpHiblP6L9XicpeKs9vqUp6NqrYoypNqP37rTA/0?wx_fmt=png)