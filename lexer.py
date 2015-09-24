#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""

"""


class Token(object):
    pass


class DoubleLeftBracesToken(Token):
    pass


class DoubleRightBracesToken(Token):
    pass


class ControlBeginToken(Token):
    pass


class ControlEndToken(Token):
    pass


class SepToken(Token):
    pass


class ForToken(Token):
    pass


class IfToken(Token):
    pass


class VarToken(Token):
    def __init__(self, name):
        self.name = name


class LiteralToken(Token):
    def __init__(self, ss):
        self.val = ss
        

class Lexer(object):
    def __init__(self, source):
        self.source = source

        self.in_var = False
        self.in_control = False
        self.cur_idx = 0

    def next_token(self):
        while self.cur_idx < len(self.source):
            if self.in_var is False and self.in_control is False:
                idx1 = self.source.find("{{", self.cur_idx)
                idx2 = self.source.find("{%", self.cur_idx)
                
            if self.source.startswith("{{", self.cur_idx):
                self.cur_idx += 2
                self.in_var = True
                return DoubleLeftBracesToken()
            elif self.source.startswith("}}", self.cur_idx):
                self.cur_idx += 2
                self.in_var = False
                return DoubleRightBracesToken()
            elif self.source.startswith("{%", self.cur_idx):
                self.cur_idx += 2
                self.in_control = True
                return ControlBeginToken()
            elif self.source.startswith("%}", self.cur_idx):
                self.cur_idx += 2
                self.in_control = False
                return ControlEndToken()
