from django.contrib import admin
from .models import (
    Customer, Vendor, CustomerAddress, CustomerWalletTransaction, KYCRecord,
    Franchise, FranchiseOwner, Location, DeliveryZone,
    VehicleCategory, Vehicle, RentalPlan,
    Booking, PickupDropTask,
    MaintenanceRecord, InspectionRecord, InsuranceRecord, ServiceHistory,
    Payment, Deposit, Invoice, Refund, Subscription,
    Offer, Referral,
    SupportTicket, TicketMessage, FAQ, Feedback,
    SystemLog, Notification, UserRole, GlobalSetting
)

models_list = [
    Customer, Vendor, CustomerAddress, CustomerWalletTransaction, KYCRecord,
    Franchise, FranchiseOwner, Location, DeliveryZone,
    VehicleCategory, Vehicle, RentalPlan,
    Booking, PickupDropTask,
    MaintenanceRecord, InspectionRecord, InsuranceRecord, ServiceHistory,
    Payment, Deposit, Invoice, Refund, Subscription,
    Offer, Referral,
    SupportTicket, TicketMessage, FAQ, Feedback,
    SystemLog, Notification, UserRole, GlobalSetting
]

for m in models_list:
    try:
        admin.site.register(m)
    except admin.sites.AlreadyRegistered:
        pass
