from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    GalleryImageViewSet, ContactSubmissionViewSet,
    StaffViewSet, ManagementMemberViewSet,ActivityViewSet,
    StudentRegistrationViewSet, register_user,
    login_user, logout_user, get_user_profile,
    update_user_profile, dashboard_stats
)

router = DefaultRouter()
router.register(r'gallery', GalleryImageViewSet, basename='gallery')
router.register(r'contact', ContactSubmissionViewSet, basename='contact')
router.register(r'staff', StaffViewSet, basename='staff')
router.register(r'management', ManagementMemberViewSet, basename='management')
router.register(r'registrations', StudentRegistrationViewSet, basename='registrations')
router.register(r'activities', ActivityViewSet, basename='activities')

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),
    
    # Authentication URLs
    path('auth/register/', register_user, name='register'),
    path('auth/login/', login_user, name='login'),
    path('auth/logout/', logout_user, name='logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', get_user_profile, name='user_profile'),
    path('auth/profile/update/', update_user_profile, name='update_profile'),
    
    # Dashboard
    path('dashboard/stats/', dashboard_stats, name='dashboard_stats'),
]
