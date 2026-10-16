# api/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Dashboard Analytics
    path("dashboard/stats/", views.dashboard_stats_api, name="api_dashboard_stats"),
    path("dashboard/charts/", views.dashboard_charts_api, name="api_dashboard_charts"),

    # Customers & KYC
    path("customers/", views.customer_list_create_api, name="api_customer_list_create"),
    path("customers/<str:customer_id>/", views.customer_detail_api, name="api_customer_detail"),
    path("customers/<str:customer_id>/status/", views.customer_block_api, name="api_customer_status"),
    path("vendor/profile/", views.vendor_profile_api, name="api_vendor_profile"),
    path("vendor/profile/<str:vendor_id>/", views.vendor_profile_api, name="api_vendor_profile_detail"),
    path("vendors/profile/", views.vendor_profile_api, name="api_vendors_profile"),
    path("vendors/profile/<str:vendor_id>/", views.vendor_profile_api, name="api_vendors_profile_detail"),
    path("vendors/", views.vendor_list_create_api, name="api_vendor_list_create"),
    path("vendors/<str:vendor_id>/", views.vendor_detail_api, name="api_vendor_detail"),
    path("vendors/<str:vendor_id>/status/", views.vendor_block_api, name="api_vendor_status"),
    path("vendor/register/", views.vendor_register_api, name="api_vendor_register"),
    path("vendors/register/", views.vendor_register_api, name="api_vendors_register"),
    path("vendor/send-otp/", views.vendor_send_otp_api, name="api_vendor_send_otp"),
    path("vendors/send-otp/", views.vendor_send_otp_api, name="api_vendors_send_otp"),
    path("vendor/verify-otp/", views.vendor_verify_otp_api, name="api_vendor_verify_otp"),
    path("vendors/verify-otp/", views.vendor_verify_otp_api, name="api_vendors_verify_otp"),
    path("customer/send-otp/", views.customer_send_otp_api, name="api_customer_send_otp"),
    path("customers/send-otp/", views.customer_send_otp_api, name="api_customers_send_otp"),
    path("customer/verify-otp/", views.customer_verify_otp_api, name="api_customer_verify_otp"),
    path("customers/verify-otp/", views.customer_verify_otp_api, name="api_customers_verify_otp"),
    path("customer/register/", views.customer_register_api, name="api_customer_register"),
    path("customers/register/", views.customer_register_api, name="api_customers_register"),
    path("customer/profile/", views.customer_profile_api, name="api_customer_profile"),
    path("customers/profile/", views.customer_profile_api, name="api_customers_profile"),
    path("customer/<str:customer_id>/profile/", views.customer_profile_api, name="api_customer_profile_by_id"),
    path("customers/<str:customer_id>/profile/", views.customer_profile_api, name="api_customers_profile_by_id"),
    path("customer/my-bookings/", views.customer_my_bookings_api, name="api_customer_my_bookings"),
    path("customer/<str:customer_id>/bookings/", views.customer_my_bookings_api, name="api_customer_bookings_by_id"),
    path("customers/<str:customer_id>/bookings/", views.customer_my_bookings_api, name="api_customers_bookings_by_id"),
    path("customer/wallet/", views.customer_wallet_api, name="api_customer_wallet"),
    path("customers/wallet/", views.customer_wallet_api, name="api_customers_wallet"),
    path("customer/<str:customer_id>/wallet/", views.customer_wallet_api, name="api_customer_wallet_by_id"),
    path("customer/wallet/transactions/", views.customer_wallet_transactions_api, name="api_customer_wallet_transactions"),
    path("customer/<str:customer_id>/wallet/transactions/", views.customer_wallet_transactions_api, name="api_customer_wallet_transactions_by_id"),

    path("kyc/", views.kyc_list_api, name="api_kyc_list"),
    path("kyc/<str:kyc_id>/", views.kyc_action_api, name="api_kyc_action"),

    # Vehicles & Categories
    path("vehicles/", views.vehicle_list_create_api, name="api_vehicle_list_create"),
    path("vehicle/add/", views.vehicle_list_create_api, name="api_vehicle_add"),
    path("vehicles/add/", views.vehicle_list_create_api, name="api_vehicles_add"),
    path("vehicles/search/", views.search_vehicles_availability_api, name="api_vehicles_search"),
    path("vehicles/available/", views.search_vehicles_availability_api, name="api_vehicles_available"),
    path("bikes/search/", views.search_vehicles_availability_api, name="api_bikes_search"),
    path("vehicles/categories/", views.vehicle_categories_api, name="api_vehicle_categories_alias"),
    path("vehicle-categories/", views.vehicle_categories_api, name="api_vehicle_categories"),
    path("vehicle-categories/<str:category_id>/", views.vehicle_category_detail_api, name="api_vehicle_category_detail"),
    path("vehicles/<str:vehicle_id>/", views.vehicle_detail_api, name="api_vehicle_detail"),
    path("vehicle/<str:vehicle_id>/", views.vehicle_detail_api, name="api_vehicle_detail_alias"),
    path("rental-plans/", views.rental_plans_api, name="api_rental_plans"),
    path("rental-plans/<int:plan_id>/", views.rental_plan_detail_api, name="api_rental_plan_detail"),
    path("delivery-zones/<int:zone_id>/", views.delivery_zone_detail_api, name="api_delivery_zone_detail"),
    path("inspections/<int:inspection_id>/", views.inspection_detail_api, name="api_inspection_detail"),
    path("insurance/<int:insurance_id>/", views.insurance_detail_api, name="api_insurance_detail"),
    path("support/faqs/<int:faq_id>/", views.faq_detail_api, name="api_faq_detail"),
    path("faqs/<int:faq_id>/", views.faq_detail_api, name="api_faq_detail_alias"),
    path("faqs/", views.faqs_api, name="api_faqs_alias"),
    path("franchise-owners/", views.franchise_owners_api, name="api_franchise_owners"),
    path("franchise-owners/<int:owner_id>/", views.franchise_owner_detail_api, name="api_franchise_owner_detail"),


    # Bookings & Operations
    path("bookings/", views.booking_list_create_api, name="api_booking_list_create"),
    path("booking/", views.booking_list_create_api, name="api_booking_list_create_alias"),
    path("bookings/my-bookings/", views.customer_my_bookings_api, name="api_bookings_my_bookings"),
    path("bookings/<str:booking_id>/", views.booking_detail_api, name="api_booking_detail"),
    path("booking/<str:booking_id>/", views.booking_detail_api, name="api_booking_detail_alias"),
    path("bookings/<str:booking_id>/status/", views.booking_status_update_api, name="api_booking_status_update"),
    path("booking/<str:booking_id>/status/", views.booking_status_update_api, name="api_booking_status_update_alias"),
    path("pickup-drop/", views.pickup_drop_list_api, name="api_pickup_drop_list"),
    path("pickup-drop/<str:task_id>/", views.pickup_drop_detail_api, name="api_pickup_drop_detail"),
    path("pickup-drop/<str:task_id>/status/", views.pickup_drop_status_api, name="api_pickup_drop_status"),
    path("pickup-delivery/", views.pickup_drop_list_api, name="api_pickup_delivery_list_alias"),
    path("pickup-delivery/<str:task_id>/", views.pickup_drop_detail_api, name="api_pickup_delivery_detail_alias"),
    path("pickup-delivery/<str:task_id>/status/", views.pickup_drop_status_api, name="api_pickup_delivery_status_alias"),

    # Franchises & Locations
    path("franchises/", views.franchise_list_api, name="api_franchise_list"),
    path("franchises/<str:franchise_id>/", views.franchise_detail_api, name="api_franchise_detail"),
    path("locations/cities/", views.available_cities_api, name="api_available_cities"),
    path("cities/", views.available_cities_api, name="api_cities_alias"),
    path("available-cities/", views.available_cities_api, name="api_available_cities_alias"),
    path("cities/<str:city_name>/vehicles/", views.vehicles_by_city_api, name="api_vehicles_by_city"),
    path("city/vehicles/", views.vehicles_by_city_api, name="api_city_vehicles_query"),
    path("locations/", views.location_list_api, name="api_location_list"),
    path("locations/<str:location_id>/", views.location_detail_api, name="api_location_detail"),
    path("delivery-zones/", views.delivery_zone_list_api, name="api_delivery_zones"),


    # Fleet Maintenance
    path("maintenance/", views.maintenance_list_create_api, name="api_maintenance_list_create"),
    path("maintenance/<str:record_id>/", views.maintenance_detail_api, name="api_maintenance_detail"),
    path("maintenance/<str:record_id>/update/", views.maintenance_detail_api, name="api_maintenance_update"),
    path("maintenance/<str:record_id>/edit/", views.maintenance_detail_api, name="api_maintenance_edit"),
    path("inspections/", views.inspections_list_api, name="api_inspections_list"),
    path("insurance/", views.insurance_list_api, name="api_insurance_list"),

    # Finance & Accounts
    path("payments/", views.payment_list_api, name="api_payment_list"),
    path("deposits/", views.deposits_list_api, name="api_deposits_list"),
    path("invoices/", views.invoices_list_api, name="api_invoices_list"),
    path("refunds/", views.refunds_list_api, name="api_refunds_list"),
    path("subscriptions/", views.subscriptions_list_api, name="api_subscriptions_list"),

    # Offers & Referrals
    path("offers/", views.offer_list_create_api, name="api_offers_list_create"),
    path("offers/<str:offer_id>/", views.offer_detail_api, name="api_offer_detail"),
    path("referrals/", views.referrals_list_api, name="api_referrals_list"),

    # Support & Communications
    path("support/tickets/", views.support_tickets_api, name="api_support_tickets"),
    path("support/tickets/<str:ticket_id>/", views.support_ticket_detail_api, name="api_support_ticket_detail"),
    path("support/tickets/<str:ticket_id>/status/", views.support_ticket_status_api, name="api_support_ticket_status"),
    path("support/tickets/<str:ticket_id>/reply/", views.support_ticket_reply_api, name="api_support_ticket_reply"),
    path("tickets/", views.support_tickets_api, name="api_tickets_alias"),
    path("tickets/<str:ticket_id>/", views.support_ticket_detail_api, name="api_ticket_detail_alias"),
    path("tickets/<str:ticket_id>/status/", views.support_ticket_status_api, name="api_ticket_status_alias"),
    path("tickets/<str:ticket_id>/reply/", views.support_ticket_reply_api, name="api_ticket_reply_alias"),
    path("support/faqs/", views.faqs_api, name="api_faqs"),
    path("support/feedback/", views.feedback_api, name="api_support_feedback"),
    path("feedback/", views.feedback_api, name="api_feedback"),
    path("ratings/", views.feedback_api, name="api_ratings"),
    path("reviews/", views.feedback_api, name="api_reviews"),
    path("bookings/<str:booking_id>/rating/", views.feedback_api, name="api_booking_rating"),
    path("vehicles/<str:vehicle_id>/ratings/", views.feedback_api, name="api_vehicle_ratings"),
    path("notifications/", views.notifications_api, name="api_notifications"),
    path("reports/export/", views.reports_export_api, name="api_reports_export"),

    # System & Settings
    path("logs/", views.system_logs_api, name="api_system_logs"),
    path("settings/", views.settings_api, name="api_settings"),
]