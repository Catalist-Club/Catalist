# 流浪动物公益社团项目

一个基于邮箱认证的流浪动物公益网站，致力于帮助流浪动物找到温暖的家。

## 项目特点

- 邮箱认证系统（注册/登录/登出）
- 响应式设计，适配移动端和桌面端
- 动物信息展示和上传功能
- 领养申请功能
- 管理员审核机制
- 用户间消息通信系统
- 多页面内容管理
- 动态内容编辑功能
- **猫脸识别系统**：支持管理员录入动物档案、生成 CNN 哈希、调整识别参数，并允许普通用户通过摄像头或图片识别动物身份

## 技术栈

- HTML5
- CSS3
- JavaScript (ES6+)
- Python HTTP服务器
- SQLite数据库

## 安装和运行

1. 克隆项目:
   ```
   git clone https://github.com/Catalist-Club/Catalist.git
   ```

2. 进入项目目录:
   ```
   cd Catalist
   ```

3. 安装 Python 依赖（需 Python 3.9+）:
   ```
   pip install -r requirements.txt
   ```
   
### 是这样的，Meow非常严肃地提醒用户如果电脑上没有GPU还硬要安装requirements.txt里的官方完整镜像的话会慢死并且GPU对此加速不显著，请通过如下命令代替requirements.txt:
  ```
   TMPDIR=~/pip_tmp pip install \
    legacy-cgi \
    -r requirements.txt \
    --no-cache-dir \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    --break-system-packages \
    --extra-index-url https://download.pytorch.org/whl/cpu
  ```
  如果你非常不讨厌浪费磁盘空间，使用如下命令：
  ```
    pip install -r requirements.txt \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    --no-cache-dir \
    --break-system-packages
  ```

4. （可选）下载动物脸识别模型权重文件并放置在 `models/cat_face/cat_resnet101.pth`。
   - 系统默认使用 ImageNet 预训练的 ResNet18 作为特征提取器。
   - 我们有已经训练好若干识别模型并且可以从[kaggle](https://www.kaggle.com/code/somehappy/thenbnotebook)上[下载](https://www.kaggle.com/code/somehappy/cat-face-detection-practive-resnet)。
   - 如需更精确的动物脸识别，可下载社区训练好的模型（例如某些 GitHub 仓库提供的 `cat_resnet18.pth`）并通过管理员面板更新模型路径。

5. 运行服务器:
   ```
   python server.py
   ```

6. 在浏览器中访问: http://localhost:40277

## 功能说明

### 用户认证
- 用户可以通过邮箱注册账户
- 注册时需要验证邮箱格式和密码强度
- 用户登录后可以申请领养动物
- 管理员账户拥有特殊权限

### 动物信息管理
- 展示待领养的动物信息
- 包括动物名称、年龄、性别、描述和图片
- 用户可以上传新的动物信息（需管理员审核）
- 管理员可以审核和管理所有动物信息

### 领养申请系统
- 登录用户可以申请领养动物
- 管理员可以查看和处理领养申请

### 内容管理系统
- 管理员可以编辑网站各页面的文本内容
- 动态内容加载，无需修改代码即可更新页面
- 多页面结构（首页、关于、联系方式等）

### 动物脸识别
- 管理员可通过“动物脸识别管理”面板创建动物档案，录入基础信息、特征描述、绝育/芯片状态等
- 支持上传多张参考图片，自动生成 CNN 哈希值，并可指定主展示图
- 识别参数（匹配阈值、返回结果数、哈希距离上限、模型权重路径等）可在后台实时调整
- 普通用户可在首页开启摄像头或上传图片识别动物，查看匹配度、档案详情和参考图像
- 识别请求会记录到数据库，便于后续追踪和调优

### 页面结构
- 首页：项目介绍和主要功能入口
- 关于页面：项目使命和团队介绍
- 联系页面：联系方式和地址信息
- 动物列表：待领养动物展示
- 消息中心：用户通信系统
- 管理员面板：管理功能入口
- 内容管理：网站文本编辑

## 开发说明

项目使用纯JavaScript实现前端功能，Python实现后端服务器和数据库操作。

## 项目结构

```
.
├── index.html          # 主页面
├── about.html          # 关于我们页面
├── contact.html        # 联系我们页面
├── admin.html          # 管理员控制台
├── upload.html         # 动物信息上传页面
├── messages.html       # 用户消息页面
├── content-management.html # 内容管理页面
├── css/
│   └── style.css       # 样式文件
├── js/
│   ├── auth.js         # 认证系统
│   └── main.js         # 主应用逻辑（包含动物脸识别前端代码）
├── backend/
│   ├── __init__.py
│   └── cat_recognition.py # 动物脸识别服务（PyTorch）
├── uploads/            # 用户上传的图片与识别查询
│   └── cat_references/ # 动物参考图像和自动生成的哈希
├── models/             # 可选的本地预训练模型（需要手动添加）
├── requirements.txt    # Python 依赖
├── server.py           # Python HTTP服务器和数据库操作
└── data/               # SQLite 数据文件目录
```
