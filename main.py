from fastapi import FastAPI,Request,Form
from fastapi.responses import HTMLResponse,RedirectResponse
import psycopg2
from fastapi.staticfiles import StaticFiles
from psycopg2.extras import RealDictCursor
from fastapi.templating import Jinja2Templates
from typing import Union
from starlette.middleware.sessions import SessionMiddleware
app=FastAPI() 
app.add_middleware(SessionMiddleware,secret_key="kaviya")
templates=Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")
import os

def connect_database():
    return psycopg2.connect(os.getenv("DATABASE_URL"))
@app.get("/")
def display(request:Request,error:str=""):
    return templates.TemplateResponse("login.html",{"request":request,"error":error})
@app.post("/")
def getdata(request:Request,UserName:str=Form(...),PassWord:str=Form(...),UserType:str=Form(...),Balance:Union[float,str,None]=Form(None)):
    if Balance == "" or Balance is None:
        Balance = None
    conn=connect_database()
    cur=conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("select * from user_data where \"Username\"=%s;",(UserName,))
    u=cur.fetchone()
    if u:
       if u['password']==PassWord:
           us=u['user_type'].strip().lower()
           if us=='admin':
               cur.close()
               conn.close()
               request.session['username']=UserName
               request.session['password']=PassWord
               request.session['balance']=Balance
               request.session['user_type']=UserType
               return RedirectResponse(url="/admin",status_code=303)
           if us=='investor':
               cur.close()
               conn.close()
               request.session['username']=UserName
               request.session['password']=PassWord
               request.session['balance']=Balance
               request.session['user_type']=UserType
               return RedirectResponse(url="/investor",status_code=303)
           else:
               cur.close()
               conn.close()
               return templates.TemplateResponse("login.html",{"request":request,"error":"Invalid type"})
       else:
           cur.close()
           conn.close()
           return templates.TemplateResponse("login.html",{"request":request,"error":"Error:Invalid password!"})
    else:
        if UserType.strip().lower() not in ['admin','investor']:
            cur.close()
            conn.close()
            return templates.TemplateResponse("login.html",{"request":request,"error":"Invalid type"})
        us=UserType.strip().lower()
        if us=='investor' and Balance is None:
            cur.close()
            conn.close()
            return templates.TemplateResponse("login.html",{"request":request,"error":"Investor must enter balance!"})
        cur.execute("Insert into user_data(\"Username\",password,user_type,balance)values(%s,%s,%s,%s);",(UserName,PassWord,UserType,Balance))
        conn.commit()  
        request.session['username']=UserName
        request.session['password']=PassWord
        request.session['balance']=Balance
        request.session['user_type']=UserType
        cur.close()
        conn.close()
        if us=='admin':
            return RedirectResponse(url="/admin",status_code=303)
        if us=='investor':
            return RedirectResponse(url="/investor",status_code=303)
@app.get("/admin")
def display_admin(request:Request):
    return templates.TemplateResponse("admin.html",{"request":request})
@app.get("/investor")
def display_investor(request:Request):
    return templates.TemplateResponse("ivestoroption.html",{"request":request})
@app.get("/investor/new")
def display_newinvestor(request:Request):
    return templates.TemplateResponse("newinvest.html",{"request":request})
@app.get("/investor/exist")
def display_existsinvestor(request:Request):
    return templates.TemplateResponse("einvestor.html",{"request":request})
@app.get("/admin/viewusers")
def display_stocks(request:Request):
    conn=connect_database()
    cur=conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("select * from user_data where user_type='investor';")
    investors=cur.fetchall()
    cur.close()
    conn.close()
    return templates.TemplateResponse("userdetail.html",{"request":request,"investors":investors})
@app.get("/add_user")
def display_form(request:Request):
    return templates.TemplateResponse("addform.html",{"request":request})
@app.post("/add_user") 
def get_data(UserName:str=Form(...),PassWord:str=Form(...),Balance:float=Form(...)):
    conn=connect_database()
    cur=conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("Insert into user_data(\"Username\",password,user_type,balance)values(%s,%s,%s,%s)",(UserName,PassWord,'investor',Balance))
    conn.commit()
    cur.close()
    conn.close()
    return RedirectResponse(url="/admin/viewusers",status_code=303)
