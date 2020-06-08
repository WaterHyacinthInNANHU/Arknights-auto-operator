# 明日方舟刷图(网页控制版)

<b>配置</b>

1.安装mumu模拟器并装好Arknights，并登录一次你自己的账号，成功后退出即可

2.安装python环境，我的是3.7.6，推荐3.7及以上

3.修改ActivateEnv.bat文件：
ActivateEnv.bat

```bat
call activate pyt
```

conda用户请将 "pyt" 修改为你想要程序运行所在的环境名

非conda用户直接删除这一句就行（使用默认环境），留下个空白文件，最后保存

4.运行环境配置：

安装命令：在src文件夹下打开命令行：

```
pip install -r requirements.txt
```

5.百度API配置

养成材料清单生成功能需要用到百度文字识别的API，这里需要申请一个应用接口，按[这里的教程](https://blog.csdn.net/XnCSD/article/details/80786793?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task)申请即可，需要用到其中的AppID, API Key, Secrect Key三个参数

全部配置好之后管理员身份运行start.bat，控制台输出Welcome doctor!字样说明配置成功

6.注册myserver账号

在我建立的[网站](http://101.132.147.44/arknights/public/index.php/login.html)注册一个账号即可

<b>使用</b>

1.双击项目根目录下的```start - myserver.bat``` 文件，启动程序。

2.手机浏览器进入[控制台页面](http://101.132.147.44/arknights/public/index.php/panel)，选择对应的命令并点击开始执行即可。


<b>图标生成</b>

由于程序运行的原理就是找到imgs文件夹里对应的图标然后点击，故图标资源的获取非常重要

但有时候可能会报错没找到对应的图标，这就需要手动添加了

然而我只是个萌新，只打到第五章，很多关卡图标我没法生成QWQ，这里也提供了图标生成工具

用法：

运行getImg.bat，会要输入图标的名字（一定要和imgs文件夹已有的图标名字不一样否则有覆盖原来图标的危险！！！一般名字就取图标的名字或拼音），输入后回车，移动鼠标尖尖到要截取的区域的左上角，按下空格，再移动到区域右下角，按下空格，这样截取好的图标会存在imgs文件夹下


<b>注意事项</b>

1.运行开始后运行信息会打印在终端，也会保存在log.txt

2.生成的MaterialList.txt中的内容可以由[企鹅物流刷图规划器](https://penguin-stats.io/planner)导入，省去自己添加已有材料的麻烦

3.运行程序时确保系统分辨率为1920*1080，显示比例为125%
