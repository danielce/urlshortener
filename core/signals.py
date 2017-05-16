from allauth.account.signals import user_signed_up
from invitations.models import Invitation
from django.dispatch import receiver
from .models import Organization


def get_organization(email):
    try:
        obj = Invitation.objects.get(
            email=email, accepted=True
        )
    except Invitation.DoesNotExist:
        o = Organization.objects.create(
            account_type=Organization.FREE
        )
        o.save()
    else:
        o = obj.inviter.organization

    return o


@receiver(user_signed_up)
def user_signup(request, user, **kwargs):
    email = user.email
    user.organization = get_organization(email)
    user.save()
