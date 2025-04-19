from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
import razorpay

from .tasks import *


def index(request):
    return render(request, 'index.html') 


def loggin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')  
            else:
                employee = Employee.objects.filter(user=user).first()
                if employee is not None:
                    if employee.position == 'entry':
                        return redirect('select_slot')
                    elif employee.position == 'exit':
                        return redirect('vacate_slot_list')
                return render(request, 'login.html', {'error_message': 'Unauthorized access!', 'alert_type': 'error'})
        else:
            return render(request, 'login.html', {'error_message': 'Wrong credentials!', 'alert_type': 'error'})
    
    return render(request, 'login.html')


def logoutuser(request):
    logout(request)
    return redirect('index')


def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


def show_slots(request):
    car_slots = ParkingSlot.objects.filter(vehicle_type='car')  
    bike_slots = ParkingSlot.objects.filter(vehicle_type='bike')  
    
    return render(request, 'combined_slot_view.html', {
        'car_slots': car_slots,
        'bike_slots': bike_slots
    })


def add_employee(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        position = request.POST['position']
        username = request.POST['username']
        password = request.POST['password']
        hire_date = request.POST['hire_date']
        mobile_number = request.POST['mobile_number']

        user = User.objects.create_user(first_name=name, username=username, password=password, email=email)

        employee = Employee.objects.create(user=user, position=position, hire_date=hire_date, mobile_number=mobile_number)

        return redirect('admin_dashboard')
    
    return render(request, 'add_employee.html')


def show_employee(request):
    employees = Employee.objects.all()  
    return render(request, 'show_employee.html', {'employees': employees})


def edit_employee(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        position = request.POST['position']
        hire_date = request.POST['hire_date']

        employee.user.first_name = name
        employee.user.email = email
        employee.user.save()

        employee.position = position
        employee.hire_date = hire_date
        employee.save()

        return redirect('show_employee')
    
    return render(request, 'edit_employee.html', {'employee': employee})


def delete_employee(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    if request.method == 'POST':
        employee.user.delete() 
        return redirect('show_employee')
    
    return render(request, 'confirm_delete.html', {'employee': employee})


def show_transactions(request):
    transactions = Transaction.objects.all()
    return render(request, 'show_transactions.html', {'transactions': transactions})


def select_slot(request):
    if request.method == 'POST':
        vehicle_type = request.POST['vehicle_type']

        if vehicle_type == 'car':
            return redirect('car_slot')  
        elif vehicle_type == 'bike':
            return redirect('bike_slot') 
        else:
            return render(request, 'select_slot.html', {'error_message': 'Invalid vehicle type selected!', 'alert_type': 'error'})

    return render(request, 'select_slot.html')


def car_slot(request):
    slots = ParkingSlot.objects.filter(vehicle_type='car')  

    if request.method == 'POST':
        selected_slot_number = request.POST['slot_number']
       
        request.session['selected_slot'] = selected_slot_number
        return redirect('customer_form') 

    return render(request, 'car_slot.html', {'slots': slots})


def bike_slot(request):
    slots = ParkingSlot.objects.filter(vehicle_type='bike') 

    if request.method == 'POST':
        selected_slot_number = request.POST['slot_number']
        
        request.session['selected_slot'] = selected_slot_number
        return redirect('customer_form') 

    return render(request, 'bike_slot.html', {'slots': slots})


def customer_form(request):
    slot_number = request.session.get('selected_slot')
    if request.method == 'POST':
        customer_name = request.POST['customer_name']
        customer_email = request.POST['customer_email']
        plate_number = request.POST['plate_number']  
        check_in_time = request.POST['check_in_time']

        slot = ParkingSlot.objects.filter(slot_number=slot_number, is_available=True).first()
        
        if slot:
            Booking.objects.create(user=request.user, slot=slot, customer_name=customer_name, customer_email=customer_email, plate_number=plate_number, check_in_time=check_in_time) 
            slot.is_available = False
            slot.save()

            send_booking_confirmation.delay(customer_name,plate_number,slot_number,customer_email)
            

            return render(request, 'booking_success.html')
        else:
            return render(request, 'customer_form.html', {'selected_slot': slot_number, 'error_message': 'Selected slot is no longer available!', 'alert_type': 'error'})

    return render(request, 'customer_form.html', {'selected_slot': slot_number})


def vacate_slot_list(request):
    if request.method == 'POST':
        slot_number = request.POST.get('slot_number')
        if slot_number:
            request.session['selected_slot'] = slot_number
            return redirect('exit_form')

    slots = ParkingSlot.objects.filter(is_available=False)
    return render(request, 'vacate_slot_list.html', {'slots': slots})


def exit_form(request):
    slot_number = request.session.get('selected_slot')
    booking = Booking.objects.filter(slot__slot_number=slot_number, check_out_time__isnull=True).first()

    if request.method == 'POST':
        check_out_time = request.POST['check_out_time']

        booking.check_out_time = check_out_time
        booking.save()

        return redirect('transaction', booking_id=booking.id)

    return render(request, 'exit_form.html', {'booking': booking})


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def generate_payment_link(amount, customer_name, customer_email, booking_id):
    # Convert amount to paise (smallest currency unit for Razorpay)
    amount_in_paisa = int(amount * 100)

    # Create a Razorpay Payment Link
    payment_link = client.payment_link.create({
        "amount": amount_in_paisa,
        "currency": "INR",
        "description": f"Payment for booking ID {booking_id}",
        "customer": {
            "name": customer_name,
            "email": customer_email
        }
    })

    # Return the payment link URL
    return payment_link['short_url']


def transaction(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    check_in_time = booking.check_in_time
    check_out_time = booking.check_out_time
    duration = check_out_time - check_in_time
    minutes_parked = duration.total_seconds() / 60

    if minutes_parked <= 60:
        amount = 20.00
    else:
        amount = 10.00 + (minutes_parked // 60) * 10.00

    payment_link_url = generate_payment_link(amount, booking.customer_name, booking.customer_email, booking_id)

    # Create a transaction record in the database
    transaction = Transaction.objects.create(
        booking=booking,
        amount=amount,
        payment_status='Pending',
        razorpay_order_id=None  # You can store payment link ID or keep it null if not needed
    )

    # Prepare the email message with the Razorpay payment link
    send_payment_email.delay(booking.customer_name,booking.plate_number,amount,payment_link_url,booking.customer_email)

    # Render the transaction page with the necessary details
    return render(request, 'transaction.html', {
        'transaction': transaction,
        'booking': booking,
        'amount': amount
    })


def finalize_transaction(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    transaction = Transaction.objects.get(booking=booking)

    if transaction:

        transaction.payment_status = 'Completed'
        transaction.save()
        
        # Update the slot availability
        if booking.slot:
            booking.slot.is_available = True
            booking.slot.save()
        
        # Set a success message
        
    else:
        # Pass error message to the template
        return render(request, transaction.html, {'message': "No transaction found for this booking."})
    
    # Redirect to the vacated slot list page
    return redirect('vacate_slot_list')



