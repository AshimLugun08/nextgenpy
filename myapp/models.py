from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# ==============================================================================
# 1. CUSTOMERS & KYC
# ==============================================================================

class Customer(models.Model):
    KYC_STATUS = [
        ("pending", "Pending"),
        ("verified", "Verified"),
        ("rejected", "Rejected"),
    ]

    customer_id = models.CharField(
        max_length=12, unique=True, blank=True, editable=False
    )
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    profile_image = models.URLField(blank=True, null=True)

    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True)

    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    pincode = models.CharField(max_length=10, blank=True)

    # KYC details
    kyc_status = models.CharField(
        max_length=20,
        choices=KYC_STATUS,
        default="pending"
    )
    aadhaar_last_four = models.CharField(max_length=4, blank=True)
    aadhaar_name = models.CharField(max_length=150, blank=True)
    kyc_submitted_at = models.DateTimeField(null=True, blank=True)
    kyc_verified_at = models.DateTimeField(null=True, blank=True)
    kyc_remarks = models.TextField(blank=True)

    # Driving licence details
    licence_number = models.CharField(max_length=50, blank=True)
    licence_name = models.CharField(max_length=150, blank=True)
    licence_issue_date = models.DateField(null=True, blank=True)
    licence_expiry_date = models.DateField(null=True, blank=True)
    vehicle_class = models.CharField(max_length=100, blank=True)
    issuing_authority = models.CharField(max_length=150, blank=True)
    licence_verified = models.BooleanField(default=False)

    # Account status & metrics
    is_active = models.BooleanField(default=True)
    wallet_balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    total_bookings = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )

    joined_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-joined_at"]

    def save(self, *args, **kwargs):
        if not self.customer_id:
            last_customer = (
                Customer.objects
                .filter(customer_id__startswith="CU")
                .order_by("-id")
                .first()
            )
            next_number = last_customer.id + 1001 if last_customer else 1001
            self.customer_id = f"CU{next_number}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_id} - {self.full_name}"


class Vendor(models.Model):
    KYC_STATUS = [
        ("pending", "Pending"),
        ("verified", "Verified"),
        ("rejected", "Rejected"),
    ]

    vendor_id = models.CharField(
        max_length=12, unique=True, blank=True, editable=False
    )
    full_name = models.CharField(max_length=150)
    business_name = models.CharField(max_length=150, blank=True, default="", verbose_name="Business / Company Name")
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    gst_no = models.CharField(max_length=20, blank=True, null=True, verbose_name="GST Number")
    profile_image = models.URLField(blank=True, null=True)

    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True)

    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    pincode = models.CharField(max_length=10, blank=True)

    # KYC details
    kyc_status = models.CharField(
        max_length=20,
        choices=KYC_STATUS,
        default="pending"
    )
    pan_number = models.CharField(max_length=20, blank=True, verbose_name="PAN Card Number")
    pan_card_image = models.TextField(blank=True, null=True, verbose_name="PAN Card Image")
    aadhaar_number = models.CharField(max_length=20, blank=True, verbose_name="Aadhaar Number")
    aadhaar_last_four = models.CharField(max_length=4, blank=True)
    aadhaar_name = models.CharField(max_length=150, blank=True)
    aadhaar_front_image = models.TextField(blank=True, null=True, verbose_name="Aadhaar Front Image")
    aadhaar_back_image = models.TextField(blank=True, null=True, verbose_name="Aadhaar Back Image")
    kyc_submitted_at = models.DateTimeField(null=True, blank=True)
    kyc_verified_at = models.DateTimeField(null=True, blank=True)
    kyc_remarks = models.TextField(blank=True)

    # Driving licence / ID details
    licence_number = models.CharField(max_length=50, blank=True)
    licence_name = models.CharField(max_length=150, blank=True)
    licence_front_image = models.TextField(blank=True, null=True, verbose_name="Driving Licence Front Image")
    licence_back_image = models.TextField(blank=True, null=True, verbose_name="Driving Licence Back Image")
    licence_issue_date = models.DateField(null=True, blank=True)
    licence_expiry_date = models.DateField(null=True, blank=True)
    vehicle_class = models.CharField(max_length=100, blank=True)
    issuing_authority = models.CharField(max_length=150, blank=True)
    licence_verified = models.BooleanField(default=False)

    # Account status & metrics
    is_active = models.BooleanField(default=True)
    wallet_balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    total_bookings = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    rating = models.DecimalField(
        max_digits=3, decimal_places=1, default=4.8
    )

    joined_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-joined_at"]

    def save(self, *args, **kwargs):
        if not self.vendor_id:
            last_vendor = (
                Vendor.objects
                .filter(vendor_id__startswith="VN")
                .order_by("-id")
                .first()
            )
            next_number = last_vendor.id + 1001 if last_vendor else 1001
            self.vendor_id = f"VN{next_number}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.vendor_id} - {self.full_name}"


