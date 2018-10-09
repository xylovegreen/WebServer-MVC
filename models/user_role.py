import json
from enum import (
    Enum,
    auto,
)


class UserRole(Enum):
    guest = auto()
    normal = auto()
    admin = auto()


class UserRoleEncoder(json.JSONEncoder):
    prefix = "__enum"

    def default(self, o):
        if isinstance(o, UserRole):
            return {self.prefix: o.name}
        else:
            return super().default(self, o)


def userrole_decode(d):
    if UserRoleEncoder.prefix in d:
        name = d[UserRoleEncoder.prefix]
        return UserRole[name]
    else:
        return d