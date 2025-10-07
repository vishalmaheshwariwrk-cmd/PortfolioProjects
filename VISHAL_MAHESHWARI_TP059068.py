#VISHAL MAHESHWARI
#TP059068

#this is the main menu where everything is combined
def main():
    menu()
    choice=int(input("Enter your selection: "))
    while choice != 6:
        if (choice==1):
            registration()
        elif (choice==2):
            testing()
        elif (choice==3):
            statistical_information()
        elif (choice==4):
            patientsRecords()
        elif (choice==5):
            deceasedPatients()
        menu()
        choice=int(input("Enter you Selection:"))

    
def menu():
    
    print("\nSelect the operation you want to perform")
    print("1. Registration")
    print("2. Testing")
    print("3. statistical_information")
    print("4. Paitent Records")
    print("5. Deceased Paitent records")
    print("6. End the program")




#All the main input required from the user
def registration():

    pName=str(input("Please enter your fullname: "))
    pDob=str(input("enter your Date of Birth in folowing order ddmmyyyy: "))
    pAge=int(input("enter your Age: "))
    pContact=str(input("if you want us to contact you through email type E if personal number type C: "))
    if pContact=="C" or pContact=="c":
        pEa=""
        pCn=str(input("enter your contact number: "))#to make sure contact is no more than 10 digits
        while len(pCn)<10:
            pCn=str(input("enter a valid contact number: "))
    elif pContact=="E" or pContact=="e":
        pCn=""
        pEa=str(input("enter your email address: "))
    pHeight=int(input("enter your Height in cm: "))
    pWeight=int(input("enter your Weight in kg: "))
    a=["Asymptomatic individuals with history of travelling overseaes(ATO):","individuals had travlled to countries with high amount of cases but no symptoms \n","Asymptomatic individuals with history of contact with known case of COVID-19(ACC):","These individuals had close contact wiith active patients but no symptoms \n","Asymptomatic individuals who had attended event associated with known COVID-19 outbreak(AEO):","These individuals had attended event associated with known COVID-19 outbreak but do not show any symptoms \n","Asymptomatic hospital staff(AHS):","Hospital staff who have not show any symptoms","\nSymptomatic individuals(SID):","Individuals who have shown COVID-19 symptoms \n"] 

    print("\nIdentify which group you are from") 
  
    print(*a, sep = "\n") 
    pType=str(input("\nRead from the following and write which category you fall into, ATO,ACC,AEO,SID,AHS: "))
    i=False
    groupCodes=["ATO","ACC","AEO","SID","AHS"]
    while (i == False):
        if (pType in groupCodes):
            i= True
        else:
            pType=str(input("choose from the following, ATO,ACC,AEO,SID,AHS: "))
    
    pZone=str(input("Select your zone from the following, East, West, North, South: "))
    staff=str(input("\nAre you a hospital staff, yes or no:"))
    
    text_file = open("assignment_trial.txt")#to save the input in the file
    pId=0
    for line in text_file:
        pId=pId+1
    pId=pId+1
    pId="P"+str(pId)
    text_file.close()
    

    text_file = open("assignment_trial.txt","a")    
    text_file.write("\n")

    text_file.write(str(pId)+","+pName+","+pDob+","+str(pAge)+","+str(pCn)+","+pEa+","+str(pHeight)+","+str(pWeight)+","+pType+","+pZone+","+staff)

    text_file.close()
    print("\nyour patient id is: ",pId)
    
            
        

def testing():
    pId=str(input("\nPlease enter the patient ID for testing to commence: "))
    staff=str(input("\nAre you a hospital staff member: "))
    text_file=open("assignment_trial.txt")
    for line in text_file:
        line=line.split(",")
        if line[0]==pId:
            pType=line[8]
            break
    text_file.close()
    
    test_1=firstTest(pType,pId,staff)
    test_2="N"
    test_3="N"
    if test_1=="N":
       test_2=secondTest(pType,pId,staff)
       if test_2=="N":
           test_3=thirdTest(pType,pId,staff)

    pStatus=status(test_1,test_2,test_3)
    
    text_file = open("assignment_testingpart.txt")#to save the input in the file
    pCaseId=0
    for line in text_file:
        pCaseId=pCaseId+1
    pCaseId=pCaseId+1
    pCaseId="C."+str(pCaseId)
    text_file.close()

    text_file = open("assignment_testingpart.txt","a")#opening of a file to store the data collected from the user
    text_file.write("\n")
    text_file.write(str(pId)+","+pType+","+pStatus+","+test_1+","+test_2+","+test_3+","+str(pCaseId))
    #storing the data in a particular order with the help of commas

    text_file.close()
    if pStatus=="ACTIVE" or pStatus=="RECOVERED" or pStatus=="DECEASED":
        print("\nyourcase Id is: ", pCaseId) #printing of the case ID once everything is executed 
           
    

