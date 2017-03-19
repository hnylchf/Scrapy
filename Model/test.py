#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.append("..")
import logging.config
import re

str = '''看来我还是低估了BLZ的决心。尽管H难度相对比较便当，但M勇气试炼的难度充分展现了BLZ的恶意。只能说真是坑爹啊！
[img]../images/36bfdca017d47b2164a54b7e769b50d1_cfb37c34b980a9266e664ec2d244d582.jpg[/img]

　　整个副本技能枯燥乏味，但是组合反复无常，极度考验个人能力。可以说是专门为某些顶级pfu公会自虐设计的。
　　M奥丁具有长达11分钟的低容错流程，M高姆则有巨大的dps压力和紧凑的流程，还要求有极快的个人反应。M海拉就不提了，截至目前只有M会S会两个妖孽正常过，根本不在一般团队的考虑范围。
[img]../images/36bfdca017d47b2164a54b7e769b50d1_cfb37c34b980a9266e664ec2d244d582xxx.html[/img]
　　更气的是这三个boss除了个别职业的圣物之外根本不掉什么好东西，以至于伐木是几乎没有提升的。也就是说大家如果想体验一下M海拉，几乎只有等砍一条路。
　　前两天打进P3时候就想好要写这篇心得的，然而被众人演到今天才过。回头一看隔壁大表哥的帖子已经连高姆都推倒了。[img]../images/36bfdca017d47b2164a54b7e769b50d1_cfb37c34b980a9266e664ec2d244d582xxx.html[/img]
　　后面的开荒也许会比较零散比如说有全团巅峰再去碰狗之类的打算，所以这个副本系列打算做成三篇独立的攻略，打到哪里写到哪里。绝不是为了骗分！'''


# links = re.findall(r'\[img].*[/img]]', str)
# for l in links:
#     print l
#     str = str.replace(l,'xxxxxxxxxxx')
# print str



res = []
e = '[/img]'
str_list = str.split(e)
for s in str_list:
    list = []
    img_index = s.find('[img]')
    if img_index >= 1:
        text = s[0:img_index]
        img = s[img_index:len(s)] + "[/img]"
        list.append(text)
        list.append(img)
    else:
        list.append(s)
    res.append(list)

for s in res:
    if len(s) == 2:
        print 'text：' + s[0]
        print 'img：' + s[1]
    else:
        print 'text:'+s[0]