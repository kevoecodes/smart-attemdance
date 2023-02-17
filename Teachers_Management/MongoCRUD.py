from datetime import datetime
from Mongo_DB.MongoDB import MongoDB
from bson.objectid import ObjectId

class MongoTeachersManager(MongoDB):
    def __init__(self) -> None:
        super().__init__()
        self.teacher = None
    def isTeacher(self, data, spec=False):
        if 'id' in data:
            teacher = self.teachers_coll.find_one({"_id": ObjectId(str(data['id']))})

        elif 'lecturer_id' in data:
            teacher = self.teachers_coll.find_one({"lecturer_id": data['lecturer_id']})

        if spec:
            for key, value in data.items():
                if key != "reg_at" and key != "gender":

                    if key == "first_name" or key == "last_name":
                        by_name = self.teachers_coll.find_one({key: value})
                        if by_name is not None:
                            print(by_name)
                            if by_name['first_name'] == data['first_name'] and by_name['last_name'] == data['last_name']:
                                return True

        if teacher is not None:
            self.teacher = teacher
            return True
    def addTeacher(self, data):
        data['reg_at'] = datetime.now()

        self.teachers_coll.insert_one(data)
        return True

    def getAllTeachers(self, data = None):
        if data == None:
            teachers = self.teachers_coll.find()
            res = []
            for i in teachers:
                res.append({
                    "id": i['_id'],
                    "created_at": i["reg_at"],
                    "mobileNo": i['mobileNo'],
                    "gender": i['gender'],
                    "first_name": i['first_name'],
                    "last_name": i['last_name'],
                })
            return res

        """  students = self.students_coll.find({"regNo": data['regNo']})
        return students """

    def getTeacherData(self, data):
        student = None
        if 'id' in data:
            student = self.teachers_coll.find_one({"_id": ObjectId(str(data['id']))})
        if 'lecturer_id' in data:
            student = self.teachers_coll.find_one({"lecturer_id": str(data['lecturer_id'])})
        return student

    def editTeacher(self, data):
        self.students_coll.update_one({"regNo": data['regNo']},{"$set": {
            "mobileNo": data['new_mobileNo'],
            "regNo": data['new_regNo'],
            "first_name": data['new_first_name'],
            "last_name": data['new_last_name'],
            "email": data['new_email'],
            "gender": data['new_gender']
        }})
