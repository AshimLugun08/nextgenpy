from django.urls import path
from . import views

urlpatterns = [
    # Dashboards
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard_alias'),
    path('reports/dashboard/', views.reports_dashboard, name='admin_reports'),
    path('vehicles/dashboard/', views.vehicles_dashboard, name='vehicles_dashboard'),

    # Vehicles
    path('vehicles/', views.vehicle_list, name='admin_vehicles'),
    path('vehicles/add/', views.vehicle_form, name='admin_vehicle_form'),
    path('vehicles/categories/', views.vehicle_categories, name='admin_vehicle_categories'),
    path('vehicles/<str:pk>/', views.vehicle_detail, name='admin_vehicle_detail'),

    # Bookings & Pickup/Drop
    path('bookings/', views.booking_list, name='admin_bookings'),
    path('bookings/<str:pk>/', views.booking_detail, name='admin_booking_detail'),
    path('pickup-drop/', views.pickup_drop_list, name='admin_pickup_drop'),
    path('pickup-drop/<str:pk>/', views.pickup_drop_detail, name='admin_pickup_drop_detail'),

    # Users, Customers, Vendors & KYC
    path('customers/', views.customer_list, name='admin_customers'),
    path('customers/<str:pk>/', views.customer_detail, name='admin_customer_detail'),
    path('vendors/', views.vendor_list, name='admin_vendors'),
    path('vendors/<str:pk>/', views.vendor_detail, name='admin_vendor_detail'),
    path('users/', views.user_list, name='admin_users'),
    path('users/roles/', views.user_roles, name='admin_roles'),
    path('kyc/', views.kyc_list, name='admin_kyc'),
    path('kyc/<str:pk>/', views.kyc_detail, name='admin_kyc_detail'),

    # Franchises & Locations
    path('franchises/', views.franchise_list, name='admin_franchises'),
    path('franchises/owners/', views.franchise_owners, name='admin_franchise_owners'),
    path('franchises/<str:pk>/', views.franchise_detail, name='admin_franchise_detail'),
    path('locations/', views.location_list, name='admin_locations'),
    path('locations/add/', views.location_form, name='admin_location_form'),
    path('locations/<str:pk>/edit/', views.location_form, name='admin_location_edit'),
    path('locations/<str:pk>/delete/', views.location_delete, name='admin_location_delete'),
    path('locations/delivery-zones/', views.delivery_zones, name='admin_delivery_zones'),


    # Maintenance & Logs
    path('maintenance/', views.maintenance_list, name='admin_maintenance'),
    path('maintenance/inspections/', views.maintenance_inspections, name='admin_inspections'),
    path('maintenance/insurance/', views.maintenance_insurance, name='admin_insurance'),
    path('maintenance/history/', views.maintenance_service_history, name='admin_service_history'),
    path('maintenance/<str:pk>/', views.maintenance_detail, name='admin_maintenance_detail'),
    path('logs/', views.system_logs, name='admin_logs'),

    # Payments & Subscriptions
    path('payments/', views.payment_list, name='admin_payments'),
    path('payments/deposits/', views.deposits_list, name='admin_deposits'),
    path('payments/invoices/', views.invoices_list, name='admin_invoices'),
    path('payments/invoices/<str:pk>/', views.invoice_detail, name='admin_invoice_detail'),
    path('payments/refunds/', views.refunds_list, name='admin_refunds'),
    path('payments/wallet/', views.wallet_view, name='admin_wallet'),
    path('payments/<str:pk>/', views.payment_detail, name='admin_payment_detail'),
    path('subscriptions/', views.subscription_list, name='admin_subscriptions'),
    path('subscriptions/<str:pk>/', views.subscription_detail, name='admin_subscription_detail'),

    # Offers & Rental Plans
    path('offers/', views.offer_list, name='admin_offers'),
    path('offers/add/', views.offer_form, name='admin_offer_form'),
    path('offers/referrals/', views.referrals_list, name='admin_referrals'),
    path('rental-plans/', views.rental_plan_list, name='admin_rental_plans'),
    path('rental-plans/add/', views.rental_plan_form, name='admin_rental_plan_form'),

    # Support, Notifications & Settings
    path('support/tickets/', views.support_tickets, name='admin_support'),
    path('support/tickets/<str:pk>/', views.support_ticket_detail, name='admin_ticket_detail'),
    path('support/faqs/', views.support_faqs, name='admin_faqs'),
    path('support/feedback/', views.support_feedback, name='admin_feedback'),
    path('notifications/', views.notifications_list, name='admin_notifications'),
    path('settings/', views.global_settings, name='admin_settings'),
]