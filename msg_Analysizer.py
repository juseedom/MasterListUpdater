import os
from datetime import datetime


class Msg():
    """Msg is a class including information about 
    No., Time, Type, and Call ID"""
    def __init__(self, Msg_No, Msg_Time, Msg_Type, Msg_CallID):
        self.m_no = Msg_No
        self.m_time = Msg_Time
        self.m_type = Msg_Type
        self.m_callid = Msg_CallID
        self.m_tag = None
    def __len__(self):
        self.__len__ = 1
    def dsp(self):
        print '[No.] %d\n[Time] %s\n[Message Type] %s\n[Call ID] %d \n'\
              %(self.m_no, self.m_time, self.m_type, self.m_callid)
    def read(self,content):
        self.m_content = content
        
def read_lines(lines,msg):
    content = ''
    no = 0
    for line in lines:
        if line[:4] == '='*4:
            if(len(content)):
                tmp_msg=Msg(no,mtime,mtype,callid)
                tmp_msg.read(content)
                msg.append(tmp_msg)
                content = ''
            continue
        elif line[:4] == '[No.':
            no = int(line[6:])
            continue
        elif line[:6] == '[Time]':
            str_time = str(line[7:])
            str_time = str_time.replace('\n','')
            if (str_time.find('/')!=-1):
                mtime = datetime.strptime(str_time,"%d/%m/%Y %H:%M:%S")
            else:
                mtime = datetime.strptime(str_time,"%Y-%m-%d %H:%M:%S")
            continue
        elif line[:10] == '[Message T':
            mtype = str(line[15:])
            mtype = mtype.replace('\n','')
            continue
        elif line[:4] == '[Cal':
            callid = long(line[10:])
            continue
        elif line[:1]!= '[':
            content = content+line
            continue

    
def read_msg(filepath = None,msg = []):
    #try:
    f = open(filepath,'r')
    lines = f.readlines()
    read_lines(lines,msg)
    #except Exception:
     #   print u'Read File Failed...'
    #finally:
     #   if f.closed == False:
      #     f.close()
      
def process_msg(msg = None):
    if msg.m_type == 'RRC_MOBIL_FROM_EUTRA_CMD':
        i = 0
        i = msg.m_content.find('cs-FallbackIndicator ---')
        if i != -1:
            msg.m_tag = msg.m_content[i:i+32]
            return True
    elif msg.m_type == 'RRC_CONN_REL':
        i = 0
        i = msg.m_content.find('redirectedCarrierInfo')
        if i != -1:
            msg.m_tag = msg.m_content[i:]
            return True
    elif msg.m_type == 'S1AP_UE_CONTEXT_MOD_REQ' or msg.m_type == 'S1AP_INITIAL_CONTEXT_SETUP_REQ':
        i = 0
        i = msg.m_content.find('cSFallbackIndicator')
        if i != -1:
            return True
    elif msg.m_type == 'S1AP_HANDOVER_REQUIRED':
        i = 0
        i = msg.m_content.find('cs-fallback-triggered')
        if i!=-1:
            msg.m_tag = 'csfb attempt'
            return True
    else:
        return False



        
        
dirpath = 'D:\\RNP&RNO\\ENGINEER\\OSS\\PRS\\TopN\\Week47\\CSFB_IRAT\\131830\\txt\\'
files = os.listdir(dirpath)
for f in files:
        if f[-3:] == 'txt':
            msgs = []
            read_msg(dirpath+f,msgs)
            '''for i in range(len(msgs)):
                if process_msg(msgs[i]):
                    print 'find one process'
                    if msgs[i].m_time.second>10:
                        t = datetime(msgs[i].m_time.year,msgs[i].m_time.month,msgs[i].m_time.day,\
                                     msgs[i].m_time.hour,msgs[i].m_time.minute,msgs[i].m_time.second -10)
                    else:
                        t = datetime(msgs[i].m_time.year,msgs[i].m_time.month,msgs[i].m_time.day,\
                                     msgs[i].m_time.hour,msgs[i].m_time.minute-1,msgs[i].m_time.second +50)
                    for j in range(i,-1,-1):
                        if msgs[j].m_time > t:
                            if msgs[j].m_callid == msgs[i].m_callid:
                                msgs[j].dsp()'''
            print f
            irat_ho_att = 0
            irat_ho_exe = 0
            csfb_ho_att = 0
            csfb_ho_exe = 0
            csfb = 0
            irat_redir = 0
            for msg in msgs:
                if process_msg(msg):
                    if msg.m_type == 'S1AP_HANDOVER_REQUIRED':
                        if msg.m_tag != None:
                            csfb_ho_att = csfb_ho_att + 1
                        irat_ho_att = irat_ho_att + 1
                    if msg.m_type == 'RRC_MOBIL_FROM_EUTRA_CMD':
                        if msg.m_tag != None:
                            csfb_ho_exe = csfb_ho_exe + 1
                        irat_ho_exe = irat_ho_exe + 1
                    elif msg.m_type == 'RRC_CONN_REL':
                        irat_redir = irat_redir + 1
                    else:
                        csfb = csfb + 1
            print 'Totally %d CSFB,\n%d IRAT HO Attempt (%d due to CSFB)\n%d IRAT HO Execute (%d due to CSFB)\
            \n%d IRAT Redirection' %(csfb,irat_ho_att,csfb_ho_att,irat_ho_exe,csfb_ho_exe,irat_redir)
