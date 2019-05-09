from flask import Flask, render_template, request    # imports required on Flask side
import sqlite3

app = Flask(__name__, template_folder="templates", static_folder="templates")
# pass the Flask app to variable app
# in this case, there are 3 arguments.

# The first argument __name__ variable passed to the Flask class is a Python predefined variable,
# which is set to the name of the module in which it is used, which is called "__main__" i think.

# The second argument specifies the folder which templates(i.e. .html) are in. The default folder for templates
# is "templates", so in this case this argument template_folder is redundant.

# The third argument specifies the folder which statics(e.g. .css, .js) are in. The default folder for statics
# is "static", but since we passed "templates" into static_folder, Flask will see statics in the folder "templates"
# instead of "static".

# It may be useful to put both static and templates in the same folder or separate them into folder which names
# differ from the default. This is up to the programmer to decide what is best.
#


# handles web address path at / ,example.com or example.com/, with the methods GET and POST
@app.route("/", methods=["GET", "POST"])
def home():  # a method which contains what this path does, required by Flask to declare
	if request.method == 'POST':  # checks if request at this path is GET, which is the method of our form in index.html
		sub = request.form.get("subject", None)  # get value from form which name is "subject", set default to None.
		name = request.form.get("Notes", None)
		cost = request.form.get("Cost", None)
		if sub == "top-up" and len(cost)>0:  # if value of sub is "top-up" i.e. top-up is selected and cost is not empty
			if "." in cost:  # Data check, check for decimal
				temp=cost.split(".")
				if len(temp)>2:  # handle weird cost e.g. 15.50.05->cost.split(".")->cost=["15","50","05"]:len(cost)>2
					return render_template("index.html", status="err", namein=name, costin=cost)  # pass error message
				elif len(temp[1])>2:  # check if decimal point > 2 as money does not have > 2 d.p.
					return render_template("index.html", status="err", namein=name, costin=cost)  # pass user input
				else:  # ok! 97% confidence that input is money format
					cost=float(cost)  # since cost is of type text, convert it to a floating point number i.e. decimal
					if cost>=100:  # sorta easter egg
						return render_template("impossible.html", cost=cost)  # pass the cost in to display on the page.
					else:
						conn = sqlite3.connect("/home/mymoney/save-the-world-2019/money.db")  # connect to the database money.db
						cursor = conn.cursor()  # set up cursor
						cursor.execute("select * from numpep_moneyleft")  # select everything frm table numpep_moneyleft
						moneynow = list(cursor.fetchall()[1])  # puts second row(monLeft) in a list.Note:first row at[0]
						moneynow = [round(x+cost, 2) for x in moneynow]  # add money to all, make 2dp <1>
						cursor.execute("update numpep_moneyleft set pcme=?,pcpme1=?,pcpme2=?,pcpmh1=?,ccpme1=? where whatThing='monLeft'", tuple(moneynow))
                        # ^^^^ updates database. ? is to get value from the tuple at the second argument.
                        # the WHERE specifies which row of table numpep_moneyleft to update for columns pcme, pcpme etc.
                        # <1> why round is required? shouldn't all values be at most 2dp?
                        # <1> yes, they should be. but because computers are not
                        # perfect, 1.2+5.65 becomes 6.8500000000000005, which should be 6.85. As such, we need to round.
                        conn.commit()  # commit changes to database
						conn.close()  # close database
						return render_template("index.html", status="good", namein="", costin="")
                        # display page again, pass status and empty namein and costin, which is to clear input fields
			else:  # if no dot i.e. decimal
				try:
					cost=float(cost)  # try to convert cost to float. actually int fits better but whatever
				except ValueError:  # catch ValueError i.e. cost is not a number, cannot convert to float
					return render_template("index.html", status="err", namein=name, costin=cost)
				if cost>=100:
					return render_template("impossible.html", cost=cost)  # easter egg(?) again, but for whole numbers
				conn = sqlite3.connect("/home/mymoney/save-the-world-2019/money.db")
				cursor = conn.cursor()
				cursor.execute("select * from numpep_moneyleft")
				moneynow = list(cursor.fetchall()[1])
				moneynow.pop(0)
				moneynow = [round(x+cost, 2) for x in moneynow]
				cursor.execute("update numpep_moneyleft set pcme=?,pcpme1=?,pcpme2=?,pcpmh1=?,ccpme1=? where whatThing='monLeft'", tuple(moneynow))
				conn.commit()
				conn.close()
				return render_template("index.html", status="good", namein="", costin="")

		elif not name or not cost:  # if these 2 fields are left blank
			return render_template("index.html", status="err", namein=name, costin=cost)
		else:  # if not top up
			if "." in cost:
				temp=cost.split(".")
				if len(temp)>2:
					return render_template("index.html", status="err", namein=name, costin=cost)
				elif len(temp[1])>2:
					return render_template("index.html", status="err", namein=name, costin=cost)
			try:
				cost=float(cost)
			except ValueError:
				return render_template("index.html", status="err", namein=name, costin=cost)
			conn = sqlite3.connect("/home/mymoney/save-the-world-2019/money.db")
			cursor = conn.cursor()
			pep=0
			if sub=="Math" or sub=="GP":
				pep=25
				cursor.execute("select * from numpep_moneyleft")
				moneynow = list(cursor.fetchall()[1])
				moneynow.pop(0)
				moneynow = [round(x-(cost/pep), 2) for x in moneynow]
				cursor.execute("update numpep_moneyleft set pcme=?,pcpme1=?,pcpme2=?,pcpmh1=?,ccpme1=? where whatThing='monLeft'", tuple(moneynow))
				conn.commit()
				conn.close()
				return render_template("index.html", status="good", namein="", costin="")
			elif sub=="H1 History":
				cursor.execute("select pcpmh1 from numpep_moneyleft")
				pep+=int(cursor.fetchone()[0])
				moneynow = list(cursor.fetchone())
				moneynow = [round(x-(cost/pep), 2) for x in moneynow]
				cursor.execute("update numpep_moneyleft set pcpmh1=? where whatThing='monLeft'", tuple(moneynow))
				conn.commit()
				conn.close()
				return render_template("index.html", status="good", namein="", costin="")
			elif sub=="Physics":
				cursor.execute("select pcme,pcpme1,pcpme2,pcpmh1 from numpep_moneyleft")
				for i in cursor.fetchone():
					pep+=int(i)
				moneynow = list(cursor.fetchone())
				moneynow = [round(x-(cost/pep), 2) for x in moneynow]
				cursor.execute("update numpep_moneyleft set pcme=?,pcpme1=?,pcpme2=?,pcpmh1=? where whatThing='monLeft'", tuple(moneynow))
				conn.commit()
				conn.close()
				return render_template("index.html", status="good", namein="", costin="")
			elif sub=="Chemistry":
				cursor.execute("select pcme,ccpme1 from numpep_moneyleft")
				for i in cursor.fetchone():
					pep+=int(i)
				moneynow = list(cursor.fetchone())
				moneynow = [round(x-(cost/pep), 2) for x in moneynow]
				cursor.execute("update numpep_moneyleft set pcme=?,ccpme1=? where whatThing='monLeft'", tuple(moneynow))
				conn.commit()
				conn.close()
				return render_template("index.html", status="good", namein="", costin="")
			elif sub=="Computing":
				cursor.execute("select pcpme1,pcpme2,pcpmh1,ccpme1 from numpep_moneyleft")
				for i in cursor.fetchone():
					pep+=int(i)
				moneynow = list(cursor.fetchone())
				moneynow = [round(x-(cost/pep), 2) for x in moneynow]
				cursor.execute("update numpep_moneyleft set pcpme1=?,pcpme2=?,pcpmh1=?,ccpme1=? where whatThing='monLeft'", tuple(moneynow))
				conn.commit()
				conn.close()
				return render_template("index.html", status="good", namein="", costin="")
			elif sub=="H1 Econs":
				cursor.execute("select pcpme1,ccpme1 from numpep_moneyleft")
				for i in cursor.fetchone():
					pep+=int(i)
				moneynow = list(cursor.fetchone())
				moneynow = [round(x-(cost/pep), 2) for x in moneynow]
				cursor.execute("update numpep_moneyleft set pcpme1=?,ccpme1=? where whatThing='monLeft'", tuple(moneynow))
				conn.commit()
				conn.close()
				return render_template("index.html", status="good", namein="", costin="")
			elif sub=="H2 Econs":
				cursor.execute("select pcme,pcpme2 from numpep_moneyleft")
				for i in cursor.fetchone():
					pep+=int(i)
				moneynow = list(cursor.fetchone())
				moneynow = [round(x-(cost/pep), 2) for x in moneynow]
				cursor.execute("update numpep_moneyleft set pcme=?,pcpme2=? where whatThing='monLeft'", tuple(moneynow))
				conn.commit()
				conn.close()
				return render_template("index.html", status="good", namein="", costin="")

	else: return render_template("index.html", status="new", namein="", costin="")
    # if not form input, display form with no error or success status, and empty form.

