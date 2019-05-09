from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, template_folder="templates", static_folder="templates")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        sub = request.form.get("subject", None)
        name = request.form.get("Notes", None)
        cost = request.form.get("Cost", None)
        if sub == "top-up" and len(cost)>0:
            if "." in cost:
                temp=cost.split(".")
                if len(temp)>2:
                    return render_template("index.html", status="err", namein=name, costin=cost)
                elif len(temp[1])>2:
                    return render_template("index.html", status="err", namein=name, costin=cost)
                else:
                    cost=float(cost)
                    if cost>=100:
                        return render_template("impossible.html", cost=cost)
                    else:
                        conn = sqlite3.connect("money.db")
                        cursor = conn.cursor()
                        cursor.execute("select * from numpep_moneyleft")
                        moneynow = list(cursor.fetchall()[1])
                        moneynow = [round(x+cost, 2) for x in moneynow]
                        cursor.execute("update numpep_moneyleft set pcme=?,pcpme1=?,pcpme2=?,pcpmh1=?,ccpme1=? where whatThing='monLeft'", tuple(moneynow))
                        conn.commit()
                        conn.close()
                        return render_template("index.html", status="good", namein="", costin="")
            else:
                try:
                    cost=float(cost)
                except ValueError:
                    return render_template("index.html", status="err", namein=name, costin=cost)
                if cost>=100:
                    return render_template("impossible.html", cost=cost)
                conn = sqlite3.connect("money.db")
                cursor = conn.cursor()
                cursor.execute("select * from numpep_moneyleft")
                moneynow = list(cursor.fetchall()[1])
                moneynow.pop(0)
                moneynow = [round(x+cost, 2) for x in moneynow]
                cursor.execute("update numpep_moneyleft set pcme=?,pcpme1=?,pcpme2=?,pcpmh1=?,ccpme1=? where whatThing='monLeft'", tuple(moneynow))
                conn.commit()
                conn.close()
                return render_template("index.html", status="good", namein="", costin="")
        elif not name or not cost:
            return render_template("index.html", status="err", namein=name, costin=cost)
        else:
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
            conn = sqlite3.connect("money.db")
            cursor = conn.cursor()
            pep=0
            if sub=="Math":
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


@app.route("/money", methods=["GET"])
def money():
    combi = request.args.get("combi")
    mon=""
    monf=0.0
    if combi=="pcme" or combi=="pcpme1" or combi=="pcpme2" or combi=="pcpmh1" or combi=="ccpme1":
        conn = sqlite3.connect("money.db")
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
# app.run(host='0.0.0.0', port=80)
