from allauth.account.signals import user_signed_up
from invitations.models import Invitation
from django.dispatch import receiver
from .models import Organization


def get_organization(email):
    created = False
    try:
        obj = Invitation.objects.get(
            email=email, accepted=True
        )
    except Invitation.DoesNotExist:
        o = Organization.objects.create(
            account_type=Organization.FREE
        )
        o.save()
        created = True
    else:
        o = obj.inviter.organization

    return o, created


@receiver(user_signed_up)
def user_signup(request, user, **kwargs):
    email = user.email
    created, user.organization = get_organization(email)
    if created:
        user.is_supervisor = True
    user.save()