@app.get("/delete_user")
def display_form(request:Request):
    return templates.TemplateResponse("removeform.html",{"request":request})
@app.post("/delete_user")
def delete_user(request: Request, UserName: str = Form(...)):
    conn = connect_database()
    cur = conn.cursor(cursor_factory=RealDictCursor)

   
    cur.execute("DELETE FROM purchase WHERE \"Username\" = %s;", (UserName,))
    
    
    cur.execute("DELETE FROM user_data WHERE \"Username\" = %s;", (UserName,))

    conn.commit()
    cur.close()
    conn.close()
    return RedirectResponse(url="/admin/viewusers", status_code=303)

@app.get("/admin/viewstocks")
def display_stocks(request:Request):
    conn=connect_database()
    cur=conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("select * from stocks;")
    stocks=cur.fetchall()
    cur.close()
    conn.close()
    return templates.TemplateResponse("stockdisplay.html",{"request":request,"stocks":stocks})   
@app.get("/admin/addstock")
def display_form(request:Request):
    return templates.TemplateResponse("addstock.html",{"request":request})
@app.post("/admin/addstock")
def get_data(request:Request,stockid:int=Form(...),stocksymbol:str=Form(...),company:str=Form(...),Price:float=Form(...),Available_shares:float=Form(...),Sector:str=Form(...),Rating:float=Form(...)):
    conn=connect_database()
    cur=conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('Insert into stocks(stockid,symbol,company,"price(per share)",available_shares,sector,rating)values(%s,%s,%s,%s,%s,%s,%s)',(stockid,stocksymbol,company,Price,Available_shares,Sector,Rating))
    conn.commit()
    cur.close()
    conn.close()
    return RedirectResponse(url="/admin/viewstocks",status_code=303)
@app.get("/delete_stock")
def display_delete_form(request:Request):
    return templates.TemplateResponse("deleteform.html",{"request":request})
@app.post("/deletestock")
def delete_stock(request:Request,stocksymbol:str=Form(...)):
    conn=connect_database()
    cur=conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("delete from stocks where symbol=%s;",(stocksymbol,))
    conn.commit()
    conn.close()
    cur.close()
    return RedirectResponse(url="/admin/viewstocks",status_code=303)
@app.get("/investor/Register")
def display_register(request:Request):
    uname=request.session.get("username")
    pword=request.session.get("password")
    return templates.TemplateResponse("newuser.html",{"request":request,"uname":uname,"pword":pword})
@app.post("/investor/Register")
def get_register_data(request:Request,Balance:float=Form(...)):
    conn=connect_database()
    cur=conn.cursor(cursor_factory=RealDictCursor)
    uname=request.session.get("username")
    pword=request.session.get("password")
    cur.execute("Update user_data set  balance= %s where \"Username\"=%s and password=%s;",(Balance,uname,pword))
    conn.commit()
    cur.close()
    conn.close()
    return RedirectResponse(url="/investor/new",status_code=303)
@app.get("/view_stocks")
def displaystocks(request:Request):
    conn=connect_database()
    cur=conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("select * from stocks;")
    stocks=cur.fetchall()  
    return templates.TemplateResponse("stockbyuser.html",{"request":request,"stocks":stocks})
@app.get("/feedback")
def display_feedback(request: Request):
    return templates.TemplateResponse("feedbackform.html", {"request": request})

@app.post("/feedback")
def get_feedback(request: Request, email: str = Form(...), desc: str = Form(...)):
    conn = connect_database()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    
    cur.execute('SELECT description FROM feedback_user WHERE emailid = %s;', (email,))
    description = cur.fetchone()

    if description is None:
       
        cur.execute('INSERT INTO feedback_user (emailid, description) VALUES (%s, %s);', (email, desc))
    else:
      
        cur.execute('UPDATE feedback_user SET description = %s WHERE emailid = %s;', (desc, email))

    conn.commit()
    cur.close()
    conn.close()
    return RedirectResponse(url="/", status_code=303)
