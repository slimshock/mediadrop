# -*- coding: utf-8 -*-
# This file is a part of MediaCore CE, Copyright 2009-2012 MediaCore Inc.
# The source code in this file is dual licensed under the MIT license or the 
# GPL version 3 or (at your option) any later version.
# See LICENSE.txt in the main project directory, for more information.
#
# Copyright (c) 2012 Felix Schwarz (www.schwarz.eu)

__all__ = ['Resource', 'InsufficientPermissionsError', 'IPermissionPolicy', 
    'UserPermissions', 'PermissionSystem']


class Resource(object):
    def __init__(self, realm, id, **kwargs):
        self.realm = realm
        self.id = id
        self.data = kwargs


class IPermissionPolicy(object):
    permissions = ()
    
    def permits(self, permission, user_permissions, resource):
        return None


class InsufficientPermissionsError(Exception):
    def __init__(self, permission, resource=None):
        self.permission = permission
        self.resource = resource


class UserPermissions(object):
    
    def __init__(self, user, permission_system):
        self.user = user
        self.groups = set(user.groups)
        self.permission_system = permission_system
        self.data = {}
    
    def assert_permission(self, permission, resource=None):
        self.permission_system.assert_permission(permission, self, resource)
    
    def contains_permission(self, permission, resource=None):
        return self.permission_system.has_permission(permission, self, resource)



class PermissionSystem(object):
    def __init__(self, policies):
        self.policies = tuple(policies)
    
    def policies_for_permission(self, permission):
        applicable_policies = []
        for policy in self.policies:
            if permission in policy.permissions:
                applicable_policies.append(policy)
        return applicable_policies
    
    def assert_permission(self, permission, user_permissions, resource=None):
        decision = self.has_permission(permission, user_permissions, resource)
        if decision == False:
            self.raise_error(permission, resource)
    
    def has_permission(self, permission, user_permissions, resource=None):
        for policy in self.policies_for_permission(permission):
            decision = policy.permits(permission, user_permissions, resource)
            if decision in (True, False):
                return decision
        return False
    
    def raise_error(self, permission, resource):
        raise InsufficientPermissionsError(permission, resource)
