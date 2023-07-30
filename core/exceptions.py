from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Iterable, List, Optional, Union
from uuid import UUID

from graphql import GraphQLError


if TYPE_CHECKING:
    from ..order.models import OrderLine


class AllocationError(Exception):
    def __init__(self, order_lines):
        lines = [str(line) for line in order_lines]
        super().__init__(f"Unable to deallocate stock for lines {', '.join(lines)}.")
        self.order_lines = order_lines


class PreorderAllocationError(Exception):
    def __init__(self, order_line):
        super().__init__(f"Unable to allocate in stock for line {str(order_line)}.")
        self.order_line = order_line


class ReadOnlyException(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = "API runs in read-only mode"
        super().__init__(msg)




class PermissionDenied(Exception):
    def __init__(self, message=None, *, permissions: Optional[Iterable[Enum]] = None):
        if not message:
            if permissions:
                permission_list = ", ".join(p.name for p in permissions)
                message = (
                    f"You need one of the following permissions: {permission_list}"
                )
            else:
                message = "You do not have permission to perform this action"
        super().__init__(message)
        self.permissions = permissions



class CircularSubscriptionSyncEvent(GraphQLError):
    pass


class SyncEventError(Exception):
    def __init__(self, message, code=None):
        super(SyncEventError, self).__init__(message, code)
        self.message = message
        self.code = code

    def __str__(self):
        return self.message
