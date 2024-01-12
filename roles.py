from privileges import Privileges


class RoleType:
    """
    Represents a single role type with a unique ID, a name, and associated privileges.

    Attributes:
        uid (int): The unique identifier for the role.
        name (str): The name of the role.
        privileges (int): The associated privileges for the role.

    Methods:
        __repr__: Provides a string representation of the role.
    """
    def __init__(self, uid: int, name: str, privileges: int) -> None:
        """
        Initialize a RoleType instance.

        Args:
            uid (int): The unique identifier for the role.
            name (str): The name of the role.
            privileges (int): The associated privileges for the role.
        """
        self._uid = uid
        self._name = name
        self._privileges = privileges

    @property
    def uid(self):
        """Get the unique identifier of the role."""
        return self._uid

    @property
    def name(self):
        """Get the name of the role."""
        return self._name

    @property
    def privileges(self):
        """Get the associated privileges for the role."""
        return self._privileges

    def __repr__(self) -> str:
        """Return a string representation of the role."""
        return f'{self.name}({hex(self.uid)})'


class Roles:
    """
    Represents a collection of role types and their combined roles.

    Attributes:
        roles (int): The combined roles represented as an integer.
        privileges (dict): A dictionary of Privileges objects associated with each role type.

    Methods:
        add_role: Add a role to the combined roles.
        remove_role: Remove a role from the combined roles.
        has_role: Check if a role is assigned.
        __repr__: Provides a binary representation of the roles.
        __eq__: Compare two Roles objects based on their roles.
    """
    USER       = RoleType(0x01, 'User',          0x31)
    MANAGER    = RoleType(0x02, 'Manager',       0xff)
    CONTROLLER = RoleType(0x04, 'Controller',    0xff)
    AUDITOR    = RoleType(0x08, 'Auditor',       0x21)
    ADMIN      = RoleType(0x10, 'Administrator', 0xff)
    SYSTEMUSER = RoleType(0x20, 'System User',   0xf5)
    RESERVED_A = RoleType(0x40, 'RESERVED',      0x00)
    RESERVED_B = RoleType(0x80, 'RESERVED',      0x00)

    def __init__(self) -> None:
        """
        Initialize a Roles instance with default roles and associated privileges.
        """
        self._roles = 0x00
        self._privileges = {
            Roles.USER.uid: Privileges(Roles.USER.privileges),
            Roles.MANAGER.uid: Privileges(Roles.MANAGER.privileges),
            Roles.CONTROLLER.uid: Privileges(Roles.CONTROLLER.privileges),
            Roles.AUDITOR.uid: Privileges(Roles.AUDITOR.privileges),
            Roles.ADMIN.uid: Privileges(Roles.ADMIN.privileges),
            Roles.SYSTEMUSER.uid: Privileges(Roles.SYSTEMUSER.privileges),
            Roles.RESERVED_A.uid: Privileges(Roles.RESERVED_A.privileges),
            Roles.RESERVED_B.uid: Privileges(Roles.RESERVED_B.privileges)
        }

    @property
    def privileges(self):
        """Get the dictionary of associated Privileges objects for each role type."""
        return self._privileges

    @property
    def roles(self):
        """Get the combined roles."""
        return self._roles
    
    @roles.setter
    def roles(self, value: int):
        """Set the combined roles, if value is within 0x00 to 0xff range."""
        if value <= 0xff:
            self._roles = value

    def add_role(self, role: RoleType):
        """Add a role to the combined roles."""
        self.roles |= role.uid
    
    def remove_role(self, role: RoleType):
        """Remove a role from the combined roles."""
        self.roles &= ~role.uid
    
    def has_role(self, role: RoleType):
        """Check if a role is assigned."""
        return (self.roles & role.uid) == role.uid
    
    def __repr__(self) -> str:
        """Return a binary representation of the roles."""
        return format(self.roles, f'0{8}b')
    
    def __eq__(self, __value: object) -> bool:
        """Compare two Roles objects based on their roles."""
        if isinstance(__value, Roles):
            return self.roles == __value.roles
        return False