class CustomerAddress(models.Model):
    ADDRESS_TYPES = [
        ("home", "Home"),
        ("work", "Work"),
        ("other", "Other"),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="addresses"
    )
    address_type = models.CharField(
        max_length=10,
        choices=ADDRESS_TYPES,
        default="home"
    )
    address_line = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.full_name} - {self.address_type}"


class CustomerWalletTransaction(models.Model):
    TRANSACTION_TYPES = [
        ("credit", "Credit"),
        ("debit", "Debit"),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="wallet_transactions"
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer.customer_id} - {self.amount}"


class KYCRecord(models.Model):
    kyc_id = models.CharField(max_length=20, unique=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="kyc_records")
    document_type = models.CharField(max_length=50, default="Aadhaar + Driving Licence")
    aadhaar_number = models.CharField(max_length=20, blank=True)
    aadhaar_front_image = models.URLField(blank=True, null=True)
    aadhaar_back_image = models.URLField(blank=True, null=True)
    licence_number = models.CharField(max_length=50, blank=True)
    licence_front_image = models.URLField(blank=True, null=True)
    licence_back_image = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Customer.KYC_STATUS, default="pending")
    rejection_reason = models.TextField(blank=True)
    submitted_at = models.DateTimeField(default=timezone.now)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["-submitted_at"]

    def save(self, *args, **kwargs):
        if not self.kyc_id:
            last = KYCRecord.objects.order_by("-id").first()
            next_num = (last.id + 1001) if last else 1001
            self.kyc_id = f"KYC{next_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.kyc_id} - {self.customer.full_name}"


# ==============================================================================
# 2. FRANCHISES & LOCATIONS
# ==============================================================================

class Franchise(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("pending", "Pending"),
        ("inactive", "Inactive"),
    ]

    franchise_id = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=150)
    owner_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=15.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-joined_at"]

    def save(self, *args, **kwargs):
        if not self.franchise_id:
            last = Franchise.objects.order_by("-id").first()
            next_num = (last.id + 101) if last else 101
            self.franchise_id = f"FR{next_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.franchise_id} - {self.name}"


