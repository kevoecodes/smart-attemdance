from datetime import datetime, timedelta, timezone

from bson.objectid import ObjectId
from Mongo_DB.MongoDB import MongoDB

class MongoModulesManager(MongoDB):
    def __init__(self):
        super().__init__()

    def isModule(self, data):
        if "module_code" in data:
            mod = self.modules_coll.find_one({"module_code": data['module_code']})
        if "module_name" in data:
            by_module_name = self.modules_coll.find_one({"module_name": data['module_name']})

        if mod is not None or by_module_name is not None:
            return True

        return False

    def registerModule(self, data):
        mod_data = {}
        mod_data['module_code'] = data['module_code']
        mod_data['module_name'] = data['module_name']
        mod_data['lecturer_id'] = data['staff_id']
        mod_data['course_type'] = data['course_type']
        if 'staff_id_2' in data:
            mod_data['lecturer_id_2'] = data['staff_id_2']

        mod_data['created_at'] = datetime.now(timezone(timedelta(hours=3)))
        timetable = []
        if 'mon' in data and data['mon'] == 'on':
            timetable.append(
                {
                    "day": "Monday",
                    "day_no": 1,
                    "module_code": data['module_code'],
                    "from": int(data['mon_from']),
                    "to": int(data['mon_to'])
                }
            )
        if 'tue' in data and data['tue'] == 'on':
            timetable.append(
                {
                    "day": "Tuesday",
                    "day_no": 2,
                    "module_code": data['module_code'],
                    "from": int(data['tue_from']),
                    "to": int(data['tue_to'])
                }
            )

        if 'wed' in data and data['wed'] == 'on':
            timetable.append(
                {
                    "day": "Wednesday",
                    "day_no": 3,
                    "module_code": data['module_code'],
                    "from": int(data['wed_from']),
                    "to": int(data['wed_to'])
                }
            )

        if 'thu' in data and data['thu'] == 'on':
            timetable.append(
                {
                    "day": "Thursday",
                    "day_no": 4,
                    "module_code": data['module_code'],
                    "from": int(data['thu_from']),
                    "to": int(data['thu_to'])
                }
            )
        if 'fri' in data and data['fri'] == 'on':
            timetable.append(
                {
                    "day": "Friday",
                    "day_no": 5,
                    "module_code": data['module_code'],
                    "from": int(data['fri_from']),
                    "to": int(data['fri_to'])
                }
            )
        self.timetable_coll.insert_many(timetable)
        self.modules_coll.insert_one(mod_data)

        return True

    def studentModules(self, data):
        modules = self.modules_coll.find()
        feed = []
        for module in modules:
            res = {}
            att = self.attendence_coll.find({"regNo": data['regNo'], 'module_code': module['module_code']})
            res['module_name'] = module['module_name']
            res['module_code'] = module['module_code']
            res['attended'] = 0
            res['late'] = 0
            for x in att:
                res['attended'] = res['attended'] + 1
                if 'status' in x and x['status'] == "Late":
                    res['late'] = res['late'] + 1

            feed.append(res)

        return feed

    def getAllModules(self, data=None):
        modules = [] 
        if data == None:
            queries = self.modules_coll.find()
            for i in queries:
                modules.append({
                    'id': i['_id'],
                    "module_name": i['module_name'],
                    "module_code": i['module_code'],
                    'id': i['_id']
                })
        if data is not None:
            if 'staff_id' in data:
                queries = self.modules_coll.find({"$or": [{"lecturer_id": data['staff_id']}, {"lecturer_id_2": data['staff_id']}]})
                
                for i in queries:
                    modules.append({
                        'id': i['_id'],
                        "module_name": i['module_name'],
                        "module_code": i['module_code'],
                        'id': i['_id']
                    })

        
        return modules

    def getModule(self, data):
        if 'module_code' in data:
            modules = self.modules_coll.find_one({"module_code": data['module_code']})
        elif 'id' in data:
            modules = self.modules_coll.find_one({"_id": ObjectId(str(data['id']))})

        return modules

    def moduleTimetable(self, data):
        #Querying the timetable with module code
        pass

    def currentModule(self):
        #Getting the current timetable
        pass

    def deleteModule(self, data):
        self.modules_coll.delete_one({"module_code": data['module_code']})
    
    def editModuleView(self, data):
        id = None
        if 'id' in data:
            module_data = self.modules_coll.find_one({"_id": ObjectId(str(data['id']))})
            id = data['id']
        if 'module_code' in data:
            
            module_data = self.modules_coll.find_one({"module_code": data['module_code']})
        timetable = {}
        the_timetable = self.timetable_coll.find({"module_code": module_data['module_code']})
        days = ['mon', 'tue', 'wed', 'thu', 'fri']
        
        for x in the_timetable:
            v = {}
            if x['from'] < 1000:
                if x['from'] < 100:
                    x['from'] = f"00{x['from']}"
                elif x['from'] < 1000:
                    x['from'] = f"0{x['from']}"
            if x['to'] < 1000:
                if x['to'] < 100:
                    x['to'] = f"00{x['to']}"
                elif x['to'] < 1000:
                    x['to'] = f"0{x['to']}"
            
            v[f"{days[x['day_no']-1]}_from"] = x['from']
            v[f"{days[x['day_no']-1]}_to"] = x['to']
            v[days[x['day_no']-1]] = 'on'
            timetable.update(v)

        return {"edit_mode": True, "id": id, "timetable": timetable, "data": module_data}


    def editModule(self, data):
        module = self.modules_coll.find_one({"module_code": data['module_code']})

        if module is not None:
            self.modules_coll.update_one({"module_code": data['module_code']}, {"$set": {
                "module_code": data['new_module_code'],
                "module_name": data['new_module_name'],
                'lecturer_id': data['staff_id'],
                'lecturer_id_2': data['staff_id_2'],
                'course_type': data['course_type']
            }})
            timetable = []
            long_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            days = ['mon', 'tue', 'wed', 'thu', 'fri']
            rem_days = [False, False, False, False, False]
            for x in range(0, 5):
                is_on_timetable = self.timetable_coll.find_one({"module_code": data['module_code'], 'day_no': (x+1)})
                if days[x] in data and data[days[x]] == 'on' and is_on_timetable is not None:
                    self.timetable_coll.update_one({"module_code": data['module_code'], "day_no": (x+1)},
                        {"$set":
                            {
                                "day_no": x + 1,
                                "module_code": data['new_module_code'],
                                "from": int(data[f"{days[x]}_from"]),
                                "to": int(data[f"{days[x]}_to"])
                            }
                        }
                    )
                    rem_days[x] = True

                
                elif days[x] in data and data[days[x]] == 'on' and is_on_timetable is None:
                    timetable = {    
                        "day": long_day[x],              
                        "day_no": x + 1,
                        "module_code": data['new_module_code'],
                        "from": int(data[f"{days[x]}_from"]),
                        "to": int(data[f"{days[x]}_to"])
                    }
                    self.timetable_coll.insert_one(timetable)
                    rem_days[x] = True
                    

            print('The days', rem_days)
            for x in range(0, 5):
                is_on_timetable = self.timetable_coll.find_one({"module_code": data['module_code'], 'day_no': (x+1)})
                print(rem_days[x])
                if days[x] not in data and rem_days[x] == False and is_on_timetable is not None:
                    self.timetable_coll.delete_one({"module_code": data['module_code'], "day_no": (x+1)})

            return True
