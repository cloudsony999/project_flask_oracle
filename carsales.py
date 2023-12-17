from flask import Flask, render_template, request, redirect
import cx_Oracle
carsales = Flask(__name__)
def connection():
    h = 'localhost' #Your host name/ip
    p = '1521' #Your port number 
    sid = 'xe' #Your sid
    u = 'scott' #Your login user name 
    pw = 'tiger' #Your login password
    d = cx_Oracle.makedsn(h, p, sid=sid)
    conn = cx_Oracle.connect(user=u, password=pw, dsn=d) 
    return conn
@carsales.route("/")
def main():
 cars = []
 conn = connection()
 cursor = conn.cursor()
 cursor.execute("SELECT * FROM TblCars")
 for row in cursor.fetchall():
    cars.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
 conn.close()
 return render_template("carslist.html", cars = cars)

@carsales.route("/addcar", methods = ['GET','POST'])
def addcar():
 #IT WILL ADD A NEW CAR IN OUR CRUD PROJECT
 if request.method == 'GET':
    return render_template("addcar.html", car = {})
 if request.method == 'POST':
    id = int(request.form["id"])
    name = request.form["name"]
    year = int(request.form["year"])
    price = float(request.form["price"])
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO TblCars VALUES (:id, :name, :year, :price)", [id, name, year, price])
    conn.commit()
 conn.close()
 return redirect('/')


@carsales.route('/updatecar/<int:id>',methods = ['GET','POST'])
def updatecar(id):
 #IT WILL UPDATE A NEW CAR IN OUR CRUD PROJECT
 cr = []
 conn = connection()
 cursor = conn.cursor()
 if request.method == 'GET':
    cursor.execute("SELECT * FROM TblCars WHERE id = :id", [id])
    row = cursor.fetchone()
    cr.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
    conn.close()
    return render_template("addcar.html", car = cr[0])
 if request.method == 'POST':
    name = str(request.form["name"])
    year = int(request.form["year"])
    price = float(request.form["price"])
    cursor.execute("UPDATE TblCars SET name = :id, year =:year, price = :price WHERE id = :id", [name,
    year, price, id])
    conn.commit()
    conn.close()
 return redirect('/')

@carsales.route('/deletecar/<int:id>')
def deletecar(id):
 conn = connection()
 cursor = conn.cursor()
 cursor.execute("DELETE FROM TblCars WHERE id = :crid", [id])
 conn.commit()
 conn.close()
 return redirect('/')

if(__name__ == "__main__"):
 carsales.run(debug=True)
