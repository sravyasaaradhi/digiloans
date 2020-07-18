from flask import Flask, render_template, request, redirect, url_for, flash,jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
import requests, json
from datetime import datetime
from flask_mysqldb import MySQL
from sqlalchemy import text
import time
from array import *
import mysql.connector

app = Flask(__name__)
app.secret_key = "Secret Key"

# SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://digiinternapi_user:Di76@51r$132h@15.206.199.1/digiinternapi_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
@app.route("/")
def home():
    return render_template("index.html")

class Borrowers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrowerName = db.Column(db.String(20))
    userId = db.Column(db.Integer)
    city = db.Column(db.String(20))
    email = db.Column(db.String(100))
    mobileNumber = db.Column(db.String(255))
    loanType = db.Column(db.String(25))
    appliedOn = db.Column(db.String(50))

    def __init__(self, borrowerName, userId, city, email, mobileNumber, loanType, appliedOn):
        self.borrowerName = borrowerName
        self.userId = userId
        self.city = city
        self.email = email
        self.mobileNumber = mobileNumber
        self.loanType = loanType
        self.appliedOn = appliedOn

class PendingRequests(db.Model):
    #id = db.Column(db.Integer,primary_key=True)
    borrowerId = db.Column(db.Integer,primary_key=True)
    borrowerName = db.Column(db.String(20))
    email = db.Column(db.String(100))
    mobileNumber = db.Column(db.String(255))



    def __init__(self, borrowerId, borrowerName, email, mobileNumber ):
        self.borrowerId = borrowerId
        self.borrowerName = borrowerName
        self.email = email
        self.mobileNumber = mobileNumber


class RejectedApplications(db.Model):
    #id = db.Column(db.Integer)
    borrowerId = db.Column(db.Integer, primary_key=True)
    borrowerName = db.Column(db.String(20))
    email = db.Column(db.String(100))
    mobileNumber = db.Column(db.String(255))



    def __init__(self, borrowerId, borrowerName, email, mobileNumber ):
        self.borrowerId = borrowerId
        self.borrowerName = borrowerName
        self.email = email
        self.mobileNumber = mobileNumber


class  ManageRequests(db.Model):
    #id = db.Column(db.Integer)
    borrowerId = db.Column(db.Integer, primary_key=True)
    borrowerName = db.Column(db.String(20))
    email = db.Column(db.String(100))
    mobileNumber = db.Column(db.Integer)
    creditLimit = db.Column(db.Integer)

    def __init__(self, borrowerId, borrowerName, email, mobileNumber, creditLimit ):
        self.borrowerId = borrowerId
        self.borrowerName = borrowerName
        self.email = email
        self.mobileNumber = mobileNumber
        self. creditLimit = creditLimit

class PendingRequest(db.Model):
    #id = db.Column(db.Integer)
    loan_id = db.Column(db.Integer, primary_key=True)
    browerName = db.Column(db.String(20))
    mobilenumber = db.Column(db.String(50))
    profileScore = db.Column(db.Integer)
    loanType = db.Column(db.String(50))
    creditLimit = db.Column(db.Integer)
    loanAmount = db.Column(db.Integer)
    days = db.Column(db.Integer)
    interstPayable = db.Column(db.Integer)
    processingFee = db.Column(db.Integer)
    promocode = db.Column(db.String(50))
    repaymentAmount = db.Column(db.Integer)
    requesteddate = db.Column(db.String(50))
    repaymentDate = db.Column(db.String(50))


    def __init__(self, loan_id, browerName,mobilenumber, profileScore, loanType, creditLimit, loanAmount, days, interstPayable, processingFee, promocode, repaymentAmount, requesteddate, repaymentDate):
        self.loan_id = loan_id
        self.browerName = browerName
        self.mobilenumber = mobilenumber
        self.profileScore = profileScore
        self.loanType = loanType
        self.creditLimit = creditLimit
        self.loanAmount = loanAmount
        self.days = days
        self.interstPayable = interstPayable
        self.processingFee = processingFee
        self.promocode = promocode
        self.repaymentAmount = repaymentAmount
        self.requesteddate = requesteddate
        self.repaymentDate = repaymentDate

class MappedLender(db.Model):
    #id = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer)
    assignedDate = db.Column(db.String(60))
    status = db.Column(db.String(50))
    loanAmount = db.Column(db.Integer)
    repaymentDate = db.Column(db.String)


    def __init__(self,   loan_id, assignedDate,status,loanAmount,repaymentDate):
        self.loan_id = loan_id
        self.assignedDate = assignedDate
        self.status = status
        self.loanAmount = loanAmount
        self.repaymentDate = repaymentDate

class LenderLoanMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer)
    lender_id = db.Column(db.Integer)
    lender_share_amount = db.Column(db.Integer)
    createdAt = db.Column(db.DATE)
    updatedAt = db.Column(db.DateTime)

    def __init__(self, loan_id,lender_id,lender_share_amount,createdAt,updatedAt):
        self.loan_id = loan_id
        self.lender_id = lender_id
        self.lender_share_amount = lender_share_amount
        self.createdAt = createdAt
        self.updatedAt = updatedAt

class RejectedLoans(db.Model):
    #id = db.Column(db.Integer)
    loan_id = db.Column(db.Integer, primary_key=True)
    browerName = db.Column(db.String(20))
    mobilenumber = db.Column(db.String(50))
    creditLimit = db.Column(db.Integer)
    loanAmount = db.Column(db.Integer)
    days = db.Column(db.Integer)
    interstPayable = db.Column(db.Integer)
    processingFee = db.Column(db.Integer)
    requesteddate = db.Column(db.String(50))
    repaymentAmount = db.Column(db.Integer)
    repaymentDate = db.Column(db.String(50))


    def __init__(self, loan_id, browerName,mobilenumber, creditLimit, loanAmount, days, interstPayable, processingFee, requesteddate,repaymentAmount, repaymentDate):
        self.loan_id = loan_id
        self.browerName = browerName
        self.mobilenumber = mobilenumber
        self.creditLimit = creditLimit
        self.loanAmount = loanAmount
        self.days = days
        self.interstPayable = interstPayable
        self.processingFee = processingFee
        self.requesteddate = requesteddate
        self.repaymentAmount = repaymentAmount
        self.repaymentDate = repaymentDate

