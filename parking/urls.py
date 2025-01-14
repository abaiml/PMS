from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.loggin, name="loggin"),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('admin-dashboard/', login_required(views.admin_dashboard), name='admin_dashboard'),
    path('show-slots/', login_required(views.show_slots), name='show_slots'),
    path('add-employee/', login_required(views.add_employee), name="add_employee"),
    path('show-employee/', login_required(views.show_employee), name="show_employee"),
    path('edit-employee/<int:employee_id>/', login_required(views.edit_employee), name="edit_employee"),
    path('delete-employee/<int:employee_id>/', login_required(views.delete_employee), name="delete_employee"),
    path('show-transactions/', login_required(views.show_transactions), name="show_transactions"),
    path('select-slot/', login_required(views.select_slot), name='select_slot'),  
    path('car-slot/', login_required(views.car_slot), name='car_slot'),
    path('bike-slot/', login_required(views.bike_slot), name='bike_slot'),
    path('customer-form/', login_required(views.customer_form), name='customer_form'), 
    path('vacate-slot-list/', login_required(views.vacate_slot_list), name='vacate_slot_list'),
    path('exit-form/', login_required(views.exit_form), name='exit_form'),
    path('transaction/<int:booking_id>/', login_required(views.transaction), name='transaction'),
    path('finalize-transaction/<int:booking_id>/', login_required(views.finalize_transaction), name='finalize_transaction'),
]

