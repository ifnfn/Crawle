#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import traceback
import redis
import threading
import tornado.escape
from .singleton import Singleton

global Debug
Debug = True

MAX_TRY = 3


class EngineCommands(Singleton):
    """
    命令管理器
    """

    mutex = threading.Lock()

    def __init__(self):
        self.db = redis.Redis(host='127.0.0.1', port=6379, db=0)
        self.db.flushall()
        self.pipe = self.db.pipeline()
        self.commandList = []

    def AddCommand(self, cmd):
        if 'source' in cmd or 'text' in cmd:
            EngineCommands.mutex.acquire()
            # self.commandList.append(cmd)

            self.pipe.rpush('command', tornado.escape.json_encode(cmd))
            self.pipe.execute()
            EngineCommands.mutex.release()

    def GetCommand(self):
        ret = {}
        EngineCommands.mutex.acquire()
        # cmd = self.commandList.pop()
        cmd = self.db.lpop('command')
        if cmd:
            try:
                ret = tornado.escape.json_decode(cmd)
            except:
                print(cmd)

        EngineCommands.mutex.release()

        return ret


commands = EngineCommands()


class KolaParser:
    """
    网页解析器
    """

    def __init__(self):
        self.cmd = {}
        self.name = self.__class__.__module__ + '.' + self.__class__.__name__
        self.cmd['engine'] = self.name
        self.cmd['cache'] = True

    def AddCommand(self):
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


class EngineBase:
    """
    解析引擎
    """

    def __init__(self):
        self.parserList = []

    def Start(self):
        pass
