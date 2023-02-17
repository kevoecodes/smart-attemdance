from datetime import datetime, timezone, timedelta
from Mongo_DB.MongoDB import MongoDB

class MongoTImetableManager(MongoDB):
    def __init__(self):
        super().__init__()

    def getCurrentClass(self):
        day = datetime.now(timezone(timedelta(hours=3))).isoweekday()
        hour = datetime.now(timezone(timedelta(hours=3))).hour
        mins = datetime.now(timezone(timedelta(hours=3))).minute
        if int(mins) < 10:
            mins = f"0{mins}"
            
        #print(hour, mins)
        now = int(f"{hour}{mins}")
        print(now)
        timetable = self.timetable_coll.find({
            "day_no": day
        })
        
        for mod in timetable:
            from_ = int(mod['from'])
            #print(from_)
            to = int(mod['to'])
            #print(to)
            if now in range(from_, to):
                module = {}
                module.update(self.modules_coll.find_one({"module_code": mod['module_code']}))
                module.update(mod)

                return module

        return None


    def constructTimeTable(self):
        pass