class FranchiseOwner(models.Model):
    owner_id = models.CharField(max_length=20, unique=True, blank=True)
    franchise = models.ForeignKey(Franchise, on_delete=models.SET_NULL, null=True, blank=True, related_name="owners")
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    pan_number = models.CharField(max_length=20, blank=True)
    aadhaar_number = models.CharField(max_length=20, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account = models.CharField(max_length=30, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, default="active")
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.owner_id:
            last = FranchiseOwner.objects.order_by("-id").first()
            next_num = (last.id + 101) if last else 101
            self.owner_id = f"FO{next_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.owner_id} - {self.full_name}"


class Location(models.Model):
    location_id = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=150)
    franchise = models.ForeignKey(Franchise, on_delete=models.SET_NULL, null=True, blank=True, related_name="locations")
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.TextField()
    pincode = models.CharField(max_length=10, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    operating_hours = models.CharField(max_length=100, default="07:00 AM - 10:00 PM")
    total_capacity = models.PositiveIntegerField(default=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.location_id:
            last = Location.objects.order_by("-id").first()
            next_num = (last.id + 101) if last else 101
            self.location_id = f"LOC{next_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.city})"


class DeliveryZone(models.Model):
    zone_id = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=150)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="delivery_zones")
    radius_km = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)
    delivery_charge = models.DecimalField(max_digits=8, decimal_places=2, default=50.0)
    min_booking_amount = models.DecimalField(max_digits=8, decimal_places=2, default=300.0)
    estimated_delivery_time = models.CharField(max_length=50, default="30-45 mins")
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.zone_id:
            last = DeliveryZone.objects.order_by("-id").first()
            next_num = (last.id + 101) if last else 101
            self.zone_id = f"DZ{next_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.location.name}"


# ==============================================================================
# 3. VEHICLES & CATEGORIES
# ==============================================================================

class VehicleCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default="bi-bicycle")
    image = models.URLField(blank=True, null=True)
    base_hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=50)
    base_daily_rate = models.DecimalField(max_digits=8, decimal_places=2, default=350)
    base_weekly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=2100)
    base_monthly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=6500)
    deposit_amount = models.DecimalField(max_digits=8, decimal_places=2, default=1000)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Vehicle Categories"

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    FUEL_CHOICES = [
        ("Petrol", "Petrol"),
        ("Electric", "Electric"),
        ("Diesel", "Diesel"),
    ]

    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Rented", "Rented"),
        ("Reserved", "Reserved"),
        ("Maintenance", "Maintenance"),
        ("Inactive", "Inactive"),
    ]

    vehicle_id = models.CharField(max_length=20, unique=True, blank=True)
    vehicle_number = models.CharField(max_length=50, unique=True)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    category = models.ForeignKey(VehicleCategory, on_delete=models.SET_NULL, null=True, related_name="vehicles")
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default="Petrol")
    battery_capacity_or_engine = models.CharField(max_length=50, default="110cc")
    range_km = models.PositiveIntegerField(default=120)

    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="vehicles")
    franchise = models.ForeignKey(Franchise, on_delete=models.SET_NULL, null=True, blank=True, related_name="vehicles")

    rental_price_per_hour = models.DecimalField(max_digits=8, decimal_places=2, default=60)
    rental_price_per_day = models.DecimalField(max_digits=8, decimal_places=2, default=450)
    rental_price_per_week = models.DecimalField(max_digits=8, decimal_places=2, default=2700)
    rental_price_per_month = models.DecimalField(max_digits=8, decimal_places=2, default=8500)
    security_deposit = models.DecimalField(max_digits=8, decimal_places=2, default=1000)

    availability_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Available")
    odometer_reading = models.PositiveIntegerField(default=5000)
    fuel_or_battery_level = models.PositiveIntegerField(default=100)

    color = models.CharField(max_length=50, default="Black")
    registration_year = models.PositiveIntegerField(default=2024)
    vehicle_type = models.CharField(max_length=50, default="Scooter", blank=True)
    engine_number = models.CharField(max_length=100, blank=True)
    engine_capacity = models.CharField(max_length=50, blank=True)
    chassis_number = models.CharField(max_length=100, blank=True)
    delivery_charge = models.DecimalField(max_digits=8, decimal_places=2, default=100)
    late_return_fee = models.DecimalField(max_digits=8, decimal_places=2, default=100)

    # Insurance
    insurance_policy_number = models.CharField(max_length=100, blank=True)
    insurance_provider = models.CharField(max_length=150, blank=True)
    insurance_start_date = models.DateField(null=True, blank=True)
    insurance_expiry_date = models.DateField(null=True, blank=True)

    # Registration
    registration_date = models.DateField(null=True, blank=True)
    rc_expiry_date = models.DateField(null=True, blank=True)
    fitness_valid_until = models.DateField(null=True, blank=True)

    image = models.TextField(blank=True, null=True)
    images = models.JSONField(default=list, blank=True)
    image_front = models.TextField(blank=True, null=True, verbose_name="Front View Image")
    image_side = models.TextField(blank=True, null=True, verbose_name="Side View Image")
    image_back = models.TextField(blank=True, null=True, verbose_name="Back View Image")
    image_dashboard = models.TextField(blank=True, null=True, verbose_name="Dashboard Image")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        if not self.vehicle_id:
            last = Vehicle.objects.order_by("-id").first()
            next_num = (last.id + 1001) if last else 1001
            self.vehicle_id = f"VH{next_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.vehicle_id} - {self.brand} {self.model} ({self.vehicle_number})"


