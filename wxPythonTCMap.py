# -*- coding: utf-8 -*-

import wx
import wx.xrc
import wx.richtext
import wx._adv, wx._html # 这行只是为了解决打包后运行时报错的问题
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from pandas import DataFrame
import pandas as pd

wx.ID_keywordInput = 1000
wx.ID_searchBtn = 1001
wx.ID_viewContent = 1002

###########################################################################
## Class getTCMapSearchList
###########################################################################

class getTCMapSearchList ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"抓取腾讯地图搜索列表", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

        self.keywordInput = wx.TextCtrl( self, wx.ID_keywordInput, u"宾馆", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.keywordInput, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

        self.searchBtn = wx.Button( self, wx.ID_searchBtn, u"搜索", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.searchBtn, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
        
        self.viewContent = wx.TextCtrl( self, wx.ID_viewContent, u"抓取腾讯地图中 坐标为：116.368490,39.978840 周边，在搜索列表中的 名称、电话、地址信息并保存成Excel\n===========================================\n", wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH|wx.VSCROLL )
        bSizer1.Add( self.viewContent, 1, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.searchBtn.Bind( wx.EVT_BUTTON, self.searchFunc )

    def __del__( self ):
        pass

    # Virtual event handlers, overide them in your derived class
    def searchFunc( self, event ):    
        self.TXMapInfoAll=DataFrame()
        self.browser = webdriver.Chrome()

        self.browser.get("https://map.qq.com/?type=around&where=116.368490,39.978840&radius=2000&what=" + self.keywordInput.GetValue() + "&c=11")

        self.contentStr = '抓取腾讯地图中 坐标为：116.368490,39.978840 周边，在搜索列表中的 名称、电话、地址信息并保存成Excel\n===========================================\n'
        self.contentStr += '==开始抓取=======================\n'
        self.viewContent.SetValue(self.contentStr)

        time.sleep(5)
        self.PoiResultDiv = self.browser.find_element_by_id("PoiResultDiv")
        self.html = self.PoiResultDiv.get_attribute('innerHTML')
        
        self.contentStr += '==抓取内容完毕=======================\n'
        self.viewContent.SetValue(self.contentStr)

        self.browser.close()

        self.contentStr += '==正在处理内容……=======================\n'
        self.viewContent.SetValue(self.contentStr)

        self.name = []
        self.phone = []
        self.address = []
        self.soup = BeautifulSoup(self.html, 'lxml')
        self.PoiName = self.soup.select('.PoiName')
        for pname in self.PoiName:
            self.name.append(pname.text)

        self.poiRichInfo = self.soup.select('.poiRichInfo')
        for pinfo in self.poiRichInfo:
            self.phone.append(pinfo.contents[3].text)
            self.address.append(pinfo.contents[5].text)
        # print(self.name)
        # print(self.phone)
        # print(self.address)
        self.contentStr += '==文件内容=======================\n'
        self.viewContent.SetValue(self.contentStr)
        self.TXMapInfo=DataFrame([self.name,self.phone,self.address]).T
        self.TXMapInfo.columns=['名称','电话','地址']
        self.TXMapInfoAll=pd.concat([self.TXMapInfoAll,self.TXMapInfo])        
        self.TXMapInfoAll.to_excel('TXMap.xls')
        self.contentStr += '==完成，文件已保存在项目根目录=======================\n'
        self.viewContent.SetValue(self.contentStr)
        # event.Skip()

if __name__ == '__main__':
    app = wx.App()
    frame = getTCMapSearchList(None)
    frame.Show()
    app.MainLoop()
