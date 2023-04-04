from flask import Flask,request
import json
import datetime
app=Flask(__name__)

from database import get_database_connection




@app.route('/result',methods=['GET'])
def result():
    db = get_database_connection()
    mycursor=db.cursor(dictionary=True)
    result=request.args
    date=result.get("Date")
    if date:
        query = f"select * from todolist where Date = '{date}';"
    else:
        
        now = datetime.datetime.now()
        today = now.strftime("%Y-%m-%d")
        query = f"select * from todolist where Date = '{today}';"
    mycursor.execute(query)
    data=mycursor.fetchall()
    return json.dumps(data,default=str)


@app.route('/insert', methods=['POST'])
def insert():
    
    msg = "success"
    try:
        db = get_database_connection()
        mycursor = db.cursor()
        result=request.get_json()
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        sql = "INSERT INTO todolist (Description,Date,completed) VALUES (%s, %s,%s)"
        val = ( result['Description'],date,result['completed'])
        mycursor.execute(sql, val)
        db.commit()
        return msg
    except Exception as msg:
        return str(msg)
    
@app.route("/update/<int:id>/",methods=['PUT'])
def updat(id):
     msg = "success"
     try:
        db = get_database_connection()
        mycursor =db.cursor()
        result=request.get_json()
        
        now=datetime.datetime.now()
        today= now.strftime("%Y-%m-%d %H:%M:%S")
        description = result['Description']
        date = result.get("Date", today)
        sql= "update todolist set Description =%s, Date = %s where id = %s"
        val=(description, date, id)
        mycursor.execute(sql, val)
        db.commit()
        return msg
     except Exception as msg:
        return str(msg)
     

@app.route('/delete/<int:id>/',methods=['DELETE'])
def dell(id):
    
     msg='sucess'
     try:
        db = get_database_connection()
        mycursor =db.cursor()
        sql=f"DELETE FROM todolist WHERE id = '{id}'"
        mycursor.execute(sql)
        db.commit()
        return msg
     
     except Exception as msg:
        return msg
if __name__=='__main__':
    

    app.run(debug=True)