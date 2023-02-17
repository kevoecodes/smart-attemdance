from Mongo_DB.MongoDB import MongoDB
from  datetime import datetime
from bson.objectid import ObjectId
class MongoStaffsManager(MongoDB):
    def __init__(self) -> None:
        super().__init__()
        self.teacher = None
        self.assuarer = None
        self.is_created = False
        self.staff_type = None

    def isStaff(self, data):
        if 'staff_id' in data:
            staff = self.staffs_coll.find_one({"staff_id": data['staff_id']})

            if staff is not None:
                return True

            return False


    def isAssuarer(self, data, spec=False):
        assuarer = None
        if 'id' in data:
            assuarer = self.staffs_coll.find_one({"_id": ObjectId(str(data['id'])), "staff_type": "Assuarer"})

        elif 'staff_id' in data:
            assuarer = self.staffs_coll.find_one({"staff_id": data['staff_id'], 'staff_type': "Assuarer"})

        if spec:
            for key, value in data.items():
                if key != "reg_at" and key != "gender":

                    if key == "first_name" or key == "last_name":
                        by_name = self.staffs_coll.find_one({key: value})
                        if by_name is not None:
                            print(by_name)
                            if by_name['first_name'] == data['first_name'] and by_name['last_name'] == data['last_name']:
                                return True

        if assuarer is not None:
            self.assuarer = assuarer
            return True

    def isTeacher(self, data, spec=False):
        teacher = None
        if 'id' in data:
            teacher = self.staffs_coll.find_one({"_id": ObjectId(str(data['id'])), "staff_type": "Lecturer"})

        elif 'staff_id' in data:
            teacher = self.staffs_coll.find_one({"staff_id": data['staff_id'], 'staff_type': "Lecturer"})

        if spec:
            for key, value in data.items():
                if key != "reg_at" and key != "gender":

                    if key == "first_name" or key == "last_name":
                        by_name = self.staffs_coll.find_one({key: value})
                        if by_name is not None:
                            print(by_name)
                            if by_name['first_name'] == data['first_name'] and by_name['last_name'] == data['last_name']:
                                return True

        if teacher is not None:
            self.teacher = teacher
            return True
    def addTeacher(self, data):
        data['reg_at'] = datetime.now()
        data['staff_type'] = "Lecturer"

        self.staffs_coll.insert_one(data)
        return True

    def addAssuarer(self, data):
        data['reg_at'] = datetime.now()
        data['staff_type'] = "Assuarer"

        self.staffs_coll.insert_one(data)
        return True

    def getAllStaffs(self, data = None, staff = None):
        if data == None:
            teachers = self.staffs_coll.find().sort('reg_at', -1)
            res = []
            for i in teachers:
                if staff is not None:
                    print(staff)
                    if staff['staff_id'] != i['staff_id']:
                        res.append({
                            "id": i['_id'],
                            "created_at": i["reg_at"],
                            "mobileNo": i['mobileNo'],
                            "gender": i['gender'],
                            "first_name": i['first_name'],
                            "last_name": i['last_name'],
                            "staff_type": i['staff_type']
                        })
                else:
                    res.append({
                        "id": i['_id'],
                        "created_at": i["reg_at"],
                        "mobileNo": i['mobileNo'],
                        "gender": i['gender'],
                        "first_name": i['first_name'],
                        "last_name": i['last_name'],
                        "staff_type": i['staff_type']
                    })

            return res
        return None


    def getStaffData(self, data):
        staff = None
        if 'id' in data:
            staff = self.staffs_coll.find_one({"_id": ObjectId(str(data['id']))})
        if 'staff_id' in data:
            staff = self.staffs_coll.find_one({"staff_id": str(data['staff_id'])})
        if staff is not None:
            self.staff_type = staff['staff_type']
        return staff

    def editStaff(self, data):
        print(data)
        self.staffs_coll.update_one({"staff_id": data['staff_id']},{"$set": {
            "mobileNo": data['mobileNo'],
            "staff_id": data['new_staff_id'],
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "email": data['email'],
            "gender": data['gender']
        }})

        return True

    def deleteStaff(self, data):
        if 'staff_id' in data:
            self.staffs_coll.delete_one({"staff_id": data['staff_id']})
            return True

        return False