def firstTest(pType,pId,staff): #testing stage 1
    print("\nFIRST TEST")
    status=str(input("\nIs the patient Positive or Negative, write P/N: "))
    if staff=="yes" and status=="P":
        action="HQFR"
        print("Home quarantine (follow up test required)")
    elif staff=="yes" and status=="N":
        action="CWFR"
        print("Continue working followup test required")
    elif staff=="no" and status=="P":
        if pType=="ATO" or pType=="ACC" or pType=="AEO" or pType=="SID":#if patient in following type assigning proper action
            action="QNHF"
            print("\nAs you are Positive you will Quarantine in hospital normal ward or ICU (NO follow-up test required)")
            print("\n***The following detail is for the staff to fill***\n")
            pCondition=str(input("is the patient in a serious condition yes or no: "))
            if pCondition=="yes":
                pWard= "ICU"
                print("patient is in",pWard,"(Intensive care unit)")
            else:
                pWard="NW"
                print("patient is in", pWard,"(Normal Ward)")
    elif staff=="no" and status=="N":
        if pType=="ATO" or pType=="ACC" or pType=="AEO":
            action="QDFR"
            print("Quarantine in designated centres (follow-Up test REQUIRED)")
        elif pType=="SID":
            action="HQFR"
            print("you will go under home quarentine with follow up test required")
    return status
        

def secondTest(pType,pId,staff):
    print("\nSECOND TEST")
    status=str(input("\nIs the patient Positive or Negative, write P/N: "))
    if staff=="yes" and status=="P":
        action="HQNF"
        print("You will go under home quarantine with no follow up required")
    elif staff=="yes" and status=="N":
        action="CWFR"
        print("Continue working followup test required.")
    elif staff=="no" and status=="P":
        if pType=="ATO" or pType=="ACC" or pType=="AEO" or pType=="SID":#if patient in following type assigning proper action
            action="QNHF"
            print("As you are Positive you will Quarantine in hospital normal ward or ICU (NO follow-up test required)")
            print("\n***The following detail is for the staff to fill***\n")
            pCondition=str(input("is the patient in a serious condition yes or no: "))
            if pCondition=="yes":
                pWard= "ICU"
                print("patient is in",pWard,"(Intensive care unit)")
            else:
                pWard="NW"
                print("patient is in", pWard,"(Normal Ward)")
    elif staff=="no" and status=="N":
        if pType=="ATO" or pType=="ACC" or pType=="AEO":
            action="QDFR"
            print("Quarantine in designated centres (follow-Up test REQUIRED)")
        elif pType=="SID":
            action="HQFR"
            print("you will go under home quarentine with follow up test required")
    return status
    
def thirdTest(pType,pId,staff):
    print("\nTHIRD TEST")
    status=str(input("\nIs the patient Positive or Negative, write P/N: "))
    if staff=="yes" and status=="P":
        action="HQNF"
        print("You will go under home quarantine with no follow up required")
    elif staff=="yes" and status=="N":
        action="CWFR"
        print("you will go under home quarantine with follow up test required")
    elif staff=="no" and status=="P":
        if pType=="ATO" or pType=="ACC" or pType=="AEO" or pType=="SID":#if patient in following type assigning proper action
            action="QNHF"
            print("As you are Positive you will Quarantine in hospital normal ward or ICU (NO follow-up test required)")
            print("***The following detail is for the staff to fill***")
            pCondition=str(input("is the patient in a serious condition yes or no: "))
            if pCondition=="yes":
                pWard= "ICU"
                print("patient is in",pWard,"(Intensive care unit)")
            else:
                pWard="NW"
                print("patient is in", pWard,"(Normal Ward)")
    elif staff=="no" and status=="N":
        if pType=="ATO" or pType=="ACC" or pType=="AEO" or pType=="SID":
            action="RU"
            print("You can go back home")
    return status



def status(t1,t2,t3):
    if t1=="P" or t2=="P" or t3=="P":
        pStatus="ACTIVE"
    print("\nTHIS IS FOR THE STAFF TO ENTER \n")
    pStatus=str(input("Is the Patient ACTIVE or RECOVERED or DECEASED: "))

    return pStatus
    
        

    
