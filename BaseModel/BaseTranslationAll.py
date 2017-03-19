#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import httplib
import urllib
import random
import md5
import ConfigUtil
import json
import time
import logging.config


class BaseTranslationAll():
    fLang = None
    q = None
    toLang = None
    appid = ConfigUtil.getConfig('translation', 'translation_appid')
    secretKey = ConfigUtil.getConfig('translation', 'translation_secretKey')
    myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

    def __init__(self,query,fLang = 'zh',toLang='en'):
        self.q = query
        self.toLang = toLang
        self.fLang = fLang

    def send(self):
        en_text =  self.send_translation(self.q,self.fLang,self.toLang)
        cn_text =  self.send_translation(self.q,self.toLang,self.fLang)
        return cn_text

    def send_translation(self,q,from_lan='zh',to_lan='en'):
        url = ''
        try:
            q = q.encode('utf-8')
            salt = random.randint(32768, 65536)
            sign = self.appid + q + str(salt) + self.secretKey
            m1 = md5.new()
            m1.update(sign)
            sign = m1.hexdigest()
            query = urllib.quote(q)
            url = self.myurl + '?appid=' + self.appid + '&q=' + query + '&from=' + from_lan + '&to=' + to_lan + '&salt=' + str(
                salt) + '&sign=' + sign
        except Exception,e:
            print  e

        flag = True
        while flag:
            try:
                res = urllib.urlopen(url)
                html = res.read()
                j = json.loads(html)
                if j.has_key('error_code'):
                    error_code = j['error_code']
                    if error_code == 54005 or error_code == 54003: #访问频繁 暂停5秒
                        time.sleep(5)
                    elif error_code == 54004: #余额不足
                        logging.error('百度翻译余额不足')
                        flag = False
                else:
                    result = ''#组合多段文本返回
                    for r in j['trans_result']:
                        result = result + r['dst'] + '\n'
                    return result
            except Exception,e:
                flag = False
                logging.error(e)



if __name__ == '__main__':
    a = Translation('''前言
　　看来我还是低估了BLZ的决心。尽管H难度相对比较便当，但M勇气试炼的难度充分展现了BLZ的恶意。只能说真是坑爹啊！
　　整个副本技能枯燥乏味，但是组合反复无常，极度考验个人能力。可以说是专门为某些顶级pfu公会自虐设计的。
　　M奥丁具有长达11分钟的低容错流程，M高姆则有巨大的dps压力和紧凑的流程，还要求有极快的个人反应。M海拉就不提了，截至目前只有M会S会两个妖孽正常过，根本不在一般团队的考虑范围。
　　更气的是这三个boss除了个别职业的圣物之外根本不掉什么好东西，以至于伐木是几乎没有提升的。也就是说大家如果想体验一下M海拉，几乎只有等砍一条路。
　　前两天打进P3时候就想好要写这篇心得的，然而被众人演到今天才过。回头一看隔壁大表哥的帖子已经连高姆都推倒了。
　　后面的开荒也许会比较零散比如说有全团巅峰再去碰狗之类的打算，所以这个副本系列打算做成三篇独立的攻略，打到哪里写到哪里。绝不是为了骗分！
　　
M奥丁简介
　　M奥丁是一个又臭又长的boss。对团队个人能力有比较高的要求，也需要一定的硬件和配置。
　　4-5治疗的配置均可。但整体的dps压力并不算十分巨大，还是5治疗比较适合大众团队。
　　DPS方面，远程双/多线职业优势明显。无论是双线压血还是转火都是远程占优。近战最好不超过6个。
　　和H模式的机制区别只有两点：
　　P1和P2每一个小怪死在符文内后会点4个同色烙印debuff，需要在对应颜色符文上蹭一下获得“受到保护”buff，以抵挡下一次奥丁的神准冲击。没吃到的话不开免疫类技能必死。
　　P3会给每个人标一个符文烙印debuff，8秒后和15码内不同色的人互炸。
　　处理方法是每到一个场地标5个相距15码的光柱，同色光柱集合。如果回不来的保证15码内没有其他不同色的人即可。
　　P1基本是熟悉技能，P2主要考验的是机制处理，P3最麻烦的则是T的生存。
天赋推荐及理由
　　这个boss比较有趣的一点是，奶德所有的天赋都是有用的，每一层都有一个最合适的选择。
　　1.结界常规选择。考虑到符文使者阶段可能有多个治疗被点，结界远程辅助刷T的作用还是很明显的。其他两个作用不大。
　　2.闪现非常重要，第一时间带位吃buff的关键技能。P3远端放风闪现回来加速跑buff也是很有用的。请善用闪现后的加速。
　　3.平衡/守护亲和守护亲和是常规选择。由于站位会很分散，开荒早期经常会出现加不到人的情况，平衡亲和多5码射程也是可选的。
　　个人建议开荒早期选择平衡亲和，P2熟练进P3接近击杀之后再改换守护亲和。
　　4.蛮力猛击小怪可以晕，5秒足够你出圈躲个技能再走回来了。也可以在小怪残血时候直接晕到死自己提前跑位。另外两个作用不大。台风是作死选择
　　5-7.栽培+平常心+繁盛可以说是7.1版本奶德最强天赋组合，前几个天赋还有的变，这三个几乎是雷打不动通吃所有boss。
治疗策略分析
　　boss整体的压力并不算很大，而且比较恒定。但因为战斗时间太长(一般开荒会打到11分钟以上)，对续航控制是有一定要求的。
　　因此有必要仔细规划一下抬血技能的时间轴。毕竟大技能加的血越多，需要小技能的缺口就越少。整体的蓝就省下来了。
　　个人强烈推荐我们的2分钟宁静全部交在勇气号角上。这样P1可以放出两次，P2两次，P3如果打得慢也可以有2次。11分钟的boss放6次宁静，完全最大化效果。
　　具体时间节点是：P1第1、5次号角，P2两次号角，P3的第1、4次光辉冲击。这个时间轴很完美，几乎是完全卡cd施放。
　　boss并没有明显的治疗压力点，和治疗相关的减员点也并不多。减员大多是因为自己犯蠢没得救。
　　唯一值得注意的是，P2男人的勇气号角会紧接碎裂aoe。如果血不满的话，100w号角+70w碎裂伤害是有可能秒人的。因此一定要在号角吼完的一瞬间立即宁静。
　　而神准冲击aoe不会接碎裂，所以血线只需要满足吃下神准冲击而不死即可。后面有时间慢慢抬。其他治疗的3分钟抬血可以轮流交给P2的神准冲击。
　　理论上激活能用4次。但因为P1压力很小，进P2几乎满蓝。从P2开始尽量吃到3次激活。
　　规划一下的话大致是：P2第一个女人、P2第二个男人、P3第二或第三个场地。
　　引导药水最好进P3再喝(没有碎片跑来晕你和长枪戳菊花了)。第一个风只要不点你直接原地坐下喝水。还有个激活的情况下，这些蓝P3肯定够用了。
　　两次神准冲击的间隔约为1分10秒，所以每一个小boss阶段都会有繁盛。最好交在大家都在跑buff期间。神器1分半cd，尽量卡cd使用吧。
P1: Might of the Valarjar
　　参考aoe时间轴如下图：''')
    html = a.send()
    print html