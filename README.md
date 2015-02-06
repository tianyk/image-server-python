### 运行环境
Python 2.7.8

### 服务器/WEB框架
tornado (4.0.2)

### 依赖库
    * 图像处理 Pillow (2.7.0)


## 接口说明

### 图片处理（imageView）

#### 描述
此接口可对图片进行缩放操作，生成各种缩略图


#### 接口规格
注意：接口规格不含任何空格与换行符，下列内容经过格式化以便阅读。

    imageView/<mode>
             /w/<Width>
             /h/<Height>
             /format/<Format>

或

    imageView/<mode>
             /w/<LongEdge>
             /h/<ShortEdge>
             /format/<Format>
             /interlace/<Interlace>

其中 `<mode> `分为如下几种情况：

| 模式 | 说明 |
| ---- | ---- |
|`/0/w/<LongEdge>/h/<ShortEdge>`|限定缩略图的长边最多为<LongEdge>，短边最多为<ShortEdge>，进行等比缩放，不裁剪。如果只指定 w 参数则表示限定长边（短边自适应），只指定 h 参数则表示限定短边（长边自适应）。|
|`/1/w/<Width>/h/<Height>`|限定缩略图的宽最少为<Width>，高最少为<Height>，进行等比缩放，居中裁剪。转后的缩略图通常恰好是 <Width>x<Height> 的大小（有一个边缩放的时候会因为超出矩形框而被裁剪掉多余部分）。如果只指定 w 参数或只指定 h 参数，代表限定为长宽相等的正方图。|
|`/2/w/<Width>/h/<Height>`|限定缩略图的宽最多为<Width>，高最多为<Height>，进行等比缩放，不裁剪。如果只指定 w 参数则表示限定长边（短边自适应），只指定 h 参数则表示限定短边（长边自适应）。它和模式0类似，区别只是限定宽和高，不是限定长边和短边。从应用场景来说，模式0适合移动设备上做缩略图，模式2适合PC上做缩略图。|
|`/2/w/<Width>/h/<Height>`|限定缩略图的宽最多为<Width>，高最多为<Height>，进行等比缩放，不裁剪。如果只指定 w 参数则表示限定长边（短边自适应），只指定 h 参数则表示限定短边（长边自适应）。它和模式0类似，区别只是限定宽和高，不是限定长边和短边。从应用场景来说，模式0适合移动设备上做缩略图，模式2适合PC上做缩略图。|
|`/3/w/<Width>/h/<Height>`|限定缩略图的宽最少为<Width>，高最少为<Height>，进行等比缩放，不裁剪。你可以理解为模式1是模式3的结果再做居中裁剪得到的。|
|`/4/w/<LongEdge>/h/<ShortEdge>`|限定缩略图的长边最少为<LongEdge>，短边最少为<ShortEdge>，进行等比缩放，不裁剪。这个模式很适合在手持设备做图片的全屏查看（把这里的长边短边分别设为手机屏幕的分辨率即可），生成的图片尺寸刚好充满整个屏幕（某一个边可能会超出屏幕）。|
|`/5/w/<LongEdge>/h/<ShortEdge>`|限定缩略图的长边最少为<LongEdge>，短边最少为<ShortEdge>，进行等比缩放，居中裁剪。同上模式4，但超出限定的矩形部分会被裁剪。|

注意：

1. 可以仅指定w参数或h参数；
2. 新图的宽/高/长边/短边，不会比原图大，即本接口总是缩小图片；
3. 所有模式都可以只指定w参数或只指定h参数，并获得合理结果。在w、h为限定最大值时，未指定某参数等价于将该参数设置为无穷大（自适应）；在w、h为限定最小值时，未指定参数等于给定的参数，也就限定的矩形是正方形。

|参数名称|必填|说明|
|--------|----|----|
|`/format/<Format>`|  | 新图的输出格式。取值范围：jpg，gif，png，webp，缺省为原图格式。|
|`/interlace/<Interlace>`|  | 是否支持渐进显示。取值范围：1 支持渐进显示，0不支持渐进显示(缺省为0)。适用目标格式：jpg。效果：网速慢时，图片显示由模糊到清晰。|

#### 请求
##### 请求报文格式
    
    GET <ImageDownloadURI>?<接口规格> HTTP/1.1

#### 示例

    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageView/0/w/500/h/200

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageView/0/w/500/h/200)


    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageView/1/w/500/h/200

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageView/1/w/500/h/200)


    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageView/2/w/500/h/200


![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageView/2/w/500/h/200)


    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageView/3/w/500/h/200

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageView/3/w/500/h/200)


    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageView/4/w/500/h/200

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageView/4/w/500/h/200)


    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageView/5/w/500/h/200

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageView/5/w/500/h/200)

