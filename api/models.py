from django.db import models
from django.contrib.auth.models import User


# Gallery Model
class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('Sports', 'Sports'),
        ('Cultural', 'Cultural'),
        ('Academic', 'Academic'),
        ('Events', 'Events'),
        ('Facilities', 'Facilities'),
        ('NCC', 'NCC'),
        ('Science', 'Science'),
        ('Celebrations', 'Celebrations'),
    ]
    
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
    
    def __str__(self):
        return self.title


# Contact Submission Model
class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


# Staff Model
class Staff(models.Model):
    STAFF_TYPE_CHOICES = [
        ('teaching', 'Teaching'),
        ('non_teaching', 'Non-Teaching'),
    ]
    
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    subject = models.CharField(max_length=100, blank=True, null=True)
    staff_type = models.CharField(max_length=20, choices=STAFF_TYPE_CHOICES)
    photo = models.ImageField(upload_to='staff/', blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    date_of_joining = models.DateField()
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Staff Member'
        verbose_name_plural = 'Staff Members'
    
    def __str__(self):
        return f"{self.name} - {self.designation}"


# Management Model
class ManagementMember(models.Model):
    POSITION_CHOICES = [
        ('committee', 'College Committee'),
        ('president', 'President'),
        ('secretary', 'Secretary'),
        ('principal', 'Principal'),
    ]
    
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    designation = models.CharField(max_length=100)
    message = models.TextField()
    qualification = models.CharField(max_length=200, blank=True, null=True)
    photo = models.ImageField(upload_to='management/', blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Management Member'
        verbose_name_plural = 'Management Members'
    
    def __str__(self):
        return f"{self.name} - {self.get_position_display()}"


# Student Registration Model
class StudentRegistration(models.Model):
    CLASS_CHOICES = [
        ('6', 'Class 6'),
        ('7', 'Class 7'),
        ('8', 'Class 8'),
        ('9', 'Class 9'),
        ('10', 'Class 10'),
        ('11', 'Class 11'),
        ('12', 'Class 12'),
    ]
    
    STREAM_CHOICES = [
        ('science', 'Science'),
        ('commerce', 'Commerce'),
        ('arts', 'Arts'),
    ]
    
    # Personal Details
    full_name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    mother_name = models.CharField(max_length=200)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    category = models.CharField(max_length=20)
    
    # Contact Details
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    
    # Academic Details
    previous_school = models.CharField(max_length=200)
    class_applying_for = models.CharField(max_length=10, choices=CLASS_CHOICES)
    stream = models.CharField(max_length=20, choices=STREAM_CHOICES, blank=True, null=True)
    previous_class_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    # Documents
    photo = models.ImageField(upload_to='registrations/photos/', blank=True, null=True)
    birth_certificate = models.FileField(upload_to='registrations/documents/', blank=True, null=True)
    marksheet = models.FileField(upload_to='registrations/documents/', blank=True, null=True)
    
    # Status
    registered_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-registered_at']
        verbose_name = 'Student Registration'
        verbose_name_plural = 'Student Registrations'
    
    def __str__(self):
        return f"{self.full_name} - Class {self.class_applying_for}"


# User Profile Extension
class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"
# Activity Model
class Activity(models.Model):
    CATEGORY_CHOICES = [
        ('Sports', 'Sports'),
        ('Cultural', 'Cultural'),
        ('Academic', 'Academic'),
        ('NCC', 'NCC'),
        ('Science', 'Science'),
        ('Social', 'Social Service'),
        ('Arts', 'Arts & Crafts'),
        ('Other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='activities/', blank=True, null=True)
    date = models.DateField()
    venue = models.CharField(max_length=200, blank=True, null=True)
    participants = models.IntegerField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
    
    def __str__(self):
        return f"{self.title} - {self.category}"