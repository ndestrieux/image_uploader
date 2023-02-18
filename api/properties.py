from enum import Enum


class UserTypeChoices(Enum):
    BASIC = "Basic"
    PREMIUM = "Premium"
    ENTERPRISE = "Enterprise"
    CUSTOM = "Custom"


profile_properties = {
    UserTypeChoices.BASIC.name: {
        "thumbnail_sizes": [
            200,
        ],
        "original_image_access": False,
        "binary_image_access": False,
    },
    UserTypeChoices.PREMIUM.name: {
        "thumbnail_sizes": [
            200,
            400,
        ],
        "original_image_access": True,
        "binary_image_access": False,
    },
    UserTypeChoices.ENTERPRISE.name: {
        "thumbnail_sizes": [
            200,
            400,
        ],
        "original_image_access": True,
        "binary_image_access": True,
    },
}
