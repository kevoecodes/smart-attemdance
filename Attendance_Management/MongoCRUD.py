from datetime import datetime, timezone, timedelta
from bson import json_util
import json
from Modules_Management.MongoCRUD import MongoModulesManager
from Mongo_DB.MongoDB import MongoDB
from Channels_Management.ChannelsManager import PostToAttendanceChannel
from Timetable_Management.MongoCRUD import MongoTImetableManager
import calendar

class AttendanceManager(MongoDB):
    def __init__(self):
        super().__init__()

    def attendClass(self, data):
        current_class = MongoTImetableManager().getCurrentClass()
        print(current_class)
        stud_data = {}
        at = datetime.now(timezone(timedelta(hours=3)))
        stud_data['regNo'] = data['regNo']
        stud_data['full_name'] = f"{data['first_name']} {data['last_name']}"
        stud_data['att_time'] = at
        stud_data['att_date'] = datetime.now(timezone(timedelta(hours=3))).day
        stud_data['att_month'] = datetime.now(timezone(timedelta(hours=3))).month
        stud_data['module_code'] = current_class['module_code']
        stud_data['module_name'] = current_class['module_name']
        print(self.hasAttended(data, current_class['module_code']))
        if not self.hasAttended(data, current_class['module_code']):
            hour = datetime.now(timezone(timedelta(hours=3))).hour
            mins = datetime.now(timezone(timedelta(hours=3))).minute
            if int(mins) < 10:
                mins = f"0{mins}"
            
            #print(hour, mins)
            now = int(f"{hour}{mins}")
            ontime = int(current_class['from']) + 2
            stud_data['status'] = "Ontime"
            if int(now) > ontime:
                stud_data['status'] = "Late"
            stud_data['att_at'] = at
            print(stud_data)
            PostToAttendanceChannel(stud_data)
            self.attendence_coll.insert_one(stud_data)

            return True
        
        return False
    
    def hasAttended(self, data, module_code):
        att_data = None
        print(data)
        if 'regNo'in data:
            att_data = self.attendence_coll.find_one({
                "att_date": datetime.now(timezone(timedelta(hours=3))).day,
                "regNo": data['regNo'],
                'module_code': module_code
            })
            print(att_data)
        print(att_data)

        if att_data is not None:
            return True

        return False

    def getAttRange(self, data):
        now = datetime.now()
        """  att_data = self.attendence_coll.find({
            "att_date": data['att_date'],
            "att_month": data['att_month']
        }) """
        current_class = MongoTImetableManager().getCurrentClass()
        att_data = []
        if current_class is not None:
            att_data = self.attendence_coll.find({
                "att_date": now.day,
                "att_month": now.month,
                "module_code": current_class['module_code']
            })
        return att_data

    def getAtt(self, module_code):
        attendance_data = json.loads(json_util.dumps(self.attendence_coll.find({
            "att_month": datetime.now(timezone(timedelta(hours=3))).month,
            'module_code': module_code
        })))
        stud_data = json.loads(json_util.dumps(self.students_coll.find()))
        print(len(stud_data))
        the_attendance = []
        for student in stud_data:
            the_att = {}
            the_att['full_name'] = student['first_name'] + ' ' + student['last_name']
            the_att['regNo'] = student['regNo']
            cols = []
            for attendance in attendance_data:
                print(attendance['regNo'] == student['regNo'])
                if attendance['regNo'] == student['regNo']:
                    cols.append(attendance['att_date'])
            the_att['cols'] = cols

            the_attendance.append(the_att)
        return the_attendance
    
    def getStudentAtt(self, data):
        if "module_code" in data:
            attendance_data = json.loads(json_util.dumps(self.attendence_coll.find({
                "att_month": datetime.now(timezone(timedelta(hours=3))).month,
                'module_code': data['module_code'],
                'regNo': data['regNo']
            })))

        else:
            attendance_data = []
            attendance_data = self.attendence_coll.find({
                "att_month": datetime.now(timezone(timedelta(hours=3))).month,
                'regNo': data['regNo']
            })
            


        return attendance_data

    def studentWeekAttendance(self, data):
        modules = self.modules_coll.find()
        the_month = calendar.monthcalendar(2022, 5)
        print(the_month)
        the_week = []
        today = datetime.now(timezone(timedelta(hours=3))).day
        attendance = []
        shit = []
    
        timetable = self.timetable_coll.find({"module_code": data['module_code']})
        for v in the_month:
            #print(today in v)
            if today in v:
                the_week = v
                print(the_week)
                for class_ in timetable:
                    
                    print(class_)
                    print(the_week[class_['day_no'] - 1])
                    att = self.attendence_coll.find_one({
                        "att_month": datetime.now(timezone(timedelta(hours=3))).month,
                        "att_date": the_week[class_['day_no'] - 1],
                        'module_code': class_['module_code'],
                        'regNo': data['regNo']
                    })
                    res = {}
                    res['date'] = f"5/{the_week[class_['day_no']-1]}/2022"
                    res['day'] = class_['day']
                    res['attended'] = None
                    res['late'] = None
                    res['x'] = class_['day_no']
                    
                    if att is not None:
                        print('The Att', att)
                        res['attended'] = True
                        res['late'] = False
                        if att['status'] == 'Late':
                            res['late'] = True
                    #print(today > the_week[class_['day_no'] - 1], today, the_week[class_['day_no'] - 1])
                    if att is None and today > the_week[class_['day_no'] - 1]:
                        res['attended'] = False
                        res['late'] = False

                    shit.append(res)
                    #attendance.append(res)

        for x in range(0, 7):
            for v in shit:
                print(v)
                if v['x'] == x:
                    attendance.append(v)
        for c in attendance:
            del c['x']                  
        return attendance

            


