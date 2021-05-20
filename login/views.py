import mysql.connector
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
import random

# Create your views here.
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="123456",
    database="Company"
)
mycursor = mydb.cursor()

global username
username = ''

# email
global email
email = ''

global name
name = ''

def login_view(request, *args, **kwargs):
    dataList = []
    print("hello")

    if request.method == "POST":
        print("da5al function")
        user_email = request.POST.get('email')

        print("da al email el user mdakhlo: " + str(user_email))
        dataList.append(user_email)
        password = request.POST.get("password")
        dataList.append(password)

        try:
            print("try")
            sql = "Select username, password , email, name From accounts where email =%s"
            val = (user_email,)
            mycursor.execute(sql, val)
            myresult = mycursor.fetchone()
            username = myresult[0]
            password = myresult[1]
            email = myresult[2]
            name = myresult[3]

            request.session['email'] = email
            request.session['username'] = username
            request.session['name'] = name
            print(request.session['username'])
            print(myresult[0])
            print(myresult[1])
            print("5alas awel try")
            if myresult[2] == user_email:
                return render(request, "home.html", {"username": request.session['username'], "email": myresult[2], "name": myresult[3]})
        except:
            return render(request, "login.html", {})

    return render(request, "login.html", {})

def profile_view(request, *args, **kwargs):
    username = request.session['username']
    email = request.session['email']
    name = request.session['name']
    print(username)
    print(email)
    print(email)
    return render(request, "profile.html", {"username": username, "email": email, "name": name})


def forgot_password(request):
    return render(request, "forgot_password.html")


def send_code(request):
    email = request.session['email']
    #  random number
    number = str(random.randint(100000, 999999))
    #  Put the message in the browser
    request.session['message'] = number
    #  E-mail verification code
    send_mail("Reset password", "Reset password verification code:"+number, "youssef.maha29@gmail.com", [email])
    print(number)
    return render(request, "password_change.html")

def password_change(request):
    if request.method == "POST":
        username = request.session['username']
        verification_code = request.session['message']
        code = request.POST.get('verification_code')
        print(code)
        print(verification_code)
        new_password = request.POST.get('new_password1')
        new_password_confirm = request.POST.get('new_password2')
        if(verification_code == code):
            if (new_password == new_password_confirm):
                print("da5al el condition")
                try:
                    sql = "update accounts  set password=%s where username= %s"
                    val = (new_password, username)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print("check database")
                    return HttpResponse("Successfully reset!")
                except:
                    return render(request, "password_change.html", {})
            return HttpResponse("Passwords doesn't match")
        return HttpResponse("The verification code is wrong or expired!")
    return render(request, "password_change.html", {})

