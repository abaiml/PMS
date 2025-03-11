🚗 Smart Parking Management System (SPMS)
A Django-based web application for managing parking slots efficiently. The system automates parking allocation, booking, and payments while providing real-time monitoring.

📌 Features

User Authentication: Secure login and role-based access (Admin, Entry, Exit Employees).
Slot Management: Book and vacate parking slots for cars and bikes.
Razorpay Integration: Online payments for parking charges.
Email Notifications: Automatic emails for slot booking and payments.
Admin Dashboard: Manage employees, customers, and transactions.
Transaction Management: Track all payments and generate invoices.

📂 Project Structure

management/ (Project settings)
│-- parking/ (Main app)
│   ├── models.py          # Database models (Employee, ParkingSlot, Booking, Transaction)
│   ├── views.py           # Core business logic
│   ├── urls.py            # Route definitions
│   ├── templates/         # HTML templates
│   ├── static/            # CSS, JS, Images
│-- management/
│   ├── settings.py        # Django settings
│   ├── urls.py            # Project-wide URLs
│   ├── wsgi.py            # WSGI entry point
│-- db.sqlite3             # SQLite database
│-- requirements.txt       # Dependencies
│-- README.md              # Project Documentation

🛠️ Installation

1. Clone the repository

git clone https://github.com/abaiml/PMS.git
cd PMS

2. Create a virtual environment & activate it

python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows

3. Install dependencies

pip install -r requirements.txt

4. Apply database migrations

python manage.py migrate

5. Run the development server

python manage.py runserver
Open your browser and go to http://127.0.0.1:8000/.

🔑 Environment Variables

Create a .env file and add the following credentials:

SECRET_KEY=your-secret-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret

📧 Email Notifications
The system sends automated emails for booking confirmation and payment details. Ensure that SMTP settings in settings.py are configured correctly.

💰 Payment Integration
SPMS uses Razorpay for handling online payments. Update your Razorpay credentials in settings.py before deploying.

🏗️ Deployment

1. Set up production server (e.g., AWS, Heroku)
2. Set DEBUG=False in settings.py
3. Run migrations and collect static files
python manage.py migrate
python manage.py collectstatic --noinput
4. Configure a WSGI server (e.g., Gunicorn, Nginx)
5. Use a production-ready database (e.g., PostgreSQL)

📜 License
This project is open-source and available under the MIT License.

🤝 Contributing
Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss.

📞 Support
For any issues or feature requests, create an issue in the repository or contact the developer ayushbora1001@gmail.com.
