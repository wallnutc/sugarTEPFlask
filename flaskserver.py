import mysql.connector
from flask import Flask, render_template, url_for, redirect, request, make_response, jsonify
import simplejson as json
from json import JSONEncoder
import datetime
import math
from datetime import timedelta
from decimal import Decimal
from flask_cors import CORS
from math import atan, tan
#from sqlalchemy import create_engine

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

#connection_config_dict = {'host': 'localhost','user' : 'cian','database' :'modulerdatabase','auth_plugin' :'mysql_native_password'}
connection_config_dict = {'host': 'mvroso.mysql.pythonanywhere-services.com','user' : 'mvroso','password' : '1234abcd', 'database' :'mvroso$ModulerDatabase','auth_plugin' :'mysql_native_password'}
#engine = create_engine('mysql+mysqlconnector://mvroso:1234abcd@mvroso.mysql.pythonanywhere-services.com[:3306]/mvroso$ModulerDatabase', pool_recycle=280)

colours =  [["#A54BDD","#A3B824","#FFB400","#FF3D3D","#00A2B1","#F28F00","#D639BD","#0F86DC","#FF7448","#DD0F83","#00C4D0","#FF4894","#00BF63","#FF6A6A","#C07F32"],
            ["#CDC3CE","#CBCDB0","#CECAA9","#CEBEBA","#B6CDCD","#CEC7AD","#DEC0DC","#BCCCCE","#CEC4B9","#CEBDCC","#B2CECE","#CEBFCD","#B3CEBE","#CEC3C1","#CEC9B8"],
            ["#D291EE","#CEDC4F","#FFD22C","#FF7F74","#4FD1D8","#F9BB37","#EB80DE","#65C3EE","#FFA575","#EE67C1","#44E2E8","#FF85CA","#46DF8E","#FF9E9A","#E0B868"],
            ["#AE59E0","#ACBF2D","#FFBA09","#FF4A48","#10ABB9","#F3980B","#DA47C4","#2092E0","#FF7E51","#E0218F","#0ECAD5","#FF549F","#0EC56C","#FF7474","#C68A3D"],
            ["#250864","#181E04","#4D1200","#630606","#00232C","#510E00","#500644","#02155A","#570C07","#5B021E","#00282F","#5D0712","#002E0A","#570B0B","#400D05"],
            ["#1E055B","#131803","#440D00","#570404","#001D25","#480A00","#450439","#010D52","#4E0805","#4F0111","#002128","#51050B","#002E0A","#4E0808","#3A0904"],
            ["#331070","#2A3108","#612600","#710D0D","#002730","#621E00","#5C0C4E","#032067","#69180F","#660323","#003A42","#6C1020","#004E1E","#6A1717","#4E1B0B"],
            ["#F6C9FC","#F0F871","#FFEA4F","#FFB39F","#8EF6F7","#FEDD62","#FBB9F8","#AAF3FC","#FFCC99","#FCADF3","#7AF9FA","#FFB5F4","#7DF9B0","#FFC7C0","#F9E593"],
            ["#F1E4FA","#F1F4DE","#FFF4D9","#FFE2E2","#D9F1F3","#FDEED9","#F9E1F5","#DBEDFA","#FFEAE4","#FADBEC","#D9F6F8","#FFE4EF","#D9F5E8","#FFE9E9","#F6ECE0"],
            ["#7A35B5","#758519","#C47E00","#CB2B2B","#007885","#BC6400","#A92895","#0B60B1","#C75132","#B20B61","#00909A","#C93269","#008F45","#C74A4A","#955923"],
            ["#42177F","#37400B","#743600","#861212","#003F49","#752B00","#6E115F","#052E77","#7C2316","#780535","#004B53","#81162F","#004E1E","#7C2020","#5D260F"],
            ["#C075E7","#BDCD3E","#FFC61A","#FF6660","#2FBEC8","#F6A921","#E264D1","#43AAE7","#FF9163","#E744A8","#29D6DE","#FF6CB4","#2AD27D","#FF8987","#D3A152"],
            ["#D1C4D3","#CFD2A9","#D4CE9F","#D4BDB7","#B2D1D1","#D4CAA5","#D3BFD2","#BAD0D3","#D4C5B5","#D3BBD0","#ACD2D2","#D4BED1","#ADD2BC","#D4C3C1","#D2CCB3"],
            ["#9744D0","#94A720","#EBA200","#EE3737","#0094A2","#E08100","#C733B0","#0E79CE","#EC6841","#CF0E78","#00B3BE","#ED4186","#00AF59","#EC5F5F","#B2722D"],
            ["#E4ADF5","#DFEA60","#FFDE3E","#FF9989","#6FE3E8","#FBCC4C","#F39CEB","#87DBF5","#FFB987","#F58ADA","#5FEDF1","#FF9DDF","#61EC9F","#FFB2AD","#ECCE7E"],
            ["#5E269A","#566312","#9C5A00","#A91F1F","#005C67","#994800","#8C1D7A","#084794","#A23A24","#95084B","#006E77","#A5244C","#006F32","#A23535","#794019"]]

aColours = [["#A54BDD","#A3B824","#FFB400","#FF3D3D","#00A2B1","#F28F00","#D639BD","#0F86DC","#FF7448","#DD0F83","#00C4D0","#FF4894","#00BF63","#FF6A6A","#C07F32"],
            ["#E4ADF5","#DFEA60","#FFDE3E","#FF9989","#6FE3E8","#FBCC4C","#F39CEB","#87DBF5","#FFB987","#F58ADA","#5FEDF1","#FF9DDF","#61EC9F","#FFB2AD","#ECCE7E"],
            ["#250864","#181E04","#4D1200","#630606","#00232C","#510E00","#500644","#02155A","#570C07","#5B021E","#00282F","#5D0712","#002E0A","#570B0B","#400D05"],
            ["#5E269A","#566312","#9C5A00","#A91F1F","#005C67","#994800","#8C1D7A","#084794","#A23A24","#95084B","#006E77","#A5244C","#006F32","#A23535","#794019"],
            ["#9744D0","#94A720","#EBA200","#EE3737","#0094A2","#E08100","#C733B0","#0E79CE","#EC6841","#CF0E78","#00B3BE","#ED4186","#00AF59","#EC5F5F","#B2722D"],
            ["#7A35B5","#758519","#C47E00","#CB2B2B","#007885","#BC6400","#A92895","#0B60B1","#C75132","#B20B61","#00909A","#C93269","#008F45","#C74A4A","#955923"],
            ["#CDC3CE","#CBCDB0","#CECAA9","#CEBEBA","#B6CDCD","#CEC7AD","#DEC0DC","#BCCCCE","#CEC4B9","#CEBDCC","#B2CECE","#CEBFCD","#B3CEBE","#CEC3C1","#CEC9B8"],
            ["#D1C4D3","#CFD2A9","#D4CE9F","#D4BDB7","#B2D1D1","#D4CAA5","#D3BFD2","#BAD0D3","#D4C5B5","#D3BBD0","#ACD2D2","#D4BED1","#ADD2BC","#D4C3C1","#D2CCB3"],
            ["#C075E7","#BDCD3E","#FFC61A","#FF6660","#2FBEC8","#F6A921","#E264D1","#43AAE7","#FF9163","#E744A8","#29D6DE","#FF6CB4","#2AD27D","#FF8987","#D3A152"],
            ["#331070","#2A3108","#612600","#710D0D","#002730","#621E00","#5C0C4E","#032067","#69180F","#660323","#003A42","#6C1020","#004E1E","#6A1717","#4E1B0B"],
            ["#AE59E0","#ACBF2D","#FFBA09","#FF4A48","#10ABB9","#F3980B","#DA47C4","#2092E0","#FF7E51","#E0218F","#0ECAD5","#FF549F","#0EC56C","#FF7474","#C68A3D"],
            ["#42177F","#37400B","#743600","#861212","#003F49","#752B00","#6E115F","#052E77","#7C2316","#780535","#004B53","#81162F","#004E1E","#7C2020","#5D260F"],
            ["#D291EE","#CEDC4F","#FFD22C","#FF7F74","#4FD1D8","#F9BB37","#EB80DE","#65C3EE","#FFA575","#EE67C1","#44E2E8","#FF85CA","#46DF8E","#FF9E9A","#E0B868"]]


