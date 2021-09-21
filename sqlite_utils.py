import sqlite3
import datetime
import traceback
import os
import sys
from inspect import currentframe, getframeinfo
import random

SCANLOG_DB_FILE = "scanlog.db"
TBL_NAME = "scanlog"
DB_DIR=".db"
SCANLOG_DB = os.path.join(DB_DIR, SCANLOG_DB_FILE)

# https://stackoverflow.com/questions/26286203/custom-print-function-that-wraps-print
def scanlog_print(*args, **kwargs):
   print( "> "+" ".join(map(str,args)) + "", **kwargs)

def scanlog_execute(cmd):
    try:
        con = sqlite3.connect(SCANLOG_DB)
        cur = con.cursor()
        cur.execute(cmd)
        con.commit()
    except sqlite3.Error as er:
        scanlog_print('SQLite error: %s' % (' '.join(er.args)))
        scanlog_print("Exception class is: ", er.__class__)
        scanlog_print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        scanlog_print(traceback.format_exception(exc_type, exc_value, exc_tb))
        frameinfo = getframeinfo(currentframe())
        scanlog_print(frameinfo.filename, frameinfo.lineno)
    con.close()


def scanlog_init_db():
   try:
       scanlog_print(f"Using file {SCANLOG_DB}")
       if not os.path.isfile(SCANLOG_DB):
           os.makedirs(DB_DIR, exist_ok = True)
       con = sqlite3.connect(SCANLOG_DB)
       cur = con.cursor()
       cmd = f'''CREATE TABLE IF NOT EXISTS {TBL_NAME}(id INTEGER PRIMARY KEY AUTOINCREMENT, scanned text, parent text, edate INTEGER, date TEXT, action text, tot_secs INTEGER, UNIQUE(scanned,parent))'''
       cur.execute(cmd)
       cnt = scanlog_get_len_records()
       if cnt == 0:
           scanlog_print("will add dummy records")
           scanlog_insert_sample_records()
       else:
           scanlog_print("dummy records exist")
           return
       con.commit()
   except sqlite3.Error as er:
       scanlog_print('SQLite error: %s' % (' '.join(er.args)))
       scanlog_print("Exception class is: ", er.__class__)
       scanlog_print('SQLite traceback: ')
       exc_type, exc_value, exc_tb = sys.exc_info()
       scanlog_print(traceback.format_exception(exc_type, exc_value, exc_tb))
       frameinfo = getframeinfo(currentframe())
       scanlog_print(frameinfo.filename, frameinfo.lineno)
   con.close()

def scanlog_get_len_records():
   try:
       con = sqlite3.connect(SCANLOG_DB)
       cur = con.cursor()
       cmd = f"SELECT * FROM {TBL_NAME}"
       cur.execute(cmd)
       rows = cur.fetchall()
       cnt = len(rows)
   except sqlite3.Error as er:
       scanlog_print('SQLite error: %s' % (' '.join(er.args)))
       scanlog_print("Exception class is: ", er.__class__)
       scanlog_print('SQLite traceback: ')
       exc_type, exc_value, exc_tb = sys.exc_info()
       scanlog_print(traceback.format_exception(exc_type, exc_value, exc_tb))
   con.close()
   return cnt