class DisbursedLoans(db.Model):
    #id = db.Column(db.Integer)
    loan_id= db.Column(db.Integer, primary_key=True)
    browerName = db.Column(db.String(20))
    lenderNameid = db.Column(db.String(100))
    disbDate = db.Column(db.String(50))
    amtDisb = db.Column(db.Integer)
    tenure = db.Column(db.Integer)
    interest = db.Column(db.Integer)
    procFee = db.Column(db.Integer)
    repayAmt = db.Column(db.Integer)
    repayDate = db.Column(db.String(50))
    referencenumber =db.Column(db.Integer)


    def __init__(self, loan_id, browerName, lenderNameid, disbDate,amtDisb,tenure,interest,procFee,repayAmt,repayDate,referencenumber):
        self.loan_id = loan_id
        self.browerName= browerName
        self.lenderNameid = lenderNameid
        self.disbDate = disbDate
        self.amtDisb = amtDisb
        self.tenure = tenure
        self.interest = interest
        self.procFee = procFee
        self.repayAmt = repayAmt
        self.repayDate = repayDate
        self.referencenumber =referencenumber

class ClosedLoans(db.Model):
    #id = db.Column(db.Integer)
    loan_id = db.Column(db.Integer, primary_key=True)
    browerName = db.Column(db.String(20))
    lenderName = db.Column(db.String(100))
    creditLimit = db.Column(db.Integer)
    rom = db.Column(db.Integer)
    disbDate = db.Column(db.String(50))
    loanAmt = db.Column(db.Integer)
    tenure = db.Column(db.Integer)
    interest = db.Column(db.Integer)
    procFee = db.Column(db.Integer)
    repayAmt = db.Column(db.Integer)
    closedDate = db.Column(db.String(50))
    resiveAmt = db.Column(db.Integer)
    paidAmt = db.Column(db.String(50))

    def __init__(self, loan_id, browerName, lenderName,creditLimit,rom, disbDate,loanAmt,tenure,interest,procFee,repayAmt,closedDate,resiveAmt,paidAmt ):
        self.loan_id = loan_id
        self.browerName = browerName
        self.lenderName = lenderName
        self.creditLimit = creditLimit
        self.rom = rom
        self.disbDate = disbDate
        self.loanAmt = loanAmt
        self.tenure = tenure
        self.interest = interest
        self.procFee = procFee
        self.repayAmt = repayAmt
        self.closedDate = closedDate
        self.resiveAmt = resiveAmt
        self.paidAmt = paidAmt

class Authorization(db.Model):
    #id = db.Column(db.Integer,)
    borrowerId = db.Column(db.Integer, primary_key=True)
    borrowerName = db.Column(db.String(20))
    email = db.Column(db.String(100))
    mobileNumber = db.Column(db.Integer)



    def __init__(self, borrowerId, borrowerName, email, mobileNumber ):
        self.borrowerId = borrowerId
        self.borrowerName = borrowerName
        self.email = email
        self.mobileNumber = mobileNumber

class SendtoBank(db.Model):
    #id = db.Column(db.Integer,)
    loan_id = db.Column(db.Integer, primary_key=True)
    browerName= db.Column(db.String(20))
    loanType = db.Column(db.String(100))
    nooflenders = db.Column(db.Integer)
    loanAmount = db.Column(db.String(100))
    repaymentAmount = db.Column(db.Integer)
    requesteddate = db.Column(db.String(100))
    repaymentDate = db.Column(db.Integer)



    def __init__(self,  loan_id ,browerName,  loanType , nooflenders , loanAmount, 	repaymentAmount ,requesteddate,repaymentDate):
        self.loan_id= loan_id
        self.browerName = browerName
        self.loanType = loanType
        self.nooflenders  = nooflenders
        self.loanAmount = loanAmount
        self.repaymentAmount =repaymentAmount
        self.requesteddate = requesteddate
        self.repaymentDate = repaymentDate

class Transit(db.Model):
    #id = db.Column(db.Integer,)
    loan_id = db.Column(db.Integer, primary_key=True)
    browerName= db.Column(db.String(20))
    nooflenders = db.Column(db.Integer)
    loanAmount = db.Column(db.Integer)
    repaymentAmount = db.Column(db.Integer)
    requesteddate = db.Column(db.String(100))
    repaymentDate = db.Column(db.String(100))



    def __init__(self,  loan_id ,browerName, nooflenders , loanAmount, repaymentAmount ,requesteddate,repaymentDate):
        self.loan_id= loan_id
        self.browerName = browerName
        self.nooflenders  = nooflenders
        self.loanAmount = loanAmount
        self.repaymentAmount= repaymentAmount
        self.requesteddate = requesteddate
        self.repaymentDate =  repaymentDate


class Move(db.Model):
    #id = db.Column(db.Integer,)
    loanId= db.Column(db.Integer, primary_key=True)
    disbDate = db.Column(db.String(100))
    referencenumber = db.Column(db.String(20))


    def __init__(self,loanId,disbDate, referencenumber ):

        self.loanId = loanId
        self.disbDate= disbDate
        self. referencenumber= referencenumber

class Arrears(db.Model):
    # id = db.Column(db.Integer,)
    number = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.String(20))
    arrearamount = db.Column(db.String(100))
    browerName = db.Column(db.String(20))
    repayAmt = db.Column(db.String(100))

    def __init__(self, number, loan_id, arrearamount, browerName, repayAmt):
        self.number = number
        self.loan_id = loan_id
        self.arrearamount = arrearamount
        self.browerName = browerName
        self.repayAmt = repayAmt


