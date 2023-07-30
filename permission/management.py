from django.apps import apps as global_apps
from django.contrib.auth import get_permission_codename
from django.contrib.contenttypes.management import create_contenttypes
from django.db import DEFAULT_DB_ALIAS, router


def _get_all_permissions(opts):
    """Return (codename, name) for all permissions in the given opts."""
    return [*_get_builtin_permissions(opts), *opts.permissions]


def _get_builtin_permissions(opts):
    """Return (codename, name) for all builtin permissions."""
    perms = []
    for action in ("add", "change", "delete", "view"):
        perms.append(
            (
                get_permission_codename(action, opts),
                "Can %s %s" % (action, opts.verbose_name_raw),
            )
        )
    return perms


def create_permissions(
    app_config,
    verbosity=2,
    interactive=True,
    using=DEFAULT_DB_ALIAS,
    apps=global_apps,
    **kwargs,
):
    if not app_config.models_module:
        return

    create_contenttypes(
        app_config,
        verbosity=verbosity,
        interactive=interactive,
        using=using,
        apps=apps,
        **kwargs,
    )

    app_label = app_config.label
    try:
        app_config = apps.get_app_config(app_label)
        ContentType = apps.get_model("contenttypes", "ContentType")
        Permission = apps.get_model("auth", "Permission")
    except LookupError:
        return

    if not router.allow_migrate(using, Permission):
        return
    # This will hold the permissions we're looking for as
    # (content_type, (codename, name))
    searched_perms = []
    # The codenames and ctypes that should exist.
    ctypes = set()
    for model in app_config.get_models():
        ctype = ContentType.objects.db_manager(using).get_for_model(
            model, for_concrete_model=False
        )

        ctypes.add(ctype)
        for perm in _get_all_permissions(model._meta):
            searched_perms.append((ctype, perm))

    # Find all the Permissions that have a context_type for a model we're
    # looking for. We don't need to check for codenames since we already have
    # a list of the ones we're going to create.
    all_perms = set(
        Permission.objects.using(using)
        .filter(
            content_type__in=ctypes,
        )
        .values_list("content_type", "codename")
    )

    perms = [
        Permission(codename=codename, name=name, content_type=ct)
        for ct, (codename, name) in searched_perms
        if (ct.pk, codename) not in all_perms
    ]
    Permission.objects.using(using).bulk_create(perms)
    if verbosity >= 2:
        for perm in perms:
            print("Adding permission '%s'" % perm)
