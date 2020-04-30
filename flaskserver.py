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
            if isinstance(obj, datetime.datetime):
                return obj.isoformat()
            if isinstance(obj, datetime.timedelta):
                return str(obj)

def round_up(n, decimals=0): 
    multiplier = 10 ** decimals 
    return math.ceil(n * multiplier) / multiplier

def timelineData(values, classes):
  json = []
  for item in values:
    time = item[2] - item[1]
    intTime = int(time.days + 1)
    hours = round_up(item[3]/intTime, 2)
    name = item[0]
    date = item[1]
    while (date <= item[2]):
      entry = []
      entry.append(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%b-%d'))
      entry.append(name)
      entry.append(hours)
      json.append(entry)
      date = date + timedelta(days=1)
  final = parseTimelineClasses(classes, json)
  return final

def parseTimelineClasses(classes, json):
  start1 = "2018-09-09"
  end1 = "2018-11-25"
  start2 = "2019-01-20"
  end2 = "2019-04-07"
  noclass = ["2018-10-21", "2019-03-03"]
  for item in classes:
    time = item[4] - item[3]
    hours = int(time.seconds/3600)
    if (item[2] == 1):
      sunday =  datetime.datetime.strptime(start1, '%Y-%m-%d')
      while(sunday <= datetime.datetime.strptime(end1, '%Y-%m-%d')):
        if sunday not in noclass:
          entry = []
          date = sunday + timedelta(days=item[1])
          entry.append(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%b-%d'))
          entry.append(item[0])
          entry.append(hours)
          json.append(entry)
        sunday = sunday + timedelta(days=7)
    elif (item[2] == 2):
      sunday =  datetime.datetime.strptime(start2, '%Y-%m-%d')
      while(sunday <= datetime.datetime.strptime(end2, '%Y-%m-%d')):
        if sunday not in noclass:
          entry = []
          date = sunday + timedelta(days=item[1])
          entry.append(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%b-%d'))
          entry.append(item[0])
          entry.append(hours)
          json.append(entry)
        sunday = sunday + timedelta(days=7)
  return json
    


@app.route("/")
@app.route("/login")
def login():
  return render_template("test.html")


def parseClasses(classes, details):
  start1 = "2018-09-09"
  end1 = "2018-11-25"
  start2 = "2019-01-20"
  end2 = "2019-04-07"
  noclass = ["2018-10-21", "2019-03-03"]
  class_keys = ["activityType", "location", "start_time", "end_time","date","title", "description"]
  json = []
  for item in classes:
    if (item[5] == 1):
      sunday =  datetime.datetime.strptime(start1, '%Y-%m-%d')
      while(sunday <= datetime.datetime.strptime(end1, '%Y-%m-%d')):
        if sunday not in noclass:
          entry = []
          date = sunday + timedelta(days=item[4])
          entry.append(item[0])
          entry.append(item[1])
          entry.append(item[2])
          entry.append(item[3])
          entry.append(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%b-%d'))
          sort = 1
          for thing in details:
            if datetime.datetime.strptime(str(thing[0]),'%Y-%m-%d').strftime('%Y-%b-%d') == entry[4]:
              entry.append(thing[1])
              entry.append(thing[2])
              sort = 0
          if(sort):
            entry.append("None")
            entry.append("None")
          json.append(dict(zip(class_keys,entry)))
        sunday = sunday + timedelta(days=7)

    elif (item[5] == 2):
      sunday =  datetime.datetime.strptime(start2, '%Y-%m-%d')
      while(sunday <= datetime.datetime.strptime(end2, '%Y-%m-%d')):
        if sunday not in noclass:
          entry = []
          date = sunday + timedelta(days=item[4])
          entry.append(item[0])
          entry.append(item[1])
          entry.append(item[2])
          entry.append(item[3])
          entry.append(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%b-%d'))
          sort = 1
          for thing in details:
            if datetime.datetime.strptime(str(thing[0]),'%Y-%m-%d').strftime('%Y-%b-%d') == entry[4]:
              entry.append(thing[1])
              entry.append(thing[2])
              sort = 0
          if(sort):
            entry.append("None")
            entry.append("None")
          json.append(dict(zip(class_keys,entry)))
        sunday = sunday + timedelta(days=7)
  return json


def modulePopulator(moduleIDs, studentID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor()
  activity_keys = ["activityType", "title", "start_date", "due_date", "grade_percentage", "grading_description", "description", "estimated_time", "time_spent"]
  module_keys = ["module_code" , "module_name", "module_lecturer", "activities", "classes"]
  total_json = []

  for item in moduleIDs:
    module=[]
    activities=[]
    classes=[]
    cur.execute("SELECT m.module_code, m.module_name, s.staff_name FROM Modules as m LEFT JOIN Staff as s ON (s.staff_ID = m.staff_ID) WHERE m.module_ID = %s", (str(item[0]),))
    detailslist = cur.fetchall()
    module.append(detailslist[0][0])
    module.append(detailslist[0][1])
    module.append(detailslist[0][2])

    if(studentID):
      cur.execute("SELECT at.activity_type, a.activity_name, a.start_date, a.end_date, a.module_value, a.grading, a.activity_description, a.hours, u.hours, cd.class_name FROM Activities AS a LEFT JOIN Class_Details as cd ON (a.lecture_ID = cd.class_ID) LEFT JOIN Activity_Type as at ON (at.activity_type_ID = a.activity_type_ID) LEFT JOIN Student_Progress as u ON (u.student_ID = %s AND u.activity_ID = a.activity_ID) WHERE a.module_ID = %s", (studentID,str(item[0])))
    else: cur.execute("SELECT at.activity_type, a.activity_name, a.start_date, a.end_date, a.module_value, a.grading, a.activity_description, a.hours, a.student_hours, cd.class_name FROM Activities AS a LEFT JOIN Class_Details as cd ON (a.lecture_ID = cd.class_ID) LEFT JOIN Activity_Type as at ON (at.activity_type_ID = a.activity_type_ID) WHERE a.module_ID = %s", (str(item[0]),))
    activitylist = cur.fetchall()
    for j in activitylist:
      activities.append(dict(zip(activity_keys, j)))
    module.append(activities)
    cur.execute("SELECT at.activity_type, c.class_location, c.start_time, c.end_time, c.class_day, c.class_semester FROM Classes AS c LEFT JOIN Days as d ON (c.class_day = d.day_ID) LEFT JOIN Activity_Type as at ON (at.activity_type_ID = c.activity_type_ID) WHERE c.module_ID = %s", (str(item[0]),))
    classlist = cur.fetchall()
    cur.execute("SELECT class_date, class_name, class_description from Class_Details WHERE module_ID = %s", (str(item[0]),))
    classdetails = cur.fetchall()
    classes = parseClasses(classlist, classdetails)
    module.append(classes)

    total_json.append(dict(zip(module_keys, module)))
  return total_json

    
@app.route("/modulesByStudent<string:studentID>")
def modulesByStudent(studentID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor()
  json_data = []
  cur.execute("SELECT course_ID FROM Students WHERE student_ID = %s ", (studentID,))
  courseID = cur.fetchall()
  courseID = str(courseID[0][0])
  cur.execute("Select m.module_ID FROM Modules as m LEFT JOIN Module_Course as mc ON (mc.module_ID = m.module_ID) WHERE mc.course_ID = %s", (courseID,))
  module_list = cur.fetchall()
  json_data = modulePopulator(module_list,studentID)

  response = app.response_class(
        response=json.dumps(json_data, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

@app.route("/modulesByStaff<string:staffID>")
def modulesByStaff(staffID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor()
  json_data = []
  cur.execute("Select module_ID FROM Modules WHERE staff_ID = %s", (staffID,))
  module_list = cur.fetchall()
  json_data = modulePopulator(module_list,0)

  response = app.response_class(
        response=json.dumps(json_data, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

@app.route("/moduleByModule<string:moduleID>")
def moduleByModule(moduleID):
  json_data = []
  module_list = []
  module_list.append(moduleID)
  json_data = modulePopulator(module_list,0)
  response = app.response_class(
        response=json.dumps(json_data, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

@app.route("/modulesByCourse<string:courseID>")
def modulesByCourse(courseID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor()
  json_data = []
  cur.execute("Select m.module_ID FROM Modules as m LEFT JOIN Module_Course as mc ON (mc.module_ID = m.module_ID) WHERE mc.course_ID = %s", (courseID,))
  module_list = cur.fetchall()
  json_data = modulePopulator(module_list,0)

  response = app.response_class(
        response=json.dumps(json_data, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

@app.route("/studentsByModule<string:moduleID>")
def studentsByModule(moduleID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor()
  json_data = []
  cur.execute("SELECT c.course_name, s.student_name, s.student_ID, s.student_number FROM Students as s LEFT JOIN Courses as c ON (s.course_ID = c.course_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = %s AND mc.course_ID = s.course_ID)", (moduleID,))
  student_list = cur.fetchall()
  student_keys = ["course_name", "student_name", "student_ID", "student_number"]
  for item in student_list:
    json_data.append(dict(zip(student_keys, item)))

  response = app.response_class(
        response=json.dumps(json_data, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response


@app.route("/timelineByCourse<string:courseID>")
def timelineByCourse(courseID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor()
  json_data = []
  values = []
  classes = []
  cur.execute("SELECT m.module_name, a.start_date, a.end_date, a.hours FROM Activities AS a LEFT JOIN Modules as m ON (m.module_ID = a.module_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = m.module_ID) WHERE mc.course_ID = %s", (courseID,))
  values = cur.fetchall()
  cur.execute("SELECT  m.module_name, c.class_day, c.class_semester, c.start_time, c.end_time FROM Classes AS c LEFT JOIN Modules as m ON (m.module_ID = c.module_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = m.module_ID) WHERE mc.course_ID = %s", (courseID,))
  classes = cur.fetchall()
  json_data.append(timelineData(values, classes))

  values = []
  classes = []
  cur.execute("SELECT at.activity_type, a.start_date, a.end_date, a.hours FROM Activities AS a LEFT JOIN Activity_Type as at ON (at.activity_type_ID = a.activity_type_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = a.module_ID) WHERE mc.course_ID = %s", (courseID,))
  values = cur.fetchall()
  cur.execute("SELECT at.activity_type, c.class_day, c.class_semester, c.start_time, c.end_time FROM Classes AS c LEFT JOIN Activity_Type as at ON (at.activity_type_ID = c.activity_type_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = c.module_ID) WHERE mc.course_ID = %s", (courseID,))
  classes = cur.fetchall()
  json_data.append(timelineData(values, classes))

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

  binning = {
        "month": [1],
        "day": [6]
      }

  json_data.append(schema_data)
  json_data.append(binning)
  response = app.response_class(
        response=json.dumps(json_data, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

if __name__ == '__main__':
    app.run(debug=True)
