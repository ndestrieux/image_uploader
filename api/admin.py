from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from nested_admin.nested import NestedModelAdminMixin, NestedStackedInline

from api.models import CustomUser, Profile, RegularUser, ThumbnailSize


class CustomThumbnailSizeInlineAdminForm(NestedStackedInline):
    model = ThumbnailSize
    extra = 1


class CustomProfileInlineAdminForm(NestedStackedInline):
    model = Profile
    inlines = [
        CustomThumbnailSizeInlineAdminForm,
    ]
    can_delete = False


@admin.register(CustomUser)
class CustomUserAdmin(NestedModelAdminMixin, UserAdmin):
    model = CustomUser
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                    "type",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "type",
                )
            },
        ),
    )
    readonly_fields = ("type",)
    inlines = [
        CustomProfileInlineAdminForm,
    ]
    list_display = (
        "username",
        "type",
    )


class RegularThumbnailSizeInlineAdminForm(NestedStackedInline):
    model = ThumbnailSize
    readonly_fields = ("size",)
    extra = 0
    max_num = 0
    can_delete = False


class RegularProfileInlineAdminForm(NestedStackedInline):
    model = Profile
    inlines = [
        RegularThumbnailSizeInlineAdminForm,
    ]
    readonly_fields = (
        "original_image_access",
        "binary_image_access",
    )


@admin.register(RegularUser)
class RegularUserAdmin(NestedModelAdminMixin, UserAdmin):
    model = RegularUser
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                    "type",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "type",
                )
            },
        ),
    )
    inlines = [
        RegularProfileInlineAdminForm,
    ]
    list_display = (
        "username",
        "type",
    )

    def get_inline_instances(self, request, obj=None):
        return obj and super().get_inline_instances(request, obj) or []
