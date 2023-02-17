from pymongo import MongoClient

class MongoDB:
    def __init__(self) -> None:
        self.client = MongoClient('mongodb://127.0.0.1:27017/')
        self.db = 'smart_attendance'
        #self.class_db = 'CLASS_DB'
        self.students_coll = self.client[self.db]['Students']
        self.teachers_coll = self.client[self.db]['Teachers']
        self.assuarers_coll = self.client[self.db]['Assuarers']
        self.attendence_coll = self.client[self.db]['Attendance']
        self.modules_coll = self.client[self.db]['Modules']
        self.timetable_coll = self.client[self.db]['Timetable']
        self.random_coll = self.client[self.db]['Randoms']
        self.staffs_coll = self.client[self.db]['Staffs']

        #self.messages_coll = self.client[db]['Messages']

        self.votes_coll = self.client[self.db]['Votes']
        self.students_collection = self.client["NIDA_B_DB"]['LOC']