class RentalPlan(models.Model):
    DURATION_CHOICES = [
        ("Hourly", "Hourly"),
        ("Daily", "Daily"),
        ("Weekly", "Weekly"),
        ("Monthly", "Monthly"),
    ]

    plan_id = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=150)
    duration_type = models.CharField(max_length=20, choices=DURATION_CHOICES, default="Daily")
    vehicle_category = models.ForeignKey(VehicleCategory, on_delete=models.SET_NULL, null=True, blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    km_limit_per_day = models.PositiveIntegerField(default=150)
    extra_km_charge = models.DecimalField(max_digits=6, decimal_places=2, default=5.0)
    features = models.TextField(blank=True, help_text="Comma-separated or bullet points")
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.plan_id:
            last = RentalPlan.objects.order_by("-id").first()
            next_num = (last.id + 101) if last else 101
            self.plan_id = f"RP{next_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.plan_id} - {self.name}"


# ==============================================================================
# 4. BOOKINGS, PICKUP & DROP
# ==============================================================================

class Booking(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Active", "Active"),
        ("Pickup", "Pickup"),
        ("Drop Off", "Drop Off"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Partially Paid", "Partially Paid"),
        ("Refunded", "Refunded"),
    ]

    booking_id = models.CharField(max_length=20, unique=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="bookings")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="bookings")
    rental_plan = models.ForeignKey(RentalPlan, on_delete=models.SET_NULL, null=True, blank=True)

    pickup_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name="pickup_bookings")
    drop_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name="drop_bookings")

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    actual_return_datetime = models.DateTimeField(null=True, blank=True)

    rental_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Confirmed")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="Paid")

    start_odometer = models.PositiveIntegerField(default=0)
    end_odometer = models.PositiveIntegerField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    image = models.TextField(blank=True, null=True, verbose_name="Booking Image")

    DELIVERY_TYPE_CHOICES = [
        ("Self Pickup", "Self Pickup"),
        ("Doorstep", "Doorstep"),
    ]

    PICKUP_DROP_STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("Ready", "Ready"),
        ("Out for Delivery", "Out for Delivery"),
        ("Pickup", "Pickup"),
        ("Picked Up", "Picked Up"),
        ("Drop Off", "Drop Off"),
        ("Dropped Off", "Dropped Off"),
        ("Return Pending", "Return Pending"),
        ("Returned", "Returned"),
    ]

    delivery_type = models.CharField(max_length=50, choices=DELIVERY_TYPE_CHOICES, default="Self Pickup")
    pickup_drop_status = models.CharField(max_length=50, choices=PICKUP_DROP_STATUS_CHOICES, default="Scheduled")

    # Doorstep Delivery & Return GPS coordinates & addresses
    delivery_address = models.TextField(blank=True, null=True, help_text="Doorstep delivery address")
    delivery_latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    delivery_longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    return_address = models.TextField(blank=True, null=True, help_text="Doorstep return / pickup address")
    return_latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    return_longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.booking_id:
            last = Booking.objects.order_by("-id").first()
            next_num = (last.id + 10245) if last else 10245
            self.booking_id = f"BK{next_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_id} - {self.customer.full_name} ({self.vehicle.model})"


