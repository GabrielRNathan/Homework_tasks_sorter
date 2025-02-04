from datetime import *
from tkinter import *

class Tasks:
    def __init__(self, date, task, subject, teacher, description, done): # Initialise the class with variables relevant to the homework task
        global idno
        self.__date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        self.__task = task
        self.__subject = subject
        self.__teacher = teacher
        self.__description = description
        self.__done = bool(int(done))
        self.__idno = idno
        idno += 1
        if showing == "all" or showing == "undone":
            self.__showing = True
        else:
            self.__showing = False

    def remove(self,root):#Delete the object
        global tasks, idno
        if self.daysLeft() <= -2 and self.__doneTk.get():
            self.taskLabel.destroy()
            self.subjectLabel.destroy()
            self.teacherLabel.destroy()
            self.descButton.destroy()
            self.dateLabel.destroy()
            self.cbutton.destroy()
            idno -= 1
            for i in range(self.__idno+1,idno+1):
                tasks[i].lowerIdno()
            tasks.pop(self.__idno)

    def tempRemove(self, root):#Stop showing the object
        self.__showing = False
        self.taskLabel.grid_forget()
        self.subjectLabel.grid_forget()
        self.teacherLabel.grid_forget()
        self.descButton.grid_forget()
        self.dateLabel.grid_forget()
        self.cbutton.grid_forget()

    def reGrid(self, root, x):
        self.__showing = True
        self.taskLabel.grid(column=0, row=x)
        self.subjectLabel.grid(column=1, row=x)
        self.teacherLabel.grid(column=2, row=x)
        self.descButton.grid(column=3, row=x)
        self.dateLabel.grid(column=4, row=x)
        self.cbutton.grid(column=5, row=x)

    def getDate(self): # Return the values if needed outside of the class
        return self.__date
    def getTask(self):
        return self.__task
    def getSubject(self):
        return self.__subject
    def getTeacher(self):
        return self.__teacher
    def getDescription(self):
        return self.__description
    def getDone(self):
        return self.__done
    def getIdno(self):
        return self.__idno

    def lowerIdno(self):
        self.__idno -= 1

    def daysLeft(self): # Number of days left to complete the homework
        A = datetime.now()
        difference = self.__date - A
        return difference.days+1
    def description(self):#New widget with a description of the task
        root1 = Tk()
        root1.title("Description - "+self.__task)
        label = Label(root1, text=self.__description)
        label.grid()
        root1.mainloop()

    def guiInfo(self,root,x):#Has the actual tkinter code for how to make one line
        self.__showing = True
        self.taskLabel = Label(root, text = self.getTask(), bg = self.__colour, fg=self.__colour1, width=20, bd=1, relief="solid",pady=2)
        self.taskLabel.grid(column=0, row=x)
        self.subjectLabel = Label(root, text = self.getSubject(), bg = self.__colour, fg=self.__colour1, width=12, bd=1, relief="solid",pady=2)
        self.subjectLabel.grid(column=1, row=x)
        self.teacherLabel = Label(root, text = self.getTeacher(), bg = self.__colour, fg=self.__colour1, width=15, bd=1, relief="solid",pady=2)
        self.teacherLabel.grid(column=2, row=x)
        self.descButton = Button(root, text = "description", bg = self.__colour, fg=self.__colour1, width=10, bd=0,command=lambda:self.description(),padx=0,pady=0)
        self.descButton.config(relief="solid")
        self.descButton.grid(column=3, row=x) # Allow user to click to see the decription
        self.dateLabel = Label(root, text = (str(self.getDate().strftime("%d"))+"/"+str(self.getDate().strftime("%m"))+"/"+str(self.getDate().strftime("%Y"))), bg = self.__colour, fg=self.__colour1, width=15, bd=1, relief="solid",pady=2)
        self.dateLabel.grid(column=4, row=x)
        self.cbutton = Checkbutton(root, bg = self.__colour, fg=self.__colour1, width=2, bd=1, relief="solid", command=lambda:self.remove(root), variable=self.__doneTk, onvalue=True, offvalue=False, pady=0)
        self.cbutton.grid(column=5, row=x)#Allow user to tick this box
        self.remove(root)

    def firstGui(self, root):
        self.__doneTk = BooleanVar()
        self.__doneTk.set(self.__done)

        self.__colour1="black"
        if self.daysLeft() <= 0:
            self.__colour = "black"
            self.__colour1 = "white"
        elif self.daysLeft() <= 1:
            self.__colour = "red"
        elif self.daysLeft() <= 3:
            self.__colour = "orange"
        else:
            self.__colour = "green"
        self.guiInfo(root,self.__idno+1)
        

    def doneGUI(self, root,x):#Refers each line to the correct code for different conditions for showing.
        if self.__doneTk.get():
            self.reGrid(root,x)
        else:
            self.tempRemove(root)
            
    def undoneGUI(self, root, x):
        if self.__doneTk.get():
            self.tempRemove(root)
        else:
            if not self.__showing:
                self.reGrid(root, x)

    def everyGUI(self,root, x):
        if not self.__showing:
            self.reGrid(root, x)

    def checkGUI(self, root, x):
        if self.__showing:
            self.reGrid(root, x)

