#!/usr/bin/env python3
'''Log manager class for FIX'''

from threading import Thread, Lock
from datetime import datetime, date
import re
#import threading
#import _thread

class FIX_Log(object):
    FIX_LOG_IN = 'fix_log.in'
    FIX_LOG_OUT = 'fix_log.out'
    
    def __init__(self, silent = False, log_in=None,  log_out=None):
        self.mutex = Lock()
        self.silent = silent
        if (log_in is not None) and (log_out is not None):
            self.FIX_LOG_IN = log_in
            self.FIX_LOG_OUT = log_out
        else:
            self.FIX_LOG_IN = FIX_Log.FIX_LOG_IN
            self.FIX_LOG_OUT = FIX_Log.FIX_LOG_OUT
    
    def log_in_msg(self,  msg):
        self.mutex.acquire()
        #print('log_in_msg: '+msg)
        msgs=[]
        msg = msg.lstrip('\n')
        msg = re.sub(r'8=FIX.4.4', r'\n8=FIX.4.4',msg )
        splitted_msg = msg.split('\n')
        if (not self.silent):
          self.file = open(self.FIX_LOG_IN, encoding='utf-8',  mode='a')
          for msg in splitted_msg:
            if msg is not '':
              try:
                if msg.index('8=FIX') < 0:
                  self.file.write( msg )
                else:
                  self.file.write( '\n'+str(datetime.now()) +': '+msg )
              except ValueError as err:
                self.file.write( msg )
          self.file.close()
        
        self.mutex.release()
        return splitted_msg
    
    def log_out_msg(self,  msg):
        self.mutex.acquire()
        #print('log_out_msg: '+msg)
        if (not self.silent):
          self.file = open(self.FIX_LOG_OUT, encoding='utf-8',  mode='a')
          self.file.write( str(datetime.now()) +': '+msg+'\n' )         
          self.file.close()
        self.mutex.release()
    
    def set_logs(self,  log_in=None,  log_out=None):
        if (log_in is not None) and (log_out is not None):
            self.FIX_LOG_IN = log_in
            self.FIX_LOG_OUT = log_out