@app.get("/suggestions")
def display(request:Request):
    conn=connect_database()
    cur=conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("select * from feedback_user;")
    feedbacks=cur.fetchall()
    return templates.TemplateResponse("adminfb.html",{"request":request,"feedbacks":feedbacks})
@app.get("/buy")
def get_buy(request:Request):
    conn=connect_database()
    cur=conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("select * from stocks;")
    stocks=cur.fetchall()
    return templates.TemplateResponse("stockbyuser.html",{"request":request,"stocks":stocks})
from fastapi.responses import JSONResponse

@app.post("/buy")
def buy_stock(request: Request, symbol: str = Form(...), num_shares: int = Form(...), company: str = Form(...)):
    conn = connect_database()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    if num_shares <= 0:
        return JSONResponse({"error": "Invalid shares!"})

    cur.execute('SELECT "price(per share)", available_shares FROM stocks WHERE company=%s AND symbol=%s;', (company, symbol))
    row = cur.fetchone()

    if not row:
        return JSONResponse({"error": "Stock not found!"})

    price = row['price(per share)']
    avail = row['available_shares']

    if num_shares > avail:
        return JSONResponse({"error": f"Only {avail} shares available!"})

    total_price = num_shares * price
    uname = request.session.get("username")
    pword = request.session.get("password")

    cur.execute('SELECT balance FROM user_data WHERE "Username"=%s AND password=%s;', (uname, pword))
    balrow = cur.fetchone()

    if not balrow:
        return JSONResponse({"error": "User not found!"})

    balance = balrow['balance']

    if balance < total_price:
        return JSONResponse({"error": "Check your budget!"})

    remaining = balance - total_price

    
    cur.execute("UPDATE stocks SET available_shares = available_shares - %s WHERE symbol=%s AND company=%s;", (num_shares, symbol, company))
    cur.execute("INSERT INTO purchase(\"Username\", password, symbol, company, num_shares, price) VALUES (%s, %s, %s, %s, %s, %s);", (uname, pword, symbol, company, num_shares, price))
    cur.execute("UPDATE user_data SET balance = %s WHERE \"Username\"=%s AND password=%s;", (remaining, uname, pword))

    conn.commit()
    cur.close()
    conn.close()

    return JSONResponse({"message": "Successfully purchased!"})
@app.get("/investor/mystocks")
def display_userstocks(request: Request):
    conn = connect_database()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    uname = request.session.get("username")
    pword = request.session.get("password")
    cur.execute('''
        SELECT symbol, company, SUM(num_shares) AS num_shares, price
        FROM purchase
        WHERE "Username"=%s AND password=%s
        GROUP BY symbol, company, price
        ORDER BY company;
    ''', (uname, pword))
    my_purchase = cur.fetchall()
    cur.close()
    conn.close()
    return templates.TemplateResponse("mystocks.html", {"request": request, "my_purchase": my_purchase})
@app.post("/investor/mystocks")
def sell_stocks(request: Request, symbol: str = Form(...), num_shares: int = Form(...), company: str = Form(...)):
    conn = connect_database()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    uname = request.session.get("username")
    pword = request.session.get("password")

    cur.execute('''
        SELECT * FROM purchase
        WHERE "Username"=%s AND password=%s AND company=%s AND symbol=%s;
    ''', (uname, pword, company, symbol))

    row = cur.fetchone()

    if not row:
        conn.close()
        return JSONResponse({"error": "Stock not found!"})

    available_shares = row["num_shares"]
    if num_shares > available_shares:
        conn.close()
        return JSONResponse({"error": f"Only {available_shares} shares available!"})
    if num_shares == available_shares:
        cur.execute('DELETE FROM purchase WHERE "Username"=%s AND password=%s AND company=%s AND symbol=%s;',
                    (uname, pword, company, symbol))
    else:
        cur.execute('''
            UPDATE purchase
            SET num_shares = num_shares - %s
            WHERE "Username"=%s AND password=%s AND company=%s AND symbol=%s;
        ''', (num_shares, uname, pword, company, symbol))

    price_per_share = row['price']
    refund_amount = num_shares * price_per_share

    cur.execute('UPDATE user_data SET balance = balance + %s WHERE "Username"=%s AND password=%s;',
                (refund_amount, uname, pword))

    cur.execute('SELECT balance FROM user_data WHERE "Username"=%s AND password=%s;', (uname, pword))
    new_balance = cur.fetchone()["balance"]

    conn.commit()
    cur.close()
    conn.close()
    return JSONResponse({
        "message": f"✅ You sold {num_shares} shares of {company} ({symbol}). 💰 Balance: ₹{new_balance:.2f}"
    })
