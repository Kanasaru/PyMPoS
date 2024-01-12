from privileges import Privileges


class RoleType:
    def __init__(self, uid: int, name: str, privileges: int) -> None:
        self._uid = uid
        self._name = name
        self._privileges = privileges

    @property
    def uid(self):
        return self._uid

    @property
    def name(self):
        return self._name

    @property
    def privileges(self):
        return self._privileges

    def __repr__(self) -> str:
        return f'{self.name}({hex(self.uid)})'


class Roles:
    USER       = RoleType(0x01, 'User',         0x31)
    MANAGER    = RoleType(0x02, 'Manager',      0xff)
    CONTROLLER = RoleType(0x04, 'Controller',   0xff)
    AUDITOR    = RoleType(0x08, 'Auditor',      0x21)
    ADMIN      = RoleType(0x10, 'Adminitrator', 0xff)
    SYSTEMUSER = RoleType(0x20, 'System User',  0xf5)
    RESERVED_0 = RoleType(0x40, 'RESERVED',     0x00)
    RESERVED_1 = RoleType(0x80, 'RESERVED',     0x00)

    def __init__(self) -> None:
        self._roles = 0x00
        self._privileges = {
            Roles.USER.uid: Privileges(Roles.USER.privileges),
            Roles.MANAGER.uid: Privileges(Roles.MANAGER.privileges),
            Roles.CONTROLLER.uid: Privileges(Roles.CONTROLLER.privileges),
            Roles.AUDITOR.uid: Privileges(Roles.AUDITOR.privileges),
            Roles.ADMIN.uid: Privileges(Roles.ADMIN.privileges),
            Roles.SYSTEMUSER.uid: Privileges(Roles.SYSTEMUSER.privileges),
            Roles.RESERVED_0.uid: Privileges(Roles.RESERVED_0.privileges),
            Roles.RESERVED_1.uid: Privileges(Roles.RESERVED_1.privileges)
        }

    @property
    def privileges(self):
        return self._privileges

    @property
    def roles(self):
        return self._roles
    
    @roles.setter
    def roles(self, value: int):
        if value <= 0xff:
            self._roles = value

    def add_role(self, role: RoleType):
        self.roles |= role.uid
    
    def remove_role(self, role: RoleType):
        self.roles &= ~role.uid
    
    def has_role(self, role: RoleType):
        return (self.roles & role.uid) == role.uid
    
    def __repr__(self) -> str:
        return format(self.roles, f'0{8}b')
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Roles):
            return self.roles == __value.roles
        return False