class TodaysDues(db.Model):
    # id = db.Column(db.Integer)
    loan_id = db.Column(db.Integer, primary_key=True)
    browerName_id = db.Column(db.String(20))

    mobilenumber = db.Column(db.String(100))
    loanamount = db.Column(db.Integer)
    tenure = db.Column(db.Integer)
    processingFees = db.Column(db.Integer)
    interest = db.Column(db.Integer)
    DisbursedDate = db.Column(db.Integer)
    repayAmt = db.Column(db.Integer)
    bankAccountnumber = db.Column(db.Integer)

    def __init__(self, loan_id, browerName_id, mobilenumber, loanamount, tenure, processingFees, interest,
                 DisbursedDate, repayAmt, bankAccountnumber):
        self.loan_id = loan_id
        self.browerName_id = browerName_id

        self.mobilenumber = mobilenumber
        self.loanamount = loanamount
        self.tenure = tenure
        self.processingFees = processingFees
        self.interest = interest
        self.DisbursedDate = DisbursedDate
        self.repayAmt = repayAmt
        self.bankAccountnumber = bankAccountnumber


class Defaulters(db.Model):
    loan_id = db.Column(db.Integer, primary_key=True)
    browerName = db.Column(db.String(20))
    mobilenumber = db.Column(db.String(100))
    NoOflenders = db.Column(db.Integer)
    loanamount = db.Column(db.Integer)
    repayAmt = db.Column(db.Integer)
    disburseddate = db.Column(db.Integer)
    defaulteddate = db.Column(db.Integer)
    dpddays = db.Column(db.Integer)
    Penalchargers = db.Column(db.Integer)
    dpdinterest = db.Column(db.Integer)
    revisedDue = db.Column(db.Integer)

    def __init__(self, loan_id, browerName, mobilenumber, NoOflenders, loanamount, repayAmt, disburseddate,
                 defaulteddate,
                 dpddays, Penalchargers, dpdinterest, revisedDue):
        self.loan_id = loan_id
        self.browerName = browerName
        self.mobilenumber = mobilenumber
        self.NoOflenderss = NoOflenders
        self.loanamount = loanamount
        self.repayAmt = repayAmt
        self.disburseddate = disburseddate
        self.defaulteddate = defaulteddate
        self.dpddays = dpddays
        self.Penalchargers = Penalchargers
        self.dpdinterest = dpdinterest
        self.revisedDue = revisedDue


class Npa(db.Model):
    loan_id = db.Column(db.Integer, primary_key=True)
    browerName = db.Column(db.String(20))
    mobilenumber = db.Column(db.String(100))
    NoOflenders = db.Column(db.Integer)
    loanamount = db.Column(db.Integer)
    repayAmt = db.Column(db.Integer)
    disburseddate = db.Column(db.Integer)
    defaulteddate = db.Column(db.Integer)
    dpddays = db.Column(db.Integer)
    Penalchargers = db.Column(db.Integer)
    dpdinterest = db.Column(db.Integer)
    revisedDue = db.Column(db.Integer)

    def __init__(self, loan_id, browerName, mobilenumber, NoOflenders, loanamount, repayAmt, disburseddate,
                 defaulteddate,
                 dpddays, Penalchargers, dpdinterest, revisedDue):
        self.loan_id = loan_id
        self.browerName = browerName
        self.mobilenumber = mobilenumber
        self.NoOflenderss = NoOflenders
        self.loanamount = loanamount
        self.repayAmt = repayAmt
        self.disburseddate = disburseddate
        self.defaulteddate = defaulteddate
        self.dpddays = dpddays
        self.Penalchargers = Penalchargers
        self.dpdinterest = dpdinterest
        self.revisedDue = revisedDue



# This is the index route where we are going to
# query on all our employee data

@app.route('/index')
def Index():

        all_data = Borrowers.query.all()
        url = "http://15.206.199.1:8080/Digiloanjune14/api/joingGetall"
        data = {'userid':1}
        r = requests.get(url,data)
        json_data = json.loads(r.text)
        #print(json_data['data'])
        #print("index")
        list = []
        for datalist in json_data['data']:
            listobj = {}
            listobj['username'] = datalist['username']

            listobj['userId'] = datalist['userId']
            listobj['city'] = datalist['city']
            listobj['email'] = datalist['email']
            listobj['phoneNumber'] = datalist['phoneNumber']
            listobj['account_type'] = datalist['account_type']
            listobj['created_at'] = datalist['created_at']

            list.append(listobj)
            # print(list)
        return render_template("Wip Borrowers.html", employees=list)



# this route is for inserting data to mysql database via html forms
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        borrowerName = request.form['borrowerName']
        userId = request.form['userId']
        city = request.form['city']
        email = request.form['email']
        mobileNumber = request.form['mobileNumber']
        loanType = request.form['loanType']
        appliedOn = request.form['appliedOn']

        my_data = Borrowers(borrowerName, userId, city,email,mobileNumber, loanType, appliedOn )
        db.session.add(my_data)
        db.session.commit()

        flash("Inserted Successfully")

        return redirect(url_for('Index'))


# this is our update route where we are going to update our employee
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Borrowers.query.get(request.form.get('userId'))
        url = "http://15.206.199.1:8080/Digiloanadminv5/api/getUerData"
        data = {"userid": 1}
        r = requests.post(url, data)
        json_data = json.loads(r.text)
        print(json_data['data']['adhar_number'])

        my_data.borrowerName = request.form['borrowerName']
        my_data.userId = request.form['userId']
        my_data.city = request.form['city']
        my_data.email = request.form['email']
        my_data.mobileNumber = request.form['mobileNumber']
        my_data.loanType = request.form['loanType']
        my_data.appliedOn = request.form['appliedOn']

        db.session.commit()

        flash(" Updated Successfully")

        return redirect(url_for('Index'))
@app.route('/view')
#@app.route('/view/<userId>', methods=['GET','POST'])
def View():
    #print(userId)
    url = "http://15.206.199.1:8080/Digiloanjune14/api/getPersonalDetails"

    data = {'userid':1}

    r = requests.post(url,data)
    json_data = json.loads(r.text)

    list = []

    list.append(json_data)

    url = "http://15.206.199.1:8080/Digiloanjune14/api/getAddressDetails"
    data={'userid':1}
    r = requests.post(url,data)
    json_data1=json.loads(r.text)

    list.append(json_data1)
    #print(json_data1)


    url = "http://15.206.199.1:8080/Digiloanjune14/api/getUserSalaryDetails"
    data={'userid':1}
    r = requests.post(url,data)
    json_data2 = json.loads(r.text)
    list.append(json_data2)
    #print(json_data2)

    url = "http://15.206.199.1:8080/Digiloanjune14/api/getUserSelfEmployed"
    data = {'userid': 1}
    r = requests.post(url, data)
    json_data3 = json.loads(r.text)
    list.append(json_data3)
    #print(json_data3)

    url = "http://15.206.199.1:8080/Digiloanjune14/api/getBankDetails"
    data = {'userid': 1}
    r = requests.post(url, data)
    json_data4 = json.loads(r.text)
    list.append(json_data4)
    #print(json_data4)

    return render_template("view.html",emp = list)


