import mysql.connector
from flask import Flask, render_template, url_for, redirect, request
#import simplejson as json
import json
from json import JSONEncoder
import datetime
from decimal import Decimal
app = Flask(__name__)
TOTAL_WEEKS = 33
courseID = 1

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, datetime.date):
                return obj.isoformat()
            if isinstance(obj, datetime.timedelta):
                return str(obj)

@app.route("/")
@app.route("/login")
def login():
  return render_template("login.html")


@app.route("/studentdata<string:studentID>")
def studentdata(studentID):

  mydb = mysql.connector.connect(
    host="localhost",
    user="cian",
    database="modulerdatabase",
    auth_plugin='mysql_native_password'
  )
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


def makeStackedWeeksJSON(row_values, modules_values):  
  json=[] 
  json_values = []
  datasets_values = []
  datasets = []
  module_hours=[]
  weeks = []
  json_keys = ["labels", "datasets", "startAxis", "endAxis"]
  datasets_keys = ["label", "data" ]

  for x in range(1,TOTAL_WEEKS+1):
    if (x<13):
      string = "Teaching "
      string = string + str(x)
    if (x==13):
      string = "Revision 1"
    if (x==14):
      string = "Exams 1"
    if x>14 and x<20:
      string = "Christmas "
      string = string + str(x-14)
    if x>=20 and x<32:
      string = "Teaching "
      string = string + str(x-7)
    if (x==32):
      string = "Revision 2"
    if (x==33):
      string = "Exams 2"
    weeks.append(string)

  for x in range(0,TOTAL_WEEKS):
    module_hours.append(0)
  current = row_values[0][0]
  startAxis = "Teaching 13"
  endAxis = "Exams 1"
  for result in row_values:
    if current < result[0]:
      if (sum(module_hours[0:14]) > 0):
        startAxis = "Teaching 1"
      if (sum(module_hours[15:len(module_hours)]) > 0):
        endAxis = "Exams 2"
      new_stack = list(module_hours)
      datasets_values.append(name)
      datasets_values.append(",".join(str(x) for x in new_stack))
      datasets.append(dict(zip(datasets_keys, datasets_values)))
      current = result[0]
      datasets_values = []
      for x in range(0,TOTAL_WEEKS):
        module_hours[x] = 0 #refresh sublist
    for item in modules_values:
      if result[0] == item[0]:
        name = item[1]
        break
    start_week = result[1]
    division = result[2] - start_week + 1
    if division != 1:
      weekly_input = round((result[3] / division),1)
    if division == 1:
      weekly_input = result[3]

    if (result[4] == 13 or result[4] == 14):
      while start_week <= result[2]:
        if (start_week != 7 and start_week != 26 and start_week <32 and (start_week > 19 or start_week < 13)):
          module_hours[start_week-1] = module_hours[start_week-1] + weekly_input 
        start_week = start_week + 1
    else:
      while start_week <= result[2]:
        module_hours[start_week-1] = module_hours[start_week-1] + weekly_input 
        start_week = start_week + 1



  if (sum(module_hours[0:13]) > 0):
    startAxis = "Teaching 1"
  if (sum(module_hours[13:len(module_hours)]) > 0):
    endAxis = "Exams 2"
  new_stack = list(module_hours)
  datasets_values.append(name)
  datasets_values.append(",".join(str(x) for x in new_stack))
  datasets.append(dict(zip(datasets_keys, datasets_values)))

  json_values.append(",".join(str(x) for x in weeks))
  json_values.append(datasets)
  json_values.append(startAxis)
  json_values.append(endAxis)
  json.append(dict(zip(json_keys, json_values)))
  return json[0]

def makeStackedModuleJSON(row_values, module_names, activity_names):
  json=[]
  json_values = []
  datasets_values = []
  datasets = []
  module_hours=[]
  modules = []
  json_keys = ["labels", "datasets"]
  datasets_keys = ["label", "data" ]

  for x in module_names:
    module_hours.append(0)
    modules.append(x[2])

  current = row_values[0][0]

  for result in row_values:
    if current < result[0]:
      new_stack = list(module_hours)
      datasets_values.append(activity_name)
      datasets_values.append(",".join(str(x) for x in new_stack))
      datasets.append(dict(zip(datasets_keys, datasets_values)))
      current = result[0]
      datasets_values = []
      for x in range(0,len(module_names)):
        module_hours[x] = 0 #refresh sublist
    for item in activity_names:
      if result[0] == item[0]:
        activity_name = item[1]
        break
    module_hours[result[1]-1] = module_hours[result[1]-1] + result[2] 



  new_stack = list(module_hours)
  datasets_values.append(activity_name)
  datasets_values.append(",".join(str(x) for x in new_stack))
  datasets.append(dict(zip(datasets_keys, datasets_values)))
  json_values.append(",".join(str(x) for x in modules))
  json_values.append(datasets)
  json.append(dict(zip(json_keys, json_values)))
  return json[0]

