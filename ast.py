#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""

"""
import copy


class Expr(object):
    pass


class Literal(Expr):
    def __init__(self, val):
        self.val = val

    def eval(self, ctx):
        return self.val


class Filter(object):
    def __init__(self, name, args=None):
        self.name = name
        self.args = args if args else []

    def apply(self, val):
        if self.name == "lengeth":
            return len(val)
        elif self.name == "upper":
            return val.upper()
        else:
            return ""


class Var(Expr):
    def __init__(self, name):
        self.name = name

    def eval(self, ctx):
        val = ctx.get(self.name, "")
        return val


class Attr(Expr):
    def __init__(self, name, attr):
        self.name = name
        self.attr = attr

    def eval(self, ctx):
        val = ctx.get(self.name, None)
        if isinstance(val, list):
            return val[int(self.attr)]
        elif isinstance(val, dict):
            return val.get(self.attr, "")
        else:
            try:
                attr_val = getattr(val, self.attr)
                if callable(attr_val):
                    attr_val = attr_val()
                return attr_val
            except:
                return ""


class DoubleBracesExp(Expr):
    def __init__(self, exp, filters=None):
        self.exp = exp
        self.filters = filters if filters else []

    def eval(self, ctx):
        val = self.exp.eval(ctx)
        for ft in self.filters:
            val = ft.apply(val)
        return val


class IfExp(Expr):
    def __init__(self, cond, conseq, alt=None):
        self.cond = cond
        self.conseq = conseq
        self.alt = alt if alt else []

    def eval(self, ctx):
        cond = self.cond.eval(ctx)
        ret = ""
        if cond:
            for exp in self.conseq:
                ret += exp.eval(ctx)
        else:
            for exp in self.alt:
                ret += exp.eval(ctx)
        return ret


class InExp(Expr):
    def __init__(self, var, exp):
        self.var = var
        self.exp = exp


class ForExp(Expr):
    def __init__(self, exp, body):
        self.test_exp = exp
        self.body = body

    def eval(self, ctx):
        val_list = self.test_exp.exp.eval(ctx)
        new_ctx = copy.deepcopy(ctx)
        ret = ""
        for val in val_list:
            new_ctx[self.test_exp.var] = val
            ret += self.body.eval(new_ctx)
        return ret

