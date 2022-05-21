from tkinter import *
import pyautogui
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import numpy as np
from tkinter import messagebox
import mysql.connector
import datetime
import os
from datetime import datetime as dt


class Application:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1920x1080+0+0")

        self.mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Yash",
            database="pblmoneytracker"
        )
        self.mycursor = self.mydb.cursor()

        self.MainOperatingFrame = Frame()
        self.AddButton = Button(self.root, text="Add Money", font="ariel 22 bold", relief=RIDGE, bd=7,
                                command=self.AddMoneyButton_Pressed)
        self.WithdrawButton = Button(self.root, text="Add Expense", font="ariel 22 bold", relief=RIDGE, bd=7,
                                     command=self.WithdrawButton_Pressed)
        self.InvestButton = Button(self.root, text="Investments", font="ariel 22 bold", relief=RIDGE, bd=7,
                                   command=self.InvestButton_Pressed)

        self.AddButton.place(x=280, y=150, width=400, height=70)
        self.WithdrawButton.place(x=280, y=280, width=400, height=70)
        self.InvestButton.place(x=280, y=410, width=400, height=70)

        # ------------------------------------------------------------------
        self.PiChartFrame = Frame(self.root, relief=RIDGE, bd=3)
        self.PiChartFrame.place(x=1000, y=100, width=700, height=500)

        self.Days7Button = Button(self.PiChartFrame, text="Last 7 Days", font="ariel 15 bold", relief=RIDGE, bd=3,
                                  bg="yellow", command=self.Days7Button_Pressed)
        # Note 30Days is changed to Lifetime
        self.Days30Button = Button(self.PiChartFrame, text="Lifetime", font="ariel 15 bold", relief=RIDGE, bd=3,
                                   command=self.Days30Button_Pressed)

        self.Days7Button.place(x=20, y=430, width=200, height=50)
        self.Days30Button.place(x=470, y=430, width=200, height=50)

        self.piChart = Frame(self.PiChartFrame, bd=5, relief=RIDGE)
        self.piChart.place(x=125, y=50, width=450, height=350)

        with open("7days.txt") as f:
            f = f.read()

        spendings = 0
        savings = 0
        invested = 0
        l = []
        f = f.split("\n")
        for i in f:
            i = i.split(" ")
            l.append(i)
        for i in l:
            spendings += int(i[1])
            savings += int(i[2])
            invested += int(i[3])

        fig = Figure(figsize=(5, 5), dpi=100)
        y = np.array([spendings, savings, invested])
        mylabels = ["Spendings", "Savings", "Invested"]
        myexplode = [0.1, 0.1, 0.1]
        mycolors = ["#922B21", "#1E8449", "#5B2C6F"]
        plot1 = fig.add_subplot(111)
        plot1.pie(y, labels=mylabels, explode=myexplode, shadow=True, colors=mycolors)

        canvas = FigureCanvasTkAgg(fig, self.piChart)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        # ------------------------------------------------------------------

        BankBalanceLabel = Label(self.root, text="Bank Balance:", font="ariel 22 bold underline", anchor=W)
        BankBalanceLabel.place(x=1000, y=700, width=300, height=50)

        CashBalanceLabel = Label(self.root, text="Cash Balance:", font="ariel 22 bold underline", anchor=W)
        CashBalanceLabel.place(x=1000, y=750, width=300, height=50)

        TotalSavingsLabel = Label(self.root, text="Total Savings:", font="ariel 22 bold underline", anchor=W)
        TotalSavingsLabel.place(x=1000, y=850, width=300, height=50)

        TotalSpendingLabel = Label(self.root, text="Monthly Spend:", font="ariel 22 bold underline", anchor=W)
        TotalSpendingLabel.place(x=1000, y=900, width=300, height=50)

        self.BankBalance_Variable = StringVar()
        self.BankBalance_Variable.set("$0.00")
        self.CashBalance_Variable = StringVar()
        self.CashBalance_Variable.set("$0.00")
        self.TotalSavings_Variable = StringVar()
        self.TotalSavings_Variable.set("$0.00")
        self.MonthlySpending_Variable = StringVar()
        self.MonthlySpending_Variable.set("$0.00")

        self.TotalInvestment_Variable = StringVar()
        self.TotalInvestment_Variable.set("$0.00")

        BankBalance = Label(self.root, textvariable=self.BankBalance_Variable, font="ariel 22 bold", anchor=W)
        CashBalance = Label(self.root, textvariable=self.CashBalance_Variable, font="ariel 22 bold", anchor=W)
        TotalSavings = Label(self.root, textvariable=self.TotalSavings_Variable, font="ariel 22 bold", anchor=W,
                             fg="green")
        TotalSpending = Label(self.root, textvariable=self.MonthlySpending_Variable, font="ariel 22 bold", anchor=W,
                              fg="red")

        BankBalance.place(x=1330, y=700, width=300, height=50)
        CashBalance.place(x=1330, y=750, width=300, height=50)
        TotalSavings.place(x=1330, y=850, width=300, height=50)
        TotalSpending.place(x=1330, y=900, width=300, height=50)

        # ------------------------------------------------------------------
        historyLabel = Label(self.root, text="H\nI\nS\nT\nO\nR\nY", font="ariel 18 bold")
        historyLabel.place(x=1800, y=700, width=50, height=250)

        self.allimg = PhotoImage(file="Images\\History_all.png")
        self.addimg = PhotoImage(file="Images\\History_add.png")
        self.expenseimg = PhotoImage(file="Images\\History_expense.png")
        self.investmentimg = PhotoImage(file="Images\\History_investment.png")

        AllSummary = Button(self.root, image=self.allimg, relief=RIDGE, bd=3, command=self.history_all)
        addSummary = Button(self.root, image=self.addimg, font="ariel 18 bold", relief=RIDGE, bd=3,
                            command=self.history_adding)
        expenseSummary = Button(self.root, image=self.expenseimg, font="ariel 18 bold", relief=RIDGE, bd=3,
                                command=self.history_expense)
        InvestmentSummary = Button(self.root, image=self.investmentimg, font="ariel 18 bold", relief=RIDGE, bd=3,
                                   command=self.history_investment)

        AllSummary.place(x=1850, y=700, width=50, height=50)
        addSummary.place(x=1850, y=770, width=50, height=50)
        expenseSummary.place(x=1850, y=820, width=50, height=50)
        InvestmentSummary.place(x=1850, y=890, width=50, height=50)

        # ------------------------------------------------------------------
        self.MonthlySavingGoal_Variable = StringVar()
        self.MonthlySavingGoalToAchieve_Variable = StringVar()
        self.MonthlyInvestmentGoal_Variable = StringVar()
        self.MonthlyInvestmentGoalToAchieve_Variable = StringVar()

        self.MonthlySavingGoal_Variable.set("$1000")
        self.MonthlySavingGoalToAchieve_Variable.set("$0.00")
        self.MonthlyInvestmentGoal_Variable.set("$1000")
        self.MonthlyInvestmentGoalToAchieve_Variable.set("$0.00")

        MonthlySavingGoalLabel = Label(self.root, text="Monthly Saving Goal:", font="ariel 22 bold", anchor=W)
        MonthlySavingGoalToAchieveLabel = Label(self.root, text="Goal To Achieve:", font="ariel 22 bold", anchor=W)
        MonthlyInvestmentGoalLabel = Label(self.root, text="Monthly Investment Goal:", font="ariel 22 bold", anchor=W)
        MonthlyInvestmentGoalToAchieveLabel = Label(self.root, text="Goal To Achieve:", font="ariel 22 bold", anchor=W)

        MonthlySavingGoalLabel.place(x=40, y=700, width=500, height=50)
        MonthlySavingGoalToAchieveLabel.place(x=40, y=750, width=500, height=50)
        MonthlyInvestmentGoalLabel.place(x=40, y=850, width=500, height=50)
        MonthlyInvestmentGoalToAchieveLabel.place(x=40, y=900, width=500, height=50)

        MonthlySavingGoal = Label(self.root, textvariable=self.MonthlySavingGoal_Variable, font="ariel 22 bold",
                                  width=10,
                                  fg="#E65100")
        MonthlySavingGoalToAchieve = Label(self.root, textvariable=self.MonthlySavingGoalToAchieve_Variable,
                                           font="ariel 22 bold", width=10)
        MonthlyInvestmentGoal = Label(self.root, textvariable=self.MonthlyInvestmentGoal_Variable, font="ariel 22 bold",
                                      width=10, fg="#E65100")
        MonthlyInvestmentGoalToAchieve = Label(self.root, textvariable=self.MonthlyInvestmentGoalToAchieve_Variable,
                                               font="ariel 22 bold", width=10)

        MonthlySavingGoal.place(x=570, y=700, width=150, height=50)
        MonthlySavingGoalToAchieve.place(x=570, y=750, width=150, height=50)
        MonthlyInvestmentGoal.place(x=570, y=850, width=150, height=50)
        MonthlyInvestmentGoalToAchieve.place(x=570, y=900, width=150, height=50)

        ExitBtn = Button(self.root, text="X", font="ariel 20 bold", relief=RIDGE, bd=3, command=self.Exit)
        ExitBtn.place(x=1845, y=5, width=70, height=70)

        # ------------------------------------------------------------------
        statsButton = Button(self.root, text="Stats", font="ariel 15 bold", relief=RIDGE, bd=3,
                             command=self.statButton_Pressed)
        statsButton.place(x=1800, y=970, width=120, height=50)
        # ------------------------------------------------------------------
        self.MoneyValues()

    def statButton_Pressed(self):
        sql = "SELECT * FROM money"

        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()

        bankBalance = myresult[0][0]
        cashBalance = myresult[0][1]
        Investment = myresult[0][2]
        Savings = myresult[0][3]
        MonthlySavings = myresult[0][4]
        MonthlyInvestment = myresult[0][5]
        totalAdd = myresult[0][6]
        totalExpense = myresult[0][7]
        monthlyAdd = myresult[0][8]
        monthlyExpense = myresult[0][9]
        self.ContentVar = StringVar()
        content = "Bank Balance: " + "\n" + "Cash Balance: " + "\n" + "Investment: " + "\n" + "Savings: "  "\n" + "Monthly Savings: " + "\n" + "Monthly Investment: " + "\n" + "Total Add: " + "\n" + "Total Expense: " + "\n" + "Monthly Add: " + "\n" + "Monthly Expense: "
        self.ContentVar.set(content)
        self.ContentValueVar = StringVar()
        contentValue = "$" + str(bankBalance) + "\n$" + str(cashBalance) + "\n$" + str(Investment) + "\n$" + str(
            Savings) + "\n$" + str(MonthlySavings) + "\n$" + str(MonthlyInvestment) + "\n$" + str(
            totalAdd) + "\n$" + str(totalExpense) + "\n$" + str(monthlyAdd) + "\n$" + str(monthlyExpense)
        self.ContentValueVar.set(contentValue)
        info = Toplevel(self.root)
        info.title("Stats")
        info.geometry("500x500")

        statlabel = Label(info, text="Stats", font="ariel 15 bold", relief=RIDGE, bd=3)
        statlabel.place(x=20, y=20, width=200, height=50)

        infoLabel = Label(info, textvariable=self.ContentVar, font="ariel 15 bold", anchor=E)
        infoLabel.place(x=20, y=80, width=300, height=400)

        info = Label(info, textvariable=self.ContentValueVar, font="ariel 15 bold", anchor=W)
        info.place(x=320, y=80, height=400)

        info.mainloop()

    def AddMoneyButton_Pressed(self):
        self.MainOperatingFrame.destroy()
        self.AddButton.config(bg='#2874A6')
        self.WithdrawButton.config(bg='white')
        self.InvestButton.config(bg='white')

        self.MainOperatingFrame = LabelFrame(self.root, text="Adding Money", font="ariel 20 bold", fg="#2874A6", bd=4,
                                             relief=RIDGE)
        self.MainOperatingFrame.place(x=1000, y=100, width=700, height=500)

        self.WhereToAddMoney = Label(self.MainOperatingFrame, text="  Where to Add Money:", font="Ariel 12 bold",
                                     bg='white', bd=2, relief=RIDGE, anchor=W)
        self.WhereToAddMoney.place(x=50, y=90, width=270, height=50)

        WTAM_List = ['Select', 'Bank Account', 'Cash']
        self.WhereToAddMoney_Entry = ttk.Combobox(self.MainOperatingFrame, value=WTAM_List, font="Ariel 12 bold")
        self.WhereToAddMoney_Entry.place(x=350, y=90, width=270, height=50)
        self.WhereToAddMoney_Entry.current(0)

        self.AmountToAdd = Label(self.MainOperatingFrame, text="  Enter amount to Add:", font="Ariel 12 bold",
                                 bg='white', bd=2, relief=RIDGE, anchor=W)
        self.AmountToAdd.place(x=50, y=160, width=270, height=50)
        self.AmountToAdd_Entry = Entry(self.MainOperatingFrame, font="Ariel 12 bold", bg='white', bd=2, relief=RIDGE,
                                       fg="green")
        self.AmountToAdd_Entry.place(x=350, y=160, width=270, height=50)

        self.AmountToAddSource = Label(self.MainOperatingFrame, text="  Enter Source of Money:", font="Ariel 12 bold",
                                       bg='white', bd=2, relief=RIDGE, anchor=W)
        self.AmountToAddSource.place(x=50, y=230, width=270, height=50)
        self.AmountToAddSource_Entry = Entry(self.MainOperatingFrame, font="Ariel 12 bold", bg='white', bd=2,
                                             relief=RIDGE)
        self.AmountToAddSource_Entry.place(x=350, y=230, width=270, height=50)

        self.AddMoneyBtnFinal = Button(self.MainOperatingFrame, text="Add Money", font="Ariel 14 bold", bg='#2874A6',
                                       bd=5, relief=RIDGE, command=self.AddMoneyBtnFinal_Pressed)
        self.AddMoneyBtnFinal.place(x=185, y=320, width=300, height=50)

        Exit_MOF = Button(self.MainOperatingFrame, text="X", font="ariel 20 bold", relief=RIDGE, bd=3,
                          command=self.Exit_MOF)
        Exit_MOF.place(x=625, y=0, width=50, height=50)

    def WithdrawButton_Pressed(self):
        self.MainOperatingFrame.destroy()
        self.AddButton.config(bg='white')
        self.WithdrawButton.config(bg='#CC0066')
        self.InvestButton.config(bg='white')

        self.MainOperatingFrame = LabelFrame(self.root, text="Add Expense", font="ariel 20 bold", fg="#CC0066", bd=4,
                                             relief=RIDGE)
        self.MainOperatingFrame.place(x=1000, y=100, width=700, height=500)

        self.WhereToAddExpense = Label(self.MainOperatingFrame, text="  From Where to Spend:", font="Ariel 12 bold",
                                       bg='white', bd=2, relief=RIDGE, anchor=W)
        self.WhereToAddExpense.place(x=50, y=90, width=270, height=50)

        WTAM_List = ['Select', 'Bank Account', 'Cash']
        self.WhereToAddExpense_Entry = ttk.Combobox(self.MainOperatingFrame, value=WTAM_List, font="Ariel 12 bold")
        self.WhereToAddExpense_Entry.place(x=350, y=90, width=270, height=50)
        self.WhereToAddExpense_Entry.current(0)

        self.ExpenseToAdd = Label(self.MainOperatingFrame, text="  Enter Expense to Add:", font="Ariel 12 bold",
                                  bg='white', bd=2, relief=RIDGE, anchor=W)
        self.ExpenseToAdd.place(x=50, y=160, width=270, height=50)
        self.ExpenseToAdd_Entry = Entry(self.MainOperatingFrame, font="Ariel 12 bold", bg='white', bd=2, relief=RIDGE,
                                        fg="#CC0066")
        self.ExpenseToAdd_Entry.place(x=350, y=160, width=270, height=50)

        self.ExpenseToAddReason = Label(self.MainOperatingFrame, text="  Enter Expense Reason:", font="Ariel 12 bold",
                                        bg='white', bd=2, relief=RIDGE, anchor=W)
        self.ExpenseToAddReason.place(x=50, y=230, width=270, height=50)
        self.ExpenseToAddReason_Entry = Entry(self.MainOperatingFrame, font="Ariel 12 bold", bg='white', bd=2,
                                              relief=RIDGE)
        self.ExpenseToAddReason_Entry.place(x=350, y=230, width=270, height=50)

        self.AddExpenseBtnFinal = Button(self.MainOperatingFrame, text="Add Expense", font="Ariel 14 bold",
                                         bg='#CC0066', bd=5, relief=RIDGE, command=self.AddExpenseBtnFinal_Pressed)
        self.AddExpenseBtnFinal.place(x=185, y=320, width=300, height=50)

        Exit_MOF = Button(self.MainOperatingFrame, text="X", font="ariel 20 bold", relief=RIDGE, bd=3,
                          command=self.Exit_MOF)
        Exit_MOF.place(x=625, y=0, width=50, height=50)

    def InvestButton_Pressed(self):
        self.MainOperatingFrame.destroy()
        self.AddButton.config(bg='white')
        self.WithdrawButton.config(bg='white')
        self.InvestButton.config(bg='#660099')

        self.MainOperatingFrame = LabelFrame(self.root, text="Add Investment", font="ariel 20 bold", fg="#660099", bd=4,
                                             relief=RIDGE)
        self.MainOperatingFrame.place(x=1000, y=100, width=700, height=500)

        self.InvestmentType = Label(self.MainOperatingFrame, text="  Investment Type:", font="Ariel 12 bold",
                                    bg='white', bd=2, relief=RIDGE, anchor=W)
        self.InvestmentType.place(x=50, y=90, width=270, height=50)

        WTAM_List = ['Select', 'Fixed Deposit', 'Mutual Fund', 'Stock', 'Crypto', 'Bonds', 'Gold', 'Silver',
                     'Savings(Cash)', 'Savings(Bank)',
                     'Other']
        self.InvestmentType_Entry = ttk.Combobox(self.MainOperatingFrame, value=WTAM_List, font="Ariel 12 bold")
        self.InvestmentType_Entry.place(x=350, y=90, width=270, height=50)
        self.InvestmentType_Entry.current(0)

        self.InvestmentAmount = Label(self.MainOperatingFrame, text="  Investment Amount:", font="Ariel 12 bold",
                                      bg='white', bd=2, relief=RIDGE, anchor=W)
        self.InvestmentAmount.place(x=50, y=160, width=270, height=50)
        self.InvestmentAmount_Entry = Entry(self.MainOperatingFrame, font="Ariel 12 bold", bg='white', bd=2,
                                            relief=RIDGE, fg="#660099")
        self.InvestmentAmount_Entry.place(x=350, y=160, width=270, height=50)

        self.InvestmentNote = Label(self.MainOperatingFrame, text="  Investment Note:", font="Ariel 12 bold",
                                    bg='white', bd=2, relief=RIDGE, anchor=W)
        self.InvestmentNote.place(x=50, y=230, width=270, height=50)
        self.InvestmentNote_Entry = Entry(self.MainOperatingFrame, font="Ariel 12 bold", bg='white', bd=2, relief=RIDGE)
        self.InvestmentNote_Entry.place(x=350, y=230, width=270, height=50)

        self.AddInvestmentBtnFinal = Button(self.MainOperatingFrame, text="Add Investment", font="Ariel 14 bold",
                                            bg='#660099', bd=5, relief=RIDGE,
                                            command=self.AddInvestmentBtnFinal_Pressed)
        self.AddInvestmentBtnFinal.place(x=185, y=320, width=300, height=50)

        Exit_MOF = Button(self.MainOperatingFrame, text="X", font="ariel 20 bold", relief=RIDGE, bd=3,
                          command=self.Exit_MOF)
        Exit_MOF.place(x=625, y=0, width=50, height=50)

    def Exit_MOF(self):
        self.MainOperatingFrame.destroy()
        self.AddButton.config(bg='white')
        self.WithdrawButton.config(bg='white')
        self.InvestButton.config(bg='white')

    def Exit(self):
        self.root.destroy()

    def Days7Button_Pressed(self):
        a = self.Days7Button.cget('bg')
        if a == 'yellow':
            pass
        else:
            self.Days7Button.config(bg='yellow')
            self.Days30Button.config(bg='systembuttonface')
            self.piChart.destroy()
            self.piChart = Frame(self.PiChartFrame, bd=5, relief=RIDGE)
            self.piChart.place(x=125, y=50, width=450, height=350)

            with open("7days.txt") as f:
                f = f.read()

            spendings = 0
            savings = 0
            invested = 0
            l = []
            f = f.split("\n")
            for i in f:
                i = i.split(" ")
                l.append(i)
            for i in l:
                spendings += int(i[1])
                savings += int(i[2])
                invested += int(i[3])

            fig = Figure(figsize=(5, 5), dpi=100)
            y = np.array([spendings, savings, invested])
            mylabels = ["Spendings", "Savings", "Invested"]
            myexplode = [0.1, 0.1, 0.1]
            mycolors = ["#922B21", "#1E8449", "#5B2C6F"]
            plot1 = fig.add_subplot(111)
            plot1.pie(y, labels=mylabels, explode=myexplode, shadow=True, colors=mycolors)

            canvas = FigureCanvasTkAgg(fig, self.piChart)
            canvas.draw()
            canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

    def Days30Button_Pressed(self):
        a = self.Days30Button.cget('bg')
        if a == 'yellow':
            pass
        else:
            self.Days7Button.config(bg='systembuttonface')
            self.Days30Button.config(bg='yellow')
            self.piChart.destroy()

            self.piChart = Frame(self.PiChartFrame, bd=5, relief=RIDGE)
            self.piChart.place(x=125, y=50, width=450, height=350)

            sql = "SELECT * FROM money"

            self.mycursor.execute(sql)
            myresult = self.mycursor.fetchall()

            spending = int(myresult[0][7])
            savings = int(myresult[0][3])
            invested = int(myresult[0][2])

            fig = Figure(figsize=(5, 5), dpi=100)
            y = np.array([spending, savings, invested])
            mylabels = ["Spendings", "Savings", "Invested"]
            myexplode = [0.1, 0.1, 0.1]
            mycolors = ["#922B21", "#1E8449", "#5B2C6F"]
            plot1 = fig.add_subplot(111)
            plot1.pie(y, labels=mylabels, explode=myexplode, shadow=True, colors=mycolors)

            canvas = FigureCanvasTkAgg(fig, self.piChart)
            canvas.draw()
            canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

    def AddMoneyBtnFinal_Pressed(self):
        print("Adding Money...")
        WTAM = self.WhereToAddMoney_Entry.get()
        ATA = self.AmountToAdd_Entry.get()
        ATAS = self.AmountToAddSource_Entry.get()
        print(WTAM, ATA, ATAS)
        if WTAM != "Select":
            if ATA != "":
                try:
                    ATA = int(ATA)
                    sql = "SELECT * FROM money"
                    self.mycursor.execute(sql)
                    myresult = self.mycursor.fetchall()

                    if WTAM == "Bank Account":
                        try:
                            BankMoney = myresult[0][0]
                            totaladd = myresult[0][6]
                            monthlyadd = myresult[0][8]
                            sql = f"UPDATE money SET bank={BankMoney + ATA}, totaladd={totaladd + ATA}, monthlyadd={monthlyadd + ATA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.MoneyValues()

                            time = str(datetime.datetime.now())
                            time = time[0:19]
                            content = f"\n{time}-----AddMoney-----${ATA}-----{WTAM}------{ATAS}-----Updated: Bank={BankMoney + ATA} TotalAdd={totaladd + ATA} MonthlyAdd={monthlyadd + ATA}"
                            with open("Summary\\addSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\AllSummary.txt", "a") as f:
                                f.write(content)

                            messagebox.showinfo("Success", "Money Added Successfully")
                            self.WhereToAddMoney_Entry.current(0)
                            self.AmountToAdd_Entry.delete(0, END)
                            self.AmountToAddSource_Entry.delete(0, END)
                        except Exception as e:
                            print(e)
                            messagebox.showerror("Error", "Something went wrong")
                    elif WTAM == "Cash":
                        try:
                            CashMoney = myresult[0][1]
                            totaladd = myresult[0][6]
                            monthlyadd = myresult[0][8]
                            sql = f"UPDATE money SET cash={CashMoney + ATA}, totaladd={totaladd + ATA}, monthlyadd={monthlyadd + ATA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.MoneyValues()

                            time = str(datetime.datetime.now())
                            time = time[0:19]
                            content = f"\n{time}-----AddMoney-----${ATA}-----{WTAM}------{ATAS}-----Updated: Cash={CashMoney + ATA} TotalAdd={totaladd + ATA} MonthlyAdd={monthlyadd + ATA}"
                            with open("Summary\\addSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\AllSummary.txt", "a") as f:
                                f.write(content)

                            messagebox.showinfo("Success", "Money Added Successfully")
                            self.WhereToAddMoney_Entry.current(0)
                            self.AmountToAdd_Entry.delete(0, END)
                            self.AmountToAddSource_Entry.delete(0, END)
                        except:
                            messagebox.showerror("Error", "Something went wrong")
                except:
                    messagebox.showinfo("Error", "Please enter valid amount to add")
            else:
                messagebox.showinfo("Error", "Please enter an amount to add")
        else:
            messagebox.showerror("Error", "Please Select/Enter All Fields")

    def AddExpenseBtnFinal_Pressed(self):
        print("Adding Expense...")
        WTAE = self.WhereToAddExpense_Entry.get()
        ETA = self.ExpenseToAdd_Entry.get()
        ETAR = self.ExpenseToAddReason_Entry.get()
        print(WTAE, ETA, ETAR)

        if WTAE != "Select":
            if ETA != "":
                try:
                    ETA = int(ETA)
                    sql = "SELECT * FROM money"
                    self.mycursor.execute(sql)
                    myresult = self.mycursor.fetchall()

                    if WTAE == "Bank Account":
                        try:
                            BankMoney = myresult[0][0]
                            totalexpense = myresult[0][7]
                            monthlyexpense = myresult[0][9]
                            sql = f"UPDATE money SET bank={BankMoney - ETA}, totalexpense={totalexpense + ETA}, monthlyexpense={monthlyexpense + ETA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.MoneyValues()

                            time = str(datetime.datetime.now())
                            time = time[0:19]
                            content = f"\n{time}-----ExpenseMoney-----${ETA}-----{WTAE}------{ETAR}-----Updated: Bank={BankMoney - ETA} TotalAdd={totalexpense + ETA} MonthlyAdd={monthlyexpense + ETA}"
                            with open("Summary\\ExpenseSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\AllSummary.txt", "a") as f:
                                f.write(content)

                            self.Days_7_GraphUpdate(ETA, 0, 0)
                            messagebox.showinfo("Success", "Expense Added Successfully")
                            self.WhereToAddExpense_Entry.current(0)
                            self.ExpenseToAdd_Entry.delete(0, END)
                            self.ExpenseToAddReason_Entry.delete(0, END)
                        except Exception as e:
                            print(e)
                            messagebox.showerror("Error", "Something went wrong")
                    elif WTAE == "Cash":
                        try:
                            CashMoney = myresult[0][1]
                            totalexpense = myresult[0][7]
                            monthlyexpense = myresult[0][9]
                            sql = f"UPDATE money SET cash={CashMoney - ETA}, totalexpense={totalexpense + ETA}, monthlyexpense={monthlyexpense + ETA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.MoneyValues()

                            time = str(datetime.datetime.now())
                            time = time[0:19]
                            content = f"\n{time}-----ExpenseMoney-----${ETA}-----{WTAE}------{ETAR}-----Updated: Cash={CashMoney - ETA} TotalAdd={totalexpense + ETA} MonthlyAdd={monthlyexpense + ETA}"
                            with open("Summary\\ExpenseSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\AllSummary.txt", "a") as f:
                                f.write(content)
                            self.Days_7_GraphUpdate(ETA, 0, 0)
                            messagebox.showinfo("Success", "Expense Added Successfully")
                            self.WhereToAddExpense_Entry.current(0)
                            self.ExpenseToAdd_Entry.delete(0, END)
                            self.ExpenseToAddReason_Entry.delete(0, END)
                        except:
                            messagebox.showerror("Error", "Something went wrong")
                except:
                    messagebox.showinfo("Error", "Please enter valid expense to add")
            else:
                messagebox.showinfo("Error", "Please enter an expense to add")
        else:
            messagebox.showerror("Error", "Please Select/Enter All Fields")

    def AddInvestmentBtnFinal_Pressed(self):
        print("Adding Investment...")
        ITE = self.InvestmentType_Entry.get()
        IA = self.InvestmentAmount_Entry.get()
        IN = self.InvestmentNote_Entry.get()
        print(ITE, IA, IN)

        if ITE != "Select":
            if IA != "":
                try:
                    IA = int(IA)

                    # WTAM_List = ['Select', 'Fixed Deposit', 'Mutual Fund', 'Stock', 'Crypto', 'Bonds', 'Gold', 'Silver', 'Savings', 'Other']

                    sql = "SELECT * FROM investments"
                    self.mycursor.execute(sql)
                    myresult = self.mycursor.fetchall()

                    sql = "SELECT * FROM money"
                    self.mycursor.execute(sql)
                    myresult2 = self.mycursor.fetchall()

                    if ITE == "Gold":
                        try:
                            gold = myresult[0][1]
                            BankMoney = myresult2[0][0]
                            investment = myresult2[0][2]
                            monthlyinvestment = myresult2[0][5]
                            sql = f"UPDATE money SET bank={BankMoney - IA}, investment={investment + IA}, monthlyinvestment={monthlyinvestment + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.MoneyValues()

                            sql = f"UPDATE investments SET gold={gold + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.getAllInvestmments()

                            time = str(datetime.datetime.now())
                            time = time[0:19]
                            content = f"\n{time}-----InvestmentMoney-----${IA}-----{ITE}------{IN}-----Updated: Bank={BankMoney - IA} Investment={investment + IA} MonthlyInvestment={monthlyinvestment + IA}"
                            with open("Summary\\InvestmentSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\AllSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\Investments\\Gold.txt", "a") as f:
                                f.write(content)
                            self.Days_7_GraphUpdate(0, 0, IA)
                            messagebox.showinfo("Success", "Investment Added Successfully")
                            self.InvestmentType_Entry.current(0)
                            self.InvestmentAmount_Entry.delete(0, END)
                            self.InvestmentNote_Entry.delete(0, END)
                        except Exception as e:
                            print(e)
                            messagebox.showerror("Error", "Something went wrong")

                    elif ITE == "Silver":
                        try:
                            silver = myresult[0][2]
                            BankMoney = myresult2[0][0]
                            investment = myresult2[0][2]
                            monthlyinvestment = myresult2[0][5]
                            sql = f"UPDATE money SET bank={BankMoney - IA}, investment={investment + IA}, monthlyinvestment={monthlyinvestment + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.MoneyValues()

                            sql = f"UPDATE investments SET silver={silver + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.getAllInvestmments()

                            time = str(datetime.datetime.now())
                            time = time[0:19]
                            content = f"\n{time}-----InvestmentMoney-----${IA}-----{ITE}------{IN}-----Updated: Bank={BankMoney - IA} Investment={investment + IA} MonthlyInvestment={monthlyinvestment + IA}"
                            with open("Summary\\InvestmentSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\AllSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\Investments\\Silver.txt", "a") as f:
                                f.write(content)
                            self.Days_7_GraphUpdate(0, 0, IA)
                            messagebox.showinfo("Success", "Investment Added Successfully")
                            self.InvestmentType_Entry.current(0)
                            self.InvestmentAmount_Entry.delete(0, END)
                            self.InvestmentNote_Entry.delete(0, END)
                        except Exception as e:
                            print(e)
                            messagebox.showerror("Error", "Something went wrong")

                    elif ITE == "Fixed Deposit":
                        try:
                            fixeddeposit = myresult[0][3]
                            BankMoney = myresult2[0][0]
                            investment = myresult2[0][2]
                            monthlyinvestment = myresult2[0][5]
                            sql = f"UPDATE money SET bank={BankMoney - IA}, investment={investment + IA}, monthlyinvestment={monthlyinvestment + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.MoneyValues()

                            sql = f"UPDATE investments SET fd={fixeddeposit + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.getAllInvestmments()

                            time = str(datetime.datetime.now())
                            time = time[0:19]
                            content = f"\n{time}-----InvestmentMoney-----${IA}-----{ITE}------{IN}-----Updated: Bank={BankMoney - IA} Investment={investment + IA} MonthlyInvestment={monthlyinvestment + IA}"
                            with open("Summary\\InvestmentSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\AllSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\Investments\\FixedDeposit.txt", "a") as f:
                                f.write(content)

                            self.Days_7_GraphUpdate(0, 0, IA)
                            messagebox.showinfo("Success", "Investment Added Successfully")
                            self.InvestmentType_Entry.current(0)
                            self.InvestmentAmount_Entry.delete(0, END)
                            self.InvestmentNote_Entry.delete(0, END)
                        except Exception as e:
                            print(e)
                            messagebox.showerror("Error", "Something went wrong")

                    elif ITE == "Stock":
                        try:
                            stock = myresult[0][0]
                            BankMoney = myresult2[0][0]
                            investment = myresult2[0][2]
                            monthlyinvestment = myresult2[0][5]
                            sql = f"UPDATE money SET bank={BankMoney - IA}, investment={investment + IA}, monthlyinvestment={monthlyinvestment + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.MoneyValues()

                            sql = f"UPDATE investments SET stock={stock + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.getAllInvestmments()

                            time = str(datetime.datetime.now())
                            time = time[0:19]
                            content = f"\n{time}-----InvestmentMoney-----${IA}-----{ITE}------{IN}-----Updated: Bank={BankMoney - IA} Investment={investment + IA} MonthlyInvestment={monthlyinvestment + IA}"
                            with open("Summary\\InvestmentSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\AllSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\Investments\\Stock.txt", "a") as f:
                                f.write(content)

                            self.Days_7_GraphUpdate(0, 0, IA)
                            messagebox.showinfo("Success", "Investment Added Successfully")
                            self.InvestmentType_Entry.current(0)
                            self.InvestmentAmount_Entry.delete(0, END)
                            self.InvestmentNote_Entry.delete(0, END)
                        except Exception as e:
                            print(e)
                            messagebox.showerror("Error", "Something went wrong")

                    elif ITE == "Crypto":
                        try:
                            crypto = myresult[0][5]
                            BankMoney = myresult2[0][0]
                            investment = myresult2[0][2]
                            monthlyinvestment = myresult2[0][5]
                            sql = f"UPDATE money SET bank={BankMoney - IA}, investment={investment + IA}, monthlyinvestment={monthlyinvestment + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.MoneyValues()

                            sql = f"UPDATE investments SET crypto={crypto + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.getAllInvestmments()

                            time = str(datetime.datetime.now())
                            time = time[0:19]
                            content = f"\n{time}-----InvestmentMoney-----${IA}-----{ITE}------{IN}-----Updated: Bank={BankMoney - IA} Investment={investment + IA} MonthlyInvestment={monthlyinvestment + IA}"
                            with open("Summary\\InvestmentSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\AllSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\Investments\\Crypto.txt", "a") as f:
                                f.write(content)

                            self.Days_7_GraphUpdate(0, 0, IA)
                            messagebox.showinfo("Success", "Investment Added Successfully")
                            self.InvestmentType_Entry.current(0)
                            self.InvestmentAmount_Entry.delete(0, END)
                            self.InvestmentNote_Entry.delete(0, END)
                        except Exception as e:
                            print(e)
                            messagebox.showerror("Error", "Something went wrong")

                    elif ITE == "Mutual Fund":
                        try:
                            mutualfund = myresult[0][4]
                            BankMoney = myresult2[0][0]
                            investment = myresult2[0][2]
                            monthlyinvestment = myresult2[0][5]
                            sql = f"UPDATE money SET bank={BankMoney - IA}, investment={investment + IA}, monthlyinvestment={monthlyinvestment + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.MoneyValues()

                            sql = f"UPDATE investments SET mutualfunds={mutualfund + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.getAllInvestmments()

                            time = str(datetime.datetime.now())
                            time = time[0:19]
                            content = f"\n{time}-----InvestmentMoney-----${IA}-----{ITE}------{IN}-----Updated: Bank={BankMoney - IA} Investment={investment + IA} MonthlyInvestment={monthlyinvestment + IA}"
                            with open("Summary\\InvestmentSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\AllSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\Investments\\MutualFund.txt", "a") as f:
                                f.write(content)

                            self.Days_7_GraphUpdate(0, 0, IA)
                            messagebox.showinfo("Success", "Investment Added Successfully")
                            self.InvestmentType_Entry.current(0)
                            self.InvestmentAmount_Entry.delete(0, END)
                            self.InvestmentNote_Entry.delete(0, END)
                        except Exception as e:
                            print(e)
                            messagebox.showerror("Error", "Something went wrong")

                    elif ITE == "Bonds":
                        try:
                            bonds = myresult[0][6]
                            BankMoney = myresult2[0][0]
                            investment = myresult2[0][2]
                            monthlyinvestment = myresult2[0][5]
                            sql = f"UPDATE money SET bank={BankMoney - IA}, investment={investment + IA}, monthlyinvestment={monthlyinvestment + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.MoneyValues()

                            sql = f"UPDATE investments SET bonds={bonds + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.getAllInvestmments()

                            time = str(datetime.datetime.now())
                            time = time[0:19]
                            content = f"\n{time}-----InvestmentMoney-----${IA}-----{ITE}------{IN}-----Updated: Bank={BankMoney - IA} Investment={investment + IA} MonthlyInvestment={monthlyinvestment + IA}"
                            with open("Summary\\InvestmentSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\AllSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\Investments\\Bonds.txt", "a") as f:
                                f.write(content)

                            self.Days_7_GraphUpdate(0, 0, IA)
                            messagebox.showinfo("Success", "Investment Added Successfully")
                            self.InvestmentType_Entry.current(0)
                            self.InvestmentAmount_Entry.delete(0, END)
                            self.InvestmentNote_Entry.delete(0, END)
                        except Exception as e:
                            print(e)
                            messagebox.showerror("Error", "Something went wrong")

                    elif ITE == "Other":
                        try:
                            other = myresult[0][8]
                            BankMoney = myresult2[0][0]
                            investment = myresult2[0][2]
                            monthlyinvestment = myresult2[0][5]
                            sql = f"UPDATE money SET bank={BankMoney - IA}, investment={investment + IA}, monthlyinvestment={monthlyinvestment + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.MoneyValues()

                            sql = f"UPDATE investments SET other={other + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.getAllInvestmments()

                            time = str(datetime.datetime.now())
                            time = time[0:19]
                            content = f"\n{time}-----InvestmentMoney-----${IA}-----{ITE}------{IN}-----Updated: Bank={BankMoney - IA} Investment={investment + IA} MonthlyInvestment={monthlyinvestment + IA}"
                            with open("Summary\\InvestmentSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\AllSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\Investments\\Other.txt", "a") as f:
                                f.write(content)

                            self.Days_7_GraphUpdate(0, 0, IA)
                            messagebox.showinfo("Success", "Investment Added Successfully")
                            self.InvestmentType_Entry.current(0)
                            self.InvestmentAmount_Entry.delete(0, END)
                            self.InvestmentNote_Entry.delete(0, END)
                        except Exception as e:
                            print(e)
                            messagebox.showerror("Error", "Something went wrong")

                    elif ITE == "Savings(Cash)":
                        try:
                            saving = myresult[0][7]
                            CashMoney = myresult2[0][1]
                            savings = myresult2[0][3]
                            monthlysavings = myresult2[0][4]
                            sql = f"UPDATE money SET cash={CashMoney - IA}, saving={savings + IA}, monthlysaving={monthlysavings + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.MoneyValues()

                            sql = f"UPDATE investments SET savings={saving + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.getAllInvestmments()

                            time = str(datetime.datetime.now())
                            time = time[0:19]
                            content = f"\n{time}-----InvestmentMoney-----${IA}-----{ITE}------{IN}-----Updated: Bank={CashMoney - IA} saving={savings + IA} monthlysaving={monthlysavings + IA}"
                            with open("Summary\\InvestmentSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\AllSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\Investments\\Other.txt", "a") as f:
                                f.write(content)

                            self.Days_7_GraphUpdate(0, IA, 0)
                            messagebox.showinfo("Success", "Savings Added Successfully")
                            self.InvestmentType_Entry.current(0)
                            self.InvestmentAmount_Entry.delete(0, END)
                            self.InvestmentNote_Entry.delete(0, END)
                        except Exception as e:
                            print(e)
                            messagebox.showerror("Error", "Something went wrong")

                    elif ITE == "Savings(Bank)":
                        try:
                            saving = myresult[0][7]
                            BankMoney = myresult2[0][0]
                            savings = myresult2[0][3]
                            monthlysavings = myresult2[0][4]
                            sql = f"UPDATE money SET bank={BankMoney - IA}, saving={savings + IA}, monthlysaving={monthlysavings + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.MoneyValues()

                            sql = f"UPDATE investments SET savings={saving + IA}"
                            self.mycursor.execute(sql)
                            self.mydb.commit()
                            self.getAllInvestmments()

                            time = str(datetime.datetime.now())
                            time = time[0:19]
                            content = f"\n{time}-----InvestmentMoney-----${IA}-----{ITE}------{IN}-----Updated: Bank={BankMoney - IA} saving={savings + IA} monthlysaving={monthlysavings + IA}"
                            with open("Summary\\InvestmentSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\AllSummary.txt", "a") as f:
                                f.write(content)
                            with open("Summary\\Investments\\Other.txt", "a") as f:
                                f.write(content)

                            self.Days_7_GraphUpdate(0, IA, 0)
                            messagebox.showinfo("Success", "Savings Added Successfully")
                            self.InvestmentType_Entry.current(0)
                            self.InvestmentAmount_Entry.delete(0, END)
                            self.InvestmentNote_Entry.delete(0, END)
                        except Exception as e:
                            print(e)
                            messagebox.showerror("Error", "Something went wrong")

                except:
                    messagebox.showinfo("Error", "Please enter valid investment amount")
            else:
                messagebox.showinfo("Error", "Please enter an investment amount")
        else:
            messagebox.showerror("Error", "Please Select/Enter All Fields")

    def MoneyValues(self):
        sql = "SELECT * FROM money"

        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()

        self.BankBalance_Variable.set("$" + str(myresult[0][0]))
        self.CashBalance_Variable.set("$" + str(myresult[0][1]))

        self.TotalInvestment_Variable.set("$" + str(myresult[0][2]))
        self.TotalSavings_Variable.set("$" + str(myresult[0][3]))

        MonthlySaving = myresult[0][4]
        MonthlyInvestment = myresult[0][5]
        self.MonthlySavingGoalToAchieve_Variable.set(
            "$" + str(int(self.MonthlySavingGoal_Variable.get()[1:]) - MonthlySaving))
        self.MonthlyInvestmentGoalToAchieve_Variable.set(
            "$" + str(int(self.MonthlyInvestmentGoal_Variable.get()[1:]) - MonthlyInvestment))

        TotalAdd = myresult[0][6]
        TotalExpense = myresult[0][7]

        monthlyAdd = myresult[0][8]
        monthlyExpense = myresult[0][9]
        self.MonthlySpending_Variable.set("$" + str(monthlyExpense))

    def history_adding(self):
        os.startfile("Summary\\addSummary.txt")

    def history_expense(self):
        os.startfile("Summary\\expenseSummary.txt")

    def history_investment(self):
        os.startfile("Summary\\investmentSummary.txt")

    def history_all(self):
        os.startfile("Summary\\allSummary.txt")

    def getAllInvestmments(self):
        sql = "SELECT * FROM investments"
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()

        stock = myresult[0][0]
        gold = myresult[0][1]
        silver = myresult[0][2]
        fd = myresult[0][3]
        mutualfunds = myresult[0][4]
        crypto = myresult[0][5]
        bonds = myresult[0][6]
        savings = myresult[0][7]
        other = myresult[0][8]

    def Days_7_GraphUpdate(self, spending, saving, investment):
        now = dt.now().strftime("%d%m%y")
        with open("7days.txt") as f:
            content = f.read()
        if now in content:
            l = []
            f = content.split("\n")
            print(f)
            for i in f:
                i = i.split(" ")
                l.append(i)
            print(l)
            for i in l:
                if i[0] == now:
                    i[1] = str(int(i[1]) + spending)
                    i[2] = str(int(i[2]) + saving)
                    i[3] = str(int(i[3]) + investment)

            lFinal = []
            for i in l:
                a = " ".join(i)
                lFinal.append(a)
            print(lFinal)
            lFinal = "\n".join(lFinal)
            print(lFinal)

            with open("7days.txt", "w") as f:
                f.write(lFinal)
        else:
            f = content.split("\n")
            f.pop(0)
            f.append(f"{now} {spending} {saving} {investment}")
            lFinal = "\n".join(f)
            print(lFinal)
            with open("7days.txt", "w") as f:
                f.write(lFinal)

        self.Days30Button_Pressed()
        self.Days7Button_Pressed()


if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.overrideredirect(1)
    root.mainloop()
