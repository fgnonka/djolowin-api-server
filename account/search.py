from typing import TYPE_CHECKING, List

from django.db.models import Q, Value, prefetch_related_objects


if TYPE_CHECKING:
    from .models import CustomUser, Address

USER_SEARCH_FIELDS = ["email", "first_name", "last_name"]
ADDRESS_SEARCH_FIELDS = [
    "first_name",
    "last_name",
    "street_address",
    "city",
    "postal_code",
    "country",
    "phone",
]


def prepare_user_search_document_value(
    user: "CustomUser",
    already_prefetched: bool = False,
    attach_addresses_data: bool = True,
):
    """Prepare 'search_document' value for a user instance - attach all fields that are used for search
    Parameter 'attach_addresses_data' is used to attach addresses data to the user instance and should be set
    to False only when user is created and addresses are not yet created or have been cleared
    """
    search_document = generate_user_fields_search_document_value(user)

    if attach_addresses_data:
        if not already_prefetched:
            prefetch_related_objects([user], "addresses")
        for address in user.addresses.all():
            search_document += generate_address_fields_search_document_value(address)

    return search_document.lower()


def generate_user_fields_search_document_value(user: "CustomUser") -> str:
    """Generate search document value for user fields"""
    value = "\n".join(
        [
            getattr(user, field_name, "")
            for field_name in USER_SEARCH_FIELDS
            if getattr(user, field_name)
        ]
    )
    if value:
        value += "\n"
    return value.lower()


def generate_address_fields_search_document_value(address: "Address") -> str:
    fields_values = [
        str(getattr(address, field_name, ""))
        if field_name != "country"
        else address.country.name + "\n" + address.country.code
        for field_name in ADDRESS_SEARCH_FIELDS
    ]
    return ("\n".join(fields_values) + "\n").lower()


def search_users(qs, value):
    if value:
        lookup = Q()
        for value_part in value.split():
            lookup &= Q(search_document__ilike=value.lower())
        qs = qs.filter(lookup)
    return qs