@app.route('/Move_to_process', methods=['GET', 'POST'])
def Move_to_process():
    if request.method == 'POST':
        borrowerId = request.form['userId']
        print(borrowerId)
        borrowerName = request.form['borrowerName']
        email = request.form['email']
        mobileNumber = request.form['mobileNumber']
        my_data = PendingRequests(borrowerId, borrowerName, email, mobileNumber)
        db.session.add(my_data)
        #delete_data = Borrowers.query.get(request.form.get('id'))
        #db.session.delete(delete_data)
        db.session.commit()
        flash("Move_to_process Successfully")
        data = PendingRequests.query.all()
        return render_template("Pending Requests.html", employees=data)


# This route is for deleting our employee
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Borrowers.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash(" Deleted Successfully")

    return redirect(url_for('Index'))


@app.route('/view_data', methods=['GET', 'POST'])
def view_data():
    my_data = Borrowers.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash(" Deleted Successfully")
    return redirect(url_for('Index'))


@app.route('/pending')
def Pending():

    data = PendingRequests.query.all()

    return render_template("Pending Requests.html", employees=data)


# this route is for inserting data to mysql database via html forms
@app.route('/insert_data_pen', methods=['POST'])
def insert_data_pen():
    if request.method == 'POST':
        my_data = PendingRequests.query.get(request.form.get('id'))
        print(my_data.borrowerName)
        borrowerId = request.form['borrowerId']
        borrowerName = request.form['borrowerName']
        email = request.form['email']
        mobileNumber = request.form['mobileNumber']

        my_data = PendingRequests(borrowerId,borrowerName,email,mobileNumber )
        db.session.add(my_data)
        db.session.commit()

        flash("Inserted Successfully")

        return redirect(url_for('Pending'))


# this is our update route where we are going to update our employee
@app.route('/update_data', methods=['GET', 'POST'])
def update_data():
    if request.method == 'POST':
        my_data = PendingRequests.query.get(request.form.get('id'))

        my_data.borrowerId = request.form['borrowerId']
        my_data.borrowerName = request.form['borrowerName']
        my_data.email = request.form['email']
        my_data.mobileNumber = request.form['mobileNumber']

        db.session.commit()
        flash(" Updated Successfully")

        return redirect(url_for('Pending'))


@app.route('/Move_to_Author', methods=['GET', 'POST'])
def Move_to_Author():
    if request.method == 'POST':
        print(request.form['userId'])
        borrowerId = request.form['userId']
        borrowerName = request.form['borrowerName']
        email = request.form['email']
        mobileNumber = request.form['mobileNumber']
        my_data = Authorization(borrowerId, borrowerName, email, mobileNumber)
        db.session.add(my_data)
        #delete_data = PendingRequests.query.get(request.form.get('id'))
        #db.session.delete(delete_data)
        db.session.commit()
        flash("Move_to_Author Successfully")
        data = Authorization.query.all()
        return render_template("Authorization Requests.html", employees=data)

@app.route('/Move_to_Reject', methods=['POST'])
def Move_to_Reject():

    if request.method == 'POST':

        borrowerId = request.form['userId']
        borrowerName = request.form['borrowerName']
        email = request.form['email']
        mobileNumber = request.form['mobileNumber']

        my_data = RejectedApplications(borrowerId,borrowerName,email,mobileNumber )
        db.session.add(my_data)
        print(123)
        #delete_data = PendingRequests.query.get(request.form.get('id'))
        print(456)
        #db.session.delete(delete_data)
        print(789)
        db.session.commit()
        print(987)
        flash("Move to rejected successfully")

        data = RejectedApplications.query.all()

        return render_template("Rejected Applications.html", employees=data)

@app.route('/Move_to_Approve', methods=['GET', 'POST'])
def Move_to_Approve():
    if request.method == 'POST':
        print("hello")
        print(request.form['creditLimit'])
        borrowerId = request.form['userId']
        borrowerName = request.form['borrowerName']
        email = request.form['email']
        mobileNumber = request.form['mobileNumber']
        creditLimit = request.form['creditLimit']
        my_data = ManageRequests(borrowerId, borrowerName, email, mobileNumber,creditLimit)
        db.session.add(my_data)
        #delete_data = PendingRequests.query.get(request.form.get('id'))
        #db.session.delete(delete_data)
        db.session.commit()
        flash("Approved Successfully")
        data = ManageRequests.query.all()
        return render_template("Manage Borrowers.html", employees=data)


@app.route('/Move_to_Close', methods=['GET', 'POST'])
def Move_to_Close():
    if request.method == 'POST':
        print("hello")
        print(datetime.now())
        # loan_id = request.form['loan_id']
        loan_id = 9
        # browerName = request.form['browerName']
        browerName = 'jay'

        # @app.route('/request/<id>', methods=['GET'])
        # def get_PendingRequest_by_id(id):
        #     get_PendingRequest = ClosedLoans.query.get(id)
        #     loans_schema = LoansSchema(many=True)
        #     creditLimit = loans_schema.dump(get_PendingRequest)
        #     return make_response(jsonify({"creditLimit": creditLimit}))

        lenderName = 'abc'
        creditLimit = 8
        rom = 1080
        disbDate = '2020-06-02'
        loanAmt = 1000
        tenure = 90
        interest = 98
        procFee = 890
        # repayAmt = request.form['repayAmt']
        repayAmt = 40
        closedDate = '2020-06-02'
        resiveAmt = 8

        my_data = ClosedLoans(loan_id, browerName, lenderName, creditLimit, rom, disbDate, loanAmt, tenure, interest,
                              procFee, repayAmt, closedDate, resiveAmt)
        db.session.add(my_data)
        # db.session.commit()
        # flash("Closed Successfully")

        print('hii')
        # print((request.form['resiveAmt'])-(request.form['repayAmt']))
        print('print123')
        number = 1
        # loan_id = request.form['loan_id']
        loan_id = 45
        res = request.form['resiveAmt']
        print(res)
        pid = request.form['repayAmt']
        print((pid))
        print(int(res) - int(pid))
        arrearamount = int(res) - int(pid)
        browerName = 'san'
        repayAmt = request.form['repayAmt']
        # arrearamount = request.form['arrears']
        my_new = Arrears(number, loan_id, arrearamount, browerName, repayAmt)

        db.session.add(my_new)

        db.session.commit()
        flash("Moved to Arrears")

        dn = ClosedLoans.query.all()
        return render_template("Closed Loans.html", employees=dn)


