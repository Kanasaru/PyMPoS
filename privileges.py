class PrivilegeType:
    """
    Represents a single privilege type with a unique ID and a name.

    Attributes:
        uid (int): The unique identifier for the privilege.
        name (str): The name of the privilege.

    Methods:
        __repr__: Provides a string representation of the privilege.
    """
    def __init__(self, uid: int, name: str) -> None:
        """
        Initialize a PrivilegeType instance.

        Args:
            uid (int): The unique identifier for the privilege.
            name (str): The name of the privilege.
        """
        self._uid = uid
        self._name = name

    @property
    def uid(self):
        """Get the unique identifier of the privilege."""
        return self._uid

    @property
    def name(self):
        """Get the name of the privilege."""
        return self._name

    def __repr__(self) -> str:
        """Return a string representation of the privilege."""
        return f'{self.name}({hex(self.uid)})'


class Privileges:
    """
    Represents a collection of privilege types and their combined permissions.

    Attributes:
        permissions (int): The combined permissions represented as an integer.

    Methods:
        add_permission: Add a privilege to the permissions.
        remove_permission: Remove a privilege from the permissions.
        has_permission: Check if a privilege is granted.
        __repr__: Provides a binary representation of the permissions.
        __eq__: Compare two Privileges objects based on their permissions.
    """
    READ     = PrivilegeType(0x01, 'READ')
    EDIT     = PrivilegeType(0x02, 'EDIT')
    ADD      = PrivilegeType(0x04, 'ADD')
    REMOVE   = PrivilegeType(0x08, 'REMOVE')
    IMPORT   = PrivilegeType(0x10, 'IMPORT')
    EXPORT   = PrivilegeType(0x20, 'EXPORT')
    APPROVE  = PrivilegeType(0x40, 'APPROVE')
    ACTIVATE = PrivilegeType(0x80, 'ACTIVATE')

    def __init__(self, permissions: int = 0x00) -> None:
        """
        Initialize a Privileges instance with optional initial permissions.

        Args:
            permissions (int): Initial permissions (default is 0x00).
        """
        self._permissions = permissions

    @property
    def permissions(self):
        """Get the combined permissions."""
        return self._permissions
    
    @permissions.setter
    def permissions(self, value: int):
        """Set the combined permissions, if value is within 0x00 to 0xff range."""
        if value <= 0xff:
            self._permissions = value

    def add_permission(self, permission: PrivilegeType):
        """Add a privilege to the permissions."""
        self.permissions |= permission.uid
    
    def remove_permission(self, permission: PrivilegeType):
        """Remove a privilege from the permissions."""
        self.permissions &= ~permission.uid
    
    def has_permission(self, permission: PrivilegeType):
        """Check if a privilege is granted."""
        return (self.permissions & permission.uid) == permission.uid
    
    def __repr__(self) -> str:
        """Return a binary representation of the permissions."""
        return format(self.permissions, f'0{8}b')
    
    def __eq__(self, __value: object) -> bool:
        """Compare two Privileges objects based on their permissions."""
        if isinstance(__value, Privileges):
            return self.permissions == __value.permissions
        return False
