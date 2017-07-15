from flask import Flask,request,render_template,request, session, g, redirect, url_for, abort, \
      flash
from flask_mysqldb import MySQL
import pandas as pd
import copy

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

mysql=MySQL()
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123QWEasdZXC'
app.config['MYSQL_DB'] = 'learn_flask_app'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL(app)

def connect_db():
    """Connects to the specific database."""
    cur = mysql.connection.cursor()
    return cur


@app.route('/')
def show_entries():
    db = connect_db()
    entries = {}
    session['query'] = False
    return render_template('show_entries.html', entries=entries)


@app.route('/query', methods=['POST'])
def query():

    cur = connect_db()


    task={
        'servicecode': request.form.get("service_code",""),
        'package_type': request.form.get('package_type',""),
        'weight': request.form.get("weight",""),
        'zone': request.form.get("zone",""),
        'base_charge': request.form.get('base_charge',""),
        'rate_plan': request.form.get('rateplan',""),
        'effectivedate': request.form.get('effectivedate',"")

    }

    selected_task = {}
    ## find the fields users filled in
    for key in task:
        if task[key]:
            selected_task[key] = task[key]

    format_key_value = []
    for key,value in selected_task.items():
        format_key_value.append(key)
        format_key_value.append(value)

    len_key = len(selected_task)
    sql ='select * from fake_data where {} ={}'+' and {} = {}'*(len_key-1)
    cur.execute(
        sql.format(*format_key_value))
    #print(sql)
    entries = cur.fetchall()
    result = []
    import copy

    for value in entries:
        entriesdict = {}
        entriesdict["service_code"] = value[0]
        entriesdict["package_type"] = value[1]
        entriesdict["weight"] = value[2]
        entriesdict["zone"] = value[3]
        entriesdict["base_charge"] = value[4]
        entriesdict["rate_plan"] = value[5]
        entriesdict["effective_date"] = value[6]
        result.append(copy.deepcopy(entriesdict))

    data=pd.DataFrame(result)

    """
    entriesdict = {"service_code" :[],"package_type" :[],"weight" :[],"base_charge":[]}
    for i,j,k,v in entries:
        entriesdict["service_code"].append(i)
        entriesdict["package_type"].append(j)
        entriesdict["weight"].append(k)
        entriesdict["base_charge"].append(v)
    """
    flash('New query was successfully executed!!')
    session['query'] = True
    return render_template('show_entries.html', tables=[data.to_html(index=False)])



if __name__ == '__main__':
    app.run()