### 高级图像处理（imageMogr)

#### 描述
此接口为开发者提供一系列高级图片处理功能，包括缩放、裁剪、旋转等等。

#### 接口规格
注意：接口规格不含任何空格与换行符，下列内容经过格式化以便阅读。

    imageMogr/auto-orient
             /thumbnail/<imageSizeGeometry>
             /strip
             /gravity/<gravityType>
             /crop/<imageSizeAndOffsetGeometry>
             /rotate/<rotateDegree>
             /format/<destinationImageFormat>
             /blur/<radius>x<sigma>
             /interlace/<Interlace>

|参数名称|必填|说明|
|--------|----|----|
|`/auto-orient`| |根据原图EXIF信息自动旋正，便于后续处理建议放在首位。|
|`/strip`| |去除图片中的元信息|
|`/blur/`| |对图片高斯模糊。|
|`/thumbnail/<imageSizeGeometry>`| | 参看缩放操作参数表，缺省为不缩放。|
|`/gravity/<gravityType>`| |参看图片处理重心参数表，目前在imageMogr2中只影响其后的裁剪偏移参数，缺省为左上角（NorthWest）。|
|`/crop/<imageSizeAndOffsetGeometry>`| |参看裁剪操作参数表，缺省为不裁剪。|
|`/rotate/<rotateDegree>`| |旋转角度。取值范围1-360，缺省为不旋转。|
|`/format/<destinationImageFormat>`| |图片格式。支持jpg、gif、png、webp，缺省为原图格式。|
|`/interlace/<Interlace>`||是否支持渐进显示。取值范围：1 支持渐进显示，0不支持渐进显示(缺省为0)。效果：网速慢时，图片显示由模糊到清晰。|


**缩放操作参数表**

|参数名称|必填|说明|
|--------|----|----|
|`/thumbnail/!<Scale>p`| |基于原图大小，按指定百分比缩放。取值范围0-1000。|
|`/thumbnail/!<Scale>px`| |以百分比形式指定目标图片宽度，高度不变。取值范围0-1000。|
|`/thumbnail/!x<Scale>p`| |以百分比形式指定目标图片高度，宽度不变。取值范围0-1000。|
|`/thumbnail/<Width>x`| |指定目标图片宽度，高度等比缩放。取值范围0-10000。|
|`/thumbnail/x<Height>`| |指定目标图片高度，宽度等比缩放。取值范围0-10000。|
|`/thumbnail/<Width>x<Height>`| |限定长边，短边自适应缩放，将目标图片限制在指定宽高矩形内。取值范围不限，但若宽高超过10000只能缩不能放。|
|`/thumbnail/!<Width>x<Height>r`| | 限定短边，长边自适应缩放，目标图片会延伸至指定宽高矩形外。取值范围不限，但若宽高超过10000只能缩不能放。|
|`/thumbnail/<Width>x<Height>!`| |限定目标图片宽高值，忽略原图宽高比例，按照指定宽高值强行缩略，可能导致目标图片变形。取值范围不限，但若宽高超过10000只能缩不能放。|
|`/thumbnail/<Width>x<Height>>`| |当原图尺寸大于给定的宽度或高度时，按照给定宽高值缩小。取值范围不限，但若宽高超过10000只能缩不能放。|
|`/thumbnail/<Width>x<Height><`| |当原图尺寸小于给定的宽度或高度时，按照给定宽高值放大。取值范围不限，但若宽高超过10000只能缩不能放。|
|`/thumbnail/<Area>@`| |按原图高宽比例等比缩放，缩放后的像素数量不超过指定值。取值范围不限，但若像素数超过100000000只能缩不能放。|

**图片处理重心参数表**
在高级图片处理现有的功能中只影响其后的裁剪偏移参数，即裁剪操作以`gravity`为原点开始偏移后，进行裁剪操作。

    NorthWest     |     North      |     NorthEast
                  |                |    
                  |                |    
    --------------+----------------+--------------
                  |                |    
    West          |     Center     |          East 
                  |                |    
    --------------+----------------+--------------
                  |                |    
                  |                |    
    SouthWest     |     South      |     SouthEast


**裁剪操作参数表（cropSize）**

|参数名称|必填|说明|
|--------|----|----|
|`/crop/!{cropSize}a<dx>a<dy>`||相对于偏移锚点，向右偏移dx个像素，同时向下偏移dy个像素。取值范围不限，小于原图宽高即可。|
|`/crop/!{cropSize}-<dx>a<dy>`||相对于偏移锚点，向下偏移dy个像素，同时从指定宽度中减去dx个像素。取值范围不限，小于原图宽高即可。|
|`/crop/!{cropSize}a<dx>-<dy>`||相对于偏移锚点，向右偏移dx个像素，同时从指定高度中减去个像素。取值范围不限，小于原图宽高即可。|
|`/crop/!{cropSize}-<dx>-<dy>`||相对于偏移锚点，从指定宽度中减去dx个像素，同时从指定高度中减去dy个像素。取值范围不限，小于原图宽高即可。|

