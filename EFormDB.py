import pymssql 
import model.WHQ as whqmodel
import config.dbconfig as Eform

# 修改登入密碼
def ChangePassword(DataBase):
    emplid = input('Type emplid : ')
    print()
    conn = pymssql.connect(Eform.Server,Eform.Account,Eform.Password,DataBase)
    cursor = conn.cursor()

    try:
        cursor.execute("Select * from AFS_ACCOUNT WHERE Accountid ='"+emplid+"'")

        row = cursor.fetchone()
        # row = cursor.fetchall()
        for i in row:
            userdetail = whqmodel.account(row[2],row[4],row[7],row[3])

        if userdetail.Password != '1':
            print(userdetail.Password)
            cursor.execute("update AFS_ACCOUNT set password = '1' where Accountid = '"+userdetail.AccountID+"'")   
            conn.commit()
            print("Update "+userdetail.AccountID+" complete!")
        else:
            print("Password is already "+userdetail.Password+" not need to change")

        conn.close

    except Exception as message :
        print(message)
# 修改分機號碼
def ChangePhoneNumber(DataBase):
    # phone 2491
    NameArray = []
    Phone = input('Type Phone Number : ')

    conn = pymssql.connect(Eform.Server,Eform.Account,Eform.Password,DataBase)
    cursor = conn.cursor()

    try:
        cursor.execute("Select Accountid , Name , Deptid , Phone_A from AFC_ACCOUNT WHERE Phone_A like '%"+Phone+"%'")

        DataArray = cursor.fetchall()
        # row = cursor.fetchall()
        for row in DataArray:
            a = whqmodel.phonenumber(row[0],row[1],row[2],row[3])
            NameArray.append(row[0]+"|"+row[1])

        print(NameArray)
        if len(NameArray)==1:
            empty_emplid = input("Which emplid phone number do you want empty ? Please type Emplyee ID. ")
            cursor.execute("update AFC_Account set Phone_A = '' where Accountid = '"+empty_emplid+"'")   
            conn.commit()
        conn.close

    except Exception as message :
        print(message)
# 退回上一關卡
def ChangeSignStep(DataBase):
    conn = pymssql.connect(Eform.Server,Eform.Account,Eform.Password,DataBase)
    cursor = conn.cursor()   

    try:
        Sequenceid = input("Please Enter the Doc number : ")     

        # Chesk if exist
        cursor.execute("select Count(*) from afs_flow where sequenceid = '"+Sequenceid+"'")
        count = cursor.fetchone()

        if count[0] > 0:
            # Start Get FormID 、 Serialid
            cursor.execute("select Serialid , Formid from afs_flow where sequenceid = '"+Sequenceid+"'")
            row = cursor.fetchone()
            Serialid = row[0]
            Formid = row[1]



            cursor.execute("Select count(*) from afs_flow_history where sequenceid = '"+Sequenceid+"'")
            Canreturn = cursor.fetchone()
            if Canreturn[0] != 0:

                # Start Get Flow History
                cursor.execute("select xUniqueid,serialid , sequenceid , ApplyID , Formid , ApplyName , Status , Step , StepName , ToBeSignedID , ToBeSignedName , UseSpecialSignForm , SpecialSignFormNameID from afs_flow_history where sequenceid = '"+Sequenceid+"' and xUniqueid = (select max(xUniqueid) from afs_flow_history where sequenceid = '"+Sequenceid+"')")

                FlowHistory = cursor.fetchone()
                item = whqmodel.SignMode(FlowHistory[0],FlowHistory[1],FlowHistory[2],FlowHistory[3],FlowHistory[4],FlowHistory[5],FlowHistory[6],FlowHistory[7],FlowHistory[8],FlowHistory[9],FlowHistory[10],FlowHistory[11],FlowHistory[12])
                # update Flow

                test = "update afs_flow set Status = '"+str(item.status)+"',Step='"+item.step+"' ,StepName='"+item.StepName+"',ToBeSignedID='"+item.ToBeSignedID+"',ToBeSignedName='"+item.ToBeSignedName+"',UseSpecialSignForm='"+str(item.UseSpecialSignForm)+"',SpecialSignFormNameID='"+item.SpecialSignFormNameID+"' where sequenceid = '"+Sequenceid+"'"
                print(test)
                SignedID = str(item.ToBeSignedID).replace('<','').replace('>','')
                cursor.execute("update afs_flow set Status = '"+str(item.status)+"',Step='"+item.step+"' ,StepName='"+item.StepName+"',ToBeSignedID='"+item.ToBeSignedID+"',ToBeSignedName='"+item.ToBeSignedName+"',UseSpecialSignForm='"+str(item.UseSpecialSignForm)+"',SpecialSignFormNameID='"+item.SpecialSignFormNameID+"' where sequenceid = '"+Sequenceid+"'")
                conn.commit()
                print("Update Success")
                # Delete Flow History

                cursor.execute("delete afs_flow_history where xUniqueid = '"+str(item.xUniqueid)+"'")
                conn.commit()
                print("Delete Success")

                SignTable = 'afu_sign_'+Formid

                # Delete latest Sign History
                cursor.execute("select sIdentityID,sSignerID from "+SignTable+" where sFormSerialid = '"+Serialid+"' and sIdentityID = (Select max(sIdentityID) from "+SignTable+" where sFormSerialid = '"+Serialid+"')")
                sIdentityID = cursor.fetchone()
                if sIdentityID[0] !='0' and sIdentityID[1] == SignedID:
                    test2 = "Delete from "+SignTable+" where sIdentityID = '"+str(sIdentityID[0])+"' and sSignerID = '"+SignedID+"'"
                    print(test2)
                    cursor.execute("Delete from "+SignTable+" where sIdentityID = '"+str(sIdentityID[0])+"' and sSignerID = '"+SignedID+"'")
                    conn.commit()
                    print("Delete Success")
                else:
                    print("Error ! Cannot find this SerialID or signedID in"+SignTable)

                conn.close
            else:
                print("Afs_flow_history don't have this record")
        else:
            print("Error! Cannot find this SequenceID")

    except Exception as message :
        print(message)