def gui():
    root = Tk()
    
    menubar = Menu(root)#Create the menu for the gui
    file = Menu(menubar, tearoff=0)
    file.add_command(label="Save", command=save)
    file.add_separator()
    file.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="File", menu=file)

    menubar.add_command(label="New", command=lambda:new(root))

    order = Menu(root, tearoff=0)
    order.add_command(label="Newest",command=lambda:newest(root))
    order.add_command(label="Oldest",command=lambda:oldest(root))
    order.add_separator()
    order.add_command(label="By subjct",command=lambda:bySubject(root))
    menubar.add_cascade(label="Order", menu=order)

    show = Menu(root, tearoff=0)
    show.add_command(label="Done", command=lambda:done(root))
    show.add_command(label="Undone", command=lambda:undone(root))
    show.add_command(label="All", command=lambda:every(root))
    menubar.add_cascade(label="Show", menu=show)

    root.config(menu=menubar)
    root.configure(background="black")
    root.title("Homework") # Create the top row of the table
    label = Label(root, text = "task", bg="white", width=20, bd=1, relief="solid")
    label.grid(row=0, column=0)
    label1 = Label(root, text = "subject", bg="white", width=12, bd=1, relief="solid")
    label1.grid(row=0, column=1)
    label2 = Label(root, text = "teacher", bg="white", width=15, bd=1, relief="solid")
    label2.grid(row=0, column=2)
    label3 = Label(root, text = "description", bg="white", width=10, bd=1, relief="solid")
    label3.grid(row=0, column=3)
    label4 = Label(root, text = "date", bg="white", width=15, bd=1, relief="solid")
    label4.grid(row=0, column=4)
    label5 = Label(root, text = "done", bg="white", width=5, bd=1, relief="solid")
    label5.grid(row=0, column=5)
    for i in tasks:#Create the rows of the table.
        i.firstGui(root)
    root.mainloop()
    
##Save all the recent changes
def save():
    f = open("task.txt", "w")
    for i in tasks:
        f.write(str(i.getDate())+'\n')
        f.write(i.getTask()+'\n')
        f.write(i.getSubject()+'\n')
        f.write(i.getTeacher()+'\n')
        f.write(i.getDescription()+'\n')
        f.write(str(int(i.getDone()))+'\n')
    f.close()

##These procedures decide the order
def newest(root):
    global order
    order="new"
    dates = []
    for i in tasks:
        dates.append([i.getDate(), i.getIdno()])
    sortedDates = sorted(dates, key=lambda x: x[0], reverse=True)
    x = 0
    for sub in sortedDates:
        x += 1
        tasks[sub[1]].checkGUI(root, x)

def oldest(root):
    global order
    order = "oldest"
    dates = []
    for i in tasks:
        dates.append([i.getDate(), i.getIdno()])
    sortedDates = sorted(dates, key=lambda x: x[0], reverse=False)
    x = 0
    for sub in sortedDates:
        x += 1
        tasks[sub[1]].checkGUI(root, x)

def bySubject(root):
    global order
    order = "subject"
    subjects = []
    for i in tasks:
        subjects.append([i.getSubject(), i.getIdno(),])
    sortedSubjects = []
    for i in range(len(subjects)):
        greatest = 0
        for j in subjects:
            if subjects[greatest][0] < j[0]:
                greatest = subjects.index(j)
        sortedSubjects.append(subjects[greatest])
        subjects.pop(greatest)
    x = 0
    for sub in sortedSubjects:
        x += 1
        tasks[sub[1]].checkGUI(root, x)

## These procedures decide what is showing
def done(root):
    global showing
    showing = "done"
    x=0
    for i in tasks:
        x+=1
        i.doneGUI(root,x)

def undone(root):
    global show
    showing = "undone"
    x = 0
    for i in tasks:
        x += 1
        i.undoneGUI(root, x)

def every(root):
    global show
    showing = "all"
    x = 0
    for i in tasks:
        x += 1
        i.everyGUI(root, x)

