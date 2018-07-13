#coding=utf-8
from flask import redirect,url_for,session
class login_required(object):
    def __init__(self,func):
        self.func = func
    def __get__(self,obj,typ=None):
        #print( self.func,obj,typ )
        def wrapper(*args,**kws):
            if 'username' in session:
                return self.func(obj,*args,**kws)
            else:
                return redirect(url_for('login'))
        return wrapper
__all__ = ["login_required"]
