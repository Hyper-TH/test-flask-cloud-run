from flask import Flask, render_template
from flask import request
from flask_mysqldb import MySQL
from flask_cors import CORS
import json
import os
mysql = MySQL()
app = Flask(__name__, template_folder='template')
CORS(app)

# My SQL Instance configurations
# Change these details to match your instance configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'student'
app.config['MYSQL_HOST'] = '35.246.117.104'
# app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)

# Starting point
@app.route('/')
def home():
    return render_template("index.html")

# Starting point
@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template("index.html")

# Add student
@app.route("/add", methods=['GET', 'POST']) #Add Student
def add():
    if request.method == "POST":
        name = request.form['studentName']
        email = request.form['email']
        cursor = mysql.connection.cursor() #create a connection to the SQL instance
        cursor.execute('''INSERT INTO students (studentName, email) VALUES(%s,%s)''',(name,email)) # execute
        mysql.connection.commit()
        cursor.close()
    
        return render_template("success.html")

# Delete student
@app.route("/delete", methods=['GET', 'POST']) #Delete Student
def delete():
    if request.method == "POST":
        ID = request.form['ID']
        cursor = mysql.connection.cursor() #create a connection to the SQL instance
        cursor.execute('''DELETE FROM students WHERE studentID=%s''', (ID,)) # execute
        mysql.connection.commit()
        cursor.close()

        return render_template("success.html")

# Delete student
@app.route("/update", methods=['GET', 'POST']) #Delete Student
def update():
    if request.method == "POST":
        ID = request.form['ID']
        name = request.form['studentName']
        email = request.form['email']
        cursor = mysql.connection.cursor() # create a connection to the SQL instance
        cursor.execute('''UPDATE students SET studentName=%s, email=%s WHERE studentID=%s''', (name,email,ID)) # execute
        mysql.connection.commit()
        cursor.close()

        return render_template("success.html")


# Change to add form html
@app.route('/addPage', methods=['GET', 'POST'])
def addPage():
    return render_template("add.html")

# Change to delete form html
@app.route('/deletePage', methods=['GET', 'POST'])
def deletePage():
    return render_template("delete.html")

# Change to update form html
@app.route('/updatePage', methods=['GET','POST'])
def updatePage():
    return render_template("update.html")

# Show all students in JSON form
@app.route("/read", methods=['GET', 'POST']) #Default - Show Data
def read(): # Name of the method
    cur = mysql.connection.cursor() #create a connection to the SQL instance
    cur.execute('''SELECT * FROM students''') # execute an SQL statment
    rv = cur.fetchall() #Retreive all rows returend by the SQL statment
    Results=[]
    for row in rv: #Format the Output Results and add to return string
        Result={}       
        Result['Name']=row[0].replace('\n',' ')
        Result['Email']=row[1]
        Result['ID']=row[2]
        Results.append(Result)
    response={'Results':Results, 'count':len(Results)}

    ret=app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )
    
    return ret

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080') # Run the flask app at port 8080
