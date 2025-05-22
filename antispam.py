import json
from typing import Union

from twisted.web.resource import Resource
from twisted.web.server import Request

from synapse.module_api import ModuleApi

import logging

logger = logging.getLogger(__name__)


class ExceptionsAntiSpam:
    def __init__(self, config: dict, api: ModuleApi):
        self.api = api
        self.evil_users = config.get("evil_users") or []
        logger.info('exception\'s custom antispam online')

        self.api.register_spam_checker_callbacks(
            user_may_invite=self.user_may_invite,
            user_may_create_room=self.user_may_create_room,
        )

    def user_good(self, user: str) -> bool:
        if user.endswith(":parat.swiss"):
            return True;
        elif user.endswith(":treff.top"):
            return True;
        else:
            if len(user) > 128:
                return False;
            else:
                return True;

    async def user_may_invite(inviter: str, invitee: str, room_id: str) -> bool:
        if user_good(inviter):
            return True
        else:
            logger.info('invite from user %s blocked', inviter)
            return false

    async def user_may_create_room(user: str) -> bool:
        if user.endswith(":parat.swiss"):
            return True
        else:
            logger.info('room create from user %s blocked', user)
            return False