class PickupDropTask(models.Model):
    TASK_TYPE = [
        ("Pickup", "Pickup"),
        ("Drop", "Drop"),
    ]

    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    task_id = models.CharField(max_length=20, unique=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="tasks")
    task_type = models.CharField(max_length=20, choices=TASK_TYPE, default="Pickup")
    customer_name = models.CharField(max_length=150, blank=True)
    vehicle_info = models.CharField(max_length=150, blank=True)
    location_name = models.CharField(max_length=150, blank=True)
    assigned_agent = models.CharField(max_length=100, default="Unassigned")
    scheduled_time = models.DateTimeField(default=timezone.now)
    completed_time = models.DateTimeField(null=True, blank=True)
    odometer_reading = models.PositiveIntegerField(default=0)
    fuel_level = models.PositiveIntegerField(default=100)
    checklist_status = models.CharField(max_length=20, default="Passed")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Scheduled")
    delivery_type = models.CharField(max_length=50, default="Self Pickup", blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["scheduled_time"]

    def save(self, *args, **kwargs):
        if not self.task_id:
            last = PickupDropTask.objects.order_by("-id").first()
            next_num = (last.id + 101) if last else 101
            self.task_id = f"PD{next_num}"
        if not self.customer_name and self.booking:
            self.customer_name = self.booking.customer.full_name
        if not self.vehicle_info and self.booking:
            self.vehicle_info = f"{self.booking.vehicle.brand} {self.booking.vehicle.model} ({self.booking.vehicle.vehicle_number})"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.task_id} - {self.task_type} for {self.booking.booking_id}"


# ==============================================================================
# 5. MAINTENANCE, INSPECTIONS, INSURANCE, LOGS
# ==============================================================================

class MaintenanceRecord(models.Model):
    TYPE_CHOICES = [
        ("Routine Service", "Routine Service"),
        ("Repair", "Repair"),
        ("Battery Maintenance", "Battery Maintenance"),
        ("Tyre Replacement", "Tyre Replacement"),
        ("Accident Repair", "Accident Repair"),
    ]

    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    record_id = models.CharField(max_length=20, unique=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="maintenance_records")
    maintenance_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default="Routine Service")
    scheduled_date = models.DateField(default=timezone.now)
    completion_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_center = models.CharField(max_length=150, default="Authorized Service Center")
    technician_name = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="In Progress")
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-scheduled_date"]

    def save(self, *args, **kwargs):
        if not self.record_id:
            last = MaintenanceRecord.objects.order_by("-id").first()
            next_num = (last.id + 101) if last else 101
            self.record_id = f"MN{next_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.record_id} - {self.vehicle.vehicle_number} ({self.maintenance_type})"


class InspectionRecord(models.Model):
    CONDITION_CHOICES = [
        ("Excellent", "Excellent"),
        ("Good", "Good"),
        ("Fair", "Fair"),
        ("Poor", "Poor"),
    ]

    inspection_id = models.CharField(max_length=20, unique=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="inspections")
    inspector_name = models.CharField(max_length=100)
    inspection_date = models.DateField(default=timezone.now)
    overall_condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default="Good")
    odometer_reading = models.PositiveIntegerField(default=0)
    brakes_ok = models.BooleanField(default=True)
    tyres_ok = models.BooleanField(default=True)
    lights_ok = models.BooleanField(default=True)
    battery_ok = models.BooleanField(default=True)
    passed = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-inspection_date"]

    def save(self, *args, **kwargs):
        if not self.inspection_id:
            last = InspectionRecord.objects.order_by("-id").first()
            next_num = (last.id + 101) if last else 101
            self.inspection_id = f"INS{next_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.inspection_id} - {self.vehicle.vehicle_number}"


