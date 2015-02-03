### 运行环境
Python 2.7.8

### 服务器/WEB框架
tornado (4.0.2)

### 依赖库
* 图像处理 Pillow (2.7.0)
* EXIF信息 [pyexiv2](http://tilloy.net/dev/pyexiv2/) (0.3.2)


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
**请求报文格式**
    
    GET <ImageDownloadURI>?<接口规格> HTTP/1.1

#### 示例
说明：
原图规格`600 * 400`


**mode=0**

    <ImageDownloadURI>?imageView/0/w/500/h/200

返回图片规格为`300 * 200`

**计算过程**

    w = 600 # 原图宽度600像素
    h = 400 # 原图高度400像素
    origin_long_edge = 600 # 原图长边600像素
    origin_short_edge = 400 # 原图短边400像素

    long_edge = 500 # 缩放后长边最多为500像素
    short_edge = 200 # 缩放后短边最多为200像素

    ratio_long = long_edge / origin_long_edge = 0.83
    ratio_short = short_edge / origin_short_edge = 0.50
    # 取比例的最小值
    min_ratio = min(ratio_long, ratio_short) = 0.50

    resize_long_edge = origin_long_edge * min_ratio = 300 # 长边要求最多为500
    resize_short_edge = origin_short_edge * min_ratio = 200 # 短边要求最多为200


**mode=1**

    <ImageDownloadURI>?imageView/1/w/500/h/200

返回图片规格为 `500 * 200`

**计算过程**

    w = 600 # 原图宽度600像素
    h = 400 # 原图高度400像素

    with = 500 # 宽度要求最少为500像素
    height = 200 # 高度要求最少为200像素

    ratio_w = width / w = 0.83
    ratio_h = height / h = 0.50
    # 取最大比例
    max_ratio = max(ratio_w, ratio_h) = 0.83 

    # 图片缩放后大小
    resize_w = w * max_ratio = 500 
    resize_h = h * max_ratio = 332

    # 图片居中裁剪 
    # 以左上角为圆点(0, 0)，右上角为(w, 0), 左下角为(0, h)
    # 依次左、上、右、下
    box[0] = (resize_w - w) / 2 = 0
    box[1] = (resize_h - h) / 2 = 66
    box[2] = box[0] + w = 500
    box[3] = box[1] + h = 266


**mode=2**

    <ImageDownloadURI>?imageView/2/w/500/h/200

返回图片规格为`300 * 200`

**计算过程**

    w = 600 # 原图宽度600像素
    h = 400 # 原图高度400像素

    with = 500 # 宽度要求最多为500像素
    height = 200 # 高度要求最多为200像素

    ratio_w = width / w = 0.83
    ratio_h = height / h = 0.50
    # 取最小比例
    min_ratio = min(ratio_w, ratio_h) = 0.50 

    # 图片缩放后大小
    resize_w = w * min_ratio = 300 # 宽度最多500像素
    resize_h = h * min_ratio = 200 # 高度最多200像素


**mode=3**

    <ImageDownloadURI>?imageView/2/w/500/h/200

返回图片规格为`500 * 332`

**计算过程**

    w = 600 # 原图宽度600像素
    h = 400 # 原图高度400像素

    with = 500 # 宽度要求最多少500像素
    height = 200 # 高度要求最少为200像素

    ratio_w = width / w = 0.83
    ratio_h = height / h = 0.50
    # 取最大比例
    max_ratio = max(ratio_w, ratio_h) = 0.83 

    # 图片缩放后大小
    resize_w = w * min_ratio = 500 # 宽度最少500像素
    resize_h = h * min_ratio = 332 # 高度最少200像素


**mode=4**

    <ImageDownloadURI>?imageView/2/w/500/h/200

返回图片规格为`500 * 332`

**计算过程**

    w = 600 # 原图宽度600像素
    h = 400 # 原图高度400像素
    origin_long_edge = 600 # 原图长边600像素
    origin_short_edge = 400 # 原图短边400像素

    long_edge = 500 # 缩放后长边最少为500像素
    short_edge = 200 # 缩放后短边最少为200像素

    ratio_long = long_edge / origin_long_edge = 0.83
    ratio_short = short_edge / origin_short_edge = 0.50
    # 取比例的最小值
    max_ratio = max(ratio_long, ratio_short) = 0.83
  
    # 图片缩放后大小
    resize_long_edge = w * min_ratio = 500 # 长边最少500像素
    resize_ratio_short = h * min_ratio = 332 # 短边最少200像素

**mode=5**

    <ImageDownloadURI>?imageView/2/w/500/h/200

返回图片规格为`500 * 200`

    w = 600 # 原图宽度600像素
    h = 400 # 原图高度400像素
    origin_long_edge = 600 # 原图长边600像素
    origin_short_edge = 400 # 原图短边400像素

    long_edge = 500 # 缩放后长边最少为500像素
    short_edge = 200 # 缩放后短边最少为200像素

    ratio_long = long_edge / origin_long_edge = 0.83
    ratio_short = short_edge / origin_short_edge = 0.50
    # 取比例的最小值
    max_ratio = max(ratio_long, ratio_short) = 0.83

    # 图片缩放后大小
    resize_long_edge = w * min_ratio = 500 # 长边最少500像素。即缩放后宽度
    resize_ratio_short = h * min_ratio = 332 # 短边最少200像素。即缩放后高度
    resize_w = resize_long_edge
    resize_h = resize_ratio_short

    # 图片居中裁剪 
    box[0] = (resize_w - long_edge) / 2 = 0
    box[1] = (resize_h - short_edge) / 2 = 66
    box[2] = box[0] + long_edge = 500
    box[3] = box[1] + short_edge = 266


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


**缩放操作参数表***

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
**请求报文格式**

    GET <imageDownloadURI>?<接口规格> HTTP/1.1

#### 示例
说明：
原图规格`600 * 400`

**缩放操作**

**请求参数**

    <ImageDownloadURI>?imageMogr/thumbnail/!75p

返回图片规格为`450 * 300`

**计算过程**

    w = 600 # 原图宽为600像素
    h = 400 # 原图高为400像素
    scale = 75 # 缩放系数

    resize_w = w * (scale / 100) = 450 # 缩放后宽度为450像素
    resize_h = h * (scale / 100) = 300 # 缩放后高度为300像素 


**请求参数**

    <ImageDownloadURI>?imageMogr/thumbnail/!75px

返回图片规格`450 * 400`

**计算过程**

    w = 600 # 原图宽为600像素
    h = 400 # 原图高为400像素
    scale = 75 # 缩放系数

    resize_w = w * (scale / 100) = 450 # 缩放后宽度为450像素
    resize_h = h = 400 # 高度不缩放


**请求参数**

    <ImageDownloadURI>?imageMogr/thumbnail/!x75p

返回图片规格`600 * 300`

**计算过程**

    w = 600 # 原图宽为600像素
    h = 400 # 原图高为400像素
    scale = 75 # 缩放系数

    resize_w = w = 600 # 高度不缩放
    resize_h = h * (scale / 100) = 300 # 缩放后高度为300像素


**请求参数**
    
    <ImageDownloadURI>?imageMogr/thumbnail/300x

返回图片规格`300 * 200`

**计算过程**
    
    w = 600 # 原图宽为600像素
    h = 400 # 原图高为400像素
    resize_w = 300 # 缩放后图片宽度为300像素

    ratio = resize_w / w = 0.50 # 缩放比例为0.50
    resize_h = h * ratio = 200 # 高度等比缩放


**请求参数**

    <ImageDownloadURI>?imageMogr/thumbnail/x300

返回图片格式`450 * 300`

**计算过程**

    w = 600 # 原图宽为600像素
    h = 400 # 原图高为400像素
    resize_h = 300 # 缩放后图片高度为300像素

    ratio = resize_h / h = 0.75 # 高度缩放比例
    resize_w = w * ratio = 450 # 宽度等比缩放


**请求参数**

    <ImageDownloadURI>?imageMogr/thumbnail/500x300

返回图片规格`450 * 300`
    
**计算过程**
    
    w = 600 # 原图宽为600像素
    h = 400 # 原图高为400像素
    long_edge = 500 # 缩放后最大长边
    short_edge = 300 # 缩放后最大短边

    origin_long_edge = max(w, h) = 600 # 长边
    origin_short_edge = min(w, h) = 400 # 短边
        
    ratio_long = long_edge / origin_long_edge = 0.83 # 长边缩放比例
    ratio_short = short_edge / origin_short_edge = 0.75 # 短边缩放比例
    # 目标图片在指定高宽内，取最小缩放比例
    min_ratio = min(ratio_long, ratio_short) = 0.75 # 最小缩放比例

    resize_w = w * min_ratio = 450 # 缩放后宽度
    resize_h = h * min_ratio = 300 # 缩放后高度


**请求参数**
    
    <ImageDownloadURI>?imageMogr/thumbnail/!500x300r

返回图片格式`500 * 332`

**计算过程**
    
    w = 600 # 原图宽为600像素
    h = 400 # 原图高为400像素
    long_edge = 500 # 缩放后最大长边
    short_edge = 300 # 缩放后最大短边

    origin_long_edge = max(w, h) = 600 # 长边
    origin_short_edge = min(w, h) = 400 # 短边
        
    ratio_long = long_edge / origin_long_edge = 0.83 # 长边缩放比例
    ratio_short = short_edge / origin_short_edge = 0.75 # 短边缩放比例
    # 目标图片在指定高宽外，取最大缩放比例
    max_ratio = min(ratio_long, ratio_short) = 0.83 # 最小缩放比例

    resize_w = w * max_ratio = 500 # 缩放后宽度
    resize_h = h * max_ratio = 332 # 缩放后高度


**请求参数**
    
    <ImageDownloadURI>?imageMogr/thumbnail/500x300!

返回图片格式`500 * 300`

**计算过程**
    
    w = 600 # 原图宽为600像素
    h = 400 # 原图高为400像素
    width = 500 # 缩放后宽度
    height = 300 # 缩放后高度

    resize_w = width
    resize_h = height 


**请求参数**
    
    <ImageDownloadURI>?imageMogr/thumbnail/500x300>

返回图片格式`500 * 300`

**计算过程**
    
    w = 600 # 原图宽为600像素
    h = 400 # 原图高为400像素
    # 仅当宽、高都比原图小时才会进行缩放
    width = 500 # 缩放后宽度
    height = 300 # 缩放后高度

    ratio_w = width / w = 0.83
    ratio_h = height / w = 0.75
    # 取最小比例
    min_ratio = min(ratio_w, ratio_h) = 0.75

    resize_w = w * min_ratio = 500 
    resize_h = h * min_ratio = 332


**请求参数**
    
    <ImageDownloadURI>?imageMogr/thumbnail/800x800<

返回图片格式`800 * 532`

**计算过程**
    
    w = 600 # 原图宽为600像素
    h = 400 # 原图高为400像素
    # 仅当宽、高都比原图大时才会进行缩放
    width = 800 # 缩放后宽度
    height = 800 # 缩放后高度

    ratio_w = width / w = 1.33
    ratio_h = height / w = 2.00
    min_ratio = min(ratio_w, ratio_h) = 1.33

    resize_w = w * min_ratio = 800 
    resize_h = h * min_ratio = 532


**请求参数**
    
    <ImageDownloadURI>?imageMogr/thumbnail/3600000@

返回图片格式`800 * 532`

**计算过程**
    
    w = 600 # 原图宽为600像素
    h = 400 # 原图高为400像素
    max_area = 360000 # 等比例缩放后最大像素为3600000
    origin_area = w * h = 240000 # 原图像素

    ratio = math.sqrt(max_area / origin_area) = 3.87 # 面积比开方即为等比缩放比例

    resize_w = w * ratio = 2322 # 缩放后宽度
    resize_h = h * ratio = 1548 # 缩放后高度



**基础裁剪**

**请求参数**
    
    <ImageDownloadURI>?imageMogr/thumbnail/3600000@

返回图片格式`800 * 532`

**计算过程**
    
    w = 600 # 原图宽为600像素
    h = 400 # 原图高为400像素
    max_area = 360000 # 等比例缩放后最大像素为3600000
    origin_area = w * h = 240000 # 原图像素

    ratio = math.sqrt(max_area / origin_area) = 3.87 # 面积比开方即为等比缩放比例

    resize_w = w * ratio = 2322 # 缩放后宽度
    resize_h = h * ratio = 1548 # 缩放后高度


