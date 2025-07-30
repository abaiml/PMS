# 🚗 Smart Parking Management System (SPMS)

A Django-based web application for managing parking slots efficiently. The system automates parking allocation, booking, payments, and notifications while providing real-time monitoring

---

## 📌 Features

- **User Authentication**: Secure login and role-based access (Admin, Entry, Exit Employees).
- **Slot Management**: Book and vacate parking slots for cars and bikes.
- **Razorpay Integration**: Online payments for parking charges.
- **Email Notifications**: Automatic emails for slot booking and payments.
- **Asynchronous Task Processing (Celery + Redis)**: Background email sending and other async operations.
- **Admin Dashboard**: Manage employees, customers, and transactions.
- **Transaction Management**: Track all payments and generate invoices.

---

## 📂 Project Structure

```
management/ (Project settings)
│-- parking/ (Main app)
│   ├── models.py          # Database models (Employee, ParkingSlot, Booking, Transaction)
│   ├── views.py           # Core business logic
│   ├── urls.py            # Route definitions
│   ├── templates/         # HTML templates
│   ├── static/            # CSS, JS, Images
│   ├── celery.py          # Celery app configuration
│   ├── tasks.py           # Asynchronous tasks (e.g., email sending)
│-- management/
│   ├── settings.py        # Django settings
│   ├── urls.py            # Project-wide URLs
│   ├── wsgi.py            # WSGI entry point
│   ├── __init__.py        # Initialize Celery app
│-- db.sqlite3             # SQLite database
│-- requirements.txt       # Dependencies
│-- README.md              # Project Documentation
```

---

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/abaiml/PMS.git
   cd PMS
   ```

2. **Create a virtual environment & activate it**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Run Redis server**
   ```bash
   redis-server
   ```

6. **Start Celery Worker**
   ```bash
   celery -A management worker --pool=solo --loglevel=info
   ```

7. **Run the Django development server**
   ```bash
   python manage.py runserver
   ```

8. Open your browser and go to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔑 Environment Variables

Create a `.env` file and add the following credentials:

```dotenv
SECRET_KEY=your-secret-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
CELERY_BROKER_URL=your-redis-broker-url
```

---

## 📧 Email Notifications

The system sends **automated emails** for:
- Parking slot booking confirmation
- Payment details after parking session ends

Emails are processed **asynchronously** using **Celery** to improve performance and user experience.

---

## 💰 Payment Integration

SPMS uses **Razorpay** for handling online payments securely.
Update your Razorpay credentials in `.env` before deploying.

---

## ⚙️ Celery + Redis Integration

- **Celery** is used for background tasks (email notifications).
- **Redis** acts as the message broker.
- Make sure Redis server is running before you start Celery workers.

---

## 📜 License

This project is open-source and available under the **MIT License**.

---

## 🤝 Contributing

Feel free to fork the repository and submit pull requests.
For major changes, please open an issue first to discuss.

---

## 📞 Support

For any issues or feature requests, create an issue in the repository
or contact the developer at **ayushbora1001@gmail.com**.

---

