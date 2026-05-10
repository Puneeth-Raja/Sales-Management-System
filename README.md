# Sales Intelligence Hub

## Overview

Sales Intelligence Hub is a web-based sales and financial tracking system developed using Python, Streamlit, MySQL, and Plotly. The application helps organizations manage branch-wise sales operations, payment tracking, and business analytics through an interactive dashboard.

The system supports role-based access for administrators and branch users, enabling secure and efficient management of sales data across multiple branches.

---

## Features

* Secure login authentication system
* Role-based access control (Super Admin & Branch Users)
* Add and manage customer sales records
* Track received and pending payments
* Branch-wise sales monitoring
* Interactive analytics dashboard
* Sales trend visualization using charts
* Payment method analysis
* Real-time KPI metrics

---

## Tech Stack

| Technology      | Purpose                   |
| --------------- | ------------------------- |
| Python          | Backend Logic             |
| Streamlit       | Web Application Framework |
| MySQL           | Database Management       |
| Pandas          | Data Handling             |
| Plotly          | Data Visualization        |
| MySQL Connector | Database Connectivity     |

---

## Project Structure

```bash
Sales Intelligence Hub/
│
├── app.py               # Main application entry point
├── dashboard.py         # Dashboard and analytics module
├── login.py             # Authentication system
├── db.py                # Database connection setup
├── database.sql         # Database schema
├── requirements.txt     # Required Python packages
```

---

## Dashboard Modules

### 1. Dashboard

* Displays overall sales KPIs
* Gross sales, received amount, and pending amount
* Sales trends visualization
* Branch performance analytics

### 2. Add Sales

* Add new customer sales records
* Assign branch details
* Store financial transaction information

### 3. Payment Tracking

* Track payment collections
* Analyze payment methods
* Monitor pending balances

### 4. Analytics

* Branch-wise performance comparison
* Interactive charts and reports
* Business insights for decision-making

---

## Database Design

The system uses MySQL with multiple related tables such as:

* Users
* Branches
* Customer Sales
* Payment Splits

The database structure supports branch-level sales tracking and financial reporting.

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Puneeth-Raja/Sales-Management-System.git
cd Sales-Intelligence-Hub
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Database

* Create a MySQL database
* Import the `database.sql` file
* Update database credentials inside `db.py`

### 4. Run the Application

```bash
streamlit run app.py
```

---

## Future Enhancements

* Export reports to Excel/PDF
* Advanced filtering and search
* Email notifications for pending payments
* AI-based sales forecasting
* Cloud deployment support
* User activity logs

---

## Learning Outcomes

This project demonstrates practical implementation of:

* Full-stack Python development
* Database integration with MySQL
* Data visualization and analytics
* Role-based authentication
* Business intelligence dashboard development

---

## Author

**Puneeth Raja K**
