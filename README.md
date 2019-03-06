## PT-Attend
PT-Attend是一个脚本合集，用来进行自动签到，可以顺便保号（大概），站点不是很多，因此暂时只有5个脚本
### 依赖
pip3 install opencv-python bs4 html5lib
如果u2跑起来有问题的话就再apt install -y python-opencv
### 使用方式
在Scripts文件夹内对应脚本处填写自己的站点Cookie，可以在谷歌浏览器的开发模式中找到：
![Cookie](https://i.loli.net/2019/03/06/5c7fa60d29a72.png)
对于幼儿园，由于使用了谷歌识图，所以在大陆机器上使用请配置好代理，脚本中已经预留了位置；

完成Cookie填写后将在Scri目录下的.Execute_in_Sequence.sh和.Auto_Clean.sh加入crontab即可，例如：
```
# PT Auto Attend
58 23 * * * /home/PT-Attend/Script/.Auto_Clean.sh
0 * * * * /home/PT-Attend/Script/.Execute_in_Sequence.sh
```
