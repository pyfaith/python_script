# -*- coding: utf-8 -*-
# Date: 2018/9/23
'''
21点游戏规则:
    10、J、Q、K点数都当作10点，
    A可当作1点或11点，
    2到9则为原面值点数。
    一开始将各发给玩家两张牌，
    玩家可以看到庄家其中一张牌，
    之后可根据自己的牌点数和庄家那张已翻开的牌，
    决定是否要补牌。
    牌值以求取得更接近21点，而又不超过21点的点数。
    点数越大且不超过21点为胜方。
'''

import time
import random
import sys


class Card:
    '''创建扑克牌类, 每个对象代表一张牌
    '''
    def __init__(self, card_type, card_text, card_value):
        '''记录一张牌的信息,

        :param card_type: str
            牌面类型(♥♠♦♣)
        :param card_name: str
            牌面显示文本(k,Q, A)
        :param card_value: int
            牌面真实的点数(10, 9,8)
        '''
        self.card_type = card_type
        self.card_text = card_text
        self.card_value = card_value

class Role:
    '''创建角色类, 用来表示庄家与玩家'''
    def __init__(self):
        '''
        :param card: Card
            牌面
        '''

        #定义一个空列表, 用来存储当前角色手中的牌
        self.cards = []

    def show(self):
        '''用来展示角色手中所有的牌'''
        for card in self.cards:
            print(card.card_type, card.card_text, sep="", end="")
        #打印当前角色手中所有牌后,用于控制换行
        print()

    def get_value(self, min_or_max):
        '''获得当前角色手中牌的点数.(分最小值和最大值)
        :param min_or_max: "max", "min"
            当值为min时,返回的是最小点数, 即所有的A当成1时的点数.(用来判断是否爆牌的情况)
            当值为max时, 返回的是在不爆牌的前提下的可表示的最大点数,此时A可能表示11, 也可能表示1.
        '''

        #总的点数
        sum2 = 0
        #A牌面出现的次数
        A = 0

        for card in self.cards:
            #累加计算总的点数
            sum2 += card.card_value
            if card.card_text == "A":
                #获取A出现的次数
                A += 1

        if min_or_max == "max":
            for i in range(A):
                # 在总的点数上 -10 , 即将A当做1点看待
                value = sum2 - i * 10
                if value <= 21:
                    return value

        #最小值,即将所有A当做1来看待,则最大值和最小值相等
        return sum2 - A * 10

    def burst(self):
        '''
        判断是否爆牌
        :return: bool
        '''
        #判断是否爆牌只需判断最小值是否>21点即可
        return self.get_value("min") > 21

class CardManger:
    '''扑克牌管理类, 管理一整副扑克牌, 并且能够进行发牌'''

    def __init__(self):
        #定义空列表,用来储存扑克牌,52张
        self.cards = []
        #定义所有牌的类型
        all_card_type = "♥♠♦♣"
        #定义所有牌面所显示的文本
        all_card_text = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
        #定义所有牌面文本对应的真实点数
        all_card_value = [11, 10, 10, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2]

        #对牌面类型及牌面显示文本进行遍历
        for card_type in all_card_type:
            for index, card_text in enumerate(all_card_text):
                #创建Card类型的对象(一张扑克牌)
                card = Card(card_type, card_text, all_card_value[index])
                #将创建好的对象加入到整副扑克牌中
                self.cards.append(card)

        #打乱牌面顺序, 洗牌操作
        random.shuffle(self.cards)

    def send_card(self, role, num=1):
        '''发牌操作

        :param role: Role
            电脑或玩家对象
        :param num: int
            发牌的次数, 默认为1
        :return:
        '''
        for i in range(num):
            card = self.cards.pop()
            role.cards.append(card)

def main():

    #获取一整副牌
    cards = CardManger()
    #定义电脑(庄家)对象
    computer = Role()
    #定义玩家对象
    palyer = Role()

    #开始发牌, 给庄家发一张牌, 玩家发两张牌
    cards.send_card(computer)
    cards.send_card(palyer, 2)
    #显示庄家和玩家手中的牌
    computer.show()
    palyer.show()

    #询问玩家是否要牌
    while True:
        choice = input("是否再要一张牌?(y/n)")
        if choice == "y":
            cards.send_card(palyer)
            #发完牌后显示庄家和玩家手中的牌
            computer.show()
            palyer.show()
            #判断玩家是否爆牌
            if palyer.burst():
                print("爆牌, 您输了!")
                sys.exit()
        #玩家不要牌了,停止发牌
        else:
            break

    #玩家停牌, 庄家发牌. 只要庄家点数<17点, 就不断发牌,在>17点, <=21点时, 停牌
    while True:
        print("庄家发牌中...")
        time.sleep(1)
        cards.send_card(computer)
        #显示牌面
        computer.show()
        palyer.show()

        #判断庄家是否爆牌
        if computer.burst():
            print("庄家爆牌了, 你赢了!")
            sys.exit()
        #判断庄家牌面是否大于17, 大于停牌
        elif computer.get_value("max") >= 17:
            break

    #如果庄家和玩家都没有爆牌, 则比较点数大小
    computer_value = computer.get_value("max")
    palyer_value = palyer.get_value("max")


    if computer_value > palyer_value:
        print("你输了, 庄家牌比你大!")
    elif computer_value == palyer_value:
        print("平局")
    else:
        print("你赢了")

if __name__ == '__main__':
    main()








