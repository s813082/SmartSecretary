import pymssql
import config.dbconfig as Eform
import model.WHQ as model

conn = pymssql.connect(Eform.Server,Eform.Account,Eform.Password,Eform.DataBase)
cursor = conn.cursor()

Sequenceid = 'P26F0012020050056'

try:
    
    cursor.execute("select serialid , sequenceid ,formid,ApplyID,ApplyName,Status,Step ,StepName,ToBeSignedID,ToBeSignedName,UseSpecialSignForm,SpecialSignFormNameID from afs_flow  where sequenceid = '"+Sequenceid+"'")

    row = cursor.fetchone()
    print("====get record====")
    print("| serialid | sequenceid | ApplyID | Formid | ApplyName |Status | Step | StepName | ToBeSignedID | ToBeSignedName | UseSpecialSignForm | SpecialSignFormNameID |")
    
    model.SignMode.FormID = row[2]
    model.SignMode.serialid = row[0]

    cursor.execute("select serialid , sequenceid ,ApplyID,ApplyName,Status,Step ,StepName,ToBeSignedID,ToBeSignedName,UseSpecialSignForm,SpecialSignFormNameID from afs_flow_history  where sequenceid = '"+Sequenceid+"' and xUniqueid = (select max(xuniqueid) from afs_flow_history where sequenceid = '"+Sequenceid+"')")
    row_history = cursor.fetchone()
    print("====get history record====")
    print("| serialid | sequenceid | ApplyID | ApplyName |Status | Step | StepName | ToBeSignedID | ToBeSignedName | UseSpecialSignForm | SpecialSignFormNameID |")
    print(row_history)

    print(model.SignMode.FormID)
    SignForm = "afu_sign_"+model.SignMode.FormID
    print(SignForm)
    
    cursor.execute("select * from "+SignForm+" where sformserialid = '"+model.SignMode.serialid+"'")
    sign_history = cursor.fetchall()

    for i in sign_history:
        print(i)

    conn.close

except Exception as message :
    print(message)