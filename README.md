# tflearn_captcha_crack
使用TFLearn构建卷积神经网络识别验证码的尝试。

**⚠️注意：** 该仓库不提供训练数据集、训练结果模型，包含模型文件`seu_captcha.tflearn.*`为存放示例。

### 测试方法与结果

（附测试log）

* 测试对象：如example目录下图片


* 同时使用原PIL库分析方法和CNN预测，对比结果


* 500张准确率约为99.6%

### 环境与依赖

**建议使用Anaconda，并隔离环境**

* TensorFlow
* TFLearn
* Numpy
* PIL（Pillow）

### 模块使用方法

1. 配置参数

```python
MODEL_NAME = 'seu_captcha.tflearn' # 模型名称

MAX_CAPTCHA = 4  # 验证码字符长度（4位验证码）（4）
CHAR_SET_LEN = 10  # 验证码字符取值（0-9）（10）
IMAGE_WIDTH = 210  # 图像宽度
IMAGE_HEIGHT = 100  # 图像高度
```

2. 抓取验证码并转换为 `PIL.Image` 对象

```python
import requests  # 此处使用requests库发起请求
from PIL import Image
import io

response = requests.get(VERCODE_URL)
img = Image.open(io.BytesIO(response.content))
```

3. 初始化CNN

```python
from tflearn_captcha_crack import CNN_Captcha_Crack

cnn = CNN_Captcha_Crack()
```

4. 使用CNN识别验证码

```python
result = cnn.predict(img)
```