def statistical_information():

    fname = "assignment_testingpart.txt"
    count = 0
    with open(fname, 'r') as f:
        for line in f:
            count += 1
    print("\n""Total number of cases are:", count)

    fname = "assignment_testingpart.txt"
    count = 0
    with open(fname, 'r') as f:
        for line in f:
            count += 1
    print("\n""Total number of Test 1's are:", count)

    text_file=open("assignment_testingpart.txt")
    count=0
    for line in text_file:
        line = line.split(",") 
        if line[3]=="N":
            count= count + 1
    print("Total Number of Test 2's are: ",count)

    text_file=open("assignment_testingpart.txt")
    count=0
    for line in text_file:
        line = line.split(",") 
        if line[3]=="N" and line[4]=="N":
            count= count + 1
    print("Total Number of Test 3's are: ",count)
 
    


    text_file=open("assignment_testingpart.txt")
    count=0
    for line in text_file:
        line = line.rstrip()
        if "ACTIVE" in line:
            count= count + 1
    print("\nNumber of Active cases are: ",count)

    text_file.close()

    text_file=open("assignment_testingpart.txt")
    count=0
    for line in text_file:
        line = line.rstrip()
        if "RECOVERED" in line:
            count= count + 1
    print("Number of Recovered cases are: ",count)

    text_file=open("assignment_testingpart.txt")
    count=0
    for line in text_file:
        line = line.rstrip()
        if "DECEASED" in line:
            count= count + 1
    print("Number of Deceased cases are: ",count, "\n")

    text_file.close()

    text_file=open("assignment_trial.txt")
    count=0
    for line in text_file:
        line = line.rstrip()
        if "East" in line:
            count= count + 1
    print("Number of cases from zone A- East are: ",count)

    text_file=open("assignment_trial.txt")
    count=0
    for line in text_file:
        line = line.rstrip()
        if "West" in line:
            count= count + 1
    print("Number of cases from zone B-West are: ",count)

    text_file.close()
    
    text_file=open("assignment_trial.txt")
    count=0
    for line in text_file:
        line = line.rstrip()
        if "North" in line:
            count= count + 1
    print("Number of cases from zone C-South are: ",count)

    text_file.close()

    text_file=open("assignment_trial.txt")
    count=0
    for line in text_file:
        line = line.rstrip()
        if "South" in line:
            count= count + 1
    print("Number of cases from zone D-South are: ",count, "\n")

    text_file.close()

    text_file=open("assignment_testingpart.txt")
    count=0
    for line in text_file:
        line = line.rstrip()
        if "ACC,ACTIVE" in line:
            count= count + 1
    print("Number of Active cases in group ACC are: ",count)

    text_file.close()

    text_file=open("assignment_testingpart.txt")
    count=0
    for line in text_file:
        line = line.rstrip()
        if "ATO,ACTIVE" in line:
            count= count + 1
    print("Number of Active cases in group ATO are: ",count)

    text_file.close()

    text_file=open("assignment_testingpart.txt")
    count=0
    for line in text_file:
        line = line.rstrip()
        if "AEO,ACTIVE" in line:
            count= count + 1
    print("Number of Active cases in group AEO are: ",count)

    text_file.close()

    text_file=open("assignment_testingpart.txt")
    count=0
    for line in text_file:
        line = line.rstrip()
        if "SID,ACTIVE" in line:
            count= count + 1
    print("Number of Active cases in group SID are: ",count)

    text_file.close()

    text_file=open("assignment_testingpart.txt")
    count=0
    for line in text_file:
        line = line.rstrip()
        if "AHS,ACTIVE" in line:
            count= count + 1
    print("Number of Active cases in group AHS are: ",count)

    text_file.close()



def patientsRecords():
    text_file=open("assignment_testingpart.txt")
    file=open("assignment_trial.txt")
    user_input=str(input("Enter the Patient Id(P(patient number)) or Case Id(C.(case number)): "))
    for line in text_file:
        line=line.rstrip()
        
        if user_input in line:
            x=line.split(",")
            pId=x[0]
            pName=""
            for line in file:
                i=line.split(",")
                if pId==i[0]:
                    pName=i[1]
            print("Patient ID: ",x[0], "\nPatient Name: ",pName,"\nGroup Code: ", x[1],"\nStatus: ",x[2],"\nResult in Test 1: ",x[3],"\nResult in Test 2: ",x[4],"\nResult in Test 3: ",x[5],"\nCase ID: ",x[6])
            break       
    file.close()
    text_file.close()
    


def deceasedPatients():
    text_file=open("assignment_testingpart.txt")
    file=open("assignment_trial.txt")
    for line in text_file:
        line=line.rstrip()
        
        if "DECEASED" in line:
            x=line.split(",")
            pId=x[0]
            pName=""
        
            for line in file:
                i=line.split(",")
                if pId==i[0]:
                    pName=i[1]
                    break
            print("Patient ID: ",x[0], "\nPatient Name: ",pName, "\nGroup Code: ", x[1],"\nStatus: ",x[2],"\nResult in Test 1: ",x[3],"\nResult in Test 2: ",x[4],"\nResult in Test 3: ",x[5],"\nCase ID: ",x[6],"\n")
            
    file.close()
    text_file.close()

#calling the main menu function    
main()