@app.route('/Move_to_Lender', methods=['POST'])
def Move_to_Lender():

    if request.method == 'POST':
        # print(request.form)

        loan_id = request.form['loan_id']
        lender_id = request.form.getlist('lender_names[]')


        lendershare_amount = 0
        nowTime = datetime.now();
        assignedDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = "pending"
        loanAmount = request.form['loanAmount']
        repaymentDate = request.form['repaymentDate']

        my_data = MappedLender(loan_id,assignedDate,status, loanAmount,repaymentDate)
        db.session.add(my_data)
        # nowTime.strftime('%Y-%m-%d %H:%M:%S'
        for lender in lender_id:
            my_data1 = LenderLoanMapping(loan_id, lender, 0,nowTime,nowTime)
            db.session.add(my_data1)

        db.session.commit()
        flash("Moved to Mapped Lender")

        # date = MappedLender.query.all()

        return redirect("/mapping")

@app.route('/Move_to_Rej', methods=['POST'])
def Move_to_Rej():

    if request.method == 'POST':
        loan_id = request.form['loan_id']
        browerName = request.form['browerName']
        mobilenumber = request.form['mobilenumber']
        creditLimit = request.form['creditLimit']
        loanAmount = request.form['loanAmount']
        days = request.form['days']
        interstPayable = request.form['interstPayable']
        processingFee = request.form['processingFee']
        requesteddate = request.form['requesteddate']
        repaymentAmount = request.form['repaymentAmount']
        repaymentDate = request.form['repaymentDate']
        my_data = RejectedLoans(loan_id, browerName, mobilenumber, creditLimit,loanAmount,days, interstPayable,processingFee,requesteddate,repaymentAmount,repaymentDate)
        db.session.add(my_data)
        db.session.commit()
        flash("Moved to Rejected Loans")

        date = RejectedLoans.query.all()

        return render_template("Rejected Loans.html", employees=date)


@app.route('/Export_to_Excel', methods=['POST'])
def Export_to_Excel():

    if request.method == 'POST':
        loan_id = request.form['loan_id']
        browerName = request.form['browerName']
        loantype = "personal"
        nooflenders = request.form['nooflenders']
        loanAmount = request.form['loanAmount']
        repaymentAmount = request.form['repaymentAmount']
        requesteddate = request.form['requesteddate']
        repaymentDate = request.form['repaymentDate']

        my_data = SendtoBank(loan_id, browerName,loantype,nooflenders, loanAmount,repaymentAmount,requesteddate,repaymentDate)
        db.session.add(my_data)
        db.session.commit()
        flash("Moved to Bank Loans")

        date = SendtoBank.query.all()

        return render_template("Sent to Bank.html", employees=date)


@app.route('/Move_to_Transit', methods=['POST'])
def Move_to_Transit():
    if request.method == 'POST':
        loan_id = request.form['loan_id']
        loanAmount = request.form['loanAmount']
        repaymentAmount = request.form['repaymentAmount']
        repaymentDate = request.form['repaymentDate']

        my_data = Transit(loan_id, loanAmount, repaymentAmount, repaymentDate)
        db.session.add(my_data)
        db.session.commit()
        flash("Moved to Transit ")

    date = Transit.query.all()

    return render_template("Transit.html", employees = date)

# This route is for deleting our employee
@app.route('/delete_data/<id>/', methods=['GET', 'POST'])
def delete_data(id):
    my_data = PendingRequests.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash(" Deleted Successfully")

    return redirect(url_for('Pending'))


@app.route('/rejected')
def Rejected():
    db = RejectedApplications.query.all()


    return render_template("Rejected Applications.html", employees = db)


# this route is for inserting data to mysql database via html forms
@app.route('/insert2', methods=['POST'])
def insert2():
    if request.method == 'POST':

        borrowerId = request.form['userId']
        borrowerName = request.form['borrowerName']
        email = request.form['email']
        mobileNumber = request.form['mobileNumber']

        my_data = RejectedApplications(borrowerId,borrowerName,email,mobileNumber )
        db.session.add(my_data)
        print(123)
        #delete_data = PendingRequests.query.get(request.form.get('id'))
        print(456)
        #db.session.delete(delete_data)
        print(789)
        db.session.commit()
        print(987)
        flash("Move to rejected successfully")

        data = RejectedApplications.query.all()

        return render_template("Authorization Requests.html", employees=data)


# this is our update route where we are going to update our employee
@app.route('/update2', methods=['GET', 'POST'])
def update2():
    if request.method == 'POST':
        my_data = RejectedApplications.query.get(request.form.get('borrowerId'))

        my_data.borrowerId = request.form['borrowerId']
        my_data.borrowerName = request.form['borrowerName']
        my_data.email = request.form['email']
        my_data.mobileNumber = request.form['mobileNumber']


        db.session.commit()
        flash(" Updated Successfully")

        return redirect(url_for('Rejected'))


# This route is for deleting our employee
@app.route('/delete2/<id>/', methods=['GET', 'POST'])
def delete2(id):
    my_data = RejectedApplications.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash(" Deleted Successfully")

    return redirect(url_for('Rejected'))

@app.route('/manage')
def Manage():
    data = ManageRequests.query.all()

    return render_template("Manage Borrowers.html", employees = data)


