# 📈 Stock Trading Simulation System

## 📌 Overview
A full-stack Stock Trading Simulation System that allows users to simulate stock trading with role-based access for users and administrators. Users can register, login, buy/sell stocks, manage their portfolio, and provide feedback. Administrators can manage stocks and users efficiently.

---

## 🚀 Key Features

### 👤 User Features
- User registration and login (New & Existing users)
- View available stocks
- Buy stocks based on available balance
- Sell owned stocks
- View personal portfolio
- Submit feedback

### 🛠️ Admin Features
- Add new stocks
- Remove existing stocks
- Manage users
- View user feedback

---

## 🧠 Tech Stack
- **Backend:** Python (FastAPI)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** PostgreSQL

---

## 📊 System Highlights
- Role-based authentication (Admin & User)
- Stock buy/sell simulation with validation
- Portfolio tracking system
- Admin dashboard for stock management
- Feedback management system

---

## 📸 Screenshots

### 🔐 Login Page
![Login](https://raw.githubusercontent.com/kaviya257/stock-trading-simulation-system/main/outputs/Login_page.png)

### 👤 User Dashboard
![User Options](https://raw.githubusercontent.com/kaviya257/stock-trading-simulation-system/main/outputs/User_Options.png)

### 📊 View Stocks (Admin)
![View Stocks](https://raw.githubusercontent.com/kaviya257/stock-trading-simulation-system/main/outputs/Admin_View_Stocks.png)

### ➕ Add Stock
![Add Stock](https://github.com/user-attachments/assets/7dfa3ac3-1f04-4090-92bf-5f6920adc45e)

### 🗑️ Remove Stock
![Remove Stock](https://raw.githubusercontent.com/kaviya257/stock-trading-simulation-system/main/outputs/Remove_stock.png)

### 💰 Buy Stock
![Purchase Stock](https://raw.githubusercontent.com/kaviya257/stock-trading-simulation-system/main/outputs/Purchase_shot.png)

### 📈 Sell Stock
![Sell Stock](https://raw.githubusercontent.com/kaviya257/stock-trading-simulation-system/main/outputs/Sell_Shares.png)

### 📊 Portfolio
![Portfolio](https://raw.githubusercontent.com/kaviya257/stock-trading-simulation-system/main/outputs/User_Portfolio.png)

### 💬 Feedback System
![Feedback](https://raw.githubusercontent.com/kaviya257/stock-trading-simulation-system/main/outputs/User_FeedBack.png)

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