# 刪除過期的˙單子
def DeleteEndList(DataBase):

    if DataBase == 'GLOBALEFORM':
        Sequenceid = input('Type Sequenceid : ')

        conn = pymssql.connect(Eform.Server,Eform.Account,Eform.Password,DataBase)
        cursor = conn.cursor()

        try:
            cursor.execute("Select Serialid from AFS_Flow_Archive WHERE sequenceid = '"+Sequenceid+"'")
            Data = cursor.fetchone()
            Serialid = Data[0]
            print('Update status AFS_Flow_Archive...')
            cursor.execute("update AFS_Flow_Archive set status = '100' , step = '@End' , stepname = '' , Tobesignedid = '', TobesignedName = '' WHERE sequenceid = '"+Sequenceid+"'")
            conn.commit()
            print('Delete AFS_Q_Mail...')
            cursor.execute("delete AFS_Q_Mail WHERE serialid = '"+Serialid+"'")
            conn.commit()

            conn.close

        except Exception as message :
            print(message)
    else:
        print("You chose wrong database")
# 將單子狀態改為Reject
def ChangeSatus():

    Sequenceid = input('Type Sequenceid : ')

    conn = pymssql.connect(Eform.Server, Eform.Account, Eform.Password, DataBase)
    cursor = conn.cursor()

    try:
        cursor.execute("Select Serialid from AFS_Flow_Archive WHERE sequenceid = '" + Sequenceid + "'")
        Data = cursor.fetchone()
        Serialid = Data[0]
        print('Update status AFS_Flow_Archive...')
        cursor.execute(
            "update AFS_Flow_Archive set status = '100' , step = '@End' , stepname = '' , Tobesignedid = '', TobesignedName = '' WHERE sequenceid = '" + Sequenceid + "'")
        conn.commit()
        print('Delete AFS_Q_Mail...')
        cursor.execute("delete AFS_Q_Mail WHERE serialid = '" + Serialid + "'")
        conn.commit()

        conn.close

    except Exception as message:
        print(message)


def ChangeSignName(DataBase):
    SequenceidList = []
    print('Please type the Sequenceid that you want to change, when you finish your type please type \'0\' to exit.')

    Sequenceid = input('Sequenceid : ')

    if Sequenceid != '0':
        SequenceidList.append(Sequenceid)
        while Sequenceid != '0':
            Sequenceid = input('Sequenceid : ')
            if Sequenceid != '0':
                SequenceidList.append(Sequenceid)

    if (Sequenceid == '0') & (len(SequenceidList) == 0):
        print('You have not type any Sequenceid, please retry again')
        return 'again'

    Emplid = input('Type Emplid which you want to assign : ')

    conn = pymssql.connect(Eform.Server, Eform.Account, Eform.Password, DataBase)
    cursor = conn.cursor()

    try:
        cursor.execute("select fullname from afs_account where accountid = '"+Emplid+"'")
        Data = cursor.fetchone()
        CN_Name = Data[0]
        print('Assign the form to '+Emplid+" : "+CN_Name)
        sql = "update afs_flow set tobesignedid = '<"+Emplid+">', tobesignedname = '"+CN_Name+"' where sequenceid = '"+Sequenceid+"'"
        print(sql)
        cursor.execute("update afs_flow set tobesignedid = '<"+Emplid+">', tobesignedname = '"+CN_Name+"' where sequenceid = '"+Sequenceid+"'")
        conn.commit()

        conn.close


    except Exception as message:
        print(message)