例如，  
`/crop/!300x400a10a10`表示从源图坐标为x:10,y:10处截取300x400的子图片。  
`/crop/!300x400-10a10`表示从源图坐标为x:0,y:10处截取290x400的子图片。  

注意1：必须同时指定横轴偏移和纵轴偏移。  
注意2：计算偏移值会受到位置偏移指示符（/gravity/）影响。默认为相对于左上角计算偏移值（即NorthWest），参看裁剪锚点参数表。  

**转义说明**
部分参数以“!”开头，表示参数将被转义。为便于阅读，我们采用特殊转义方法，如下所示：

    p => % (percent)
    r => ^ (reverse)
    a => + (add)

即!50x50r实际代表50x50^这样一个字符串。  
而!50x50实际代表50x50这样一个字符串（该字符串并不需要转义）。  
<imageSizeAndOffsetGeometry>中的OffsetGeometry部分可以省略，缺省为+0+0。  
即/crop/50x50等价于/crop/!50x50a0a0，执行-crop 50x50+0+0语义。  

#### 请求
##### 请求报文格式

    GET <imageDownloadURI>?<接口规格> HTTP/1.1


#### 附注
+ 参数的顺序会影响结果
+ auto-orient 参数是和图像处理顺序相关的，一般建议放在首位（根据原图EXIF信息自动旋正）

#### 示例

    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/!75p

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/!75p)


    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/!75px

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/!75px)


    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/!x75p

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/!x75p)


    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/300x

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/300x)


    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/x300

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/x300)


    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/500x300

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/500x300)

    
    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/!500x300r

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/!500x300r)


    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/500x300!

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/500x300!)


    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/500x300<

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/500x300<)


    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/800x800>

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/800x800>)


    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/3600000@

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/thumbnail/3600000@)

**基础裁剪**

    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/crop/200x

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/crop/200x)

    
    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/crop/x200

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/crop/x200)


    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/crop/300x200

![]( http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/crop/300x200)


**偏移裁剪**


    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/gravity/Center/crop/!300x300a10a10

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/gravity/Center/crop/!300x300a10a10)


    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/gravity/Center/crop/!300x300-10a10

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/gravity/Center/crop/!300x300-10a10)


    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/gravity/Center/crop/!300x300a10-10

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/gravity/Center/crop/!300x300a10-10)


    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/gravity/Center/crop/!300x300-10-10

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageMogr/gravity/Center/crop/!300x300-10-10)

### 水印处理（watermark）

#### 描述
此接口提供图片水印、文字水印

#### 图片水印

##### 规格接口规格  
注意：接口规格不含任何空格与换行符，下列内容经过格式化以便阅读。

    watermark/1
             /image/<encodedImageURL>
             /dissolve/<dissolve>
             /gravity/<gravity>
             /dx/<distanceX>
             /dy/<distanceY>

|参数名称|必填|说明|
|--------|----|----|
|`/image/<encodedImageURL>`|是|水印源图片文件名（经过URL安全的Base64编码，现阶段只支持本系统中的图片作为水印），必须有效且返回一张图片|
|~~`/dissolve/<dissolve>`~~||~~透明度，取值范围1-100，缺省值为100（完全不透明）~~|
|`/gravity/<gravity>`|| 水印位置，参考水印锚点参数表，缺省值为SouthEast（右下角）|
|`/dx/<distanceX>`||横轴边距，单位:像素(px)，缺省值为10|
|`/dy/<distanceY>`||纵轴边距，单位:像素(px)，缺省值为10|

##### 水印锚点参数表

    NorthWest     |     North      |     NorthEast
                  |                |    
                  |                |    
    --------------+----------------+--------------
                  |                |    
    West          |     Center     |          East 
                  |                |    
    --------------+----------------+--------------
                  |                |    
                  |                |    
    SouthWest     |     South      |     SouthEast


#### 文字水印
**规格接口规格**  
注意：接口规格不含任何空格与换行符，下列内容经过格式化以便阅读。

    watermark/2
             /text/<encodedText>
             /font/<encodedFontName>
             /fontsize/<fontSize>
             /fill/<encodedTextColor>
             /dissolve/<dissolve>
             /gravity/<gravity>
             /dx/<distanceX>
             /dy/<distanceY>

