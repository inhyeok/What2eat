#!/usr/bin/python
#-*- coding: utf-8 -*-

from flask import Flask, jsonify, json
import random
import MySQLdb

app = Flask(__name__)

db_sv = 'localhost'
db_user = 'root'
db_pw = ''
db_name = 'what2eat'

conn = MySQLdb.connect(db_sv, db_user, db_pw, db_name, charset='utf8', use_unicode=True)
cursor = conn.cursor()

@app.route('/')
# @on_command(['밥돌리기'])
def print_lunch():
  eat_list = []
  cursor.execute('SELECT eat FROM eat_list WHERE repeated IS NULL')
  if cursor.rowcount == 0:
    return last_set()

  # else:
  for i in range(cursor.rowcount):
    row = cursor.fetchone()
    eat_list.append(row[0])

  ran = random.randint(0,len(eat_list)-1)
  cursor.execute('UPDATE eat_list SET repeated = "Y" WHERE eat = "%s"' % eat_list[ran])
  conn.commit()
  # print eat_list[ran]
  return json.dumps({'lunch':eat_list[ran]}, ensure_ascii=False)
  # return jsonify(lunch=eat_list[ran])

def last_set():
  cursor.execute('UPDATE eat_list SET repeated = NULL WHERE repeated IS NOT NULL')
  conn.commit()
  # print "리스트를 다 돌아 초기화 되었습니다."
  return "리스트를 다 돌아 초기화 되었습니다."

# @on_command(['배고파', '뭐먹어', '밥'])

@app.route('/first_set/')
# @on_command(['what2eat'])
def first_set():
  eat_list = ['중국집', '돈까스', '스파게티', '덮밥', '설렁탕', '치킨파이터', '순대국', '샌드위치', '맥도날드', '파파이스', '파파존스', '쌀국수', '퀴즈노스', '카레', '불고기', '부대찌개']

  cursor.execute('TRUNCATE TABLE eat_list')
  conn.commit()
  for x in xrange(len(eat_list)):
    cursor.execute('INSERT INTO eat_list (eat) VALUES ("%s")' % (eat_list[x]))
    conn.commit()
  return "good"

# first_set()
# print_lunch()
# last_set()

# def main():
#   bot = Bot()
#   bot.run()

if __name__ == "__main__":
  app.run(debug=True)