class DateTimeEncoder(json.JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.isoformat()
            if isinstance(obj, datetime.timedelta) or isinstance(obj, Decimal):
                return str(obj)
            return super(DateTimeEncoder, self).default(obj)

##################################################### FUNCTIONS ##################################################
def round_up(n, decimals=1):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def triangleHours(totalhours, start, end, name, json_data):
  time = end - start
  days = int(time.days + 1)
  endHours = (2*totalhours)/days
  angle = atan(endHours/days)
  i = 0
  date = start
  while (i<days):
    hours = (i+1)*tan(angle)
    entry = []
    entry.append(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%b-%d'))
    entry.append(name)
    entry.append(round_up(hours))
    json_data.append(entry)
    date = date + timedelta(days=1)
    i = i + 1
  return json_data

def linearHours(totalhours, start, end, name, json_data):
  time = end - start
  days = int(time.days + 1)
  hours = round_up(totalhours/days, 2)
  date = start
  while (date <= end):
    entry = []
    entry.append(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%b-%d'))
    entry.append(name)
    entry.append(hours)
    json_data.append(entry)
    date = date + timedelta(days=1)
  return json_data

def timelineData(values, classes):
  json = []
  for item in values:
    if (int(item[5]) == 1):
      json = linearHours(item[3], item[1], item[2],item[0],json)
    else:
      json = triangleHours(item[3], item[1], item[2],item[0],json)
  final = parseTimelineClasses(classes, json)
  return final

def timelineStudentData(name, values, classes):
  json = []
  for item in values:
    if (item[2] == None):
      hours = 0
    elif (int(item[3]) == 1):
      json = linearHours(item[2], item[0], item[1],name,json)
    else:
      json = triangleHours(item[2], item[0], item[1], name,json)
  final = parseTimelineStudentClasses(name, classes, json)
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

def parseTimelineStudentClasses(name, classes, json):
  start1 = "2018-09-09"
  end1 = "2018-11-25"
  start2 = "2019-01-20"
  end2 = "2019-03-14"
  noclass = ["2018-10-21", "2019-03-03"]
  for item in classes:
    time = item[3] - item[2]
    hours = int(time.seconds/3600)
    if (item[1] == 1):
      sunday =  datetime.datetime.strptime(start1, '%Y-%m-%d')
      while(sunday <= datetime.datetime.strptime(end1, '%Y-%m-%d')):
        if sunday not in noclass:
          entry = []
          date = sunday + timedelta(days=item[0])
          entry.append(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%b-%d'))
          entry.append(name)
          entry.append(hours)
          json.append(entry)
        sunday = sunday + timedelta(days=7)
    elif (item[1] == 2):
      sunday =  datetime.datetime.strptime(start2, '%Y-%m-%d')
      while(sunday <= datetime.datetime.strptime(end2, '%Y-%m-%d')):
        if sunday not in noclass:
          entry = []
          date = sunday + timedelta(days=item[0])
          entry.append(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%b-%d'))
          entry.append(name)
          entry.append(hours)
          json.append(entry)
        sunday = sunday + timedelta(days=7)
  return json


def makePieBarJSON(values):
  data_keys = ["label","value", "color"]
  data = []
  for result in values:
    entry = []
    entry.append(str(result[0]))
    entry.append(result[1])
    if(len(result) > 2): entry.append(result[2])
    data.append(dict(zip(data_keys,entry)))
  return data


def modulePopulator(moduleIDs, studentID, edit):
  activity_keys = ["activity_ID", "activityType", "title", "start_date", "due_date", "grade_percentage", "grading_description", "description", "estimated_time","lecture","activity_type_ID","distribution","colour","class_time_spent","submitted","feedback", "notes"]
  module_keys = ["module_ID", "module_code" , "module_name", "module_lecturer", "module_lecturer_ID", "module_lecturer_email","credits","edit","contributors","colour","courses","total_students", "activities", "classes", "notes", "activity_feedback", "class_feedback"]
  course_keys = ["course_ID", "course_name", "coordinator_name","coordinator_email", "Total Students"]
  contributor_keys = ["lecturer_ID", "lecturer_name", "lecturer_email"]
  total_json = []
  feedback_keys = ["feedback_ID","feedback_title", "feedback_description", "feedback_question_ID"]
  feedback_mod_keys = ["feedback_title", "feedback_description", "feedback_question_ID"]
  note_keys = ["text"]
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor(buffered=True)
  for item in moduleIDs:
    module=[]
    activities=[]
    classes=[]
    courses=[]
    contributors=[]
    feedback=[]
    cur.execute("SELECT m.module_ID, m.module_code, m.module_name, s.staff_name, s.staff_ID, s.staff_email, m.module_credits FROM Modules as m LEFT JOIN Staff as s ON (s.staff_ID = m.staff_ID) WHERE m.module_ID = %s", (str(item[0]),))
    detailslist = cur.fetchall()
    module.append(detailslist[0][0])
    module.append(detailslist[0][1])
    module.append(detailslist[0][2])
    module.append(detailslist[0][3])
    module.append(detailslist[0][4])
    module.append(detailslist[0][5])
    module.append(detailslist[0][6])
    module.append(edit)
    cur.execute("SELECT mc.staff_ID, s.staff_name, s.staff_email FROM Module_Contributors as mc LEFT JOIN Staff as s ON (mc.staff_ID = s.staff_ID) WHERE mc.module_ID = %s", (str(item[0]),))
    contributorlist = cur.fetchall()
    for f in contributorlist:
      contributors.append(dict(zip(contributor_keys, f)))
    module.append(contributors)
    module.append(colours[0][int(item[0])])
    cur.execute("SELECT mc.course_ID, c.course_name, s.staff_name, s.staff_email, COUNT(st.student_ID) Students FROM Module_Course as mc LEFT JOIN Courses AS c ON (mc.course_ID = c.course_ID) LEFT JOIN Staff as s ON (s.staff_ID = c.staff_ID) LEFT JOIN Students as st ON (st.course_ID = mc.course_ID) WHERE mc.module_ID = %s GROUP BY c.course_name",(str(detailslist[0][0]),))
    courselist = cur.fetchall()
    studentcount = 0
    for k in courselist:
      courses.append(dict(zip(course_keys, k)))
      studentcount = studentcount + k[4]
    module.append(courses)
    module.append(studentcount)

    if(studentID == 1):
      cur.execute("SELECT a.activity_ID, at.activity_type, a.activity_name, a.start_date, a.end_date, a.module_value, a.grading, a.activity_description, a.hours, u.hours, cd.class_name, u.submitted, a.activity_type_ID, d.distribution FROM Activities AS a LEFT JOIN Class_Details as cd ON (a.lecture_ID = cd.class_details_ID) LEFT JOIN Activity_Type as at ON (at.activity_type_ID = a.activity_type_ID) LEFT JOIN Student_Progress as u ON (u.student_ID = %s AND u.activity_ID = a.activity_ID) LEFT JOIN Distribution as d ON (a.distribution_ID = d.distribution_ID) WHERE a.module_ID = %s", (studentID,str(item[0])))
      activity_keys = ["activity_ID", "activityType", "title", "start_date", "due_date", "grade_percentage", "grading_description", "description", "estimated_time", "time_spent","lecture","submitted","activity_type_ID","distribution", "colour", "class_time_spent","feedback"]
    else: cur.execute ("SELECT a.activity_ID, at.activity_type, a.activity_name, a.start_date, a.end_date, a.module_value, a.grading, a.activity_description, a.hours, cd.class_name, a.activity_type_ID, d.distribution FROM Activities AS a LEFT JOIN Class_Details as cd ON (a.lecture_ID = cd.class_details_ID) LEFT JOIN Activity_Type as at ON (at.activity_type_ID = a.activity_type_ID) LEFT JOIN Distribution as d ON (a.distribution_ID = d.distribution_ID) WHERE a.module_ID = %s", (str(item[0]),))
    activitylist = cur.fetchall()

    for activity in activitylist:
      cur.execute("SELECT f.feedback_set_ID, fd.feedback_name, fd.feedback_description, fd.feedback_ID FROM Feedback_Set as f LEFT JOIN Feedback_Details as fd ON (f.feedback_details_ID = fd.feedback_ID) WHERE (f.feedback_activity_ID = %s AND f.feedback_type_ID = 2)",(activity[0],))
      feedbacklist = cur.fetchall()
      feedback = []
      actent = []
      for subact in activity:
        actent.append(subact)

      if(studentID == 2):
        actent.append(aColours[int(activity[10])][int(item[0])])
      else: #actent.append(colours[int(activity[10])][int(item[0])])
        actent.append(colours[0][int(item[0])])


      cur.execute("SELECT AVG(hours) hours FROM Student_Progress WHERE activity_ID = %s",(activity[0],))
      x = cur.fetchall()
      actent.append(x[0][0])


      if(studentID != 1):
        cur.execute("SELECT SUM(submitted) submitted FROM Student_Progress WHERE activity_ID = %s",(activity[0],))
        sub = cur.fetchall()
        if sub[0][0] is None: actent.append(0)
        else: actent.append(int(sub[0][0]))

      for subfeed in feedbacklist:
        feedback.append(dict(zip(feedback_keys, subfeed)))
      actent.append(feedback)
      cur.execute("SELECT n.note_text from Activity_Notes as n WHERE n.note_activity_ID = %s", (str(activity[0]),))
      notelist = cur.fetchall()
      notes = []
      for note in notelist:
        notes.append(dict(zip(note_keys,note)))
      actent.append(notes)
      activities.append(dict(zip(activity_keys, actent)))

    module.append(activities)
    cur.execute("SELECT c.class_ID, at.activity_type, c.class_location, c.start_time, c.end_time, c.class_day, c.class_semester, c.activity_type_ID FROM Classes AS c LEFT JOIN Days as d ON (c.class_day = d.day_ID) LEFT JOIN Activity_Type as at ON (at.activity_type_ID = c.activity_type_ID) WHERE c.module_ID = %s", (str(item[0]),))
    classlist = cur.fetchall()
    cur.execute("SELECT cd.class_date, cd.class_name, cd.class_description, cd.class_ID, cd.class_details_ID, s.staff_name from Class_Details as cd LEFT JOIN Staff as s ON (cd.staff_ID = s.staff_ID) WHERE cd.module_ID = %s", (str(item[0]),))
    classdetails = cur.fetchall()
    feedback_keys = ["name", "description"]
    cur.execute("SELECT f.feedback_set_ID, fd.feedback_name, fd.feedback_description, fd.feedback_ID FROM Feedback_Set as f LEFT JOIN Feedback_Details as fd ON (f.feedback_details_ID = fd.feedback_ID) WHERE (f.feedback_activity_ID = %s AND f.feedback_type_ID = 1)",(str(detailslist[0][0]),))
    feedbacklist = cur.fetchall()
    start1 = "2018-09-09"
    end1 = "2018-11-25"
    start2 = "2019-01-20"
    end2 = "2019-04-07"
    noclass = ["2018-10-21", "2019-03-03"]
    class_keys = ["class_ID", "activityType", "location", "start_time", "end_time","date","notes","title", "description", "lecturer", "linked_activities", "feedback", "colour"]
    feedback_keys = ["feedback_ID","feedback_title", "feedback_description", "feedback_question_ID"]
    note_keys = ["text"]
    act_keys = ["activity_ID","activity_name", "start", "end"]

    for classitem in classlist:
      if(studentID == 2): colour = colours[int(classitem[7])][int(item[0])]
      else: colour = colours[0][int(item[0])]
      if (classitem[6] == 1):
        sunday =  datetime.datetime.strptime(start1, '%Y-%m-%d')
        while(sunday <= datetime.datetime.strptime(end1, '%Y-%m-%d')):
          if sunday not in noclass:
            entry = []
            date = sunday + timedelta(days=classitem[5])
            entry.append(classitem[0])
            entry.append(classitem[1])
            entry.append(classitem[2])
            entry.append(datetime.datetime.strptime(str(classitem[3]),'%H:%M:%S').strftime('%H:%M:%S'))
            entry.append(datetime.datetime.strptime(str(classitem[4]),'%H:%M:%S').strftime('%H:%M:%S'))
            entry.append(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'))
            sort = 1
            cur.execute("SELECT n.note_text from Lecture_Notes as n WHERE n.note_lecture_ID = %s AND n.note_lecture_date = %s", (classitem[0],entry[5]))
            notelist = cur.fetchall()
            notes = []
            for note in notelist:
              notes.append(dict(zip(note_keys,note)))
            entry.append(notes)
            for thing in classdetails:
              if datetime.datetime.strptime(str(thing[0]),'%Y-%m-%d').strftime('%Y-%m-%d') == entry[5]:
                entry.append(thing[1])
                entry.append(thing[2])
                entry.append(thing[5])
                cur.execute("SELECT a.activity_ID, a.activity_name, a.start_date, a.end_date from Activities as a WHERE a.lecture_ID = %s", (thing[4],))
                actlist = cur.fetchall()
                acts = []
                for act in actlist:
                  acts.append(dict(zip(act_keys,act)))
                entry.append(acts)
                sort = 0
            if(sort):
              entry.append(classitem[1])
              entry.append("None")
              entry.append(detailslist[0][3])
              entry.append([])
            cur.execute("SELECT f.feedback_set_ID, fd.feedback_name, fd.feedback_description, fd.feedback_ID FROM Feedback_Set as f LEFT JOIN Feedback_Details as fd ON (f.feedback_details_ID = fd.feedback_ID) WHERE (f.feedback_activity_ID = %s AND f.feedback_type_ID = 3)",(str(classitem[0]),))
            feedbacklist = cur.fetchall()
            feedback = []
            for subfeed in feedbacklist:
              feedback.append(dict(zip(feedback_keys, subfeed)))
            entry.append(feedback)
            entry.append(colour)
            classes.append(dict(zip(class_keys,entry)))
          sunday = sunday + timedelta(days=7)

      elif (classitem[6] == 2):
        sunday =  datetime.datetime.strptime(start2, '%Y-%m-%d')
        while(sunday <= datetime.datetime.strptime(end2, '%Y-%m-%d')):
          if sunday not in noclass:
            entry = []
            date = sunday + timedelta(days=classitem[5])
            entry.append(classitem[0])
            entry.append(classitem[1])
            entry.append(classitem[2])
            entry.append(datetime.datetime.strptime(str(classitem[3]),'%H:%M:%S').strftime('%H:%M:%S'))
            entry.append(datetime.datetime.strptime(str(classitem[4]),'%H:%M:%S').strftime('%H:%M:%S'))
            entry.append(datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'))
            sort = 1
            cur.execute("SELECT n.note_text from Lecture_Notes as n WHERE n.note_lecture_ID = %s AND n.note_lecture_date = %s", (classitem[0],entry[5]))
            notelist = cur.fetchall()
            notes = []
            for note in notelist:
              notes.append(dict(zip(note_keys,note)))
            entry.append(notes)
            for thing in classdetails:
              if datetime.datetime.strptime(str(thing[0]),'%Y-%m-%d').strftime('%Y-%m-%d') == entry[5]:
                entry.append(thing[1])
                entry.append(thing[2])
                entry.append(thing[5])
                cur.execute("SELECT a.activity_ID, a.activity_name, a.start_date, a.end_date from Activities as a WHERE a.lecture_ID = %s", (thing[4],))
                actlist = cur.fetchall()
                acts = []
                for act in actlist:
                  acts.append(dict(zip(act_keys,act)))
                entry.append(acts)
                sort = 0
            if(sort):
              entry.append(classitem[1])
              entry.append("None")
              entry.append(detailslist[0][3])
              entry.append([])
            cur.execute("SELECT f.feedback_set_ID, fd.feedback_name, fd.feedback_description, fd.feedback_ID  FROM Feedback_Set as f LEFT JOIN Feedback_Details as fd ON (f.feedback_details_ID = fd.feedback_ID) WHERE (f.feedback_activity_ID = %s AND f.feedback_type_ID = 3)",(str(classitem[0]),))
            feedbacklist = cur.fetchall()
            feedback = []
            for subfeed in feedbacklist:
              feedback.append(dict(zip(feedback_keys, subfeed)))
            entry.append(feedback)
            entry.append(colour)
            classes.append(dict(zip(class_keys,entry)))
          sunday = sunday + timedelta(days=7)
    module.append(classes)

    cur.execute("SELECT n.note_text from Module_Notes as n WHERE n.note_module_ID = %s", (detailslist[0][0],))
    notelist = cur.fetchall()
    notes = []
    for modnote in notelist:
      notes.append(dict(zip(note_keys,modnote)))
    module.append(notes)

    cur.execute("SELECT fd.feedback_name, fd.feedback_description, fd.feedback_ID FROM Feedback_Set as f LEFT JOIN Feedback_Details as fd ON (f.feedback_details_ID = fd.feedback_ID) WHERE (f.feedback_activity_ID IN (SELECT a.activity_ID FROM Activities as a WHERE a.module_ID = %s) AND f.feedback_type_ID = 2) GROUP BY feedback_ID;",(detailslist[0][0],))
    feedbacklist = cur.fetchall()
    feedback = []
    for subfeedmod in feedbacklist:
      feedback.append(dict(zip(feedback_mod_keys, subfeedmod)))
    module.append(feedback)

    cur.execute("SELECT fd.feedback_name, fd.feedback_description, fd.feedback_ID FROM Feedback_Set as f LEFT JOIN Feedback_Details as fd ON (f.feedback_details_ID = fd.feedback_ID) WHERE (f.feedback_activity_ID IN (SELECT a.class_ID FROM Classes as a WHERE a.module_ID = %s) AND f.feedback_type_ID = 3) GROUP BY feedback_ID;",(detailslist[0][0],))
    feedbacklist = cur.fetchall()
    feedback = []
    for subfeedmod in feedbacklist:
      feedback.append(dict(zip(feedback_mod_keys, subfeedmod)))
    module.append(feedback)


    total_json.append(dict(zip(module_keys, module)))
  cur.close()
  mydb.close()
  return total_json

def parseFeedbackHistogram(modulelist):
  subkeys = ["question", "dialvalue", "bardata"]
  modules = []
  likert = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
  question = []
  data = []
  datalist = []
  count = 0
  total = 0
  current = modulelist[0][0]
  lik = 0
  for entry in modulelist:
    data = []
    if (entry[0] != current):
      while(5 > lik):
        data.append(likert[lik])
        data.append(0)
        datalist.append(data)
        data = []
        lik = lik + 1
      lik = 0
      question.append(current)
      question.append(round_up(total/count))
      count = 0
      total = 0
      question.append(makePieBarJSON(datalist))
      modules.append(dict(zip(subkeys,question)))
      datalist = []
      question = []
      current = entry[0]

    while(int(entry[1]-1) > lik):
      data.append(likert[lik])
      data.append(0)
      datalist.append(data)
      data = []
      lik = lik + 1

    data.append(likert[int(entry[1]-1)])
    data.append(entry[2])
    lik = lik + 1
    datalist.append(data)
    count = count + entry[2]
    total = total + entry[1]*entry[2]


  question.append(current)
  question.append(round_up(total/count))
  question.append(makePieBarJSON(datalist))
  modules.append(dict(zip(subkeys,question)))
  datalist = []
  question = []
  return modules

def nestedCategoryStack(module_name,activities,classes,colour,hours):
  TOTAL_WEEKS = 12
  keys = ["label","color","value","category"]
  subkeys = ["label","color","value"]
  stack = []
  module = []
  module.append(module_name)
  module.append(colour)
  module.append(hours)

  for item in activities:
    entry = []
    entry.append(item[1])
    entry.append(colour)
    entry.append(item[2])
    stack.append(dict(zip(subkeys,entry)))

  for classitem in classes:
    entry = []
    entry.append(classitem[0])
    entry.append(colour)
    entry.append(int(classitem[1].seconds/3600*TOTAL_WEEKS))
    stack.append(dict(zip(subkeys,entry)))

  module.append(stack)
  return dict(zip(keys,module))

##################################################### OUTPUTS ##################################################

@app.route("/modulesByStudent<string:studentID>")
def modulesByStudent(studentID):
  mydb = mysql.connector.connect(**connection_config_dict)
  json_data = []
  cur = mydb.cursor(buffered=True)
  cur.execute("SELECT course_ID FROM Students WHERE student_ID = %s ", (studentID,))
  courseID = cur.fetchall()
  courseID = str(courseID[0][0])

  cur.execute("SELECT s.student_ID,s.student_name, s.student_number, s.student_email, s.course_ID, c.course_name FROM Students as s LEFT JOIN Courses as c ON (c.course_ID = s.course_ID) WHERE s.student_ID = %s",(studentID,))
  student=cur.fetchall()
  studentkeys = ["student_ID","student_name","student_number","student_email","course_ID","course_name"]
  details = dict(zip(studentkeys,student[0]))
  json_data.append(details)
  cur.execute("Select m.module_ID FROM Modules as m LEFT JOIN Module_Course as mc ON (mc.module_ID = m.module_ID) WHERE mc.course_ID = %s", (courseID,))
  module_list = cur.fetchall()
  cur.close()
  mydb.close()
  json_data.append(modulePopulator(module_list,int(studentID),0))
  keys=["student","modules"]
  final = dict(zip(keys, json_data))
  response = app.response_class(
        response=json.dumps(final, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

@app.route("/modulesByStaff<string:staffID>")
def modulesByStaff(staffID):
  mydb = mysql.connector.connect(**connection_config_dict)
  json_data = []
  keys = ["myModules", "contributedModules"]
  cur = mydb.cursor(buffered=True)
  cur.execute("Select module_ID FROM Modules WHERE staff_ID = %s", (staffID,))
  module_list = cur.fetchall()
  cur.execute("Select module_ID FROM Module_Contributors WHERE staff_ID = %s", (staffID,))
  cont_list = cur.fetchall()
  cur.close()
  mydb.close()
  json_data.append(modulePopulator(module_list,2,1))
  json_data.append(modulePopulator(cont_list,2,0))
  final = dict(zip(keys,json_data))
  response = app.response_class(
        response=json.dumps(final, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

@app.route("/courseByCoordinator<string:staffID>")
def modulesByCoordinator(staffID):
  mydb = mysql.connector.connect(**connection_config_dict)
  json_data = []
  courselist = []
  mycourse = []
  notelist = []
  course_keys = ["course_ID", "course_name", "course_lecturer", "course_lecturer_email", "course_lecturer_ID", "total_students", "notes"]
  keys = ["myCourse","myModules", "contributedModules"]
  cur = mydb.cursor(buffered=True)
  cur.execute("SELECT c.course_ID, c.course_name, s.staff_name, s.staff_email, c.staff_ID, COUNT(st.student_ID) total_students FROM Courses as c LEFT JOIN Staff as s ON (s.staff_ID = c.staff_ID) LEFT JOIN Students as st ON (st.course_ID = c.course_ID) WHERE c.staff_ID = %s", (staffID,))
  course = cur.fetchall()
  for item in course[0]:
    courselist.append(item)
  cur.execute("SELECT n.note_text from Course_Notes as n WHERE n.note_course_ID = %s", (course[0][0],))
  notelist = cur.fetchall()
  notes = []
  note_keys = ["text"]
  for modnote in notelist:
    notes.append(dict(zip(note_keys,modnote)))
  courselist.append(notes)
  mycourse.append(dict(zip(course_keys,courselist)))
  cur.execute("SELECT mc.module_ID FROM Module_Course mc LEFT JOIN Modules as m ON (m.module_ID = mc.module_ID) WHERE m.staff_ID = %s AND mc.course_ID = %s", (staffID,course[0][0]))
  module_list = cur.fetchall()
  cur.execute("SELECT mc.module_ID FROM Module_Course mc LEFT JOIN Modules as m ON (m.module_ID = mc.module_ID) WHERE m.staff_ID <> %s AND mc.course_ID = %s", (staffID,course[0][0]))
  cont_list = cur.fetchall()
  cur.close()
  mydb.close()
  json_data.append(mycourse)
  json_data.append(modulePopulator(module_list,2,1))
  json_data.append(modulePopulator(cont_list,2,0))
  final = dict(zip(keys,json_data))
  response = app.response_class(
        response=json.dumps(final, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

@app.route("/moduleByModule<string:moduleID>")
def moduleByModule(moduleID):
  json_data = []
  module_list = []
  module_list.append(moduleID)
  json_data = modulePopulator(module_list,0,0)
  response = app.response_class(
        response=json.dumps(json_data, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

@app.route("/modulesByCourse<string:courseID>")
def modulesByCourse(courseID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor(buffered=True)
  json_data = []
  cur.execute("Select m.module_ID FROM Modules as m LEFT JOIN Module_Course as mc ON (mc.module_ID = m.module_ID) WHERE mc.course_ID = %s", (courseID,))
  module_list = cur.fetchall()
  cur.close()
  mydb.close()
  json_data = modulePopulator(module_list,0,0)
  response = app.response_class(
        response=json.dumps(json_data, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

@app.route("/studentsByModule<string:moduleID>")
def studentsByModule(moduleID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor(buffered = True)
  json_data = []
  student = []
  json_keys = ["pie","Students"]
  cur.execute("SELECT s.course_ID, c.course_name, s.student_name, s.student_ID, s.student_number FROM Students as s LEFT JOIN Courses as c ON (s.course_ID = c.course_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = %s AND mc.course_ID = s.course_ID)", (moduleID,))
  student_list = cur.fetchall()
  cur.execute("SELECT c.course_name, COUNT(c.course_name), c.course_ID Students FROM Students as s LEFT JOIN Courses as c ON (s.course_ID = c.course_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = %s AND mc.course_ID = s.course_ID) GROUP BY c.course_name", (moduleID,))
  pie_list = cur.fetchall()
  pieJ = []
  for pie in pie_list:
      entry = []
      entry.append(pie[0])
      entry.append(pie[1])
      entry.append(colours[int(pie[2])][int(moduleID)])
      pieJ.append(entry)
  json_data.append(makePieBarJSON(pieJ))
  cur.close()
  mydb.close()
  student_keys = ["course_ID", "course_name", "student_name", "student_ID", "student_number"]
  for item in student_list:
    student.append(dict(zip(student_keys, item)))
  json_data.append(student)
  final = dict(zip(json_keys, json_data))
  response = app.response_class(
        response=json.dumps(final, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

############################################## GRAPHS ###############################################################
@app.route("/activityTypePieChartsByModule<string:moduleID>")
def activityTypePieChartsByModule(moduleID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor()
  json_data = []
  byHours = []
  byGradeModule = []
  keys = ["ByHours","ByGrade"]

  cur.execute("SELECT at.activity_type, SUM(a.hours) Hours, a.activity_type_ID FROM Activities as a LEFT JOIN Activity_Type as at ON (a.activity_type_ID = at.activity_type_ID) WHERE module_ID = %s  GROUP BY at.activity_type", (moduleID,))
  byHoursActivity = cur.fetchall()
  cur.execute("SELECT at.activity_type, CAST(SUM(timediff(c.end_time, c.start_time)) as time) as weeklyhours, c.activity_type_ID FROM Classes as c LEFT JOIN Activity_Type as at ON (c.activity_type_ID = at.activity_type_ID) WHERE c.module_ID = %s GROUP BY at.activity_type", (moduleID,))
  byHoursClass = cur.fetchall()
  for classtype in byHoursClass:
    entry = []
    hours = int(classtype[1].seconds/3600*30)
    entry.append(classtype[0])
    entry.append(hours)
    colour = colours[int(classtype[2])][int(moduleID)]
    entry.append(colour)
    byHours.append(entry)
  for activity in byHoursActivity:
    entry = []
    entry.append(activity[0])
    entry.append(activity[1])
    colour = colours[int(activity[2])][int(moduleID)]
    entry.append(colour)
    byHours.append(entry)
  json_data.append(makePieBarJSON(byHours))

  cur.execute("SELECT at.activity_type, SUM(a.module_value) Grade, a.activity_type_ID FROM Activities as a LEFT JOIN Activity_Type as at ON (a.activity_type_ID = at.activity_type_ID) WHERE module_ID = %s  GROUP BY at.activity_type", (moduleID,))
  byGrade = cur.fetchall()
  for grade in byGrade:
    entry = []
    entry.append(grade[0])
    entry.append(grade[1])
    print(grade[2], moduleID)
    entry.append(colours[int(grade[2])][int(moduleID)])
    byGradeModule.append(entry)
  json_data.append(makePieBarJSON(byGradeModule))

  final = dict(zip(keys,json_data))
  response = app.response_class(
      response=json.dumps(final, indent=4, cls=DateTimeEncoder),
      status=200,
      mimetype='application/json'
  )
  cur.close()
  mydb.close()
  return response

@app.route("/activityTypePieChartsByCourse<string:courseID>")
def activityTypePieChartsByCourse(courseID):
  TOTAL_WEEKS = 12
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor()
  json_data = []
  byHours =[]
  byGradeActivity=[]
  byModuleHours =[]
  classlist = []
  activitylist = []
  keys = ["ByModule","ByGradeAvg","ByActivity"]
  cur.execute("SELECT m.module_name, SUM(a.hours) hours, m.module_ID FROM Activities as a LEFT JOIN Modules as m ON (m.module_ID = a.module_ID) WHERE a.module_ID in (SELECT mc.module_ID FROM Module_Course as mc WHERE mc.course_ID = %s AND mc.module_ID = a.module_ID) GROUP BY a.module_ID", (courseID,))
  byModuleHoursActivity = cur.fetchall()

  cur.execute("SELECT m.module_name, CAST(SUM(timediff(c.end_time, c.start_time)) as time), m.module_ID as weeklyhours FROM Classes as c LEFT JOIN Modules as m ON (m.module_ID = c.module_ID) WHERE c.module_ID in (SELECT mc.module_ID FROM Module_Course as mc WHERE mc.course_ID = %s AND mc.module_ID = c.module_ID) GROUP BY c.module_ID", (courseID,))
  byModuleHoursClass = cur.fetchall()

  for moduleclasstype in byModuleHoursClass:
    entry = []
    hours = int(moduleclasstype[1].seconds/3600*TOTAL_WEEKS)
    entry.append(moduleclasstype[0])
    entry.append(hours)
    entry.append(colours[0][int(moduleclasstype[2])])
    classlist.append(entry)

  for moduleactivity in byModuleHoursActivity:
    entry = []
    entry.append(moduleactivity[0])
    entry.append(moduleactivity[1])
    entry.append(colours[0][int(moduleactivity[2])])
    activitylist.append(entry)
  i = 0
  while i < len(activitylist):
    entry = []
    entry.append(activitylist[i][0])
    hours = activitylist[i][1] + classlist[i][1]
    entry.append(hours)
    entry.append(activitylist[i][2])
    byModuleHours.append(entry)
    i = i +1
  json_data.append(makePieBarJSON(byModuleHours))

  cur.execute("SELECT at.activity_type, AVG(a.module_value) grade, a.activity_type_ID FROM Activities as a LEFT JOIN Activity_Type as at ON (a.activity_type_ID = at.activity_type_ID) WHERE a.module_ID in (SELECT mc.module_ID FROM Module_Course as mc WHERE mc.course_ID = %s AND mc.module_ID = a.module_ID) GROUP BY at.activity_type", (courseID,))
  byGrade = cur.fetchall()

  for grade in byGrade:
    entry = []
    entry.append(grade[0])
    entry.append(grade[1])
    byGradeActivity.append(entry)
  json_data.append(makePieBarJSON(byGradeActivity))

  cur.execute("SELECT at.activity_type, SUM(a.hours) hours, a.activity_type_ID FROM Activities as a LEFT JOIN Activity_Type as at ON (a.activity_type_ID = at.activity_type_ID) WHERE a.module_ID in (SELECT mc.module_ID FROM Module_Course as mc WHERE mc.course_ID = %s AND mc.module_ID = a.module_ID) GROUP BY at.activity_type", (courseID,))
  byHoursActivity = cur.fetchall()
  cur.execute("SELECT at.activity_type, CAST(SUM(timediff(c.end_time, c.start_time)) as time) as weeklyhours, c.activity_type_ID FROM Classes as c LEFT JOIN Activity_Type as at ON (c.activity_type_ID = at.activity_type_ID) WHERE c.module_ID in (SELECT mc.module_ID FROM Module_Course as mc WHERE mc.course_ID = %s AND mc.module_ID = c.module_ID) GROUP BY at.activity_type", (courseID,))
  byHoursClass = cur.fetchall()

  for classtype in byHoursClass:
    entry = []
    hours = int(classtype[1].seconds/3600*30)
    entry.append(classtype[0])
    entry.append(hours)
    byHours.append(entry)
  for activity in byHoursActivity:
    entry = []
    entry.append(activity[0])
    entry.append(activity[1])
    byHours.append(entry)

  json_data.append(makePieBarJSON(byHours))
  final = dict(zip(keys,json_data))
  response = app.response_class(
      response=json.dumps(final, indent=4, cls=DateTimeEncoder),
      status=200,
      mimetype='application/json'
  )
  mydb.close()
  return response

@app.route("/feedbackBarChartsByModule<string:moduleID>")
def feedbackBarChartByModule(moduleID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor(buffered = True)
  json_data = []
  keys = ["byModule","byActivity", "byClass"]

  cur.execute("SELECT fd.feedback_name, f.feedback_score, COUNT(f.feedback_score) Entries FROM Feedback as f LEFT JOIN Feedback_Set as fs ON (fs.feedback_set_ID = f.feedback_set_ID) LEFT JOIN Feedback_Details as fd ON (fs.feedback_details_ID = fd.feedback_ID) WHERE (fs.feedback_activity_ID = %s AND fs.feedback_type_ID = 1) GROUP BY f.feedback_score,fd.feedback_name ORDER BY fd.feedback_name, f.feedback_score", (moduleID,))
  modulelist = cur.fetchall()
  if(cur.rowcount > 0):json_data.append(parseFeedbackHistogram(modulelist))
  else: json_data.append([])

  cur.execute("SELECT fd.feedback_name, f.feedback_score, COUNT(f.feedback_score) Entries FROM Feedback as f LEFT JOIN Feedback_Set as fs ON (fs.feedback_set_ID = f.feedback_set_ID) LEFT JOIN Feedback_Details as fd ON (fs.feedback_details_ID = fd.feedback_ID) WHERE (fs.feedback_activity_ID in (SELECT a.activity_ID FROM Activities as a WHERE a.module_ID = %s) AND fs.feedback_type_ID = 2) GROUP BY f.feedback_score,fd.feedback_name ORDER BY fd.feedback_name, f.feedback_score", (moduleID,))
  activitylist = cur.fetchall()
  if(cur.rowcount > 0):json_data.append(parseFeedbackHistogram(activitylist))
  else: json_data.append([])

  cur.execute("SELECT fd.feedback_name, f.feedback_score, COUNT(f.feedback_score) Entries FROM Feedback as f LEFT JOIN Feedback_Set as fs ON (fs.feedback_set_ID = f.feedback_set_ID) LEFT JOIN Feedback_Details as fd ON (fs.feedback_details_ID = fd.feedback_ID) WHERE (fs.feedback_activity_ID in (SELECT c.class_ID FROM Classes as c WHERE c.module_ID = %s) AND fs.feedback_type_ID = 3) GROUP BY f.feedback_score,fd.feedback_name ORDER BY fd.feedback_name, f.feedback_score", (moduleID,))
  classlist = cur.fetchall()

  if(cur.rowcount > 0):json_data.append(parseFeedbackHistogram(classlist))
  else: json_data.append([])
  cur.close()
  mydb.close()
  final = dict(zip(keys,json_data))
  response = app.response_class(
      response=json.dumps(final, indent=4, cls=DateTimeEncoder),
      status=200,
      mimetype='application/json'
  )
  return response
@app.route("/feedbackByActivity<string:activityID>")
def feedbackByActivity(activityID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor(buffered = True)
  json_data = []
  keys = ["Questions"]
  cur.execute("SELECT fd.feedback_name, f.feedback_score, COUNT(f.feedback_score) Entries FROM Feedback as f LEFT JOIN Feedback_Set as fs ON (fs.feedback_set_ID = f.feedback_set_ID) LEFT JOIN Feedback_Details as fd ON (fs.feedback_details_ID = fd.feedback_ID) WHERE (fs.feedback_activity_ID = %s AND fs.feedback_type_ID = 2) GROUP BY f.feedback_score,fd.feedback_name ORDER BY fd.feedback_name, f.feedback_score", (activityID,))
  activitylist = cur.fetchall()
  print(activitylist)
  if(cur.rowcount > 0):json_data.append(parseFeedbackHistogram(activitylist))
  else: json_data.append([])
  cur.close()
  mydb.close()
  final = dict(zip(keys,json_data))
  response = app.response_class(
      response=json.dumps(final, indent=4, cls=DateTimeEncoder),
      status=200,
      mimetype='application/json'
  )
  return response

@app.route("/feedbackByModule<string:moduleID>")
def feedbackByModule(moduleID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor(buffered = True)
  json_data = []
  keys = ["byActivity","byClass"]
  cur.execute("SELECT fd.feedback_name, f.feedback_score, COUNT(f.feedback_score) Entries FROM Feedback as f LEFT JOIN Feedback_Set as fs ON (fs.feedback_set_ID = f.feedback_set_ID) LEFT JOIN Feedback_Details as fd ON (fs.feedback_details_ID = fd.feedback_ID) WHERE (fs.feedback_activity_ID IN (SELECT a.activity_ID FROM Activities as a WHERE a.module_ID = %s) AND fs.feedback_type_ID = 2) GROUP BY f.feedback_score, fd.feedback_name ORDER BY fd.feedback_name, f.feedback_score", (moduleID,))
  activitylist = cur.fetchall()
  if(cur.rowcount > 0):
      json_data.append(parseFeedbackHistogram(activitylist))
  else: json_data.append([])
  cur.execute("SELECT fd.feedback_name, f.feedback_score, COUNT(f.feedback_score) Entries FROM Feedback as f LEFT JOIN Feedback_Set as fs ON (fs.feedback_set_ID = f.feedback_set_ID) LEFT JOIN Feedback_Details as fd ON (fs.feedback_details_ID = fd.feedback_ID) WHERE (fs.feedback_activity_ID IN (SELECT a.class_ID FROM Classes as a WHERE a.module_ID = %s) AND fs.feedback_type_ID = 2) GROUP BY f.feedback_score, fd.feedback_name ORDER BY fd.feedback_name, f.feedback_score", (moduleID,))
  classlist = cur.fetchall()
  if(cur.rowcount > 0):
      json_data.append(parseFeedbackHistogram(classlist))
  else: json_data.append([])
  cur.close()
  mydb.close()
  final = dict(zip(keys,json_data))
  response = app.response_class(
      response=json.dumps(final, indent=4, cls=DateTimeEncoder),
      status=200,
      mimetype='application/json'
  )
  return response

@app.route("/feedbackByClass<string:classID>")
def feedbackByClass(classID):
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor(buffered = True)
  json_data = []
  keys = ["Questions"]

  cur.execute("SELECT fd.feedback_name, f.feedback_score, COUNT(f.feedback_score) Entries FROM Feedback as f LEFT JOIN Feedback_Set as fs ON (fs.feedback_set_ID = f.feedback_set_ID) LEFT JOIN Feedback_Details as fd ON (fs.feedback_details_ID = fd.feedback_ID) WHERE (fs.feedback_activity_ID  = %s AND fs.feedback_type_ID = 3) GROUP BY f.feedback_score,fd.feedback_name ORDER BY fd.feedback_name, f.feedback_score", (classID,))
  classlist = cur.fetchall()

  if(cur.rowcount > 0):json_data.append(parseFeedbackHistogram(classlist))
  else: json_data.append([])
  cur.close()
  mydb.close()
  final = dict(zip(keys,json_data))
  response = app.response_class(
      response=json.dumps(final, indent=4, cls=DateTimeEncoder),
      status=200,
      mimetype='application/json'
  )
  return response

@app.route("/nestedPieByCourse<string:courseID>")
def nestedPieByCourse(courseID):
  TOTAL_WEEKS = 12
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor(buffered = True)
  keys = ["label","color","value","category"]
  final_key = ["data"]
  modules = []
  json_data = []
  cur = mydb.cursor(buffered = True)
  cur.execute("SELECT c.course_name, SUM(a.hours) FROM Courses as c LEFT JOIN Activities as a ON (a.module_ID in (SELECT mc.module_ID FROM Module_Course as mc WHERE mc.course_ID = %s)) WHERE c.course_ID = %s",(courseID,courseID))
  activityhours = cur.fetchall()

  cur.execute("SELECT co.course_name, CAST(SUM(timediff(c.end_time, c.start_time)) as time) as weeklyhours FROM Classes as c LEFT JOIN Courses as co ON (co.course_ID = %s) WHERE (c.module_ID in (SELECT mc.module_ID FROM Module_Course as mc WHERE mc.course_ID = %s)) GROUP BY co.course_name", (courseID,courseID))
  classhours = cur.fetchall()

  if activityhours[0][1] is None: activitytotal = 0
  else : activitytotal = activityhours[0][1]

  if classhours[0][1] is None: classtotal = 0
  else: classtotal = int(classhours[0][1].seconds/3600*TOTAL_WEEKS)
  coursehours = classtotal + activitytotal

  cur.execute("SELECT module_ID FROM Module_Course WHERE course_ID = %s",(courseID,))
  moduleIDs = cur.fetchall()
  for moduleID in moduleIDs:
    colour = colours[0][int(moduleID[0])]
    cur.execute("SELECT m.module_name, at.activity_type, SUM(a.hours) FROM Activities as a LEFT JOIN Activity_Type as at ON (a.activity_type_ID = at.activity_type_ID) LEFT JOIN Modules as m ON (m.module_ID = a.module_ID) WHERE a.module_ID = %s GROUP BY at.activity_type", (moduleID[0],))
    activities = cur.fetchall()

    cur.execute("SELECT at.activity_type, CAST(SUM(timediff(c.end_time, c.start_time)) as time) as weeklyhours FROM Classes as c LEFT JOIN Activity_Type as at ON (at.activity_type_ID = c.activity_type_ID) WHERE c.module_ID = %s GROUP BY c.module_ID,c.activity_type_ID", (moduleID[0],))
    classes = cur.fetchall()

    cur.execute("SELECT SUM(hours) FROM Activities WHERE module_ID = %s",(moduleID[0],))
    activity_total = cur.fetchall()
    cur.execute("SELECT CAST(SUM(timediff(end_time, start_time)) as time) as weeklyhours FROM Classes WHERE module_ID = %s", (moduleID[0],))
    class_total = cur.fetchall()
    if activity_total[0][0] is None: activitytotal = 0
    else: activitytotal = activity_total[0][0]

    if class_total[0][0] is None: classtotal = 0
    else: classtotal = int(class_total[0][0].seconds/3600*TOTAL_WEEKS)

    hours = classtotal + activitytotal
    cur.execute("SELECT module_name FROM Modules WHERE module_ID = %s",(moduleID[0],))
    module_name = cur.fetchall()
    modules.append(nestedCategoryStack(module_name[0][0],activities,classes,colour,hours))

  json_data.append(activityhours[0][0])
  json_data.append("#ffffff")
  json_data.append(coursehours)
  json_data.append(modules)
  cur.close()
  mydb.close()
  final = []
  final.append(dict(zip(keys,json_data)))
  response = app.response_class(
      response=json.dumps(final, indent=4, cls=DateTimeEncoder),
      status=200,
      mimetype='application/json'
  )
  return response


@app.route("/timelineByCourse<string:courseID>")
def timelineByCourse(courseID):
  mydb = mysql.connector.connect(**connection_config_dict)
  json_data = []
  values = []
  classes = []
  try:
    cur = mydb.cursor(buffered=True)
    cur.execute("SELECT m.module_name, a.start_date, a.end_date, a.hours, m.module_ID, a.distribution_ID FROM Activities AS a LEFT JOIN Modules as m ON (m.module_ID = a.module_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = m.module_ID) WHERE mc.course_ID = %s", (courseID,))
    values = cur.fetchall()
    cur.execute("SELECT  m.module_name, c.class_day, c.class_semester, c.start_time, c.end_time, m.module_ID FROM Classes AS c LEFT JOIN Modules as m ON (m.module_ID = c.module_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = m.module_ID) WHERE mc.course_ID = %s", (courseID,))
    classes = cur.fetchall()
    json_data.append(timelineData(values, classes))

    values = []
    classes = []
    cur.execute("SELECT at.activity_type, a.start_date, a.end_date, a.hours, a.activity_type_ID, a.distribution_ID FROM Activities AS a LEFT JOIN Activity_Type as at ON (at.activity_type_ID = a.activity_type_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = a.module_ID) WHERE mc.course_ID = %s", (courseID,))
    values = cur.fetchall()
    cur.execute("SELECT at.activity_type, c.class_day, c.class_semester, c.start_time, c.end_time, c.activity_type_ID FROM Classes AS c LEFT JOIN Activity_Type as at ON (at.activity_type_ID = c.activity_type_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = c.module_ID) WHERE mc.course_ID = %s", (courseID,))
    classes = cur.fetchall()
    json_data.append(timelineData(values, classes))
  except Exception: # Catch exception which will be raise in connection loss
    mydb = mysql.connector.connect(**connection_config_dict)
    cur = mydb.cursor(buffered=True)
  finally:
    cur.close()
    mydb.close()

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
  keys = ["byModule","byActivity","schema","bin"]
  final = dict(zip(keys,json_data))
  response = app.response_class(
        response=json.dumps(final, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response


@app.route("/timelineByStudent<string:studentID>")
def timelineByStudent(studentID):
  mydb = mysql.connector.connect(**connection_config_dict)
  json_data = []
  studentvalues = []
  classvalues = []
  classes = []
  cur = mydb.cursor(buffered=True)
  cur.execute("SELECT course_ID FROM Students WHERE student_ID = %s",(studentID,))
  courseID = cur.fetchall()
  cur.execute("SELECT a.start_date, a.end_date, st.hours, a.distribution_ID FROM Activities AS a LEFT JOIN Student_Progress as st ON (st.student_ID = %s AND st.activity_ID = a.activity_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = a.module_ID) WHERE mc.course_ID = %s AND a.end_date < '2019-03-14'", (studentID, courseID[0][0],))
  studentvalues = cur.fetchall()

  cur.execute("SELECT c.class_day, c.class_semester, c.start_time, c.end_time FROM Classes AS c LEFT JOIN Module_Course as mc ON (mc.module_ID = c.module_ID) WHERE mc.course_ID = %s", (courseID[0][0],))
  classes = cur.fetchall()
  values = []
  cur.execute("SELECT a.start_date, a.end_date, a.hours, a.distribution_ID FROM Activities AS a LEFT JOIN Module_Course as mc ON (mc.module_ID = a.module_ID) WHERE mc.course_ID = %s AND a.end_date < '2019-03-14'", (courseID[0][0],))
  values = cur.fetchall()

  cur.execute("SELECT a.start_date, a.end_date, a.student_hours, a.distribution_ID FROM Activities AS a LEFT JOIN Module_Course as mc ON (mc.module_ID = a.module_ID) WHERE mc.course_ID = %s AND a.end_date < '2019-03-14'", (courseID[0][0],))
  classvalues = cur.fetchall()

  value_data = timelineStudentData('Your Progress',studentvalues, classes) + timelineStudentData('Estimated Progress',values, classes) + timelineStudentData('Class Average',classvalues, classes)
  json_data.append(value_data)

  cur.close()
  mydb.close()

  schema_data = [{
      "name": "Date",
      "type": "date",
      "format": "%Y-%b-%d"
    },
    {
      "name": "User",
      "type": "string"
    },
    {
      "name": "Hours",
      "type": "number"
    }
  ]


  json_data.append(schema_data)
  keys = ["data","schema"]
  final = dict(zip(keys,json_data))
  response = app.response_class(
        response=json.dumps(final, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response


@app.route("/studentTimelineByCourse<string:courseID>")
def studentTimelineByCourse(courseID):
  mydb = mysql.connector.connect(**connection_config_dict)
  json_data = []
  classvalues = []
  classes = []
  values = []
  cur = mydb.cursor(buffered=True)


  cur.execute("SELECT c.class_day, c.class_semester, c.start_time, c.end_time FROM Classes AS c LEFT JOIN Module_Course as mc ON (mc.module_ID = c.module_ID) WHERE mc.course_ID = %s", (courseID,))
  classes = cur.fetchall()

  cur.execute("SELECT a.start_date, a.end_date, a.hours, a.distribution_ID FROM Activities AS a LEFT JOIN Module_Course as mc ON (mc.module_ID = a.module_ID) WHERE mc.course_ID = %s AND a.end_date < '2019-03-14'", (courseID,))
  values = cur.fetchall()

  cur.execute("SELECT a.start_date, a.end_date, a.student_hours, a.distribution_ID FROM Activities AS a LEFT JOIN Module_Course as mc ON (mc.module_ID = a.module_ID) WHERE mc.course_ID = %s AND a.end_date < '2019-03-14'", (courseID,))
  classvalues = cur.fetchall()

  value_data = timelineStudentData('Estimated Progress',values, classes) + timelineStudentData('Course Average',classvalues, classes)
  json_data.append(value_data)

  cur.close()
  mydb.close()

  schema_data = [{
      "name": "Date",
      "type": "date",
      "format": "%Y-%b-%d"
    },
    {
      "name": "User",
      "type": "string"
    },
    {
      "name": "Hours",
      "type": "number"
    }
  ]


  json_data.append(schema_data)
  keys = ["data","schema"]
  final = dict(zip(keys,json_data))
  response = app.response_class(
        response=json.dumps(final, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

@app.route("/editTimelineByActivityDelta", methods = ['POST'])
def editTimelineByActivityDelta():
  req = request.get_json()
  mydb = mysql.connector.connect(**connection_config_dict)
  courseID = req['courseID']
  activityID = req['activityID']
  distribution = req['distribution']
  hours = int(req['hours'])
  #start = datetime.datetime.strptime("2019-04-02", '%Y-%m-%d')
  #end = datetime.datetime.strptime("2019-04-22", '%Y-%m-%d')
  start = datetime.datetime.strptime(req['start'], '%Y-%m-%d')
  end = datetime.datetime.strptime(req['end'], '%Y-%m-%d')
  json_data = []
  newvalues = []
  entryitem = []

  activityjson = []
  oldactivityjson = []
  cur = mydb.cursor(buffered=True)
  cur.execute("SELECT distribution_ID FROM Distribution WHERE distribution = %s",(distribution,))
  distribution_ID = cur.fetchall()

  cur.execute("SELECT co.course_name, a.start_date, a.end_date, a.hours, a.activity_ID, a.distribution_ID FROM Activities AS a LEFT JOIN Modules as m ON (m.module_ID = a.module_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = m.module_ID) LEFT JOIN Courses as co ON (co.course_ID = %s) WHERE mc.course_ID = %s", (courseID,courseID))
  oldvalues = cur.fetchall()
  for item in oldvalues:
    if (item[4] == activityID):
      entryitem.append(item[0])
      entryitem.append(start)
      entryitem.append(end)
      entryitem.append(hours)
      entryitem.append(item[4])
      entryitem.append(distribution_ID[0][0])
      newvalues.append(entryitem)
    else:
      newvalues.append(item)

  cur.execute("SELECT co.course_name, c.class_day, c.class_semester, c.start_time, c.end_time, mc.course_ID FROM Classes AS c LEFT JOIN Modules as m ON (m.module_ID = c.module_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = m.module_ID) LEFT JOIN Courses as co ON (co.course_ID = %s) WHERE mc.course_ID = %s", (courseID,courseID))
  classes = cur.fetchall()


  cur.execute("SELECT distribution_ID, activity_name, start_date, end_date, hours FROM Activities WHERE activity_ID = %s", (activityID,))
  activity = cur.fetchall()
  for item in activity:
    if (int(item[0]) == 1):
      oldactivityjson = linearHours(item[4], item[2], item[3], item[1], oldactivityjson)
    else:
      oldactivityjson = triangleHours(item[4], item[2], item[3], item[1], oldactivityjson)

  for item in activity:
    if (int(distribution_ID[0][0]) == 1):
      activityjson = linearHours(hours, start, end, item[1], activityjson)
    else:
      activityjson = triangleHours(hours, start, end, item[1], activityjson)

  total = []
  for x in range(0, len(activityjson)):
    newhours = activityjson[x][2]
    entry = []
    try:
      oldhours = oldactivityjson[x][2]
    except IndexError:
      oldhours = 0
    difference = newhours - oldhours
    entry.append(activityjson[x][0])
    if(difference > 0):
      entry.append("Increase")
    else: entry.append("Decrease")
    entry.append(abs(difference))
    total.append(entry)

  totalsetup = timelineData(newvalues,classes) + total
  json_data.append(totalsetup)
  cur.close()
  mydb.close()

  schema_data = [{
      "name": "Date",
      "type": "date",
      "format": "%Y-%b-%d"
    },
    {
      "name": "Course",
      "type": "string"
    },
    {
      "name": "Hours",
      "type": "number"
    }
  ]

  json_data.append(schema_data)
  keys = ["total","schema"]
  final = dict(zip(keys,json_data))
  response = app.response_class(
        response=json.dumps(final, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response


@app.route("/editTimelineByActivity", methods = ['POST'])
def editTimelineByActivity():
  req = request.get_json()
  mydb = mysql.connector.connect(**connection_config_dict)
  courseID = req['courseID']
  activityID = req['activityID']
  distribution = req['distribution']
  hours = int(req['hours'])
  start = datetime.datetime.strptime(req['start'], '%Y-%m-%d')
  end = datetime.datetime.strptime(req['end'], '%Y-%m-%d')
  json_data = []
  activityjson = []

  cur = mydb.cursor(buffered=True)
  cur.execute("SELECT distribution_ID FROM Distribution WHERE distribution = %s",(distribution,))
  distribution_ID = cur.fetchall()

  cur.execute("SELECT co.course_name, a.start_date, a.end_date, a.hours, a.activity_ID, a.distribution_ID FROM Activities AS a LEFT JOIN Modules as m ON (m.module_ID = a.module_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = m.module_ID) LEFT JOIN Courses as co ON (co.course_ID = %s) WHERE mc.course_ID = %s AND a.activity_ID != %s", (courseID,courseID, activityID))
  values = cur.fetchall()

  cur.execute("SELECT co.course_name, c.class_day, c.class_semester, c.start_time, c.end_time, mc.course_ID FROM Classes AS c LEFT JOIN Modules as m ON (m.module_ID = c.module_ID) LEFT JOIN Module_Course as mc ON (mc.module_ID = m.module_ID) LEFT JOIN Courses as co ON (co.course_ID = %s) WHERE mc.course_ID = %s", (courseID,courseID))
  classes = cur.fetchall()


  cur.execute("SELECT activity_name FROM Activities WHERE activity_ID = %s", (activityID,))
  activity = cur.fetchall()
  if (int(distribution_ID[0][0]) == 1):
    activityjson = linearHours(hours, start, end, activity[0][0], activityjson)
  else:
    activityjson = triangleHours(hours, start, end, activity[0][0], activityjson)

  totalsetup = timelineData(values,classes) + activityjson
  json_data.append(totalsetup)
  cur.close()
  mydb.close()

  schema_data = [{
      "name": "Date",
      "type": "date",
      "format": "%Y-%b-%d"
    },
    {
      "name": "Course",
      "type": "string"
    },
    {
      "name": "Hours",
      "type": "number"
    }
  ]

  json_data.append(schema_data)
  keys = ["total","schema"]
  final = dict(zip(keys,json_data))
  response = app.response_class(
        response=json.dumps(final, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

@app.route("/timelineByModule<string:moduleID>")
def timelineByModule(moduleID):
  mydb = mysql.connector.connect(**connection_config_dict)
  json_data = []
  classvalues = []
  classes = []
  values = []
  cur = mydb.cursor(buffered=True)
  cur.execute("SELECT c.class_day, c.class_semester, c.start_time, c.end_time FROM Classes AS c WHERE c.module_ID = %s", (moduleID,))
  classes = cur.fetchall()

  cur.execute("SELECT a.start_date, a.end_date, a.hours, a.distribution_ID FROM Activities AS a WHERE a.module_ID = %s AND a.end_date < '2019-03-14'", (moduleID,))
  values = cur.fetchall()

  cur.execute("SELECT a.start_date, a.end_date, a.student_hours, a.distribution_ID FROM Activities AS a WHERE a.module_ID = %s AND a.end_date < '2019-03-14'", (moduleID,))
  classvalues = cur.fetchall()

  value_data = timelineStudentData('Estimated Progress',values, classes) + timelineStudentData('Course Average',classvalues, classes)
  json_data.append(value_data)

  cur.close()
  mydb.close()

  schema_data = [{
      "name": "Date",
      "type": "date",
      "format": "%Y-%b-%d"
    },
    {
      "name": "User",
      "type": "string"
    },
    {
      "name": "Hours",
      "type": "number"
    }
  ]


  json_data.append(schema_data)
  keys = ["data","schema"]
  final = dict(zip(keys,json_data))
  response = app.response_class(
        response=json.dumps(final, indent=4, cls=DateTimeEncoder),
        status=200,
        mimetype='application/json'
    )
  return response

############################################ INPUT #############################################################

@app.route("/updateStudentProgress", methods=['POST'])
def updateStudentProgress():
  req = request.get_json()
  res = make_response(jsonify({"message": "OK"}), 200)
  activityID = str(req['activityID'])
  studentID =  str(req['studentID'])
  minutes = int(req['hours'])
  hours = round_up(minutes/60)
  submitted = req['submitted']
  mydb = mysql.connector.connect(**connection_config_dict)
  try:
    cur = mydb.cursor(buffered=True)
    cur.execute("SELECT hours FROM Student_Progress WHERE activity_ID = %s AND student_ID = %s",(activityID,studentID))
    if(cur.rowcount == 0):
      cur.execute("INSERT INTO Student_Progress (student_ID, activity_ID, hours, submitted) VALUES (%s,%s,%s,%s)",(studentID, activityID, hours,submitted))
      mydb.commit()

    elif(cur.rowcount > 0):
      response = cur.fetchall()
      hours = Decimal(hours) + response[0][0]
      cur.execute("UPDATE Student_Progress SET hours = %s, submitted = %s WHERE activity_ID = %s AND student_ID = %s",(str(hours),submitted,activityID,studentID))
      mydb.commit()

    cur.execute("SELECT AVG(hours) hours FROM Student_Progress WHERE activity_ID = %s",(activityID,))
    hours = cur.fetchall()
    avg = round_up(hours[0][0])
    cur.execute("UPDATE Activities SET student_hours = %s WHERE activity_ID = %s",(str(avg),activityID,))
  except Exception: # Catch exception which will be raise in connection loss
    mydb = mysql.connector.connect(**connection_config_dict)
    cur = mydb.cursor(buffered=True)
  finally:
    mydb.commit()
    mydb.close()
  return res

@app.route("/updateFeedback", methods=['POST'])
def updateFeedback():
  req = request.get_json()
  scoreArray = req['answers']
  questionsArray = req['questions']
  mydb = mysql.connector.connect(**connection_config_dict)
  cur = mydb.cursor(buffered=True)
  i = 0

  while (i<len(questionsArray)):
    print(questionsArray[i],scoreArray[i])
    try:
      cur = mydb.cursor(buffered=True)
      cur.execute("INSERT INTO Feedback (feedback_set_ID, feedback_score) VALUES (%s,%s)",(str(questionsArray[i]), str(scoreArray[i])))
      i=i+1
    except Exception: # Catch exception which will be raise in connection loss
      mydb = mysql.connector.connect(**connection_config_dict)
      cur = mydb.cursor(buffered=True)
    finally:
      cur.close()
      mydb.commit()
  mydb.close()
  res = make_response(jsonify({"message": "OK"}), 200)
  return res

@app.route("/updateActivity", methods=['POST'])
def updateActivity():
  req = request.get_json()
  res = make_response(jsonify({"message": "OK"}), 200)

  mydb = mysql.connector.connect(**connection_config_dict)

  activityID = int(req['activityID'])
  moduleID =  str(req['moduleID'])
  start = str(req['start'])
  end = str(req['end'])
  hours = int(req['hours'])
  grade = str(req['grade'])
  activity_type = str(req['type'])
  title = str(req['title'])
  description = str(req['description'])
  grading = str(req['gradingDescription'])
  distribution = str(req['distribution'])
  if title == "0":
    title = None
  lecture = None
  if description == "0":
    description = None
  if grading == "0":
    description = None
  cur = mydb.cursor(buffered=True)
  cur.execute("SELECT activity_type_ID FROM Activity_Type WHERE activity_type = %s",(activity_type,))
  activity_type_ID = cur.fetchall()
  cur.execute("SELECT distribution_ID FROM Distribution WHERE distribution = %s",(distribution,))
  distribution_ID = cur.fetchall()
  if activityID > 0:
    cur.execute("UPDATE Activities SET activity_type_ID = %s, start_date = %s, end_date = %s, hours = %s, module_value = %s, activity_name = %s, activity_description = %s, distribution_ID = %s, grading = %s WHERE activity_ID = %s",(activity_type_ID[0][0], start, end, hours, grade, title, description, distribution_ID[0][0], grading, activityID))
  else:
    cur.execute("INSERT INTO Activities (module_ID, activity_type_ID, start_date, end_date, hours, module_value, lecture_ID, activity_name, activity_description, distribution_ID, grading) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(moduleID, activity_type_ID[0][0], start, end, hours, grade, lecture, title, description, distribution_ID[0][0], grading))
  cur.close()
  mydb.commit()
  mydb.close()
  return res

@app.route("/updateClass", methods = ['POST'])
def updateClass():
  req = request.get_json()
  res = make_response(jsonify({"message": "OK"}), 200)

  mydb = mysql.connector.connect(**connection_config_dict)

  classID = str(req['classID'])
  moduleID =  str(req['moduleID'])
  name = str(req['name'])
  description = str(req['description'])
  date = str(req['date'])
  activities = req['activities']
  lecturer = req['lecturer']
  i = 0
  if name == "0":
    name = None
  if description == "0":
    description = None

  cur = mydb.cursor(buffered=True)
  cur.execute("SELECT class_details_ID FROM Class_Details WHERE class_ID = %s AND class_date = %s", (classID, date))
  lectureinit = cur.fetchall()

  if (cur.rowcount > 0):
      cur.execute("UPDATE Activities SET lecture_ID = %s WHERE lecture_ID = %s",(None, lectureinit[0][0]))
      cur.execute("DELETE FROM Class_Details WHERE class_ID = %s AND class_date = %s", (classID, date))
  cur.execute("INSERT INTO Class_Details (class_ID, module_ID, class_date, class_name, class_description, staff_ID) VALUES (%s,%s,%s,%s,%s,%s)",(classID, moduleID, date, name, description, lecturer))
  cur.execute("SELECT class_details_ID FROM Class_Details WHERE class_ID = %s AND class_date = %s", (classID, date))
  lecture = cur.fetchall()

  while (i<len(activities)):
      cur.execute("UPDATE Activities SET lecture_ID = %s WHERE activity_ID = %s",(lecture[0][0], str(activities[i])))
      i=i+1

  mydb.commit()
  cur.close()
  mydb.close()
  return res

@app.route("/updateClassNotes", methods = ['POST'])
def updateClassNotes():
  req = request.get_json()
  res = make_response(jsonify({"message": "OK"}), 200)

  mydb = mysql.connector.connect(**connection_config_dict)
  classID = str(req['classID'])
  date = str(req['date'])
  notes =  (req['notes'])
  i = 0
  cur = mydb.cursor(buffered=True)
  cur.execute("DELETE FROM Lecture_Notes WHERE note_lecture_ID = %s AND note_lecture_date = %s", (classID, date))
  try:
    while (i<len(notes)):
      cur.execute("INSERT INTO Lecture_Notes (note_lecture_ID, note_lecture_date, note_text) VALUES (%s,%s,%s)", (classID, date, str(notes[i])))
      i=i+1
  except Exception: # Catch exception which will be raise in connection loss
    mydb = mysql.connector.connect(**connection_config_dict)
    cur = mydb.cursor(buffered=True)
  finally:
    cur.close()
    mydb.commit()
    mydb.close()
  return res

@app.route("/updateActivityNotes", methods = ['POST'])
def updateActivityNotes():
  req = request.get_json()
  res = make_response(jsonify({"message": "OK"}), 200)

  mydb = mysql.connector.connect(**connection_config_dict)
  activityID = str(req['activityID'])
  notes =  (req['notes'])
  i = 0
  cur = mydb.cursor(buffered=True)
  cur.execute("DELETE FROM Activity_Notes WHERE note_activity_ID = %s", (activityID,))
  try:
    while (i<len(notes)):
      cur.execute("INSERT INTO Activity_Notes (note_activity_ID, note_text) VALUES (%s,%s)", (activityID, str(notes[i])))
      i=i+1
  except Exception: # Catch exception which will be raise in connection loss
    mydb = mysql.connector.connect(**connection_config_dict)
    cur = mydb.cursor(buffered=True)
  finally:
    cur.close()
    mydb.commit()
    mydb.close()
  return res

@app.route("/setFeedback", methods = ['POST'])
def setFeedback():
  req = request.get_json()
  res = make_response(jsonify({"message": "OK"}), 200)
  mydb = mysql.connector.connect(**connection_config_dict)
  activityID = str(req['activityID'])
  feedback =  req['feedback']
  feedtype = str(req['type'])
  i = 0
  cur = mydb.cursor(buffered=True)
  cur.execute("DELETE FROM Feedback WHERE feedback_set_ID in (SELECT fs.feedback_set_ID FROM Feedback_Set as fs WHERE fs.feedback_activity_ID = %s AND fs.feedback_type_ID = %s)", (activityID,feedtype))
  cur.execute("DELETE FROM Feedback_Set WHERE feedback_activity_ID = %s AND feedback_type_ID = %s", (activityID,feedtype))
  mydb.commit()
  try:
    while (i<len(feedback)):
      cur.execute("INSERT INTO Feedback_Set (feedback_activity_ID, feedback_type_ID, feedback_details_ID) VALUES (%s,%s,%s)", (activityID, feedtype,str(feedback[i])))
      i=i+1
  except Exception: # Catch exception which will be raise in connection loss
    mydb = mysql.connector.connect(**connection_config_dict)
    cur = mydb.cursor(buffered=True)
  finally:
    cur.close()
    mydb.commit()
    mydb.close()
  return res

@app.route("/updateModuleNotes", methods = ['POST'])
def updateModuleNotes():
  req = request.get_json()
  res = make_response(jsonify({"message": "OK"}), 200)

  mydb = mysql.connector.connect(**connection_config_dict)
  moduleID = str(req['moduleID'])
  notes =  (req['notes'])
  i = 0
  cur = mydb.cursor(buffered=True)
  cur.execute("DELETE FROM Module_Notes WHERE note_module_ID = %s", (moduleID,))
  try:
    while (i<len(notes)):
      cur.execute("INSERT INTO Module_Notes (note_module_ID, note_text) VALUES (%s,%s)", (moduleID, str(notes[i])))
      i=i+1
  except Exception: # Catch exception which will be raise in connection loss
    mydb = mysql.connector.connect(**connection_config_dict)
    cur = mydb.cursor(buffered=True)
  finally:
    cur.close()
    mydb.commit()
    mydb.close()
  return res

@app.route("/updateCourseNotes", methods = ['POST'])
def updateCourseNotes():
  req = request.get_json()
  res = make_response(jsonify({"message": "OK"}), 200)

  mydb = mysql.connector.connect(**connection_config_dict)
  courseID = str(req['courseID'])
  notes =  (req['notes'])
  i = 0
  cur = mydb.cursor(buffered=True)
  cur.execute("DELETE FROM Course_Notes WHERE note_course_ID = %s", (courseID,))
  try:
    while (i<len(notes)):
      cur.execute("INSERT INTO Course_Notes (note_course_ID, note_text) VALUES (%s,%s)", (courseID, str(notes[i])))
      i=i+1
  except Exception: # Catch exception which will be raise in connection loss
    mydb = mysql.connector.connect(**connection_config_dict)
    cur = mydb.cursor(buffered=True)
  finally:
    cur.close()
    mydb.commit()
    mydb.close()
  return res

@app.route("/deleteActivity", methods = ['POST'])
def deleteActivity():
  req = request.get_json()
  res = make_response(jsonify({"message": "OK"}), 200)

  mydb = mysql.connector.connect(**connection_config_dict)
  activityID = str(req['activityID'])
  cur = mydb.cursor(buffered=True)
  cur.execute("DELETE FROM Activities WHERE activity_ID = %s", (activityID,))
  mydb.commit()
  cur.close()
  mydb.close()
  return res



@app.route("/")
def test():
    return render_template("test.html")

if __name__ == '__main__':
    app.run(debug=True)