# this route is for inserting data to mysql database via html forms
@app.route('/insert3', methods=['POST'])
def insert3():
    if request.method == 'POST':
        borrowerId = request.form['borrowerId']
        borrowerName = request.form['borrowerName']
        email = request.form['email']
        mobileNumber = request.form['mobileNumber']
        creditlimit = request.form['creditlimit']


        my_data = ManageRequests(borrowerId,borrowerName,email,mobileNumber, creditlimit)
        db.session.add(my_data)
        db.session.commit()

        flash("Inserted Successfully")

        return redirect(url_for('Manage'))


# this is our update route where we are going to update our employee
@app.route('/update3', methods=['GET', 'POST'])
def update3():
    if request.method == 'POST':
        my_data = ManageRequests.query.get(request.form.get('id'))

        my_data.borrowerId = request.form['borrowerId']
        my_data.borrowerName = request.form['borrowerName']
        my_data.email = request.form['email']
        my_data.mobileNumber = request.form['mobileNumber']
        my_data.creditlimit = request.form['creditlimit']

        db.session.commit()
        flash(" Updated Successfully")

        return redirect(url_for('Manage'))


# This route is for deleting our employee
@app.route('/delete3/<id>/', methods=['GET', 'POST'])
def delete3(id):
    my_data = ManageRequests.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash(" Deleted Successfully")

    return redirect(url_for('Manage'))



@app.route('/disbursed')
def Loans():
    data1 =DisbursedLoans.query.all()

    return render_template("Disbursed Loans.html", employees = data1)


# this route is for inserting data to mysql database via html forms
@app.route('/insert4', methods=['POST'])
def insert4():
    if request.method == 'POST':
        loan_id = request.form['loan_id']
        browerName = request.form['browerName']
        lenderNameid = request.form['lenderNameid']
        disbDate = request.form['disbursedDate']
        amtDisb = request.form['amountDisbursed']
        tenure = request.form['tenure']
        interest = request.form['interest']
        procFee = request.form['processingFee']
        repayAmt = request.form['repaymentAmount']
        repayDate = request.form['repaymentDate']
        referencenumber = request.form[' referencenumber']

        my_data = DisbursedLoans(loan_id, browerName, lenderNameid, disbDate, amtDisb, tenure, interest, procFee,
                                 repayAmt, repayDate, referencenumber)
        db.session.add(my_data)
        db.session.commit()

        flash("Inserted Successfully")

        return redirect(url_for('Loans'))


# this is our update route where we are going to update our employee
@app.route('/update4', methods=['GET', 'POST'])
def update4():
    if request.method == 'POST':
        my_data = DisbursedLoans.query.get(request.form.get('id'))

        my_data.loanId = request.form['loanId']
        my_data.borrower = request.form['borrower']
        my_data.lenderName = request.form['lenderName']
        my_data.disbDate = request.form['disbDate']
        my_data.amtDisb = request.form['amtDisb']
        my_data.tenure = request.form['tenure']
        my_data.interest = request.form['interest']
        my_data.procFee = request.form['procFee']
        my_data.repayAmt = request.form['repayAmt']
        my_data.repayDate = request.form['repayDate']

        db.session.commit()
        flash(" Updated Successfully")

        return redirect(url_for('Loans'))


# This route is for deleting our employee
@app.route('/delete4/<id>/', methods=['GET', 'POST'])
def delete4(id):
    my_data =DisbursedLoans.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash(" Deleted Successfully")

    return redirect(url_for('Loans'))

@app.route('/authorize')
def Authorize():
    db1 = Authorization.query.all()

    return render_template("Authorization Requests.html", employees = db1)


# this route is for inserting data to mysql database via html forms
@app.route('/insert5', methods=['POST'])
def insert5():
    if request.method == 'POST':
        borrowerId = request.form['borrowerId']
        borrowerName = request.form['borrowerName']
        email = request.form['email']
        mobileNumber = request.form['mobileNumber']

        my_data = Authorization(borrowerId,borrowerName,email,mobileNumber )
        db.session.add(my_data)
        db.session.commit()

        flash("Inserted Successfully")

        return redirect(url_for('Authorize'))


# this is our update route where we are going to update our employee
@app.route('/update5', methods=['GET', 'POST'])
def update5():
    if request.method == 'POST':
        my_data = Authorization.query.get(request.form.get('id'))

        my_data.borrowerId = request.form['borrowerId']
        my_data.borrowerName = request.form['borrowerName']
        my_data.email = request.form['email']
        my_data.mobileNumber = request.form['mobileNumber']


        db.session.commit()
        flash(" Updated Successfully")

        return redirect(url_for('Authorize'))
# This route is for deleting our employee
@app.route('/delete5/<id>/', methods=['GET', 'POST'])
def delete5(id):
    my_data = Authorization.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash(" Deleted Successfully")

    return redirect(url_for('Authorize'))

@app.route('/insert_data_pending', methods=['POST'])
def insert_data_pending():
    if request.method == 'POST':
        my_data = PendingRequests.query.get(request.form.get('id'))
        borrowerId = my_data.userId
        borrowerName = my_data.borrowerName
        email = my_data.email
        mobileNumber = my_data.mobileNumber

        my_data = Authorization(borrowerId,borrowerName,email,mobileNumber )
        db.session.add(my_data)
        delete_data = PendingRequests.query.get(request.form.get('id'))
        db.session.delete(delete_data)
        db.session.commit()
        flash("Move to authorization Successfully")
        data = PendingRequests.query.all()
        return render_template("Authorization Requests.html",emp=data)

@app.route('/closed')
def Closed():
    dn = ClosedLoans.query.all()

    return render_template("Closed Loans.html", employees=dn)

@app.route('/close', methods=['POST'])
def close():
    if request.method == 'POST':
        loanId = request.form['loanId']
        borrowerName = request.form['borrowerName']
        lenderName = request.form['lenderName']
        creditLimit = request.form['creditLimit']
        rom = request.form['rom']
        disbDate = request.form['disbursedDate']
        loanAmt = request.form['loanAmt']
        tenure = request.form['tenure']
        interest = request.form['interest']
        procFee = request.form['processingFee']
        repayAmt = request.form['repaymentAmount']
        paidAmt = request.form['paidAmt']
        closedDate = request.form['closedDate']

        my_data = DisbursedLoans(loanId, borrowerName, lenderName,creditLimit,rom, disbDate,loanAmt,tenure,interest,
                                 procFee,repayAmt,paidAmt,closedDate )
        db.session.add(my_data)
        db.session.commit()

        flash("Inserted Successfully")

        return redirect(url_for('Loans'))

