from flask import *
from flask import request,Response,jsonify
import json
from peewee import *
db=SqliteDatabase('wake.db')
db.connect()

class BaseModel(Model):
    class Meta:
        database=db
class Course(BaseModel):
    id = PrimaryKeyField()
    name = CharField()
    type = CharField()
    teacher = CharField()
    avg = CharField()
    credit = CharField()
    college = CharField()
    comments = CharField()
    star = CharField()
    bt90 = CharField()
    bt80 = CharField()
    bt70 = CharField()
    bt60 = CharField()
    bl60 = CharField()
    av23 = CharField()
    av34 = CharField()
    av45 = CharField()
    av56 = CharField()
    av67 = CharField()
    av78 = CharField()
    link = CharField()
    class Meta:
        db_table = 'wake'

application = Flask(__name__)
#########记得把表名改了

@application.route('/')
def hello_world():
    return render_template('search.html')

@application.route('/home')
def home():
    return render_template('search2.html')

@application.route('/m/list/<sec>',methods=['GET','POST'])
def selectp(sec):
    all=sec.split('&')
    return render_template('list.html',ones=search2(all))

@application.route('/list/<sec>',methods=['GET','POST'])
def select(sec):
    all=sec.split('&')
    return search(all)

def search2(dictt):
    name = "SELECT * FROM wake WHERE (name LIKE '%" + dictt[0] + "%' OR teacher LIKE '%" + dictt[0] + "%')"
    order= " ORDER BY avg DESC"
    sql=""+name
    if dictt[1] !="" : sql+=" AND type LIKE '%"+dictt[1]+"%'"
    if dictt[2] !="": sql+=" AND avg BETWEEN "+str(int(dictt[2]))+" and "+str(int(dictt[2])+10)
    if dictt[3] !="": sql+=" AND star = '"+dictt[3]+"'"
    if dictt[4] != "": sql += " AND comments LIKE '%" + dictt[4] + "%'"
    sql+=order
    result=Course.raw(sql)
    datain=[]
    for i in result:
        con={}
        con['name']=i.name
        con['teacher']=i.teacher
        con['credit']=i.credit
        con['avg']=i.avg
        con['id']=i.id
        datain.append(con)
    return datain

def search(dictt):
    name = "SELECT * FROM wake WHERE (name LIKE '%" + dictt[0] + "%' OR teacher LIKE '%" + dictt[0] + "%')"
    order= " ORDER BY avg DESC"
    sql=""+name
    if dictt[1] !="" : sql+=" AND type LIKE '%"+dictt[1]+"%'"
    if dictt[2] !="": sql+=" AND avg BETWEEN "+str(int(dictt[2]))+" and "+str(int(dictt[2])+10)
    if dictt[3] !="": sql+=" AND star = '"+dictt[3]+"'"
    if dictt[4] != "": sql += " AND comments LIKE '%" + dictt[4] + "%'"
    sql+=order
    result=Course.raw(sql)
    datain=[]
    for i in result:
        con={}
        con['name']=i.name
        con['teacher']=i.teacher
        con['credit']=i.credit
        con['avg']=i.avg
        con['id']=i.id
        datain.append(con)
    kelist={"data":datain}
    js = json.dumps(kelist)
    resp = Response(js, status=200, mimetype="application/json")
    return resp

@application.route('/id/<ids>',methods=['GET','POST'])
def getdtl(ids):
    id=int(ids)
    return dtl(id)

@application.route('/m/id/<ids>',methods=['GET','POST'])
def getdtl2(ids):
    id=int(ids)
    return render_template('detail.html',one=dtl2(id))
def none(a):
    if a == "None": return ""
    else: return a
def dtl(a):
    sql="SELECT * FROM wake WHERE id={};".format(a)
    outss=Course.raw(sql)
    outs=outss[0]
    datain={}
    datain['name']=outs.name
    datain['type'] = outs.type
    datain['teacher']=outs.teacher
    datain['avg']=outs.avg
    datain['credit']=outs.credit
    datain['college']=outs.college
    datain['comments'] = eval('"%s"' % outs.comments)
    datain['star']=outs.star
    datain['bt90']=outs.bt90
    datain['bt80']=outs.bt80
    datain['bt70']=outs.bt70
    datain['bt60']=outs.bt60
    datain['bl60']=outs.bl60
    js=json.dumps(datain)
    resp = Response(js, status=200, mimetype="application/json")
    return resp

def dtl2(a):
    sql="SELECT * FROM wake WHERE id={};".format(a)
    outss=Course.raw(sql)
    outs=outss[0]
    datain={}
    datain['name']=outs.name
    datain['type']=none(outs.type)
    datain['teacher']=outs.teacher
    datain['avg']=outs.avg
    datain['credit']=outs.credit
    datain['college']=outs.college
    datain['comments'] = outs.comments.replace("<br>","\n").replace("点评时间","\n\n点评时间")
    datain['star']=outs.star
    datain['bt90']=outs.bt90
    datain['bt80']=outs.bt80
    datain['bt70']=outs.bt70
    datain['bt60']=outs.bt60
    datain['bl60']=outs.bl60
    return datain

@application.route('/type/<type>',methods=['GET','POST'])
def gettype(type):
    typ=type
    return typelist(typ)

@application.route('/m/type/')
def gettype2():
    return render_template('type.html',scis=search2(['','自然科学类','','','']),rws=search2(['','人文社会科学类','','','']),aas=search2(['','A系列','','','']))

def typelist(name):
    sql="SELECT * FROM wake WHERE type LIKE '%"+name+"%' ORDER BY avg DESC"
    outs=Course.raw(sql)
    datain = []
    for i in outs:
        con = {}
        con['name'] = i.name
        con['teacher'] = i.teacher
        con['credit'] = i.credit
        con['avg'] = i.avg
        con['id'] = i.id
        datain.append(con)
    kelist = {"data": datain}
    js = json.dumps(kelist)
    resp = Response(js, status=200, mimetype="application/json")
    return resp

@application.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    application.run(use_reloader=True)