def parseModuleDetails(module_name, module_staff):
  json = []
  data = []
  json_keys = []
  data.append(module_name[0][0])
  data.append(module_name[0][1])
  data.append(module_staff[0][0])
  data.append(module_staff[0][1])
  data.append(module_name[0][2])
  #json_values.append(",".join(str(x) for x in data))
  json_keys = ["name","credits","staff","email", "code"]
  json.append(dict(zip(json_keys, data)))
  return json[0]

def parseModulesList(module_names):
  json = []
  datanames = []
  dataIDs = []
  datacodes = []
  json_keys = []
  json_values = []
  for item in module_names:
    dataIDs.append(str(item[0]))
    datanames.append(item[1])
    datacodes.append(item[2])
  json_keys = ["module_ID","name", "code"]
  json_values.append(dataIDs)
  json_values.append(datanames)
  json_values.append(datacodes)
  json.append(dict(zip(json_keys, json_values)))
  return json[0]

def makePieBarJSON(module_values, module_names):
  data = []
  datasets_values = []
  datasets = []
  labels = []
  json = []
  json_values = []
  json_keys = ["labels","datasets"]
  datasets_keys = ["data"]
  for result in module_values:
    for item in module_names:
      if result[0] == item[0]:
        name = item[1]
        break
    data.append(result[1])
    labels.append(name)
  new_stack = list(data)
  datasets_values.append(",".join(str(x) for x in new_stack))
  datasets.append(dict(zip(datasets_keys, datasets_values)))

  json_values.append(",".join(str(x) for x in labels))
  json_values.append(datasets)
  json.append(dict(zip(json_keys, json_values)))
  return json[0]




@app.route('/module<string:moduleID>')
def module(moduleID):
  mydb = mysql.connector.connect(
    host="localhost",
    user="cian",
    database="modulerdatabase",
    auth_plugin='mysql_native_password'
  )
  cur = mydb.cursor()

  json_data = []
  cur.execute("SELECT activity_type_ID, name FROM Activity_Type")
  activity_type_names = cur.fetchall()
  cur.execute("SELECT activity_ID, start, end, hours, activity_type_ID FROM Activities WHERE module_ID = %s ORDER BY activity_ID", (moduleID,))
  weekly_activity_values = cur.fetchall()

  cur.execute("SELECT name, credits, module_code FROM Modules WHERE module_ID = %s", (moduleID,))
  module_name = cur.fetchall()
  cur.execute("SELECT name, email FROM Staff WHERE staff_ID in (SELECT staff_ID FROM Modules WHERE module_ID = %s)", (moduleID,))
  module_staff = cur.fetchall()

  cur.execute("SELECT activity_type_ID, SUM(hours) hours FROM Activities WHERE module_ID = %s GROUP BY activity_type_ID", (moduleID,))
  activity_hours = cur.fetchall()
  cur.execute("SELECT activity_type_ID, SUM(module_value) Grade FROM Activities WHERE module_ID = %s  GROUP BY activity_type_ID", (moduleID,)) 
  activity_grades = cur.fetchall()

  cur.execute("SELECT activity_ID, name, hours FROM Activities WHERE module_ID = %s", (moduleID,)) 
  activity_names = cur.fetchall()

  json_data.append(parseModuleDetails(module_name, module_staff))
  json_data.append(makePieBarJSON(activity_hours, activity_type_names))
  json_data.append(makePieBarJSON(activity_grades, activity_type_names))
  json_data.append(parseModulesList(activity_names))
  json_data.append(makeStackedWeeksJSON(weekly_activity_values, activity_names))
  #return json.dumps(json_data)
  return render_template("module.html", moduleDetails = json_data[0], moduleHours = json_data[1], moduleGrade = json_data[2], activityList = json_data[3], activityStacked = json_data[4], moduleID = moduleID)