def scanlog_show_records():
   scanlog_print("*" * 10, "Showing all records", "*" * 10)
   try:
       con = sqlite3.connect(SCANLOG_DB)
       #import pdb;pdb.set_trace()
       cur = con.cursor()
       cmd = f"SELECT * FROM {TBL_NAME}"
       cur.execute(cmd)
       rows = cur.fetchall()
       cnt = len(rows)
       for r in rows:
           print(r)
       con.commit()# save and close
   except sqlite3.Error as er:
       scanlog_print('SQLite error: %s' % (' '.join(er.args)))
       scanlog_print("Exception class is: ", er.__class__)
       scanlog_print('SQLite traceback: ')
       exc_type, exc_value, exc_tb = sys.exc_info()
       scanlog_print(traceback.format_exception(exc_type, exc_value, exc_tb))
   con.close()
   return cnt

  def scanlog_insert_sample_records():
   try:
       con = sqlite3.connect(SCANLOG_DB)
       #import pdb;pdb.set_trace()
       cur = con.cursor()
       date=str(datetime.datetime.now())
       cur.execute(f"INSERT INTO {TBL_NAME} (id,scanned,parent,edate,date,action,tot_secs) VALUES (NULL,'BUG-336266','BUG-100','1631847191','{date}','only_comment', 180)")
       cur.execute(f"INSERT INTO {TBL_NAME} (id,scanned,parent,edate,date,action,tot_secs) VALUES (NULL,'BUG-336267','BUG-200','1631847192','{date}','only_comment', 181)")
       cur.execute(f"INSERT INTO {TBL_NAME} (id,scanned,parent,edate,date,action,tot_secs) VALUES (NULL,'BUG-336268','BUG-100','1631847193','{date}','only_comment', 182)")
       cur.execute(f"SELECT * FROM {TBL_NAME}")
       rows = cur.fetchall()
       con.commit()# save and close
   except sqlite3.Error as er:
       scanlog_print('SQLite error: %s' % (' '.join(er.args)))
       scanlog_print("Exception class is: ", er.__class__)
       scanlog_print('SQLite traceback: ')
       exc_type, exc_value, exc_tb = sys.exc_info()
       scanlog_print(traceback.format_exception(exc_type, exc_value, exc_tb))
   con.close()

def scanlog_epoch(dt = None):
   if dt is None:
       return int(datetime.datetime.now().strftime('%s'))
   else:
       return int(dt.strftime('%s'))


# http://www.sqlite.org/draft/lang_upsert.html
def scanlog_upsert(dd):
    try:
        con = sqlite3.connect(SCANLOG_DB)
        cur = con.cursor()
        edate   = dd["edate"]
        date    = dd["date"]
        scanned = dd["scanned"]
        parent  = dd["parent"]
        action  = dd["action"]
        tot_secs= dd["tot_secs"]

        cmd = f"SELECT * FROM {TBL_NAME} WHERE scanned='{scanned}' AND parent='{parent}'";
        scanlog_print(cmd)
        cur.execute(cmd)
        rows = cur.fetchall()
        cnt = len(rows)
        print(f"cnt:{cnt}")
        if cnt == 0:
            # should be an insert
            scanlog_print(" should be an insert")
            cur.execute(f"INSERT INTO {TBL_NAME} (id,scanned,parent,edate,date,action,tot_secs) VALUES (NULL,'{scanned}','{parent}','{edate}','{date}','{action}', {tot_secs})")

        else:
            # should be an update
            scanlog_print(" should be an update")
            cmd = f'INSERT INTO {TBL_NAME} SELECT * FROM {TBL_NAME} WHERE scanned="{scanned}" and parent="{parent}" ON CONFLICT(scanned,parent) DO UPDATE SET edate={edate},date="{date}",action="{action}",tot_secs={tot_secs}'
        scanlog_print(cmd)

        cur.execute(cmd)
    except sqlite3.Error as er:
        scanlog_print('SQLite error: %s' % (' '.join(er.args)))
        scanlog_print("Exception class is: ", er.__class__)
        scanlog_print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        scanlog_print(traceback.format_exception(exc_type, exc_value, exc_tb))

    con.commit()


# main
if __name__ == '__main__':
    scanlog_init_db()
    dd = dict()
    #insert_sample_records_to_scanlog_db()
    scanlog_show_records()

    scanlog_print("upsert last record")
    action_ll = ["suggest", "do_fad", "do_reassign", "do_dup", "suggest_reassign"]
    # sample upsert example
    scanned_ticket  = 'BUG-336269'
    parent_ticket   = 'BUG-102'
    action          = action_ll[random.randint(0,len(action_ll) - 1)]
    tot_secs        = random.randint(1,1000)
    dd["scanned"]   = scanned_ticket
    dd["parent"]    = parent_ticket
    dd["edate"]     = scanlog_epoch()
    dd["date"]      = str(datetime.datetime.now())
    dd["action"]    = action
    dd["tot_secs"]  = tot_secs

    scanlog_upsert(dd)
    scanlog_show_records()