@app.get("/existing/view_stocks")
def display_stocks(request:Request):
    conn=connect_database()
    cur=conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("select * from stocks;")
    stocks=cur.fetchall()  
    return templates.TemplateResponse("stockeuser.html",{"request":request,"stocks":stocks})
@app.get("/exist/mystocks")
def display_userstocks(request: Request):
    conn = connect_database()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    uname = request.session.get("username")
    pword = request.session.get("password")
    cur.execute('''
        SELECT symbol, company, SUM(num_shares) AS num_shares, price
        FROM purchase
        WHERE "Username"=%s AND password=%s
        GROUP BY symbol, company, price
        ORDER BY company;
    ''', (uname, pword))
    my_purchase = cur.fetchall()
    cur.close()
    conn.close()
    return templates.TemplateResponse("mystockse.html", {"request": request, "my_purchase": my_purchase})
@app.post("/exist/mystocks")
def sell_stocks(request: Request, symbol: str = Form(...), num_shares: int = Form(...), company: str = Form(...)):
    conn = connect_database()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    uname = request.session.get("username")
    pword = request.session.get("password")

    cur.execute('''
        SELECT * FROM purchase
        WHERE "Username"=%s AND password=%s AND company=%s AND symbol=%s;
    ''', (uname, pword, company, symbol))

    row = cur.fetchone()

    if not row:
        conn.close()
        return JSONResponse({"error": "Stock not found!"})

    available_shares = row["num_shares"]
    if num_shares > available_shares:
        conn.close()
        return JSONResponse({"error": f"Only {available_shares} shares available!"})
    if num_shares == available_shares:
        cur.execute('DELETE FROM purchase WHERE "Username"=%s AND password=%s AND company=%s AND symbol=%s;',
                    (uname, pword, company, symbol))
    else:
        cur.execute('''
            UPDATE purchase
            SET num_shares = num_shares - %s
            WHERE "Username"=%s AND password=%s AND company=%s AND symbol=%s;
        ''', (num_shares, uname, pword, company, symbol))

    price_per_share = row['price']
    refund_amount = num_shares * price_per_share

    cur.execute('UPDATE user_data SET balance = balance + %s WHERE "Username"=%s AND password=%s;',
                (refund_amount, uname, pword))

    cur.execute('SELECT balance FROM user_data WHERE "Username"=%s AND password=%s;', (uname, pword))
    new_balance = cur.fetchone()["balance"]

    conn.commit()
    cur.close()
    conn.close()
    return JSONResponse({
        "message": f"✅ You sold {num_shares} shares of {company} ({symbol}). 💰 Balance: ₹{new_balance:.2f}"
    })
@app.get("/exist/feedback")
def display_feedback(request: Request):
    return templates.TemplateResponse("feedbackexist.html", {"request": request})

@app.post("/exist/feedback")
def get_feedback(request: Request, email: str = Form(...), desc: str = Form(...)):
    conn = connect_database()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute('SELECT description FROM feedback_user WHERE emailid = %s;', (email,))
    description = cur.fetchone()

    if description is None:
       
        cur.execute('INSERT INTO feedback_user (emailid, description) VALUES (%s, %s);', (email, desc))
    else:
        
        cur.execute('UPDATE feedback_user SET description = %s WHERE emailid = %s;', (desc, email))

    conn.commit()
    cur.close()
    conn.close()
    return RedirectResponse(url="/", status_code=303)