@app.route('/moduleUpdate', methods=['POST'])
def moduleUpdate():
  activityID = int(request.form['activity'])
  start = str(request.form['start'])
  end = str(request.form['end'])
  hours = int(request.form['hours'])

  mydb = mysql.connector.connect(
    host="localhost",
    user="cian",
   database="modulerdatabase",
    auth_plugin='mysql_native_password'
  )
  weeks = []
  for x in range(1,TOTAL_WEEKS+1):
    if (x<13):
      string = "Teaching "
      string = string + str(x)
    if (x==13):
      string = "Revision 1"
    if (x==14):
      string = "Exams 1"
    if x>14 and x<20:
      string = "Christmas "
      string = string + str(x-14)
    if x>=20 and x<32:
      string = "Teaching "
      string = string + str(x-7)
    if (x==32):
      string = "Revision 2"
    if (x==33):
      string = "Exams 2"
    weeks.append(string)
  for x in range(0, len(weeks)):
    if (start == weeks[x]):
      start = x+1
    if (end == weeks[x]):
      end = x+1
  cur = mydb.cursor()
  cur.execute("UPDATE Activities SET start = %s, end = %s, hours = %s WHERE activity_ID = %s", (start,end,hours,activityID))
  mydb.commit()
  cur.execute("SELECT module_ID FROM Activities WHERE activity_ID = %s", (activityID,))
  moduleID = cur.fetchall()
  moduleID = str(moduleID[0][0])
  return redirect(url_for("module", moduleID = moduleID))


@app.route("/student")
def student():
  mydb = mysql.connector.connect(
    host="localhost",
    user="cian",
    database="modulerdatabase",
    auth_plugin='mysql_native_password'
  )
  cur = mydb.cursor()
  json_data = []

  cur.execute("SELECT module_ID, start, end, hours, activity_type_ID FROM Activities WHERE module_ID in (SELECT module_ID FROM Modules WHERE course_ID = %s) ORDER BY module_ID", (courseID,))
  weekly_module_values = cur.fetchall()

  cur.execute("SELECT activity_type_ID, start, end, hours, activity_type_ID FROM Activities WHERE module_ID in (SELECT module_ID FROM Modules WHERE course_ID = %s) ORDER BY activity_type_ID", (courseID,))
  weekly_activity_values = cur.fetchall()

  cur.execute("SELECT module_ID, SUM(hours) hours FROM Activities WHERE module_ID in (SELECT module_ID FROM Modules WHERE course_ID = %s) GROUP BY module_ID", (courseID,)) 
  module_values = cur.fetchall()

  cur.execute("SELECT activity_type_ID, SUM(hours) hours FROM Activities WHERE module_ID in (SELECT module_ID FROM Modules WHERE course_ID = %s) GROUP BY activity_type_ID", (courseID,)) 
  activity_values = cur.fetchall()

  cur.execute("SELECT module_ID, name, module_code FROM Modules WHERE module_ID in (SELECT module_ID FROM Modules WHERE course_ID = %s) GROUP BY module_ID", (courseID,))
  module_names = cur.fetchall()

  cur.execute("SELECT activity_type_ID, name FROM Activity_Type")
  activity_names = cur.fetchall()

  cur.execute("SELECT activity_type_ID, module_ID, hours, activity_type_ID FROM Activities WHERE module_ID in (SELECT module_ID FROM Modules WHERE course_ID = %s) ORDER BY activity_type_ID", (courseID,))
  module_activity_values = cur.fetchall()

  cur.execute("SELECT name FROM Courses WHERE course_ID = %s", (courseID,))
  course_name = cur.fetchall()
  course_name = str(course_name[0][0])

  json_data.append(makeStackedWeeksJSON(weekly_module_values, module_names))
  json_data.append(makePieBarJSON(module_values, module_names))
  json_data.append(makePieBarJSON(activity_values,activity_names))
  json_data.append(makeStackedWeeksJSON(weekly_activity_values, activity_names))
  json_data.append(parseModulesList(module_names))
  json_data.append(makeStackedModuleJSON(module_activity_values, module_names, activity_names))
  #return json.dumps(json_data[0])
  
  return render_template('student.html', moduleStacked = json_data[0],  modulePie = json_data[1], activityPie = json_data[2], activityStacked = json_data[3], moduleList = json_data[4], totalModuleStack = json_data[5], courseName = course_name)

