from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import (
    GalleryImage, ContactSubmission, Staff,
    ManagementMember, StudentRegistration, UserProfile,
    Activity
)
from .serializers import (
    GalleryImageSerializer, ContactSubmissionSerializer,
    StaffSerializer, ManagementMemberSerializer,
    StudentRegistrationSerializer, UserSerializer,
    UserProfileSerializer, UserRegistrationSerializer,
    ActivitySerializer
)


# Gallery ViewSet
class GalleryImageViewSet(viewsets.ModelViewSet):
    queryset = GalleryImage.objects.filter(is_active=True)
    serializer_class = GalleryImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['uploaded_at', 'title']
    ordering = ['-uploaded_at']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]


# Contact Submission ViewSet
class ContactSubmissionViewSet(viewsets.ModelViewSet):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_read']
    search_fields = ['name', 'email', 'subject']
    ordering_fields = ['submitted_at']
    ordering = ['-submitted_at']
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        submission = self.get_object()
        submission.is_read = True
        submission.save()
        return Response({'status': 'marked as read'})


# Staff ViewSet
class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.filter(is_active=True)
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['staff_type', 'is_active']
    search_fields = ['name', 'designation', 'qualification']
    ordering_fields = ['order', 'name', 'date_of_joining']
    ordering = ['order', 'name']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]
    
    @action(detail=False, methods=['get'])
    def teaching(self, request):
        teaching_staff = self.queryset.filter(staff_type='teaching')
        serializer = self.get_serializer(teaching_staff, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def non_teaching(self, request):
        non_teaching_staff = self.queryset.filter(staff_type='non_teaching')
        serializer = self.get_serializer(non_teaching_staff, many=True)
        return Response(serializer.data)


# Management ViewSet
class ManagementMemberViewSet(viewsets.ModelViewSet):
    queryset = ManagementMember.objects.filter(is_active=True)
    serializer_class = ManagementMemberSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['position', 'is_active']
    search_fields = ['name', 'designation']
    ordering_fields = ['order', 'name']
    ordering = ['order', 'name']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]
    
    @action(detail=False, methods=['get'])
    def by_position(self, request):
        position = request.query_params.get('position', None)
        if position:
            members = self.queryset.filter(position=position)
            serializer = self.get_serializer(members, many=True)
            return Response(serializer.data)
        return Response({'error': 'Position parameter required'}, status=400)


# Student Registration ViewSet
class StudentRegistrationViewSet(viewsets.ModelViewSet):
    queryset = StudentRegistration.objects.all()
    serializer_class = StudentRegistrationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_approved', 'class_applying_for', 'stream']
    search_fields = ['full_name', 'email', 'phone']
    ordering_fields = ['registered_at']
    ordering = ['-registered_at']
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        registration = self.get_object()
        registration.is_approved = True
        registration.remarks = request.data.get('remarks', '')
        registration.save()
        return Response({'status': 'approved'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        registration = self.get_object()
        registration.is_approved = False
        registration.remarks = request.data.get('remarks', '')
        registration.save()
        return Response({'status': 'rejected'})


# Authentication Views
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register new user (student/staff/admin)
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_type': user.profile.user_type
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Login user and return JWT tokens
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Please provide both username and password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_type': user.profile.user_type if hasattr(user, 'profile') else 'student'
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Logout user by blacklisting refresh token
    """
    try:
        refresh_token = request.data.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """
    Get current user profile
    """
    user = request.user
    profile = UserProfile.objects.get(user=user)
    serializer = UserProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    """
    Update current user profile
    """
    user = request.user
    profile = UserProfile.objects.get(user=user)
    serializer = UserProfileSerializer(profile, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Dashboard Stats (Admin only)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard_stats(request):
    """
    Get dashboard statistics for admin
    """
    stats = {
        'total_students': StudentRegistration.objects.count(),
        'approved_students': StudentRegistration.objects.filter(is_approved=True).count(),
        'pending_students': StudentRegistration.objects.filter(is_approved=False).count(),
        'total_staff': Staff.objects.filter(is_active=True).count(),
        'teaching_staff': Staff.objects.filter(staff_type='teaching', is_active=True).count(),
        'non_teaching_staff': Staff.objects.filter(staff_type='non_teaching', is_active=True).count(),
        'total_gallery_images': GalleryImage.objects.filter(is_active=True).count(),
        'unread_contacts': ContactSubmission.objects.filter(is_read=False).count(),
    }
    return Response(stats)

# Activity ViewSet
class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.filter(is_active=True)
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_featured', 'is_active']
    search_fields = ['title', 'description', 'venue']
    ordering_fields = ['date', 'created_at', 'title']
    ordering = ['-date', '-created_at']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_activities = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured_activities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category = request.query_params.get('category', None)
        if category:
            activities = self.queryset.filter(category=category)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({'error': 'Category parameter required'}, status=400)
