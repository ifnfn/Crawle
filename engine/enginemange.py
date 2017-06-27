#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import re
import traceback

from .fetchTools import fetch, RegularMatch
from .engines import EngineCommands, commands
from .kindlepush import JDEngine
from .zi5 import Zi5Engine
from .sokindle import SokindleEngine

MAX_TRY = 3


class KolaEngine:
    def __init__(self):
        self.engines = []
        self.parserList = []
        self.UpdateAlbumFlag = False

        # self.AddEngine(JDEngine)
        # self.AddEngine(Zi5Engine)
        self.AddEngine(SokindleEngine)

    def GetCommand(self):
        return commands.GetCommand()

    def AddEngine(self, egClass):
        eg = egClass()
        self.engines.append(eg)
        self.parserList.extend(eg.parserList)

    # 解析菜单网页解析
    def ParserHtml(self, js):
        try:
            for engine in self.parserList:
                if engine.name == js['engine']:
                    return engine.cmd_parser(js)
        except:
            t, v, tb = sys.exc_info()
            print("VideoEngine.ParserHtml:  %s,%s, %s" %
                  (t, v, traceback.format_tb(tb)))

        return None

    def Start(self):
        for eng in self.engines:
            eng.Start()

    # {'source'  : 'http://v.qq.com/movielist/10001/0/10004-100001/0/0/100/0/0.html',
    #   'regular': ['(<h6.*?>[\\s\\S]*?</h6>|<a href=.*class="next".*</a>)'],
    #   'engine' : 'engine.qq.ParserAlbumList',
    #   'cache'  : False
    # }
    def ProcessCommand(self, cmd, times=0):
        ret = False
        cached = True
        found = False
        response = ''

        if times > MAX_TRY or type(cmd) != dict:
            return None
        try:
            # 获取数据 response
            if 'text' in cmd:
                response = cmd['text']
            else:
                if 'source' in cmd:
                    url = cmd['source']
                    method = "GET"
                    body = None
                    header = {}

                    if 'cache' in cmd:
                        cached = cmd['cache']
                    if 'method' in cmd:
                        method = cmd['method']
                    if 'header' in cmd:
                        header = cmd["header"]
                    if 'body' in cmd:
                        body = cmd['body']

                    response, found = fetch(url, method, header, body, cached)
                else:
                    return None

            if found == False:
                return None

            # 对数据 response 转码
            coding = 'utf8'
            try:
                if type(response) == bytes:
                    response = response.decode(coding)
            except:
                coding = 'GB18030'
                if type(response) == bytes:
                    response = response.decode(coding)

            # 数据正则匹配
            if 'regular' in cmd:
                response = self.RegularMatch(
                    cmd['regular'], response).encode(coding)
            if response:
                if type(response) == bytes:
                    response = response.decode(coding)
                cmd['data'] = response
            else:
                print("[WARNING] Data is empty", cmd['source'])

            return self.ParserHtml(cmd)
        except:
            t, v, tb = sys.exc_info()
            print("ProcessCommand playurl: %s, %s, %s" %
                  (t, v, traceback.format_tb(tb)))
            return self.ProcessCommand(cmd, times + 1)

        return None
