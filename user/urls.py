from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import user_views, team_views
# urlpatterns = [
# 	path('', manual_views.redirect, name="redirect"),
# 	path('login/', views.login, {'template_name':'login/login.html','authentication_form':forms.LoginForm}),
# 	path('logout/', views.logout, {'next_page':'/'}, name="logout"),
# 	path('register/', manual_views.register, name="register"),
# 	path('profile/', manual_views.profile, name="profile"),
# 	path('team/', manual_views.team_view, name="team_view"),
# 	re_path('team/(?P<pk>.+)', manual_views.every_team, name="every_team"),
# 	path('profile/changepassword/', manual_views.update_password, name="update_password")
# ]
app_name = 'user'
urlpatterns = [
    # ,'authentication_form': 'forms.RegisterForm'
    path('login/', user_views.login, name='login'),
    path('logout/', user_views.logout, name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('register/', user_views.register, name='register'),
    path('chgpasswd/', user_views.changepassword, name='changepassword'),
    path('team/register', team_views.register, name='teamregister'),
    path('team/profile', team_views.profile, name='teamprofile'),
    path('team/join', team_views.join, name='teamjoin'),
    path('team/apply/<int:apply_id>/approved',
         team_views.applyapproved, name='teamapplyapproved'),
    path('team/apply/<int:apply_id>/denied',
         team_views.applydenied, name='teamapplydenied'),

    path('team/<int:user_id>/expel', team_views.expel, name='teamexpel'),
    path('team/<int:team_id>/dismiss', team_views.dismiss, name='teamdismiss'),
]
