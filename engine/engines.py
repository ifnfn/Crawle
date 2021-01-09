#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import traceback
import queue
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs

MAX_TRY = 3


class EngineCommands:
    """
    命令管理器
    """

    def __init__(self):
        self.cmd_queue = queue.Queue()
        self.quit = False

    def AddCommand(self, cmd):
        if 'source' in cmd or 'text' in cmd:
            self.cmd_queue.put(cmd)

    def GetCommand(self):
        ret = None
        while not ret:
            try:
                ret = self.cmd_queue.get(True, 3)
            except:
                if self.quit:
                    return None

        return ret


commands = EngineCommands()


class KolaParser:
    """
    网页解析器
    """

    def __init__(self, url=None):
        self.cmd = {}
        self.name = self.__class__.__module__ + '.' + self.__class__.__name__
        self.cmd['engine'] = self.name
        self.cmd['cache'] = True
        if url:
            self.cmd['source'] = url


    def Finish(self):
        global commands
        commands.quit = True

    def AddCommand(self):
        global commands
        if self.cmd:
            try:
                commands.AddCommand(self.cmd)
            except:
                t, v, tb = sys.exc_info()
                print("VideoEngine.ParserHtml:  %s,%s, %s" %
                      (t, v, traceback.format_tb(tb)))
                print(self.cmd)

    def cmd_parser(self, text):
        return None


    def Html(self, text):
        return bs(text, "html.parser", exclude_encodings='UTF8')


class EngineBase:
    """
    解析引擎
    """

    def __init__(self):
        self.parserList = []

    def Start(self):
        pass
