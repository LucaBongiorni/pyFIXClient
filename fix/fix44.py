#!/usr/bin/python3
''' Simple FIX client'''

from collections import OrderedDict
from datetime import datetime, date


class FIX44(object):    
    PROTOCOL='FIX.4.4'
    SOH = '\x01'
    DATE_SHORT_FORMAT= '%Y%m%d'
    DATE_LONG_FORMAT= '%Y%m%d-%H:%M:%S'
    HEADER_NECESSERY_TAGS = [ 8, 35, 49, 56, 34, 52 ]
    LOGGER=None
    
    
    def __init__ (self):
        self.seqNum=0

    def init (self, SenderCompId,  TargetCompId):
        self.seqNum=0
        if (TargetCompId is None) or (TargetCompId is None):
            raise Exception
        else:
            self.SenderCompId = SenderCompId
            self.TargetCompId = TargetCompId

    def get_next_seqNum(self):
        self.seqNum+=1
        return self.seqNum

    def set_seqNum(self,  num):
        self.seqNum = num
        return self.seqNum

    def get_header(self):        
        self.header = OrderedDict([('8',  FIX44.PROTOCOL), ('35', None), ('49',  self.SenderCompId),  ('56',  self.TargetCompId),  
                                   ('34',  FIX44.get_next_seqNum(self)),  ('52',  FIX44.date_long_encode(self,  datetime.now())) ])        
        return  self.header
    
    def get_trailer(self,  msg ):
        '''assume msg is str'''    
        tag35_pos = msg.index('35=')
        tag9 = str(len(msg[tag35_pos:]))
        msg = msg[:tag35_pos]+'9='+tag9+FIX44.SOH+msg[tag35_pos:]
        tag10 = str( sum(ord(c) for c in msg) & 255 )
        if len(tag10) > 3:
          tag10 = tag10[:2]
        else:
          while len(tag10)<3:
            tag10 = '0'+tag10
        msg+='10='+tag10+FIX44.SOH
        return msg
    
    def get_groupe(self, grp_tag,  grp_tag_val,  grp_container):
        '''assume grp_container is set of dicts [(key, val),]'''
        #print("get_groupe start")
        container=''
        for it in grp_container:            
            key,  val  = it
            container+=str(key+'='+str(val))+FIX44.SOH
        container = container[:-1]
        self.res =OrderedDict ([(grp_tag,  str(grp_tag_val)+FIX44.SOH+container)])
        return self.res
    
    def generate_message(self,  body):  
        try:
           self.header = self.get_header()
           self.header.update(body)        
           self.body=''
           for key,  val  in self.header.items():
               self.body+= str(key+'='+str(val))+FIX44.SOH
           self.body = self.get_trailer(self.body)
        except (TypeError,  ValueError) as err:
            print('generate_message Exception: '+ str(err))
            return ''
        return self.body
    
    def get_tag(self,  msg,  tag_num):
        tags = msg.split(FIX44.SOH)
        tags_dict = OrderedDict([])
        for tag_val in tags:            
            item = tag_val.split('=')
            #print(item)
            if (len(item) >1):
                tags_dict.update(OrderedDict([(item[0],  item[1])]))
        return str(tags_dict.get(str(tag_num)))
    
    def generate_Login_35_A (self, hertbeat_interval = 0, password = ' ', rest=None ):
      msg = OrderedDict([('35',  'A'), ('49', self.SenderCompId), ('56' , self.TargetCompId), ('98', 0), ('108',  hertbeat_interval), ('141', 'N'), ('554', password)])
      msg.update(OrderedDict(rest))
      login = self.generate_message ( msg )  
      return login

    def generate_Logout_35_5 (self, rest=None ):
      msg = OrderedDict([('35',  '5'), ('49', self.SenderCompId), ('56' , self.TargetCompId)])
      if rest :
        msg.update(OrderedDict(rest))
      logout = self.generate_message ( msg )  
      return logout
      #logout_msg =fix.generate_message ( OrderedDict([('35',  '5'), ('49', sender), ('56' , target)]) )
    
    def date_short_encode(self, date_short):
        return d.strftime(FIX44.DATE_SHORT_FORMAT)

    def date_short_decode(self, date_short):
        return datetime.strptime(self, date_short, FIX44.DATE_SHORT_FORMAT).date()

    def date_long_encode(self, date_long):
        return date_long.strftime(FIX44.DATE_LONG_FORMAT)

    def date_long_decode(self,  date_long):
        return datetime.strptime(date_long, FIX44.DATE_LONG_FORMAT)