@app.route('/request')
def Request():
    data = PendingRequest.query.all()
    #loan_id = request.form['loan_id']

    url = "http://15.206.199.1:8080/Digiloanjune14/api/getAllNewLoanRequests"
    r = requests.get(url)

    # url1 = "http://15.206.199.1:8080/LenderAppjune22/lender/getLenderDetailsBasedOnids"
    # s = requests.get(url1)
    # #
    # json_data_lender = json.loads(s.text)
    json_data = json.loads(r.text)

    list = []
    for datalist in json_data['reg']:
        listobj = {}
        listobj['loan_id'] = datalist['loan_id']
        listobj['browerName'] = datalist['browerName']
        listobj['mobilenumber'] = datalist['mobilenumber']
        listobj['profileScore'] = datalist['profileScore']
        listobj['loanType'] = datalist['loanType']
        listobj['creditLimit'] = datalist['creditLimit']
        listobj['loanAmount'] = datalist['loanAmount']
        listobj['days'] = datalist['days']
        listobj['interstPayable'] = datalist['interstPayable']
        listobj['processingFee'] = datalist['processingFee']
        listobj['promocode'] = datalist['promocode']
        listobj['repaymentAmount'] = datalist['repaymentAmount']
        listobj['requesteddate'] = datalist['requesteddate']
        listobj['repaymentDate'] = datalist['repaymentDate']
        #requesteddate = datetime.strptime("21/07/2020", "%d/%m/%Y").strftime("%Y-%m-%d")
        #print(datalist['requesteddate'].strftime("%Y-%m-%d"))
        list.append(listobj)
        # print(list)
       # result = db.engine.execute(text('select * from pending_request where loan_id = :loanID'),
       #                            loanID=loan_id).first();
        #listobj['browerName'] = result[1]
    url = "http://15.206.199.1:8080/LenderAppjune22/lender/getLenderDetailsBasedOnids"
    joined_string = "1,2"
    data = {'userids': joined_string}
    r = requests.post(url, params={'userids': joined_string})
    json_data = json.loads(r.text)

    return render_template("Pending Request.html", employees=list, lender = json_data['data'])


@app.route('/mapping')
def Lender():
    data = db.engine.execute("select * from mapped_lender")

    list = []
    for r in data:
        print('loan_id',r.loan_id)
        listobj = {}
        listobj['loan_id'] = r.loan_id
        datalender = db.engine.execute("select lender_id,lender_share_amount from lender_loan_mapping where loan_id=1")
        lenderIds = [];
        lenderShareAmount = [];
        for x in datalender:
             print('le',x.lender_id)
             lenderIds.append(x.lender_id)
             lenderShareAmount.append(x.lender_share_amount)

        joined = [str(element) for element in lenderIds]
        joined_string = ",".join(joined)
        print('joined_string',joined_string)
        # url = "http://15.206.199.1:8080/LenderAppjune22/lender/getLenderDetailsBasedOnids"
        # data = {'userids': joined_string}
        # r = requests.post(url, params={'userids': joined_string})
        # json_data = json.loads(r.text)
        # print('json_data',json_data)
        lenderNames = [];
        # for datalist in json_data['data']:
        #     print(datalist)
        #     lenderNames.append(datalist['firstName'])

        lenderNames.append('ganga')
        print('lenderNames',lenderNames)
        joinedlenderNames = [str(element) for element in lenderNames]
        print('joinedlenderNames',joinedlenderNames)
        joined_string = ",".join(joinedlenderNames)

        joinedlenderShareAmount = [str(element) for element in lenderShareAmount]
        print('joinedlenderShareAmount', joinedlenderShareAmount)
        joined_string_amount = ",".join(joinedlenderShareAmount)

        print(joined_string);
        print(joined_string_amount);
        print('sum',sum(lenderShareAmount));
        totalShare = sum(lenderShareAmount)
        if(totalShare ==0):
            fulfillment = 0
        else:
            fulfillment = (r.loanAmount/totalShare)*100

        listobj['lastname'] = joined_string;
        listobj['fulfillment'] = 30;
        listobj['lendershare_amount'] = joined_string_amount;
        listobj['assignedDate'] = r.assignedDate;
        listobj['status'] = r.status;
        listobj['loanAmount'] = r.loanAmount;
        listobj['repaymentDate'] = r.repaymentDate;
        list.append(listobj)




    # list =[]
    # for datalist in json_data['data']:
    #     listobj ={}
    #     listobj['lastname'] = datalist['lastname']
    #     listobj['lender_share_amount'] = datalist['lender_share_amount']
    #
    #     list.append(listobj)

    # data = MappedLender.query.all()
    # url = "http://15.206.199.1:8080/LenderAppjune22/lender/getLenderDetailsBasedOnids"
    # data = {'userids':1}
    # r = requests.post(url, data)
    # json_data = json.loads(r.text)
    # print(json_data)


    # my_list = list()


    # url = "http://15.206.199.1:8080/LenderAppjune22/lender/getLenderDetailsBasedOnids"
    # data = {'userids':1}
    # r = requests.post(url, data)
    # json_data = json.loads(r.text)
    # print(json_data)
    # list = []
    # for datalist in json_data['data']:
    #     listobj ={}
    #     listobj['firstname'] = datalist['firstname']
    #     listobj['lastname'] = datalist['lastname']
    #     list.append(listobj)


            # api hit with list of ids
            # data with lender  names
            # common separates names
            # r.lender =assign here common separates names


    # print(json.dumps([dict(r) for r in data]))
    # data = MappedLender.query.all()
    # url = "http://15.206.199.1:8080/LenderAppjune22/lender/getAllLenderdata"
    #     # #data = {'userid':12}
    #     # r = requests.post(url)
    #     # json_data = json.loads(r.text)
    #     #

    return render_template("Mapped Lender.html", employees=list)


