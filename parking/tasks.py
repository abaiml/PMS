from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_confirmation(customer_name,plate_number,slot_number,customer_email):
    message = (
                f"Dear  **{customer_name}**, \n\n"
                f"Your parking slot  **{slot_number}**  has been successfully booked for your vehicle  **{plate_number}**.\n\n"
                f"Please park your vehicle in slot  **{slot_number}**. We hope you have a great day!\n\n"
                f"Thank you for choosing our parking service."
            )

    send_mail(
        'Parking Slot Booking Confirmation',
        message,
        settings.DEFAULT_FROM_EMAIL,
        [customer_email],
        fail_silently=False,
    )
    
@shared_task
def send_payment_email(customer_name, plate_number,amount,payment_link_url,customer_email):
    subject = 'Parking Slot Payment Details'
    message = (
        f"Hello {customer_name},\n\n"
        "Thank you for using our parking service!\n\n"
        "Your parking session has ended. Below are the details for your payment:\n"
        f"Plate Number: {plate_number}\n"
        f"Total Amount Due: ₹{amount:.2f}\n"
        "Please make your payment by clicking the link below:\n\n"
        f"Pay Now: {payment_link_url}\n\n"
        "If you have any questions or need assistance, feel free to ask.\n\n"
        "Best regards,\n"
        "Your Parking Management Team"
    )

    # Send the email with the payment link
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [customer_email],
        fail_silently=False
    )