class InsuranceRecord(models.Model):
    policy_number = models.CharField(max_length=50, unique=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="insurance_records")
    provider = models.CharField(max_length=150)
    coverage_type = models.CharField(max_length=100, default="Comprehensive")
    start_date = models.DateField()
    expiry_date = models.DateField()
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default="Active")

    class Meta:
        ordering = ["expiry_date"]

    def __str__(self):
        return f"{self.policy_number} ({self.vehicle.vehicle_number})"


class ServiceHistory(models.Model):
    history_id = models.CharField(max_length=20, unique=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="service_history")
    service_type = models.CharField(max_length=150)
    service_date = models.DateField(default=timezone.now)
    odometer_at_service = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_center = models.CharField(max_length=150)
    invoice_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-service_date"]

    def save(self, *args, **kwargs):
        if not self.history_id:
            last = ServiceHistory.objects.order_by("-id").first()
            next_num = (last.id + 101) if last else 101
            self.history_id = f"SH{next_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.history_id} - {self.vehicle.vehicle_number}"


# ==============================================================================
# 6. PAYMENTS, INVOICES, REFUNDS, DEPOSITS & SUBSCRIPTIONS
# ==============================================================================

class Payment(models.Model):
    METHOD_CHOICES = [
        ("UPI", "UPI"),
        ("Card", "Card"),
        ("Net Banking", "Net Banking"),
        ("Wallet", "Wallet"),
        ("Cash", "Cash"),
    ]

    STATUS_CHOICES = [
        ("Success", "Success"),
        ("Pending", "Pending"),
        ("Failed", "Failed"),
        ("Refunded", "Refunded"),
    ]

    payment_id = models.CharField(max_length=20, unique=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True, related_name="payments")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=30, choices=METHOD_CHOICES, default="UPI")
    payment_type = models.CharField(max_length=50, default="Rental Payment")
    transaction_reference = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Success")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.payment_id:
            last = Payment.objects.order_by("-id").first()
            next_num = (last.id + 1001) if last else 1001
            self.payment_id = f"PAY{next_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.payment_id} - ₹{self.amount} ({self.customer.full_name})"


class Deposit(models.Model):
    STATUS_CHOICES = [
        ("Held", "Held"),
        ("Refunded", "Refunded"),
        ("Partially Deducted", "Partially Deducted"),
        ("Forfeited", "Forfeited"),
    ]

    deposit_id = models.CharField(max_length=20, unique=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="deposits")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="deposits")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    deduction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deduction_reason = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Held")
    refunded_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.deposit_id:
            last = Deposit.objects.order_by("-id").first()
            next_num = (last.id + 101) if last else 101
            self.deposit_id = f"DEP{next_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.deposit_id} - ₹{self.amount}"


class Invoice(models.Model):
    STATUS_CHOICES = [
        ("Paid", "Paid"),
        ("Unpaid", "Unpaid"),
        ("Cancelled", "Cancelled"),
    ]

    invoice_number = models.CharField(max_length=50, unique=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="invoices")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="invoices")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Paid")
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            last = Invoice.objects.order_by("-id").first()
            next_num = (last.id + 1001) if last else 1001
            self.invoice_number = f"INV-2026-{next_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_number} - ₹{self.total_amount}"


class Refund(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processed", "Processed"),
        ("Rejected", "Rejected"),
    ]

    refund_id = models.CharField(max_length=20, unique=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name="refunds")
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True, related_name="refunds")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="refunds")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    requested_at = models.DateTimeField(default=timezone.now)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-requested_at"]

    def save(self, *args, **kwargs):
        if not self.refund_id:
            last = Refund.objects.order_by("-id").first()
            next_num = (last.id + 101) if last else 101
            self.refund_id = f"REF{next_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.refund_id} - ₹{self.amount} ({self.status})"


