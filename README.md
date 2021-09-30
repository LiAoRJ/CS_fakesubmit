# CS_fakesubmit
一个可以伪装上线Cobaltstrike的脚本  
@Author：F12团队成员 LiAoRJ  
相关原理文章已经发布在奇安信攻防社区
地址：
https://forum.butian.net/share/708

脚本使用方法
先利用项目中解密Publickey    
https://github.com/Sentinel-One/CobaltStrikeParser  
python parse_beacon_config.py stage文件名 —json
在Public_key.txt中放入通过Beacon解密获得的Publickey   
在Process_name.txt 中加入上线进程的字典  
在Computer_name.txt 中加入受控机名称的字典   
在User_name.txt 中加入受控机用户名的字典   


公众号:F12sec

官网：http://www.0dayhack.net/

![qrcode_for_gh_195dee428fe9_258](https://img-blog.csdnimg.cn/img_convert/3206b48bd631855d8295aefd35692aee.png)



