from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('create_profile', views.createProfile, name="create-profile"),
    path('profile_user', views.profileUser, name="profile-user"),
    path('profile_user_edit', views.updateProfileUser, name="profile-user-edit"),
    path('post', views.post, name='post'),
    path('post_view/<slug:slug>', views.postView, name='post-view'),
    path('edit_comment/<int:pk>', views.editComment, name='edit-comment'),
    path('delete_comment/<int:pk>', views.deleteComment, name='delete-comment'),
    path('report', views.sendReport, name='report'),
    path('delete_account', views.deleteAccount, name='delete-account'),
    path('conf_delete_account', views.confDeleteAccount, name='conf-delete-account'),
    path('notification', views.notification, name='notification'),
]
