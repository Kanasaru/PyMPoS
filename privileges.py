class PrivilegeType:
    def __init__(self, uid: int, name: str) -> None:
        self._uid = uid
        self._name = name

    @property
    def uid(self):
        return self._uid

    @property
    def name(self):
        return self._name

    def __repr__(self) -> str:
        return f'{self.name}({hex(self.uid)})'


class Privileges:
    READ     = PrivilegeType(0x01, 'READ')
    EDIT     = PrivilegeType(0x02, 'EDIT')
    ADD      = PrivilegeType(0x04, 'ADD')
    REMOVE   = PrivilegeType(0x08, 'REMOVE')
    IMPORT   = PrivilegeType(0x10, 'IMPORT')
    EXPORT   = PrivilegeType(0x20, 'EXPORT')
    APPROVE  = PrivilegeType(0x40, 'APPROVE')
    ACTIVATE = PrivilegeType(0x80, 'ACTIVATE')

    def __init__(self, permissions: int=0x00) -> None:
        self._permissions = permissions

    @property
    def permissions(self):
        return self._permissions
    
    @permissions.setter
    def permissions(self, value: int):
        if value <= 0xff:
            self._permissions = value

    def add_permission(self, permission: PrivilegeType):
        self.permissions |= permission.uid
    
    def remove_permission(self, permission: PrivilegeType):
        self.permissions &= ~permission.uid
    
    def has_permission(self, permission: PrivilegeType):
        return (self.permissions & permission.uid) == permission.uid
    
    def __repr__(self) -> str:
        return format(self.permissions, f'0{8}b')
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Privileges):
            return self.permissions == __value.permissions
        return False
