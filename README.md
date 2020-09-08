# SankakuDownloader v2.0

2020.9.8更新 测试目前可用

- 本工具用于批量下载Sankaku图站的acg图片
- 使用Python编写，PyQt5构建UI，更易于使用
- Windows版本使用PyInstaller封装，不需要安装Python即可使用
- 捆绑Aria2下载工具，支持断点续传，更稳定的下载
- 支持登入账号以使用完整的标签功能
- 支持账号信息保存
- 支持设定下载开始页，快速跳过已下载的部分
- 当下载因为各种原因停止后都会保存下载失败的url，方便用户使用其他工具重新下载


- 使用前请仔细阅读下面的说明与注意事项！

## Windows版使用方法
![](https://github.com/natsuz0ra/SankakuDownloader/raw/master/win_example.png)

从[这里](https://github.com/natsuz0ra/SankakuDownloader/releases "这里")下载打包好的版本即可，解压即可使用！
如果需要从py源码运行可以参考下文，将命令中的3去掉即可（根据所配置的环境来）。

## MacOS版使用方法
![](https://github.com/natsuz0ra/SankakuDownloader/raw/master/mac_example.png)

很遗憾，MacOS版目前还没有找到打包后就可以直接跑起来的方法，目前遇到无法启动aria2以及文件无法读取写入等问题，可能还需要一定的时间（也可能不会有，目前对MacOS软件的相关机制还完全不了解）。
下面会介绍Python源码直接使用的方法，可能会比较繁琐 :（

- 安装git
- 运行以下命令：

```shell
 git clone https://github.com/natsuz0ra/SankakuDownloader.git
 cd SankakuDownloader/MacOS_ver（此处根据你的系统选择）
 pip3 install -r requirements.txt
```
- 待需要的包下载完毕后，点击[这里](https://github.com/aria2/aria2/releases/tag/release-1.35.0 "这里")下载MacOS版本的Aria2；
- 解压，将名为aria2的可执行文件更名为aria2_sd，并放到MacOS_ver文件夹中；
- 在MacOS_ver文件夹下运行以下命令运行：

```shell
 python3 main.py
```
- 尽情下载吧！

## 需要注意的地方
- 标签请在chan上设定好后从URL复制到标签框里，必须是要chan所支持的才行
- 标签的数目以及条件过滤等功能不是无限制使用的，登入后限制小一点（会员限制更少）
- 未登入使用会有50页的限制，目前登入后可以解决（不排除未来会加会员限制）
- 在登入后会自动关闭账号的敏感内容过滤选项（beta有，chan不清楚），不确定对下载是否有影响
- 一些被版权和谐的标签（图片）应该也能够下载，只要chan上能获取到数目
- Sankaku的图片服务器本身似乎有下载速度限制，1m/s是正常现象
- 软件有时可能会自动退出，也许是网络问题（概率不大）
- 因崩溃自动退出时无法保存失败列表
- 不要让其他软件占用7865端口，有能力的大佬也可以下源码来改着用
- 什么？1.0？那个只是个很简陋的东西就不用在意了233，而且也随着api的变动而失效
