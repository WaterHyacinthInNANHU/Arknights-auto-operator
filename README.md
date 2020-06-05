# 明日方舟刷图

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

运行依赖以下库

pyautogui                 0.9.48

keyboard                  0.13.4

baidu-aip                 2.2.18.0

安装命令

```
pip install pyautogui
pip install keyboard
pip install baidu-aip
```
也可以直接运行tools文件夹下的PackageConfig.bat自动安装依赖

5.百度API配置

养成材料清单生成功能需要用到百度文字识别的API，这里需要申请一个应用接口，按[这里的教程](https://blog.csdn.net/XnCSD/article/details/80786793?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task)申请即可，需要用到其中的AppID, API Key, Secrect Key三个参数

全部配置好之后管理员身份运行start.bat，控制台输出Welcome doctor!字样说明配置成功


<b>使用</b>

1.编写命令

打开code.txt，已有如下文本
code.txt
```python
#yourpassword

ark.password = "***"
ark.APP_ID = "***"
ark.API_KEY = "***"
ark.SECRECT_KEY = "***"

#your code:
#ark.foucusOnTheWindow()
#ark.mumuInit()

#ark.exitMumu()
```
将你的游戏密码和申请到的AppID, API Key, Secrect Key填入 *** 并在#your code下面写你的命令
 
就像python代码一样，'#'后的语句不会执行，可以用#控制命令生效与否

所有参数都是游戏中图标对应的拼音或数字字母组合

下面是所有支持的命令：
```python
ark.foucusOnTheWindow()#找到并点击mumu图标切换到mumu窗口
ark.mumuInit()#用来完成登录操作，启用后打开mumu然后运行程序就可以自动打开游戏并登录上去了
ark.exitMumu()#退出模拟器

#以下命令需要登录上去之后才能正常运行

ark.wuzichoubei("huowuyunsong","CE-5",4)#运行物资筹备，参数：资源类型，关卡，刷图次数
ark.xinpiansousuo("shenxianshizu","PR-D-1",4)#运行芯片搜索，参数：资源类型，关卡，刷图次数
ark.jiaomiemoshi("longmenwaihuan",1)#运行剿灭作战，参数：关卡，刷图次数
ark.zhuxian("chapter3","S3-3",4)#运行主线关卡，参数：章节，关卡，刷图次数
ark.generateMaterialList()#自动养成材料清单生成，保存在output下的MaterialList.txt
```

2.保存code.txt，打开mumu，用以下方式中一种运行程序：
管理员身份运行start.bat，正常模式
管理员身份运行start - shutdown.bat，运行完后自动关机


<b>图标生成</b>

由于程序运行的原理就是找到imgs文件夹里对应的图标然后点击，故图标资源的获取非常重要

但有时候可能会报错没找到对应的图标，这就需要手动添加了

然而我只是个萌新，只打到第五章，很多关卡图标我没法生成QWQ，这里也提供了图标生成工具

用法：

运行getImg.bat，会要输入图标的名字（一定要和imgs文件夹已有的图标名字不一样否则有覆盖原来图标的危险！！！一般名字就取图标的名字或拼音），输入后回车，移动鼠标尖尖到要截取的区域的左上角，按下空格，再移动到区域右下角，按下空格，这样截取好的图标会存在imgs文件夹下


<b>注意事项</b>

1.要以管理员身份运行，注意运行时不要让挡住mumu左上角图标
![avatar](https://raw.githubusercontent.com/WaterHyacinthInNANHU/-/master/imgs/mumumoniqi.jpg)

2.运行开始后运行信息会打印在终端，也会保存在log.txt

3.生成的MaterialList.txt中的内容可以由[企鹅物流刷图规划器](https://penguin-stats.io/planner)导入，省去自己添加已有材料的麻烦

4.运行程序时确保系统分辨率为1920*1080，显示比例为125%
