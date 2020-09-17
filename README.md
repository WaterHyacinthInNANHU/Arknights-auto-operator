# Arknights-auto-operator (Web Control Version)

## <b>Configuration</b>

- Install mumu emulator and install Arknights, log in to your own account once, and log out after success

- Install python environment, mine is 3.7.6, recommend 3.7 series version

- Modify the ActivateEnv.bat file:

```bat
call activate pyt
```

​		For conda users, please modify "pyt" to the name of the environment where you want the program to run

​		Non-conda users can delete this sentence directly (use the default environment), leave a blank file, and save

- Operating environment configuration:

  Installation command: Open the command line in the src folder:

```
pip install -r requirements.txt
```

- Baidu API configuration

  To develop the material list generation function, you need to use Baidu text recognition API, here you need to apply for an application interface. Click [this tutorial](https://blog.csdn.net/XnCSD/article/details/80786793?depth_1-utm_source =distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task) to apply for it, you need to use the AppID, API Key, Secrect Key three parameters of it.

  This API is only used to generate  `MaterialList.txt` , if you don't need it, just ignore this entry.

- After everything is configured, run start.bat as an administrator, and the console outputs Welcome doctor! to indicate that the configuration is successful

- Register account

  Register an account on the [website](http://101.132.147.44/arknights/public/index.php/login.html) I created

## <b>Usage</b>

- Double-click the ```start-myserver.bat``` file in the project root directory to start the program.
- Enter the [Console Page](http://101.132.147.44/arknights/public/index.php/panel) in the mobile browser, select the corresponding command and click to start execution.

## <b>Notes</b>

- After the operation starts, the operation information will be printed in the terminal and also saved in log.txt

- The content in the generated `MaterialList.txt` can be imported by [Penguin Logistics Planner](https://penguin-stats.io/planner), saving yourself the trouble of adding existing materials

- When running the program, ensure that the system resolution is 1920*1080, and the display ratio is 125%

- Be sure to adjust the input method to English before running the program!

- Before running the program, make sure that there is no expanded list in the taskbar (such as wifi list)



### Issues are always welcomed!





# 明日方舟刷图(网页控制版)

## <b>配置</b>

- 安装mumu模拟器并装好Arknights，并登录一次你自己的账号，成功后退出即可

- 安装python环境，我的是3.7.6，推荐3.7系列版本

- 修改ActivateEnv.bat文件：
  ActivateEnv.bat

```bat
call activate pyt
```

​		conda用户请将 "pyt" 修改为你想要程序运行所在的环境名

​		非conda用户直接删除这一句就行（使用默认环境），留下个空白文件，最后保存

- 运行环境配置：

  安装命令：在src文件夹下打开命令行：

```
pip install -r requirements.txt
```

- 百度API配置

  养成材料清单生成功能需要用到百度文字识别的API，这里需要申请一个应用接口，按[这里的教程](https://blog.csdn.net/XnCSD/article/details/80786793?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task)申请即可，需要用到其中的AppID, API Key, Secrect Key三个参数

  该API仅用于生成`MaterialList.txt`，如果您不需要它，则忽略此项配置。

- 全部配置好之后管理员身份运行start.bat，控制台输出Welcome doctor!字样说明配置成功

- 注册myserver账号

  在我建立的[网站](http://101.132.147.44/arknights/public/index.php/login.html)注册一个账号即可

## <b>使用</b>

- 双击项目根目录下的```start - myserver.bat``` 文件，启动程序。

- 手机浏览器进入[控制台页面](http://101.132.147.44/arknights/public/index.php/panel)，选择对应的命令并点击开始执行即可。

## <b>注意事项</b>

- 运行开始后运行信息会打印在终端，也会保存在log.txt

- 生成的MaterialList.txt中的内容可以由[企鹅物流刷图规划器](https://penguin-stats.io/planner)导入，省去自己添加已有材料的麻烦

- 运行程序时确保系统分辨率为1920*1080，显示比例为125%

- 运行程序之前请务必将输入法调整至英文！

- 运行程序之前请务必保证任务栏中无被展开的列表（比如wifi列表）



### Issues are always welcomed!