class Subscription(models.Model):
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Paused", "Paused"),
        ("Cancelled", "Cancelled"),
        ("Expired", "Expired"),
    ]

    subscription_id = models.CharField(max_length=20, unique=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="subscriptions")
    rental_plan = models.ForeignKey(RentalPlan, on_delete=models.SET_NULL, null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Active")
    auto_renew = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.subscription_id:
            last = Subscription.objects.order_by("-id").first()
            next_num = (last.id + 101) if last else 101
            self.subscription_id = f"SUB{next_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subscription_id} - {self.customer.full_name}"


# ==============================================================================
# 7. OFFERS, REFERRALS
# ==============================================================================

class Offer(models.Model):
    TYPE_CHOICES = [
        ("percentage", "Percentage"),
        ("flat", "Flat Amount"),
    ]

    code = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=150)
    discount_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="percentage")
    discount_value = models.DecimalField(max_digits=8, decimal_places=2)
    min_booking_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, default=500)
    valid_from = models.DateField(default=timezone.now)
    valid_to = models.DateField()
    usage_limit = models.PositiveIntegerField(default=100)
    times_used = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.code} - {self.title}"


class Referral(models.Model):
    referral_code = models.CharField(max_length=30)
    referrer_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name="referrals_given")
    referred_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name="referral_received")
    referrer_name = models.CharField(max_length=150)
    referred_name = models.CharField(max_length=150)
    bonus_amount = models.DecimalField(max_digits=8, decimal_places=2, default=100.0)
    status = models.CharField(max_length=20, default="Completed")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.referral_code} ({self.referrer_name} -> {self.referred_name})"


# ==============================================================================
# 8. SUPPORT TICKETS, FAQS, FEEDBACK
# ==============================================================================

class SupportTicket(models.Model):
    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Urgent", "Urgent"),
    ]

    STATUS_CHOICES = [
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
        ("Closed", "Closed"),
    ]

    ticket_id = models.CharField(max_length=20, unique=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name="tickets")
    customer_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=255)
    category = models.CharField(max_length=100, default="Booking")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="Medium")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Open")
    assigned_agent = models.CharField(max_length=100, default="Support Team")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            last = SupportTicket.objects.order_by("-id").first()
            next_num = (last.id + 1001) if last else 1001
            self.ticket_id = f"TKT{next_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_id} - {self.subject}"


class TicketMessage(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name="messages")
    sender_name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Msg on {self.ticket.ticket_id} by {self.sender_name}"


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=100, default="General")
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.question


class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name="feedbacks")
    customer_name = models.CharField(max_length=150)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True, related_name="ratings")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name="ratings")
    rating = models.PositiveIntegerField(default=5)
    category = models.CharField(max_length=100, default="Ride Experience")
    title = models.CharField(max_length=150, blank=True)
    comments = models.TextField()
    image = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer_name} - {self.rating}★ ({self.booking.booking_id if self.booking else 'General'})"


# ==============================================================================
# 9. SYSTEM LOGS, NOTIFICATIONS, ROLES & SETTINGS
# ==============================================================================

class SystemLog(models.Model):
    log_id = models.CharField(max_length=20, unique=True, blank=True)
    log_level = models.CharField(max_length=20, default="info")
    module = models.CharField(max_length=50, default="General")
    action = models.CharField(max_length=255)
    performed_by = models.CharField(max_length=100, default="System")
    ip_address = models.CharField(max_length=50, default="127.0.0.1")
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.log_id:
            last = SystemLog.objects.order_by("-id").first()
            next_num = (last.id + 1001) if last else 1001
            self.log_id = f"LOG{next_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.log_id} - {self.action}"


class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=30, default="info")
    recipient = models.CharField(max_length=100, default="All Admins")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class UserRole(models.Model):
    role_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    permissions_count = models.PositiveIntegerField(default=10)
    users_count = models.PositiveIntegerField(default=1)
    is_system = models.BooleanField(default=False)

    def __str__(self):
        return self.role_name


class GlobalSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    setting_group = models.CharField(max_length=50, default="General")
    description = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.key}: {self.value}"