


class account():
    def __init__(self,AccountID,Name,Deptid,Password):
        self.AccountID = AccountID
        self.Name = Name
        self.Deptid = Deptid
        self.Password = Password

class phonenumber():
    def __init__(self,AccountID, Name , Deptid , Phone_A):
        self.AccountID = AccountID
        self.Name = Name
        self.Deptid = Deptid
        self.Phone_A = Phone_A



class SignMode():
    def __init__(self,xUniqueid,serialid , sequenceid , ApplyID , Formid , ApplyName , Status , Step , StepName , ToBeSignedID , ToBeSignedName , UseSpecialSignForm , SpecialSignFormNameID):
        self.xUniqueid = xUniqueid
        self.serialid = serialid
        self.sequenceid = sequenceid
        self.ApplyID = ApplyID
        self.FormID = Formid
        self.ApplyName = ApplyName
        self.status = Status
        self.step = Step
        self.StepName = StepName
        self.ToBeSignedID = ToBeSignedID
        self.ToBeSignedName = ToBeSignedName
        self.UseSpecialSignForm = UseSpecialSignForm
        self.SpecialSignFormNameID = SpecialSignFormNameID