@app.route("/money", methods=["GET"])  # method "GET" is the one at the end of a link
def money():
	combi = request.args.get("combi")  # gets argument "combi" (e.g. www.example.com/sth?combi=stuff gets "stuff")
	mon=""
	monf=0.0
	if combi=="pcme" or combi=="pcpme1" or combi=="pcpme2" or combi=="pcpmh1" or combi=="ccpme1":
		conn = sqlite3.connect("/home/mymoney/save-the-world-2019/money.db")
		cursor = conn.cursor()
		if combi=="pcme":cursor.execute("select pcme from numpep_moneyleft")
		if combi=="pcpme1":cursor.execute("select pcpme1 from numpep_moneyleft")
		if combi=="pcpme2":cursor.execute("select pcpme2 from numpep_moneyleft")
		if combi=="pcpmh1":cursor.execute("select pcpmh1 from numpep_moneyleft")
		if combi=="ccpme1":cursor.execute("select ccpme1 from numpep_moneyleft")
		mon = "{:.2f}".format(float((cursor.fetchall()[1])[0]))
		monf=float(mon)
		conn.close()
	else:
		combi="none"
	return render_template("money.html", combi=combi, money=mon, monl=monf)

if __name__ == "__main__":
	app.run(debug=True)
	#app.run(host='0.0.0.0', port=80)
