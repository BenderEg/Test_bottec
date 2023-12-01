from core.const import base_buttons
from db.shemas import User
from services.base_service import BaseService


class UserService(BaseService):

    async def register_user(self, id: int, name: str) -> User:
        user = await self.get_user_by_id(id)
        if user:
            user.name = name
        else:
            user = User(id=id, name=name)
            self.db.add(user)
        await self.db.refresh(user)
        await self.db.commit()
        return user

    async def start(self, id: int, name: str) -> str:
        user = await self.register_user(id, name)
        msg = f'Привет, {name}.\n'
        for_keybord = []
        if not user.group_subscription:
            for_keybord.append(('Оформить подписку на групповые рассылки.',
                               'group_subscription'))
        if not user.channel_subscription:
            for_keybord.append(('Оформить подписку на рассылки канала.',
                               'channel_subscription'))
        if not user.group_subscription and \
            not user.channel_subscription:
            for_keybord.append(('Оформить подписку на все рассылки.',
                               'subscribe'))
        for ele in base_buttons:
            for_keybord.append(ele)
        keybord = self.create_start_builder(for_keybord)
        return msg, keybord

    async def add_channel_subscription(self, id: int) -> None:
        user = await self.get_user_by_id(id)
        user.channel_subscription = True
        await self.db.commit()

    async def add_group_subscription(self, id: int) -> None:
        user = await self.get_user_by_id(id)
        user.group_subscription = True
        await self.db.commit()

    async def add_all_subscription(self, id: int) -> None:
        user = await self.get_user_by_id(id)
        user.group_subscription = True
        user.channel_subscription = True
        await self.db.commit()