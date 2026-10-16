import os
import django
from decimal import Decimal
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from django.utils import timezone
from django.contrib.auth.models import User
from myapp.models import (
    Customer, CustomerAddress, CustomerWalletTransaction, KYCRecord,
    Franchise, FranchiseOwner, Location, DeliveryZone,
    VehicleCategory, Vehicle, RentalPlan,
    Booking, PickupDropTask,
    MaintenanceRecord, InspectionRecord, InsuranceRecord, ServiceHistory,
    Payment, Deposit, Invoice, Refund, Subscription,
    Offer, Referral,
    SupportTicket, TicketMessage, FAQ, Feedback,
    SystemLog, Notification, UserRole, GlobalSetting
)


def seed():
    print("Seeding database with realistic initial data...")
    now = timezone.now()

    # 1. Superuser
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@bikerentals.com", "admin123")
        print("Superuser created: admin / admin123")

    # 2. Franchises
    f1, _ = Franchise.objects.get_or_create(
        name="Ranchi Main Hub",
        defaults={
            "franchise_id": "FR101",
            "owner_name": "Sanjay Verma",
            "email": "ranchi@bikerentals.com",
            "phone": "+91 9876543210",
            "city": "Ranchi",
            "state": "Jharkhand",
            "address": "Station Road, Near Overbridge",
            "commission_rate": Decimal("15.00"),
            "status": "active",
        }
    )
    f2, _ = Franchise.objects.get_or_create(
        name="Patna Central Hub",
        defaults={
            "franchise_id": "FR102",
            "owner_name": "Ramesh Kumar Singh",
            "email": "patna@bikerentals.com",
            "phone": "+91 9876543211",
            "city": "Patna",
            "state": "Bihar",
            "address": "Fraser Road, Dak Bunglow Chowk",
            "commission_rate": Decimal("14.00"),
            "status": "active",
        }
    )
    f3, _ = Franchise.objects.get_or_create(
        name="Delhi South Hub",
        defaults={
            "franchise_id": "FR103",
            "owner_name": "Vikram Malhotra",
            "email": "delhi@bikerentals.com",
            "phone": "+91 9876543212",
            "city": "New Delhi",
            "state": "Delhi",
            "address": "Saket District Centre",
            "commission_rate": Decimal("18.00"),
            "status": "active",
        }
    )

    # Franchise Owners
    FranchiseOwner.objects.get_or_create(
        owner_id="FO101",
        defaults={
            "franchise": f1,
            "full_name": "Sanjay Verma",
            "email": "sanjay.verma@example.com",
            "phone": "+91 9876543210",
            "pan_number": "ABCDE1234F",
            "aadhaar_number": "123456789012",
            "bank_name": "HDFC Bank",
            "bank_account": "50100234567890",
            "ifsc_code": "HDFC0001234",
            "status": "active",
        }
    )
    FranchiseOwner.objects.get_or_create(
        owner_id="FO102",
        defaults={
            "franchise": f2,
            "full_name": "Ramesh Kumar Singh",
            "email": "ramesh.singh@example.com",
            "phone": "+91 9876543211",
            "pan_number": "FGHIJ5678K",
            "aadhaar_number": "987654321098",
            "bank_name": "State Bank of India",
            "bank_account": "30987654321",
            "ifsc_code": "SBIN0000890",
            "status": "active",
        }
    )

    # 3. Locations
    loc1, _ = Location.objects.get_or_create(
        name="Ranchi Station Hub",
        defaults={
            "location_id": "LOC101",
            "franchise": f1,
            "city": "Ranchi",
            "state": "Jharkhand",
            "address": "Platform 1 Exit, Railway Station",
            "pincode": "834001",
            "latitude": Decimal("23.3512"),
            "longitude": Decimal("85.3424"),
            "contact_phone": "+91 9876500001",
            "total_capacity": 45,
            "is_active": True,
        }
    )
    loc2, _ = Location.objects.get_or_create(
        name="Lalpur Chowk Hub",
        defaults={
            "location_id": "LOC102",
            "franchise": f1,
            "city": "Ranchi",
            "state": "Jharkhand",
            "address": "Circular Road, Lalpur",
            "pincode": "834001",
            "latitude": Decimal("23.3719"),
            "longitude": Decimal("85.3344"),
            "contact_phone": "+91 9876500002",
            "total_capacity": 30,
            "is_active": True,
        }
    )
    loc3, _ = Location.objects.get_or_create(
        name="Main Road Hub",
        defaults={
            "location_id": "LOC103",
            "franchise": f1,
            "city": "Ranchi",
            "state": "Jharkhand",
            "address": "Opposite GEL Church Complex",
            "pincode": "834001",
            "latitude": Decimal("23.3615"),
            "longitude": Decimal("85.3255"),
            "contact_phone": "+91 9876500003",
            "total_capacity": 40,
            "is_active": True,
        }
    )
    loc4, _ = Location.objects.get_or_create(
        name="Doranda Hub",
        defaults={
            "location_id": "LOC104",
            "franchise": f1,
            "city": "Ranchi",
            "state": "Jharkhand",
            "address": "Hinoo Main Chowk",
            "pincode": "834002",
            "latitude": Decimal("23.3326"),
            "longitude": Decimal("85.3218"),
            "contact_phone": "+91 9876500004",
            "total_capacity": 25,
            "is_active": True,
        }
    )

    # Delivery Zones
    DeliveryZone.objects.get_or_create(
        zone_id="DZ101",
        defaults={
            "name": "Zone A - Within 5km",
            "location": loc1,
            "radius_km": Decimal("5.0"),
            "delivery_charge": Decimal("50.0"),
            "min_booking_amount": Decimal("300.0"),
            "estimated_delivery_time": "30 mins",
            "is_active": True,
        }
    )
    DeliveryZone.objects.get_or_create(
        zone_id="DZ102",
        defaults={
            "name": "Zone B - 5km to 12km",
            "location": loc1,
            "radius_km": Decimal("12.0"),
            "delivery_charge": Decimal("100.0"),
            "min_booking_amount": Decimal("500.0"),
            "estimated_delivery_time": "45-60 mins",
            "is_active": True,
        }
    )

    # 4. Vehicle Categories
    cat_scooter, _ = VehicleCategory.objects.get_or_create(
        name="Standard Scooter",
        defaults={
            "slug": "standard-scooter",
            "description": "Comfortable automatic scooters suitable for city rides",
            "icon": "bi-bicycle",
            "base_hourly_rate": Decimal("50.00"),
            "base_daily_rate": Decimal("400.00"),
            "deposit_amount": Decimal("1000.00"),
        }
    )
    cat_ev, _ = VehicleCategory.objects.get_or_create(
        name="Electric Scooter (EV)",
        defaults={
            "slug": "electric-scooter",
            "description": "Eco-friendly, silent electric scooters with high battery range",
            "icon": "bi-lightning-charge",
            "base_hourly_rate": Decimal("60.00"),
            "base_daily_rate": Decimal("500.00"),
            "deposit_amount": Decimal("1500.00"),
        }
    )
    cat_bike, _ = VehicleCategory.objects.get_or_create(
        name="Commuter Bike",
        defaults={
            "slug": "commuter-bike",
            "description": "Fuel-efficient 100-125cc commuter bikes for daily travel",
            "icon": "bi-speedometer2",
            "base_hourly_rate": Decimal("65.00"),
            "base_daily_rate": Decimal("500.00"),
            "deposit_amount": Decimal("1000.00"),
        }
    )
    cat_cruiser, _ = VehicleCategory.objects.get_or_create(
        name="Cruiser & Touring",
        defaults={
            "slug": "cruiser-touring",
            "description": "Royal Enfield and premium cruisers for long journeys and highway trips",
            "icon": "bi-compass",
            "base_hourly_rate": Decimal("140.00"),
            "base_daily_rate": Decimal("1200.00"),
            "deposit_amount": Decimal("3000.00"),
        }
    )

    # 5. Rental Plans
    RentalPlan.objects.get_or_create(
        plan_id="RP101",
        defaults={
            "name": "Daily Commuter Pass",
            "duration_type": "Daily",
            "vehicle_category": cat_scooter,
            "base_price": Decimal("399.00"),
            "discount_percentage": Decimal("10.0"),
            "km_limit_per_day": 120,
            "extra_km_charge": Decimal("4.0"),
            "features": "Free Helmet, Third Party Insurance, 120 Km Limit",
            "is_popular": True,
            "is_active": True,
        }
    )
    RentalPlan.objects.get_or_create(
        plan_id="RP102",
        defaults={
            "name": "Weekend Explorer (3 Days)",
            "duration_type": "Daily",
            "vehicle_category": cat_cruiser,
            "base_price": Decimal("2999.00"),
            "discount_percentage": Decimal("15.0"),
            "km_limit_per_day": 250,
            "extra_km_charge": Decimal("7.0"),
            "features": "Complimentary Riding Gear, Unlimited Breakdown Assistance, 750 Km total",
            "is_popular": True,
            "is_active": True,
        }
    )
    RentalPlan.objects.get_or_create(
        plan_id="RP103",
        defaults={
            "name": "Monthly Flexi-Pass",
            "duration_type": "Monthly",
            "vehicle_category": cat_ev,
            "base_price": Decimal("6999.00"),
            "discount_percentage": Decimal("20.0"),
            "km_limit_per_day": 100,
            "extra_km_charge": Decimal("3.5"),
            "features": "Free Charging at Hubs, Zero Maintenance Cost, Home Delivery Included",
            "is_popular": False,
            "is_active": True,
        }
    )

    # 6. Customers
    customers_data = [
        ("Rahul Kumar", "+91 98765 43210", "rahul.kumar@email.com", "verified", 14, Decimal("18500.00"), Decimal("1200.00"), True),
        ("Priya Sharma", "+91 87654 32109", "priya.sharma@email.com", "verified", 8, Decimal("9800.00"), Decimal("450.00"), True),
        ("Amit Verma", "+91 76543 21098", "amit.verma@email.com", "pending", 2, Decimal("3200.00"), Decimal("0.00"), True),
        ("Neha Singh", "+91 65432 10987", "neha.singh@email.com", "rejected", 3, Decimal("4200.00"), Decimal("150.00"), False),
        ("Vikash Gupta", "+91 54321 09876", "vikash.gupta@email.com", "verified", 31, Decimal("45600.00"), Decimal("3400.00"), True),
        ("Ananya Das", "+91 98123 45678", "ananya.das@email.com", "verified", 5, Decimal("6400.00"), Decimal("800.00"), True),
        ("Rohan Mehra", "+91 98234 56789", "rohan.mehra@email.com", "pending", 1, Decimal("1200.00"), Decimal("0.00"), True),
        ("Sunita Rao", "+91 98345 67890", "sunita.rao@email.com", "verified", 19, Decimal("27800.00"), Decimal("2100.00"), True),
    ]

    saved_customers = []
    for idx, (name, phone, email, kyc, bks, spent, bal, active) in enumerate(customers_data, start=1001):
        cust_id = f"CU{idx}"
        cust, created = Customer.objects.get_or_create(
            phone=phone.replace(" ", ""),
            defaults={
                "customer_id": cust_id,
                "full_name": name,
                "email": email,
                "kyc_status": kyc,
                "city": "Ranchi",
                "state": "Jharkhand",
                "address": "Main Road, Sector 2",
                "pincode": "834001",
                "is_active": active,
                "wallet_balance": bal,
                "total_bookings": bks,
                "total_spent": spent,
                "licence_number": f"JH012023000{idx}",
                "licence_name": name,
                "licence_verified": (kyc == "verified"),
                "aadhaar_last_four": str(1000 + idx)[-4:],
                "aadhaar_name": name,
                "kyc_submitted_at": now - timedelta(days=10),
                "kyc_verified_at": (now - timedelta(days=5)) if kyc == "verified" else None,
                "kyc_remarks": "Approved after document verification" if kyc == "verified" else ("Document blur" if kyc == "rejected" else "Awaiting admin check"),
            }
        )
        saved_customers.append(cust)

        # KYCRecord
        KYCRecord.objects.get_or_create(
            customer=cust,
            defaults={
                "kyc_id": f"KYC{idx}",
                "document_type": "Aadhaar + Driving Licence",
                "aadhaar_number": f"XXXX-XXXX-{str(1000 + idx)[-4:]}",
                "licence_number": f"JH012023000{idx}",
                "status": kyc,
                "submitted_at": now - timedelta(days=10),
                "verified_at": (now - timedelta(days=5)) if kyc == "verified" else None,
                "verified_by": "Admin User" if kyc == "verified" else "",
                "rejection_reason": "Licence photo is not clear. Please re-upload." if kyc == "rejected" else "",
            }
        )

        # Customer address
        CustomerAddress.objects.get_or_create(
            customer=cust,
            address_type="home",
            defaults={
                "address_line": f"Flat {idx % 50 + 1}, Ashoka Enclave",
                "city": "Ranchi",
                "state": "Jharkhand",
                "pincode": "834001",
                "is_default": True,
            }
        )

    # 7. Vehicles
    vehicles_data = [
        ("JH-01-AB-1234", "Honda", "Activa 6G", cat_scooter, "Petrol", "110cc", 280, loc1, Decimal("60.00"), Decimal("450.00"), "Available", 12500, 95),
        ("JH-01-CD-5678", "TVS", "Jupiter 125", cat_scooter, "Petrol", "125cc", 290, loc2, Decimal("65.00"), Decimal("480.00"), "Rented", 8400, 70),
        ("JH-01-EF-9012", "Royal Enfield", "Classic 350", cat_cruiser, "Petrol", "349cc", 350, loc3, Decimal("150.00"), Decimal("1200.00"), "Available", 18200, 85),
        ("JH-01-GH-3456", "Ola", "S1 Pro", cat_ev, "Electric", "4 kWh", 180, loc4, Decimal("70.00"), Decimal("550.00"), "Available", 6100, 100),
        ("JH-01-IJ-7890", "Ather", "450X Gen 3", cat_ev, "Electric", "3.7 kWh", 145, loc1, Decimal("75.00"), Decimal("580.00"), "Maintenance", 14200, 40),
        ("JH-01-KL-2345", "Hero", "Splendor Plus", cat_bike, "Petrol", "97.2cc", 450, loc2, Decimal("50.00"), Decimal("380.00"), "Available", 22100, 90),
        ("JH-01-MN-6789", "Bajaj", "Pulsar 150", cat_bike, "Petrol", "149.5cc", 380, loc3, Decimal("80.00"), Decimal("600.00"), "Rented", 15400, 60),
        ("JH-01-OP-1122", "Honda", "Dio 125", cat_scooter, "Petrol", "125cc", 270, loc1, Decimal("60.00"), Decimal("450.00"), "Available", 9800, 80),
        ("JH-01-QR-3344", "Royal Enfield", "Hunter 350", cat_cruiser, "Petrol", "349cc", 340, loc4, Decimal("130.00"), Decimal("1050.00"), "Reserved", 7200, 90),
        ("JH-01-ST-5566", "TVS", "iQube Electric", cat_ev, "Electric", "3.4 kWh", 140, loc2, Decimal("65.00"), Decimal("500.00"), "Available", 5300, 95),
    ]

    saved_vehicles = []
    for idx, (vnum, brand, model, cat, fuel, eng, rng, loc, hr_rate, day_rate, status, odo, fl) in enumerate(vehicles_data, start=1001):
        vid = f"VH{idx}"
        veh, _ = Vehicle.objects.get_or_create(
            vehicle_number=vnum,
            defaults={
                "vehicle_id": vid,
                "brand": brand,
                "model": model,
                "category": cat,
                "fuel_type": fuel,
                "battery_capacity_or_engine": eng,
                "range_km": rng,
                "current_location": loc,
                "franchise": f1,
                "rental_price_per_hour": hr_rate,
                "rental_price_per_day": day_rate,
                "security_deposit": cat.deposit_amount,
                "availability_status": status,
                "odometer_reading": odo,
                "fuel_or_battery_level": fl,
                "color": "Matte Black" if "Ola" in brand or "Royal" in brand else "Navy Blue",
                "registration_year": 2024,
                "is_active": True,
            }
        )
        saved_vehicles.append(veh)

    # 8. Bookings
    bookings_sample = [
        ("BK10245", saved_customers[0], saved_vehicles[0], loc1, loc1, now - timedelta(days=2), now + timedelta(days=1), Decimal("1200.00"), Decimal("1000.00"), "Active", "Paid"),
        ("BK10246", saved_customers[1], saved_vehicles[1], loc2, loc2, now - timedelta(days=1), now + timedelta(hours=6), Decimal("480.00"), Decimal("1000.00"), "Active", "Paid"),
        ("BK10247", saved_customers[2], saved_vehicles[2], loc3, loc3, now + timedelta(hours=2), now + timedelta(days=2), Decimal("2400.00"), Decimal("3000.00"), "Confirmed", "Paid"),
        ("BK10248", saved_customers[3], saved_vehicles[3], loc4, loc4, now + timedelta(days=1), now + timedelta(days=2), Decimal("550.00"), Decimal("1500.00"), "Pending", "Pending"),
        ("BK10249", saved_customers[4], saved_vehicles[6], loc3, loc3, now - timedelta(days=5), now - timedelta(days=2), Decimal("1800.00"), Decimal("1000.00"), "Completed", "Paid"),
        ("BK10250", saved_customers[5], saved_vehicles[8], loc4, loc4, now + timedelta(days=3), now + timedelta(days=5), Decimal("2100.00"), Decimal("3000.00"), "Confirmed", "Paid"),
    ]

    saved_bookings = []
    for b_id, cust, veh, ploc, dloc, s_dt, e_dt, rent, dep, b_stat, p_stat in bookings_sample:
        total = rent + dep
        bk, _ = Booking.objects.get_or_create(
            booking_id=b_id,
            defaults={
                "customer": cust,
                "vehicle": veh,
                "pickup_location": ploc,
                "drop_location": dloc,
                "start_datetime": s_dt,
                "end_datetime": e_dt,
                "rental_amount": rent,
                "deposit_amount": dep,
                "total_amount": total,
                "status": b_stat,
                "payment_status": p_stat,
                "start_odometer": veh.odometer_reading,
            }
        )
        saved_bookings.append(bk)

        # PickupDrop Task
        PickupDropTask.objects.get_or_create(
            booking=bk,
            task_type="Pickup",
            defaults={
                "task_id": f"PD{b_id[-4:]}1",
                "customer_name": cust.full_name,
                "vehicle_info": f"{veh.brand} {veh.model}",
                "location_name": ploc.name,
                "assigned_agent": "Alok Ranjan",
                "scheduled_time": s_dt,
                "odometer_reading": veh.odometer_reading,
                "status": "Completed" if b_stat in ["Active", "Completed"] else "Scheduled",
            }
        )

        # Payment
        Payment.objects.get_or_create(
            booking=bk,
            customer=cust,
            payment_type="Rental + Security Deposit",
            defaults={
                "payment_id": f"PAY{b_id[-4:]}",
                "amount": total,
                "payment_method": "UPI",
                "transaction_reference": f"UPI-TXN-{b_id[-4:]}-987",
                "status": "Success" if p_stat == "Paid" else "Pending",
            }
        )

        # Deposit
        Deposit.objects.get_or_create(
            booking=bk,
            customer=cust,
            defaults={
                "deposit_id": f"DEP{b_id[-4:]}",
                "amount": dep,
                "status": "Refunded" if b_stat == "Completed" else "Held",
                "refunded_at": (now - timedelta(days=2)) if b_stat == "Completed" else None,
            }
        )

        # Invoice
        Invoice.objects.get_or_create(
            booking=bk,
            defaults={
                "invoice_number": f"INV-2026-{b_id[-4:]}",
                "customer": cust,
                "subtotal": rent,
                "tax_amount": rent * Decimal("0.18"),
                "total_amount": rent * Decimal("1.18"),
                "status": "Paid" if p_stat == "Paid" else "Unpaid",
                "due_date": (s_dt + timedelta(days=1)).date(),
            }
        )

    # 9. Maintenance, Inspections, Insurance, ServiceHistory
    m_veh = saved_vehicles[4] # Ather
    MaintenanceRecord.objects.get_or_create(
        record_id="MN101",
        defaults={
            "vehicle": m_veh,
            "maintenance_type": "Battery Maintenance",
            "scheduled_date": (now - timedelta(days=1)).date(),
            "cost": Decimal("1850.00"),
            "service_center": "Ather Service Center, Circular Road",
            "technician_name": "Deepak Sharma",
            "status": "In Progress",
            "description": "Routine battery health checkup and software firmware update",
        }
    )

    InspectionRecord.objects.get_or_create(
        inspection_id="INS101",
        defaults={
            "vehicle": saved_vehicles[0],
            "inspector_name": "Manoj Tiwari",
            "inspection_date": (now - timedelta(days=3)).date(),
            "overall_condition": "Good",
            "odometer_reading": 12500,
            "passed": True,
            "notes": "All checks passed. Brakes and tyres in optimal condition.",
        }
    )

    InsuranceRecord.objects.get_or_create(
        policy_number="POL-2026-9081",
        defaults={
            "vehicle": saved_vehicles[0],
            "provider": "ICICI Lombard",
            "coverage_type": "Comprehensive Zero Dep",
            "start_date": (now - timedelta(days=180)).date(),
            "expiry_date": (now + timedelta(days=185)).date(),
            "premium_amount": Decimal("2450.00"),
            "status": "Active",
        }
    )

    ServiceHistory.objects.get_or_create(
        history_id="SH101",
        defaults={
            "vehicle": saved_vehicles[0],
            "service_type": "Periodic General Service",
            "service_date": (now - timedelta(days=45)).date(),
            "odometer_at_service": 10200,
            "cost": Decimal("850.00"),
            "service_center": "Honda Authorized Service Center, Ranchi",
            "invoice_number": "HON-SRV-4421",
            "notes": "Engine oil replaced, air filter cleaned, brake shoe adjusted",
        }
    )

    # 10. Refunds, Subscriptions
    Refund.objects.get_or_create(
        refund_id="REF101",
        defaults={
            "customer": saved_customers[3],
            "amount": Decimal("550.00"),
            "reason": "Customer cancelled booking 24 hours prior to pickup",
            "status": "Processed",
            "processed_at": now - timedelta(days=1),
        }
    )

    Subscription.objects.get_or_create(
        subscription_id="SUB101",
        defaults={
            "customer": saved_customers[4],
            "rental_plan": RentalPlan.objects.first(),
            "vehicle": saved_vehicles[0],
            "start_date": (now - timedelta(days=20)).date(),
            "end_date": (now + timedelta(days=70)).date(),
            "monthly_fee": Decimal("6999.00"),
            "status": "Active",
        }
    )

    # 11. Offers, Referrals
    Offer.objects.get_or_create(
        code="RIDE50",
        defaults={
            "title": "50% Off First Booking",
            "discount_type": "percentage",
            "discount_value": Decimal("50.00"),
            "min_booking_amount": Decimal("300.00"),
            "max_discount": Decimal("250.00"),
            "valid_from": (now - timedelta(days=30)).date(),
            "valid_to": (now + timedelta(days=60)).date(),
            "usage_limit": 500,
            "times_used": 142,
            "is_active": True,
        }
    )
    Offer.objects.get_or_create(
        code="WEEKEND100",
        defaults={
            "title": "₹100 Flat Weekend Saver",
            "discount_type": "flat",
            "discount_value": Decimal("100.00"),
            "min_booking_amount": Decimal("600.00"),
            "max_discount": Decimal("100.00"),
            "valid_from": (now - timedelta(days=15)).date(),
            "valid_to": (now + timedelta(days=45)).date(),
            "usage_limit": 300,
            "times_used": 89,
            "is_active": True,
        }
    )

    Referral.objects.get_or_create(
        referral_code="REF-RAHUL10",
        defaults={
            "referrer_customer": saved_customers[0],
            "referred_customer": saved_customers[1],
            "referrer_name": "Rahul Kumar",
            "referred_name": "Priya Sharma",
            "bonus_amount": Decimal("150.00"),
            "status": "Completed",
        }
    )

    # 12. SupportTickets, FAQs, Feedback
    ticket, _ = SupportTicket.objects.get_or_create(
        ticket_id="TKT1001",
        defaults={
            "customer": saved_customers[0],
            "customer_name": "Rahul Kumar",
            "email": "rahul.kumar@email.com",
            "phone": "+91 98765 43210",
            "subject": "Helmet size exchange request at Ranchi Station",
            "category": "Vehicle Issue",
            "priority": "Medium",
            "status": "Open",
            "assigned_agent": "Support Agent Neha",
        }
    )
    TicketMessage.objects.get_or_create(
        ticket=ticket,
        sender_name="Rahul Kumar",
        defaults={
            "is_staff": False,
            "message": "Hello, the helmet provided with Activa is Medium size, can I get Large size instead?",
        }
    )

    FAQ.objects.get_or_create(
        question="What documents do I need to rent a bike?",
        defaults={
            "answer": "You need an original Valid Driving Licence (Gear/Non-Gear based on vehicle type) and Aadhaar Card/Passport for KYC verification.",
            "category": "KYC & Documents",
            "order": 1,
            "is_active": True,
        }
    )
    FAQ.objects.get_or_create(
        question="How is security deposit refunded?",
        defaults={
            "answer": "Security deposit is automatically refunded to your original payment method or wallet within 2 to 4 hours of vehicle return inspection.",
            "category": "Payments",
            "order": 2,
            "is_active": True,
        }
    )

    Feedback.objects.get_or_create(
        customer=saved_customers[4],
        defaults={
            "customer_name": "Vikash Gupta",
            "rating": 5,
            "category": "Vehicle Condition",
            "comments": "Super clean scooter and smooth handover at Lalpur branch!",
        }
    )

    # 13. SystemLog, Notification, UserRole, GlobalSetting
    SystemLog.objects.get_or_create(
        log_id="LOG1001",
        defaults={
            "log_level": "info",
            "module": "Vehicles",
            "action": "Vehicle Status Updated",
            "performed_by": "Super Admin",
            "ip_address": "192.168.1.15",
            "details": "Changed JH-01-IJ-7890 status to Maintenance",
        }
    )

    Notification.objects.get_or_create(
        title="Fleet Maintenance Alert",
        defaults={
            "message": "Vehicle Ather 450X (JH-01-IJ-7890) scheduled service is due today.",
            "notification_type": "warning",
            "recipient": "Fleet Managers",
            "is_read": False,
        }
    )

    for role_name, desc, p_cnt, u_cnt in [
        ("Super Admin", "Full access to all modules, finance, settings and franchises", 48, 2),
        ("Fleet Manager", "Manages vehicles, maintenance, inspections and inventory", 24, 5),
        ("Franchise Partner", "Access to franchise specific bookings, vehicles and revenue", 18, 8),
        ("Support Executive", "Handles customer support tickets, FAQs and KYC verification", 12, 10),
    ]:
        UserRole.objects.get_or_create(
            role_name=role_name,
            defaults={
                "description": desc,
                "permissions_count": p_cnt,
                "users_count": u_cnt,
                "is_system": True,
            }
        )

    for key, val, grp, desc in [
        ("company_name", "NextGen EV & Bike Rentals", "General", "Business Brand Name"),
        ("support_email", "support@nextgenrentals.com", "General", "Public Support Email"),
        ("support_phone", "+91 80000 12345", "General", "Customer Helpline"),
        ("security_deposit_auto_refund", "True", "Pricing", "Auto refund deposit on return"),
        ("gst_percentage", "18.0", "Pricing", "GST Tax Rate Applied to Rentals"),
        ("late_return_penalty_per_hour", "150.0", "Pricing", "Hourly late return penalty"),
    ]:
        GlobalSetting.objects.get_or_create(
            key=key,
            defaults={"value": val, "setting_group": grp, "description": desc}
        )

    print("Seeding completed successfully!")


if __name__ == "__main__":
    seed()
