import EFormDB,config.dbconfig as DB

def main():
    print("=======Environment=========")
    if DB.Server == 'VirtualSQL':
        print("It is in 'PRD' environment")
    else:
        print("It is in 'QAS' environment")

    selectFuc = ['Change Password' , 'Change Phone Number', 'Return last sign','Delete the sign','Change Sign Name']
    selectDB = ['WHQEFORM','WIHEFORM','GLOBALEFORM']
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

action = main()
print(action)

