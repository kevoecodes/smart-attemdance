from datetime import datetime
from Mongo_DB.MongoDB import MongoDB
from bson.objectid import ObjectId

class MongoStudentsManager(MongoDB):
    def __init__(self):
        super().__init__()
        self.student_id = None
        self.student = None

    def isStudent(self, data):
        print(data)
        if 'id' in data:
            student = self.students_coll.find_one({'_id': ObjectId(str(data['id']))})
            if student is not None:
                self.student = student
                return True
            return False
        for key, value in data.items():
            if key != "reg_at" and key != "gender":

                if key == "first_name" or key == "last_name":
                    by_name = self.students_coll.find_one({key: value})
                    if by_name is not None:
                        print(by_name)
                        if by_name['first_name'] == data['first_name'] and by_name['last_name'] == data['last_name']:
                            return True

                else:
                    print(key, value)
                    student = self.students_coll.find_one({key: f"{value}"})
                    

                    if student is not None:
                        return True

                
        return False

    def registerStudent(self, data):
        try:
            stud_data = {}
            stud_data['first_name'] = data['first_name']
            stud_data['last_name'] = data['last_name']
            stud_data['email'] = data['email']
            stud_data['mobileNo'] = data['mobileNo']
            stud_data['regNo'] = data['regNo']
            stud_data['gender'] = data['gender']
            stud_data['gender'] = data['gender']
            stud_data['reg_at'] = datetime.now()
            stud_data['fprint_id'] = None

            self.student_id = self.students_coll.insert_one(stud_data).inserted_id
            return True
        
        except: return False

    def registerFingerprint(self, data):
        try:
            self.students_coll.update_one({"regNo": data["regNo"]}, {"$set": {"fprint_id": data['fprint_id']}})
            return True
        
        except: return False

    def getAllStudents(self, data = None):
        if data == None:
            res = self.students_coll.find()
        
        else:
            res = self.students_coll.find({"regNo": data['regNo']})
        students = []
        for i in res:
            students.append({
                "id": i['_id'],
                "first_name": i['first_name'],
                'last_name': i['last_name'],
                'regNo': i['regNo'],
                'gender': i['gender']
            })

        return students

    def getStudentData(self, data):
        student = None
        if 'id' in data:
            student = self.students_coll.find_one({"_id": ObjectId(str(data['id']))})
        if 'regNo' in data:
            student = self.students_coll.find_one({"regNo": str(data['regNo'])})
        if 'fprint_id' in data:
            student = self.students_coll.find_one({"fprint_id": str(data['fprint_id'])})
        return student

    def editStudent(self, data):
        self.students_coll.update_one({"regNo": data['regNo']},{"$set": {
            "mobileNo": data['mobileNo'],
            "regNo": data['new_regNo'],
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "email": data['email'],
            "gender": data['gender']
        }})

        return True
    
    def deleteStudent(self, data):
        self.students_coll.delete_one({"regNo": data['regNo']})
        return True



