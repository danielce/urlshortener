from django.conf.urls import url

from .views import (OrganizationUpdateView, OrganizationUsersListView,
                    InvitationFormView)


urlpatterns = [
    url(r'^$', OrganizationUpdateView.as_view(), name="organization-info"),
    url(r'^users/$', OrganizationUsersListView.as_view(), name="users-list"),
    url(r'^users/invitation$', InvitationFormView.as_view(), name="user-invitation"),
]