|参数名称|必填|说明|
|`/text/<encodedText>`|是|水印文字内容（经过URL安全的Base64编码）|
|`/font/<encodedFontName>`||水印文字字体（经过URL安全的Base64编码），缺省为黑体。
注意：中文水印必须指定中文字体。|
|`/fontsize/<fontSize>`||水印文字大小，单位像素|
|`/fill/<encodedTextColor>`||印文字颜色，RGB格式，可以是颜色名称（比如red）或十六进制（比如#FF0000），缺省为白色|
|~~`/dissolve/<dissolve>`~~||~~透明度，取值范围1-100，缺省值100（完全不透明）~~|
|`/gravity/<gravity>`||水印位置，参考水印位置参数表，缺省值为SouthEast（右下角）|
|`/dx/<distanceX>`||横轴边距，单位:像素(px)，缺省值为10|
|`/dy/<distanceY>`||纵轴边距，单位:像素(px)，缺省值为10|



#### 请求
请求报文格式

    GET <imageDownloadURI>?<接口规格> HTTP/1.1

##### 图片水印

    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?watermark/1/gravity/SouthEast/image/NTRkNDY2MDhlMTM4MjM5YTUxYmZkYWQwLnBuZw==/dx/10/dy/10

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?watermark/1/gravity/SouthEast/image/NTRkNDY2MDhlMTM4MjM5YTUxYmZkYWQwLnBuZw==/dx/15/dy/15)

##### 文字水印示例

    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?watermark/2/gravity/SouthEast/text/QERvb2dJbWFnZQ==/font/Y29uc29sYXM=/fontsize/20/dx/15/dy/15

![](http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?watermark/2/gravity/SouthEast/text/QERvb2dJbWFnZQ==/font/Y29uc29sYXM=/fontsize/20/dx/15/dy/15)


### 图片基本信息（imageInfo）

#### 描述
图片基本信息包括图片格式、图片大小、色彩模型。  
在图片下载URL后附加imageInfo指示符（区分大小写），即可获取JSON格式的图片基本信息。

#### 请求

##### 请求报文格式
    GET <imageDownloadUri>?imageInfo HTTP/1.1

#### 示例

    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageInfo

    {
        "width": 640, 
        "height": 427, 
        "colorModel": "RGB", 
        "format": "JPEG"
    }


### 图片EXIF信息（exif）

#### 描述
EXIF（EXchangeable Image File Format）是专门为数码相机的照片设定的可交换图像文件格式，通过在图片下载URL后附加exif指示符（区分大小写）获取。  

注意：缩略图等经过云处理的新图片不支持该方法。

#### 请求

##### 请求报文格式
    GET <imageDownloadUri>?exif HTTP/1.1

#### 示例
    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?exif   

    {
        "YResolution": [72, 1],
        "ResolutionUnit": 2,
        "Make": "Canon",
        "Flash": 16,
        "SceneCaptureType": 0,
        "DateTime": "2011:11:19 17:09:23",
        "MeteringMode": 5,
        "XResolution": [72, 1],
        "LensSpecification": [
            [18, 1],
            [55, 1],
            [0, 1],
            [0, 1]
        ],
        "ExposureProgram": 3,
        "ColorSpace": 1,
        "ExifImageWidth": 640,
        "DateTimeDigitized": "2011:11:19 17:09:23",
        "DateTimeOriginal": "2011:11:19 17:09:23",
        "LensModel": "EF-S18-55mm f/3.5-5.6 IS II",
        "LensSerialNumber": "000030d5d1",
        "WhiteBalance": 0,
        "FNumber": [28, 5],
        "CustomRendered": 0,
        "ApertureValue": [5, 1],
        "FocalLength": [45, 1],
        "SubsecTimeOriginal": "11",
        "ExposureMode": 0,
        "BodySerialNumber": "094053007294",
        "ComponentsConfiguration": "\u0000\u0000\u0000\u0000",
        "FocalPlaneXResolution": [97379, 17],
        "ExifOffset": 168,
        "ExifImageHeight": 427,
        "SubsecTimeDigitized": "11",
        "ISOSpeedRatings": 3200,
        "Model": "Canon EOS 600D",
        "Orientation": 1,
        "ExposureTime": [1, 50],
        "FocalPlaneYResolution": [331079, 57],
        "SubsecTime": "11",
        "MaxApertureValue": [20599, 3971],
        "FlashPixVersion": "0100",
        "FocalPlaneResolutionUnit": 2,
        "ExifVersion": "0230"
    }


### 图片主色调（imageAve）

#### 描述
本接口用于计算一幅图片的平均色调，并以0xRRGGBB形式返回。

#### 请求
##### 请求报文格式
    GET <imageDownloadUri>?imageAve HTTP/1.1

#### 示例
    http://10.101.110.17:8888/54d46603e138239a51bfdacf.jpg?imageAve

    {"RGB": "0x050503"}
