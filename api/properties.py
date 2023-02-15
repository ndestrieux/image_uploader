from enum import Enum


class UserTypeChoices(Enum):
    BASIC = "Basic"
    PREMIUM = "Premium"
    ENTERPRISE = "Enterprise"
    CUSTOM = "Custom"


thumbnail_size_properties = {
    UserTypeChoices.BASIC.name: [
        200,
    ],
    UserTypeChoices.PREMIUM.name: [
        200,
        400,
    ],
    UserTypeChoices.ENTERPRISE.name: [
        200,
        400,
    ],
    UserTypeChoices.CUSTOM.name: [],
}


original_image_properties = {
    UserTypeChoices.BASIC.name: False,
    UserTypeChoices.PREMIUM.name: True,
    UserTypeChoices.ENTERPRISE.name: True,
    UserTypeChoices.CUSTOM.name: False,
}


binary_image_properties = {
    UserTypeChoices.BASIC.name: False,
    UserTypeChoices.PREMIUM.name: False,
    UserTypeChoices.ENTERPRISE.name: True,
    UserTypeChoices.CUSTOM.name: False,
}
