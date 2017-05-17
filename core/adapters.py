from invitations.adapters import BaseInvitationsAdapter
from .models import create_simple_organization


class OrganizationAdapter(BaseInvitationsAdapter):
    def save_user(self, request, user, form, commit=False):
        user.organization = create_simple_organization()
        user.is_supervisor = True
        return super(OrganizationAdapter, self).save_user(request, user, form, commit)