from django.urls import path, include
from . import views

urlpatterns = [
    # =========================
    # FRONTEND PAGES
    # =========================
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('history/', views.history, name='history'),

    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),

    path('apply/<int:job_id>/', views.apply, name='apply'),
    path('applied_jobs/', views.applied_jobs, name='applied_jobs'),

    # =========================
    # AUTH / PASSWORD
    # =========================
    path('accounts/', include('allauth.urls')),
    path('activate/<int:user_id>/', views.activate_account, name='activate_account'),

    path('password_reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path(
        'password_reset_confirm/<uidb64>/<token>/',
        views.MyPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'password_reset_complete/',
        views.MyPasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),

    # =========================
    # BACKEND API (IMPORTANT)
    # =========================
    path('api/jobs/', views.api_jobs, name='api_jobs'),
]
