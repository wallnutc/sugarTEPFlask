import mysql.connector
from flask import Flask, render_template, url_for, redirect, request
import json
from json import JSONEncoder
import datetime
import math
from datetime import timedelta
from decimal import Decimal
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

connection_config_dict = {'host': 'localhost','user' : 'cian','database' :'modulerdatabase','auth_plugin' :'mysql_native_password'}
#connection_config_dict = {'host': 'mvroso.mysql.pythonanywhere-services.com','user' : 'mvroso','password' : '1234abcd', 'database' :'mvroso$ModulerDatabase','auth_plugin' :'mysql_native_password'}


class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, datetime.date):
                return obj.isoformat()
            if isinstance(obj, datetime.timedelta):
                return str(obj)

def round_up(n, decimals=0): 
    multiplier = 10 ** decimals 
    return math.ceil(n * multiplier) / multiplier

@app.route("/")
@app.route("/login")
def login():
  return render_template("test.html")


@app.route("/studentdata<string:studentID>")
def studentdata(studentID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor()
  json_data = []
  cur.execute("SELECT course_ID FROM Students WHERE student_ID = %s ", (studentID,))
  courseID = cur.fetchall()
  courseID = str(courseID[0][0])
  cur.execute("SELECT at.activity_type, m.module_code, m.module_name, s.staff_name, a.activity_name, a.start_date, a.end_date, a.module_value, a.grading, a.activity_description, a.hours, u.hours FROM Activities AS a LEFT JOIN Modules as m ON (m.module_ID = a.module_ID) LEFT JOIN Activity_Type as at ON (at.activity_type_ID = a.activity_type_ID) LEFT JOIN Staff as s ON (s.staff_ID = m.staff_ID) LEFT JOIN Student_Progress as u ON (u.student_ID = %s AND u.activity_ID = a.activity_ID) WHERE course_ID = %s", (studentID,courseID))
  activity_list = cur.fetchall()
  cur.execute("SELECT  at.activity_type, m.module_code, m.module_name, s.staff_name, c.class_location, c.class_name, c.start_time, c.end_time, d.day, c.class_description FROM Classes AS c LEFT JOIN Modules as m ON (m.module_ID = c.module_ID) LEFT JOIN Days as d ON (c.class_day = d.day_ID) LEFT JOIN Activity_Type as at ON (at.activity_type_ID = c.activity_type_ID) LEFT JOIN Staff as s ON (s.staff_ID = m.staff_ID) WHERE course_ID = %s", (courseID,))
  class_list = cur.fetchall()
  activity_keys = ["activityType", "module_code" , "module_name", "module_lecturer", "title", "start_date", "due_date", "grade_percentage", "grading_description", "description", "estimated_time", "time_spent"]
  class_keys = ["activityType", "module_code" , "module_name", "module_lecturer", "location", "title", "start_time", "end_time","day", "description"]
  data = []
  for item in activity_list:
    data.append(dict(zip(activity_keys, item)))
  json_data.append(data)
  data = []
  for item in class_list:
    data.append(dict(zip(class_keys, item)))
  json_data.append(data) 
  return json.dumps(json_data, indent=4, cls=DateTimeEncoder)


def timelineData(values):
  json = []
  for item in values:
    time = item[2] - item[1]
    intTime = int(time.days + 1)
    hours = round_up(item[3]/intTime, 2)
    name = item[0]
    date = item[1]
    while (date <= item[2]):
      entry = []
      entry.append(datetime.datetime.strptime(str(date),'%Y-%m-%d').strftime('%Y-%b-%d'))
      entry.append(name)
      entry.append(hours)
      json.append(entry)
      date = date + timedelta(days=1)
  return json


@app.route("/timelineModuleGraphs")
def coordinatorGraphs():
  mydb = mysql.connector.connect(**connection_config_dict)
  courseID = 1
  cur = mydb.cursor()
  json_data = []
  cur.execute("SELECT m.module_name, a.start_date, a.end_date, a.hours FROM Activities AS a LEFT JOIN Modules as m ON (m.module_ID = a.module_ID) WHERE course_ID = %s", (courseID,))
  values = cur.fetchall()
  json_data.append(timelineData(values))
  schema_data = [{
      "name": "Date",
      "type": "date",
      "format": "%Y-%b-%d"
    },
    {
      "name": "Module",
      "type": "string"
    },
    {
      "name": "Hours",
      "type": "number"
    }
  ]
  json_data.append(schema_data)
  response = app.response_class(
        response=json.dumps(json_data, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response
  



if __name__ == '__main__':
    app.run(debug=True)