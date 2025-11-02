from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html
from .models import (
    GalleryImage, ContactSubmission, Staff, 
    ManagementMember, StudentRegistration, UserProfile, Activity
)

# Custom Admin Site Configuration
admin.site.site_header = "ASIC Mawana Administration"
admin.site.site_title = "ASIC Admin Portal"
admin.site.index_title = "Welcome to ASIC College Administration"

# Gallery Image Admin
@admin.register(GalleryImage)
class GalleryImageAdmin(ModelAdmin):
    list_display = ['image_preview', 'title', 'category', 'uploaded_at', 'is_active']
    list_filter = ['category', 'is_active', 'uploaded_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    date_hierarchy = 'uploaded_at'
    list_per_page = 20
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px; border: 2px solid rgba(14, 165, 233, 0.3);" />',
                obj.image.url
            )
        return format_html('<span style="color: #9ca3af;">No Image</span>')
    image_preview.short_description = 'Preview'

# Contact Submission Admin
@admin.register(ContactSubmission)
class ContactSubmissionAdmin(ModelAdmin):
    list_display = ['name', 'email', 'subject', 'submitted_at', 'status_badge']
    list_filter = ['is_read', 'submitted_at']
    search_fields = ['name', 'email', 'subject', 'message']
    date_hierarchy = 'submitted_at'
    readonly_fields = ['submitted_at']
    list_per_page = 25
    
    def status_badge(self, obj):
        if obj.is_read:
            return format_html(
                '<span style="background: #10b981; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">✓ Read</span>'
            )
        return format_html(
            '<span style="background: #f59e0b; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">● New</span>'
        )
    status_badge.short_description = 'Status'
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'✓ {updated} message(s) marked as read.')
    mark_as_read.short_description = "✓ Mark as read"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} message(s) marked as unread.')
    mark_as_unread.short_description = "○ Mark as unread"

# Staff Admin
@admin.register(Staff)
class StaffAdmin(ModelAdmin):
    list_display = ['photo_preview', 'name', 'designation', 'staff_type', 'date_of_joining', 'is_active']
    list_filter = ['staff_type', 'is_active']
    search_fields = ['name', 'designation']
    list_editable = ['is_active']
    list_per_page = 20
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%; border: 2px solid #0ea5e9;" />',
                obj.photo.url
            )
        return format_html(
            '<div style="width: 50px; height: 50px; background: linear-gradient(135deg, #0ea5e9, #06b6d4); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 18px;">{}</div>',
            obj.name[0].upper() if obj.name else '?'
        )
    photo_preview.short_description = 'Photo'

# Management Member Admin
@admin.register(ManagementMember)
class ManagementMemberAdmin(ModelAdmin):
    list_display = ['photo_preview', 'name', 'position', 'designation', 'is_active']
    list_filter = ['position', 'is_active']
    search_fields = ['name', 'designation']
    list_editable = ['is_active']
    list_per_page = 20
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%; border: 2px solid #0ea5e9;" />',
                obj.photo.url
            )
        return format_html(
            '<div style="width: 50px; height: 50px; background: linear-gradient(135deg, #0ea5e9, #06b6d4); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 18px;">{}</div>',
            obj.name[0].upper() if obj.name else '?'
        )
    photo_preview.short_description = 'Photo'

# Student Registration Admin
@admin.register(StudentRegistration)
class StudentRegistrationAdmin(ModelAdmin):
    list_display = ['photo_preview', 'full_name', 'class_applying_for', 'registered_at', 'approval_badge']
    list_filter = ['is_approved', 'class_applying_for', 'stream']
    search_fields = ['full_name', 'email']
    date_hierarchy = 'registered_at'
    readonly_fields = ['registered_at']
    list_per_page = 25
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;" />',
                obj.photo.url
            )
        return format_html('<span style="color: #9ca3af;">No Photo</span>')
    photo_preview.short_description = 'Photo'
    
    def approval_badge(self, obj):
        if obj.is_approved:
            return format_html(
                '<span style="background: #10b981; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">✓ Approved</span>'
            )
        return format_html(
            '<span style="background: #ef4444; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600;">⏳ Pending</span>'
        )
    approval_badge.short_description = 'Status'
    
    actions = ['approve_applications', 'reject_applications']
    
    def approve_applications(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'✓ {updated} application(s) approved.')
    approve_applications.short_description = "✓ Approve selected"
    
    def reject_applications(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'✗ {updated} application(s) rejected.')
    reject_applications.short_description = "✗ Reject selected"

# Activity Admin - FIXED
@admin.register(Activity)
class ActivityAdmin(ModelAdmin):
    list_display = ['image_preview', 'title', 'category', 'date', 'is_featured', 'is_active']
    list_filter = ['category', 'is_featured', 'is_active']
    search_fields = ['title', 'description']
    list_editable = ['is_featured', 'is_active']
    date_hierarchy = 'date'
    list_per_page = 20
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px; border: 2px solid rgba(14, 165, 233, 0.3);" />',
                obj.image.url
            )
        return format_html('<span style="color: #9ca3af;">No Image</span>')
    image_preview.short_description = 'Preview'

# User Profile Admin
@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    list_display = ['user', 'user_type', 'phone']
    list_filter = ['user_type']
    search_fields = ['user__username', 'phone']
    list_per_page = 25