##Create a new task
def new(root):
    def setDate():#This is to set the due date for the task
        now = datetime.now().date()
        newRoot1 = Tk()
        currentDate = StringVar()
        currentDate.set(now)
        left = Button(newRoot1, text="<", command=lambda:changeD(newRoot1, currentDate, -1, label))
        left.grid(row=0,column=0)
        label = Label(newRoot1, text=datetime.strptime(str(now), "%Y-%m-%d").strftime("%B %Y"))
        label.grid(row = 0, column=1, columnspan = 5)
        right = Button(newRoot1, text=">", command = lambda:changeD(newRoot1, currentDate, 1, label))
        right.grid(row=0,column=6)
        mon = Label(newRoot1, text="M").grid(row=1,column=0)
        tue = Label(newRoot1, text="T").grid(row=1,column=1)
        wed = Label(newRoot1, text="W").grid(row=1,column=2)
        thu = Label(newRoot1, text="T").grid(row=1,column=3)
        fri = Label(newRoot1, text="F").grid(row=1,column=4)
        sat = Label(newRoot1, text="S").grid(row=1,column=5)
        sun = Label(newRoot1, text="S").grid(row=1,column=6)
        callCalendar(newRoot1, now)

    def daysInMonth(current):
        arr = [1,3,5,7,8,10,12]
        if current.month  == 2:
            if current.year % 4 == 0:
                return 29
            else:
                return 28
        elif current.month in arr:
            return 31
        else:
            return 30


    def changeD(newRoot1, currentDate, direction, label):#To change the month
        nonlocal days
        old = datetime.strptime(currentDate.get(), "%Y-%m-%d")
        m = old.month
        y = old.year
        if m + direction == 13:
            y += 1
            m = 1
        elif m + direction == 0:
            y -= 1
            m = 12
        else:
            m += direction
        if m < 10:
            m = "0"+str(m)
        new = datetime.strptime((str(m)+" "+str(y)), "%m %Y")#Fix this
        currentDate.set(new.date())
        label.config(text=new.strftime("%B %Y"))
        for i in days:
            i.remove()
        days = []
        callCalendar(newRoot1, new)

    class calendar:#Creates the buttons for the month, to choose the correct day.
        def __init__(self, newRoot1, now, i):
            start = now.weekday()
            self.x = Button(newRoot1, text=i, command=lambda:finalDate(newRoot1, now.replace(day=i)), width=2)
            self.x.grid(row=2+(start+i-1)//7, column=(start+i-1)%7)
            
        def remove(self):
            self.x.destroy()

    def callCalendar(newRoot1, now): #Calls the calendar class the right amount of times for the month
        for i in range(1, daysInMonth(now)+1):
            days.append(calendar(newRoot1, now, i))

    def submit(newRoot, task, subject, teacher, desc):#To submit the task
        nonlocal due, root
        f = open("task.txt", "a")
        f.write(str(due)+' 00:00:00\n')
        f.write(task+'\n')
        f.write(subject+'\n')
        f.write(teacher+'\n')
        f.write(desc+'\n')
        f.write('0\n')
        f.close()
        newRoot.destroy()
        tasks.append(Tasks(str(due)+' 00:00:00', task, subject, teacher, desc, 0))
        tasks[len(tasks)-1].firstGui(root)

    def finalDate(newRoot1, now):
        nonlocal due, days
        days = []
        newRoot1.destroy()
        due = now
        button.config(text=now.strftime("%d/%m/%Y"))

    days = []
    due = ""

    newRoot = Tk()
    newRoot.title("Add Task")
    label = Label(newRoot, text="Task: ").grid(row = 0, column = 0)
    taskEntry = Entry(newRoot, width=20)
    taskEntry.grid(row = 0,column = 1)
    label = Label(newRoot, text="Subject: ").grid(row = 1, column = 0)
    subjectEntry = Entry(newRoot, width=20)
    subjectEntry.grid(row = 1,column = 1)
    label = Label(newRoot, text="Teacher: ").grid(row = 2, column = 0)
    teacherEntry = Entry(newRoot, width=20)
    teacherEntry.grid(row = 2,column = 1)
    label = Label(newRoot, text="Description: ").grid(row = 3, column = 0)
    descEntry = Entry(newRoot, width=20)
    descEntry.grid(row = 3,column = 1)
    label = Label(newRoot, text="Date: ").grid(row = 4, column = 0)
    button = Button(newRoot, text="Set date", command = setDate)
    button.grid(row = 4, column =  1)
    submit1 = Button(newRoot, text="Submit", command = lambda: submit(newRoot, taskEntry.get(), subjectEntry.get(), teacherEntry.get(), descEntry.get()))
    submit1.grid(row = 5, columnspan = 2)
    newRoot.mainloop()

idno = 0
showing = "all"
order = ""
tasks = []


f = open("task.txt","r")
lines = len(f.readlines())
f.close()
f = open("task.txt","r")
for i in range(0, lines,6):
    tasks.append(Tasks(f.readline().strip('\n'),f.readline().strip('\n'),f.readline().strip('\n'),f.readline().strip('\n'),f.readline().strip('\n'),f.readline().strip('\n')))
#tasks.append(Tasks("29/01/2025","Finish the coding", "Computing","None","Complete this!","no")) #For testing
#tasks.append(Tasks("30/01/2025","Finish the coding", "Computing","None","2nd message","no")) # For testing

gui()