@app.route('/transit')
def transit():
    date = Transit.query.all()


    return render_template("Transit.html", employees=date)


@app.route('/Bank')
def Bank():
    dn = SendtoBank.query.all()

    return render_template("Sent to Bank.html", employees=dn)

@app.route('/insert_data', methods=['POST'])
def insert_data():
    if request.method == 'POST':
        loan_id = request.form['loan_id']
        disbDate = request.form['disbDate']
        # loanamount = request.form ['loanamount']
        # print(loanamount)
        # amtDisb = loanamount - 700 #disburced amout= loan-700 please verify with some one
        #
        # # amtDisb = request.form['amtDisb']
        # repay = request.form['repayDate']
        # print((repay))
        # date = request.form['disbDate']
        # repay1=datetime(repay,"%Y-%m-%d")
        # dat2= datetime(date, "%Y-%m-%d")
        # tennure= (dat2-repay1).days
        # intrst_percentage = 0.15*tennure
        # intrst_amount=(loanamount*intrst_percentage)/100
        # print((repay1))
        # # percentage=
        # print(tennure)
        #
        #
        #
        # @app.route('/products/<id>', methods=['GET'])
        # def get_product_by_id(id):
        #     get_product = PendingRequest.query.get(id)
        #     product_schema = ProductSchema()
        #     product = product_schema.dump(get_product)
        #     return make_response(jsonify({"product": product}))
        #
        # # @app.route('/products/<id>', methods=['GET'])
        # # def get_PendingRequest_by_id(id):
        # #     get_PendingRequest = DisbursedLoans.query.get(id)
        # #     loans_schema = LoansSchema(many=True)
        # #     disbursed= loans_schema.dump(get_PendingRequest)
        # #
        # #     return make_response(jsonify({"disbursed":disbursed}))
        #

        # url = "http://15.206.199.1:8080/Digiloanjune14/api/getLenderDetailsBasedOnids";
        # r = requests.post(url, params={'userids': '1,2,3'})
        # json_data = json.loads(r.text)
        # print(json_data);
        result = db.engine.execute(text('select * from pending_request where loan_id = :loanID'),
                  loanID = loan_id).first();

        reqDate = result[12];

        if(reqDate == disbDate):
            browerName = result[1];
            lenderName = 'Sravya'
            amtDisb = result[6]
            repayAmt = result[11];
            interest = result[8]
            procFee = result[9]
            tenure = result[7]
            repayDate = result[13]
            referencenumber = request.form['referencenumber']
        else:

            reqDate : reqDate
            disbDate : disbDate

            print(type(str(reqDate)))
            start_date = datetime.strptime(str(reqDate), "%Y-%m-%d")
            end_date = datetime.strptime(str(disbDate),"%Y-%m-%d")
            # print
            # abs((end_date - start_date).days)
            # delta = dt.strptime(reqDate, "%m/%d/%y") - dt.strptime(disbDate, "%m/%d/%y");



            fixedintper = 4.5
            # delta = reqDate - disbDate
            delayDays =abs((end_date - start_date).days);
            print(delayDays);
            TotalDays = result[7] - delayDays;
            print(TotalDays);
            perDayInterest = 0.15;
            print(perDayInterest)
            perDayIntAmount = (result[6]*perDayInterest)/100;
            print(perDayIntAmount)
            totalIntAmount = perDayIntAmount * TotalDays;
            print(totalIntAmount)
            totalRepayAmount = result[9] +  result[6] + totalIntAmount;
            print(totalRepayAmount)
            browerName = result[1];
            lenderName = 'Sravya'
            amtDisb = result[6]
            repayAmt = totalRepayAmount
            interest = totalIntAmount
            procFee = result[9]
            tenure = result[7]
            repayDate = result[13]
            referencenumber = request.form['referencenumber']


        my_data = DisbursedLoans(loan_id, browerName, lenderName, disbDate, amtDisb, tenure, interest, procFee,
                                 repayAmt,
                                 repayDate, referencenumber)
        db.session.add(my_data)

        db.session.commit()

        flash("Inserted Successfully")
        data1 = DisbursedLoans.query.all()

        return render_template("Disbursed Loans.html", employees=data1)


@app.route('/Rejected_loans')
def Rejected_loans():
    dn = RejectedLoans.query.all()

    return render_template('Rejected Loans.html', employees=dn)

@app.route('/Rej_loans', methods=['POST'])
def Rej_loans():
    if request.method == 'POST':
        loanId = request.form['loanId']
        borrower = request.form['borrower']
        mobilenumber = request.form['mobilenumber']
        creditlimit = request.form['creditlimit']
        loanamount = request.form['loanamount']
        tenure = request.form['tenure']
        interest = request.form['interest']
        processingfee = request.form['processingfee']
        requestdate = request.form['requestdate']
        dueamount = request.form['dueamount']
        duedate = request.form['duedate']

        my_data = RejectedLoans(loanId, borrower, mobilenumber,creditlimit,loanamount,tenure,interest,processingfee,requestdate,dueamount,duedate )
        db.session.add(my_data)
        db.session.commit()

        flash("Inserted Successfully")

        return redirect(url_for('Rej_loans'))

@app.route('/arrears')
def arrears():
    data = Arrears.query.all()
    return render_template("Arrears.html", employees=data)

# This route is for deleting our employee
@app.route('/delete9/<id>/', methods=['GET', 'POST'])
def delete9(id):
    my_data = Arrears.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash(" Deleted Successfully")

    return redirect(url_for('arrears'))

@app.route('/todaysdues')
def Todaysdues():
    dn = TodaysDues.query.all()

    return render_template("Todays Dues.html", employees=dn)


@app.route('/defaulters')
def Defaulters():
    dn = Defaulters.query.all()

    return render_template("Defaulters.html", employees=dn)


@app.route('/npa')
def NPA():
    dn = Npa.query.all()

    return render_template("NPA.html", employees=dn)


@app.route('/progress')
def progress():
    def generate():
        x = 0

        while x <= 100:
            yield "data:" + str(x) + "\n\n"
            x = x + 10
            time.sleep(0.5)

    return Response(generate(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)

