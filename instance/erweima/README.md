## 二维码制作和识别

在`Python`里面制作和识别二维码是一件很容易的事情，当然我们也看到了很多有趣的二维码，比如带图片的二维码，动态的二维码等等

首先我们先来了解一下二维码，其实我们现在看到的扫码，大部分来源于QR code码，QR code 是一种矩阵式二维条码。它是在一个矩形空间通过黑、白像素在矩阵中的不同分布进行编码。在矩阵相应元素位置上，用点（方点、圆点或其他形状）的出现表示二进制“1”，点的不出现表示二进制的“0”，点的排列组合确定了矩阵式二维条码所代表的意义。

所以我们来简单看一下二维码的结构吧：

![二维码结构](https://mmbiz.qpic.cn/mmbiz_png/mYJibSOraq9quibOI04kqca7ibfMwnSNV3UEvia1av5DaUzh4AwWteq5WtKnhnqKH4iax2lxoAsEy1ShlBsQZzmibvxg/0?wx_fmt=png)

那么这次我们将使用简单的模块来玩一下——`qrcode`（qrcode安装完毕之后，安装myqr，可以生成带图片的艺术二维码（黑白与彩色）、动态二维码（黑白与彩色）等等）：

```python
import qrcode
img = qrcode.make('数据有度')
img.save('g.png')
```

好了，完成了~是不是很简单？！

那么我们怎么自定义二维码呢？

```python
import qrcode
# version: 一个整数，范围为1到40，表示二维码的大小（最小值是1，是个12×12的矩阵），如果想让程序自动生成，将值设置为 None 并使用 fit=True 参数即可。
# error_correction: 二维码的纠错范围，可以选择4个常量: L 7%以下的错误会被纠正，M (default) 15%以下的错误会被纠正，等等
# boxsize: 每个点（方块）中的像素个数
# border: 二维码距图像外围边框距离，默认为4，而且相关规定最小为4
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data('数据有度')
# fit自适应大小
qr.make(fit=True)

# 不一定要黑白配，请随意
img = qr.make_image(fill_color="black", back_color="white")
img.save('g.png')
```

本质上，二维码就是一个字符串，扫描的时候无论微信还是其他app都是通过解析这个字符串处理相应的情况而已。

那么我们怎么解析呢？

```python
import zxing

reader = zxing.BarCodeReader()
barcode = reader.decode("g.jpg")
print(barcode.parsed)
```

这样我们的字符串就打印出来了~

> 玩出花的二维码（动态图，前提安装了myqr）：
> myqr 数据有度 -p g.gif -c -con 1.5 -bri 1.6


> github：[https://github.com/skenoy/smartanalysis](https://github.com/skenoy/smartanalysis)
> 
> 本文地址：[https://github.com/skenoy/smartanalysis/instance/erweima](https://github.com/skenoy/smartanalysis/instance/erweima)
