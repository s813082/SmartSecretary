import EFormDB,config.dbconfig as DB

def main():
    print("=======Environment=========")
    if DB.Server == 'VirtualSQL':
        print("You are in 'PRD' environment")
    else:
        print("You are in 'QAS' environment")

    selectFuc = ['Change Password 修改登入密碼' , 'Change Phone Number 修改分機號碼', 'Return last sign 退回上一關卡','Delete the sign 刪除過期的單子','Change Sign Name','DeleteDNForm 刪除DN單子','CheckDeptExit 確認部門存在否']
    selectDB = ['WHQEFORM','WIHEFORM','GLOBALEFORM','myForm']
    rowFuc = 0
    rowDB = 0


    # Select DataBase
    print("========DataBase===========")
    for j in selectDB:
        rowDB = rowDB+1
        print(rowDB," : "+j)
    print("========Function===========")
    # Select Function
    for i in selectFuc:
        rowFuc = rowFuc + 1
        print(rowFuc," : "+i)
    print("===========================")

    a = input("Chose DataBase : ")
    b = input("Chose Change function : ")
    FucDB = selectDB[int(a)-1]

    print("You choose '"+FucDB +"' to run " +selectFuc[int(b)-1]+" function")
    print("===========================")
    if b == '1':
        EFormDB.ChangePassword(FucDB)
    if b == '2':
        EFormDB.ChangePhoneNumber(FucDB)
    if b == '3':
        EFormDB.ChangeSignStep(FucDB)
    #     test sequenceid ='P26F0012020070058'
    if b == '4':
        EFormDB.DeleteEndList(FucDB)
    if b == '5':
        return EFormDB.ChangeSignName(FucDB)
    if b == '6':
        return EFormDB.DeleteDNForm(FucDB)
    if b == '7':
        return EFormDB.CheckDeptExit(FucDB)

action = main()
print(action)