@app.route("/coordinator")
def coordinator():
  mydb = mysql.connector.connect(
    host="localhost",
    user="cian",
    database="modulerdatabase",
    auth_plugin='mysql_native_password'
  )
  cur = mydb.cursor()
  json_data = []


  cur.execute("SELECT module_ID, start, end, hours, activity_type_ID FROM Activities WHERE module_ID in (SELECT module_ID FROM Modules WHERE course_ID = %s) ORDER BY module_ID", (courseID,))
  weekly_module_values = cur.fetchall()
  cur.execute("SELECT activity_type_ID, start, end, hours, activity_type_ID FROM Activities WHERE module_ID in (SELECT module_ID FROM Modules WHERE course_ID = %s) ORDER BY activity_type_ID", (courseID,))
  weekly_activity_values = cur.fetchall()
  cur.execute("SELECT activity_type_ID, module_ID, hours FROM Activities WHERE module_ID in (SELECT module_ID FROM Modules WHERE course_ID = %s) ORDER BY activity_type_ID", (courseID,))
  module_activity_values = cur.fetchall()

  cur.execute("SELECT module_ID, SUM(hours) hours FROM Activities WHERE module_ID in (SELECT module_ID FROM Modules WHERE course_ID = %s) GROUP BY module_ID", (courseID,)) 
  module_values = cur.fetchall()

  cur.execute("SELECT activity_type_ID, SUM(hours) hours FROM Activities WHERE module_ID in (SELECT module_ID FROM Modules WHERE course_ID = %s) GROUP BY activity_type_ID", (courseID,)) 
  activity_values = cur.fetchall()

  cur.execute("SELECT module_ID, name, module_code FROM Modules WHERE module_ID in (SELECT module_ID FROM Modules WHERE course_ID = %s) GROUP BY module_ID", (courseID,))
  module_names = cur.fetchall()
  cur.execute("SELECT activity_type_ID, name FROM Activity_Type")
  activity_names = cur.fetchall()

  cur.execute("SELECT name FROM Courses WHERE course_ID = %s", (courseID,))
  course_name = cur.fetchall()
  course_name = str(course_name[0][0])

  json_data.append(makeStackedWeeksJSON(weekly_module_values, module_names))
  json_data.append(makePieBarJSON(module_values, module_names))
  json_data.append(makePieBarJSON(activity_values,activity_names))
  json_data.append(makeStackedWeeksJSON(weekly_activity_values, activity_names))
  json_data.append(parseModulesList(module_names))
  json_data.append(makeStackedModuleJSON(module_activity_values, module_names, activity_names))
  #return json.dumps(json_data[5])
  return render_template('coordinator.html', moduleStacked = json_data[0],  modulePie = json_data[1], activityPie = json_data[2], activityStacked = json_data[3], moduleList = json_data[4], totalModuleStack = json_data[5], courseName = course_name)

@app.route("/coordinatorGraphs")
def coordinatorGraphs():
  mydb = mysql.connector.connect(
    host="localhost",
    user="cian",
    database="modulerdatabase",
    auth_plugin='mysql_native_password'
  )
  cur = mydb.cursor()
  json_data = []
  cur.execute("SELECT module_ID, start, end, hours, activity_type_ID FROM Activities WHERE module_ID in (SELECT module_ID FROM Modules WHERE course_ID = %s) ORDER BY module_ID", (courseID,))
  weekly_module_values = cur.fetchall()
  cur.execute("SELECT module_ID, name, module_code FROM Modules WHERE module_ID in (SELECT module_ID FROM Modules WHERE course_ID = %s) GROUP BY module_ID", (courseID,))
  module_names = cur.fetchall()
  json_data.append(makeStackedWeeksJSON(weekly_module_values, module_names))
  return json.dumps(json_data[0])
  

#
#  mydb = mysql.connector.connect(
#    host="mvroso.mysql.pythonanywhere-services.com",
#    user="mvroso",
#    password="1234abcd",
#    database="mvroso$ModulerDatabase",
#    auth_plugin='mysql_native_password'
#  )

if __name__ == '__main__':
    app.run(debug=True)