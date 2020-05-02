import mysql.connector
from flask import Flask, render_template, url_for, redirect, request, make_response, jsonify
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
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor()
  start1 = "2018-09-09"
  end1 = "2018-11-25"
  start2 = "2019-01-20"
  end2 = "2019-04-07"
  noclass = ["2018-10-21", "2019-03-03"]
  class_keys = ["class_ID", "activityType", "location", "start_time", "end_time","date","title", "description", "feedback"]
  feedback_keys = ["feedback_ID","feedback_title", "feedback_description"]
  json = []
  for item in classes:
    if (item[6] == 1):
      sunday =  datetime.datetime.strptime(start1, '%Y-%m-%d')
      while(sunday <= datetime.datetime.strptime(end1, '%Y-%m-%d')):
        if sunday not in noclass:
          entry = []
          date = sunday + timedelta(days=item[5])
          entry.append(item[0])
          entry.append(item[1])
          entry.append(item[2])
          entry.append(datetime.datetime.strptime(str(item[3]),'%H:%M:%S').strftime('%H:%M:%S'))
          entry.append(datetime.datetime.strptime(str(item[4]),'%H:%M:%S').strftime('%H:%M:%S'))
          entry.append(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'))
          sort = 1
          for thing in details:
            if datetime.datetime.strptime(str(thing[0]),'%Y-%m-%d').strftime('%Y-%m-%d') == entry[5]:
              entry.append(thing[1])
              entry.append(thing[2])
              cur.execute("SELECT fd.feedback_ID, fd.feedback_name, fd.feedback_description FROM Feedback as f LEFT JOIN Feedback_Details as fd ON (f.feedback_details_ID = fd.feedback_ID) WHERE (f.feedback_ref_ID = %s AND f.feedback_type_ID = 3)",(thing[3],))
              feedbacklist = cur.fetchall()
              feedback = []
              for subfeed in feedbacklist:
                feedback.append(dict(zip(feedback_keys, subfeed)))
              entry.append(feedback)
              sort = 0
          if(sort):
            entry.append("None")
            entry.append("None")
            entry.append("None")
          json.append(dict(zip(class_keys,entry)))
        sunday = sunday + timedelta(days=7)

    elif (item[6] == 2):
      sunday =  datetime.datetime.strptime(start2, '%Y-%m-%d')
      while(sunday <= datetime.datetime.strptime(end2, '%Y-%m-%d')):
        if sunday not in noclass:
          entry = []
          date = sunday + timedelta(days=item[5])
          entry.append(item[0])
          entry.append(item[1])
          entry.append(item[2])
          entry.append(datetime.datetime.strptime(str(item[3]),'%H:%M:%S').strftime('%H:%M:%S'))
          entry.append(datetime.datetime.strptime(str(item[4]),'%H:%M:%S').strftime('%H:%M:%S'))
          entry.append(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'))
          sort = 1
          for thing in details:
            if datetime.datetime.strptime(str(thing[0]),'%Y-%m-%d').strftime('%Y-%m-%d') == entry[5]:
              entry.append(thing[1])
              entry.append(thing[2])
              cur.execute("SELECT fd.feedback_ID, fd.feedback_name, fd.feedback_description FROM Feedback as f LEFT JOIN Feedback_Details as fd ON (f.feedback_details_ID = fd.feedback_ID) WHERE (f.feedback_ref_ID = %s AND f.feedback_type_ID = 3)",(thing[3],))
              feedbacklist = cur.fetchall()
              feedback = []
              for subfeed in feedbacklist:
                feedback.append(dict(zip(feedback_keys, subfeed)))
              entry.append(feedback)
              sort = 0
          if(sort):
            entry.append("None")
            entry.append("None")
            entry.append("None")
          json.append(dict(zip(class_keys,entry)))
        sunday = sunday + timedelta(days=7)
  return json


def modulePopulator(moduleIDs, studentID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor()
  activity_keys = ["activity_ID", "activityType", "title", "start_date", "due_date", "grade_percentage", "grading_description", "description", "estimated_time", "time_spent","lecture","class_time_spent","submitted", "feedback"]
  module_keys = ["module_ID", "module_code" , "module_name", "module_lecturer", "module_lecturer_ID","courses", "activities", "classes", "feedback"]
  course_keys = ["course_ID", "course_name", "coordinator_name","coordinator_email"]
  total_json = []

  for item in moduleIDs:
    module=[]
    activities=[]
    classes=[]
    courses=[]
    feedback=[]
    cur.execute("SELECT m.module_ID, m.module_code, m.module_name, s.staff_name, s.staff_ID FROM Modules as m LEFT JOIN Staff as s ON (s.staff_ID = m.staff_ID) WHERE m.module_ID = %s", (str(item[0]),))
    detailslist = cur.fetchall()
    module.append(detailslist[0][0])
    module.append(detailslist[0][1])
    module.append(detailslist[0][2])
    module.append(detailslist[0][3])
    module.append(detailslist[0][4])
    cur.execute("SELECT mc.course_ID, c.course_name, s.staff_name, s.staff_email FROM Module_Course as mc LEFT JOIN Courses AS c ON (mc.course_ID = c.course_ID) LEFT JOIN Staff as s ON (s.staff_ID = c.staff_ID) WHERE mc.module_ID = %s",(str(detailslist[0][0]),))
    courselist = cur.fetchall()
    for k in courselist:
      courses.append(dict(zip(course_keys, k)))
    module.append(courses)

    if(studentID):
      cur.execute("SELECT a.activity_ID, at.activity_type, a.activity_name, a.start_date, a.end_date, a.module_value, a.grading, a.activity_description, a.hours, u.hours, cd.class_name, a.student_hours, u.submitted FROM Activities AS a LEFT JOIN Class_Details as cd ON (a.lecture_ID = cd.class_ID) LEFT JOIN Activity_Type as at ON (at.activity_type_ID = a.activity_type_ID) LEFT JOIN Student_Progress as u ON (u.student_ID = %s AND u.activity_ID = a.activity_ID) WHERE a.module_ID = %s", (studentID,str(item[0])))
    else: cur.execute ("SELECT a.activity_ID, at.activity_type, a.activity_name, a.start_date, a.end_date, a.module_value, a.grading, a.activity_description, a.hours, a.hours, cd.class_name, a.student_hours FROM Activities AS a LEFT JOIN Class_Details as cd ON (a.lecture_ID = cd.class_ID) LEFT JOIN Activity_Type as at ON (at.activity_type_ID = a.activity_type_ID) WHERE a.module_ID = %s", (str(item[0]),))
    activitylist = cur.fetchall()

    for activity in activitylist:
      feedback_keys = ["feedback_ID","feedback_title", "feedback_description"]
      cur.execute("SELECT fd.feedback_ID, fd.feedback_name, fd.feedback_description FROM Feedback as f LEFT JOIN Feedback_Details as fd ON (f.feedback_details_ID = fd.feedback_ID) WHERE (f.feedback_ref_ID = %s AND f.feedback_type_ID = 2)",(activity[0],))
      feedbacklist = cur.fetchall()
      feedback = []
      actent = []
      for subact in activity:
        actent.append(subact)
      if(studentID == 0):
        cur.execute("SELECT SUM(submitted) submitted FROM Student_Progress WHERE activity_ID = %s",(str(activity[0]),))
        sub = cur.fetchall()
        if sub[0][0] is None: actent.append(0)
        else: actent.append(int(sub[0][0]))
 
      for subfeed in feedbacklist:
        feedback.append(dict(zip(feedback_keys, subfeed)))
      actent.append(feedback)
      activities.append(dict(zip(activity_keys, actent)))
    module.append(activities)
    cur.execute("SELECT c.class_ID, at.activity_type, c.class_location, c.start_time, c.end_time, c.class_day, c.class_semester FROM Classes AS c LEFT JOIN Days as d ON (c.class_day = d.day_ID) LEFT JOIN Activity_Type as at ON (at.activity_type_ID = c.activity_type_ID) WHERE c.module_ID = %s", (str(item[0]),))
    classlist = cur.fetchall()
    cur.execute("SELECT class_date, class_name, class_description, class_ID from Class_Details WHERE module_ID = %s", (str(item[0]),))
    classdetails = cur.fetchall()
    classes = parseClasses(classlist, classdetails)
    module.append(classes)

    feedback_keys = ["name", "description"]
    cur.execute("SELECT fd.feedback_name, fd.feedback_description FROM Feedback as f LEFT JOIN Feedback_Details as fd ON (f.feedback_details_ID = fd.feedback_ID) WHERE (f.feedback_ref_ID = %s AND f.feedback_type_ID = 1)",(str(detailslist[0][0]),))
    feedbacklist = cur.fetchall()
    for j in feedbacklist:
      feedback.append(dict(zip(feedback_keys, j)))

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


@app.route("/updateStudentProgress", methods=['POST'])
def updateStudentProgress():
  req = request.get_json()
  res = make_response(jsonify({"message": "OK"}), 200)
  activityID = str(req['activityID'])
  studentID =  str(req['studentID'])
  hours = int(req['hours'])

  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor(buffered=True)

  cur.execute("SELECT hours FROM Student_Progress WHERE activity_ID = %s AND student_ID = %s",(activityID,studentID))
  if(cur.rowcount == 0):
    cur.execute("INSERT INTO Student_Progress (student_ID, activity_ID, hours, submitted) VALUES (%s,%s,%s,%s)",(studentID, activityID, hours,0))
    mydb.commit()

  elif(cur.rowcount > 0):
    response = cur.fetchall()
    hours = hours + response[0][0]
    cur.execute("UPDATE Student_Progress SET hours = %s WHERE activity_ID = %s AND student_ID = %s",(str(hours),activityID,studentID))
    mydb.commit()

  cur.execute("SELECT hours FROM Student_Progress WHERE activity_ID = %s",(activityID,))
  hours = cur.fetchall()
  total = 0
  submitted = cur.rowcount
  for item in hours:
    total = total + item[0]
  avg = total / submitted
  print(avg, submitted)
  cur.execute("UPDATE Activities SET student_hours = %s WHERE activity_ID = %s",(str(avg),activityID,))
  mydb.commit()

  return res

if __name__ == '__main__':
    app.run(debug=True)
