from flask import Flask, render_template, session, request, redirect, url_for, flash
import sqlite3  #

app = Flask(__name__)
app.secret_key = "any random string"

@app.route('/')
def index():
	if 'email' in session:
		name = session['email']
		return "Logged in as+name+<br>+<a href = '/login'></b>" + "click here to logout</b></a>"
		#return 'Logged in as ' + name + '<br>' + "<b><a href = '/logout'>click here to logout</a></b>"
	return "You are not logged in <br><a href = '/login'></b>" + "click here to login</b></a>"

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/submit',methods=["GET","POST"])
def submit():
    if request.method=='POST':
        name=request.form['inputEmail']
        password=request.form['inputPassword']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from students where email=? and password=?",(name,password))
        data=cur.fetchone()

        if data:
            session["name"]=data["email"]
            return redirect("/")
        else:
            flash("Email and Password Mismatch","danger")
    return redirect(url_for("login"))

@app.route('/logout')
def logout():
	session.pop('email', None)
	return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
