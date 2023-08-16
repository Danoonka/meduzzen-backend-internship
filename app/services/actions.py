from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.models_actions import ActionBase
from app.models.models_user import Action, UserBase, CompanyBase
from app.utils.utils import toActionResponse


class ActionsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_invite_action(self, user: UserBase, company: CompanyBase) -> ActionBase:
        action = Action(
            user_id=user.user_id,
            company_id=company.company_id,
            action_type='invite',
        )
        self.session.add(action)
        await self.session.flush()
        await self.session.commit()

        return toActionResponse(action)

    async def get_action_by_id(self, action_id: int) -> Action:
        action = await self.session.scalar(
            select(Action).where(Action.action_id == action_id))

        return action

    async def decline_action(self, action_id: int) -> int:
        action = await self.get_action_by_id(action_id=action_id)
        if action:
            await self.session.delete(action)
            await self.session.flush()
            await self.session.commit()
        return action_id

    async def accept_invite_action(self, action: Action) -> Action:
        action.action_type = "member"
        self.session.add(action)
        await self.session.flush()
        await self.session.commit()

        return action

    async def add_owner_action(self, user: UserBase, company: CompanyBase) -> ActionBase:
        action = Action(
            user_id=user.user_id,
            company_id=company.company_id,
            action_type='owner',
        )
        self.session.add(action)
        await self.session.flush()
        await self.session.commit()

        return toActionResponse(action)

    async def create_request_action(self, user_id: int, company_id: int) -> ActionBase:
        action = Action(
            user_id=user_id,
            company_id=company_id,
            action_type='request',
        )
        self.session.add(action)
        await self.session.flush()
        await self.session.commit()

        return toActionResponse(action)

    async def get_all_user_invites(self, user_id: int) -> list[CompanyBase]:
        result = await self.session.execute(
            select(Action).where(Action.user_id == user_id).where(Action.action_type == "invite").options(
                selectinload(Action.company))
        )
        actions = result.scalars().all()

        companies_base_models = [
            CompanyBase(
                company_id=action.company.company_id,
                company_name=action.company.company_name,
                company_avatar=action.company.company_avatar,
                action_id=action.action_id,
                owner_id=action.company.owner_id
            ) for action in actions
        ]
        return companies_base_models

    async def get_all_company_invites(self, company_id: int) -> list[UserBase]:
        result = await self.session.execute(
            select(Action).where(Action.company_id == company_id).where(Action.action_type == "invite").options(
                selectinload(Action.user))
        )
        actions = result.scalars().all()
        user_base_models = [
            UserBase(
                user_id=action.user.user_id,
                user_email=action.user.user_email,
                user_firstname=action.user.user_firstname,
                user_lastname=action.user.user_lastname,
                user_avatar=action.user.user_avatar,
                action_id=action.action_id
            ) for action in actions
        ]
        return user_base_models

    async def get_all_user_request(self, user_id: int) -> list[CompanyBase]:
        result = await self.session.execute(
            select(Action).where(Action.user_id == user_id).where(Action.action_type == "request").options(
                selectinload(Action.company))
        )
        actions = result.scalars().all()

        companies_base_models = [
            CompanyBase(
                company_id=action.company.company_id,
                company_name=action.company.company_name,
                company_avatar=action.company.company_avatar,
                action_id=action.action_id,
                owner_id=action.company.owner_id
            ) for action in actions
        ]
        return companies_base_models

    async def get_all_company_request(self, company_id: int) -> list[UserBase]:
        result = await self.session.execute(
            select(Action).where(Action.company_id == company_id).where(Action.action_type == "request").options(
                selectinload(Action.user))
        )
        actions = result.scalars().all()
        user_base_models = [
            UserBase(
                user_id=action.user.user_id,
                user_email=action.user.user_email,
                user_firstname=action.user.user_firstname,
                user_lastname=action.user.user_lastname,
                user_avatar=action.user.user_avatar,
                action_id=action.action_id
            ) for action in actions
        ]
        return user_base_models

    async def get_all_members(self, company_id: int) -> list[UserBase]:
        result = await self.session.execute(
            select(Action).where(
                or_(
                    and_(
                        Action.company_id == company_id,
                        Action.action_type == "member"
                    ),
                    and_(
                        Action.company_id == company_id,
                        Action.action_type == "owner"
                    ),
                    and_(
                        Action.company_id == company_id,
                        Action.action_type == "admin"
                    )
                )
            ).options(selectinload(Action.user))
        )
        actions = result.scalars().all()
        user_base_models = [
            UserBase(
                user_id=action.user.user_id,
                user_email=action.user.user_email,
                user_firstname=action.user.user_firstname,
                user_lastname=action.user.user_lastname,
                user_avatar=action.user.user_avatar,
                action_id=action.action_id
            ) for action in actions
        ]
        return user_base_models

    async def get_all_user_companies(self, user_id: int) -> list[CompanyBase]:
        result = await self.session.execute(
            select(Action).where(
                or_(
                    and_(
                        Action.user_id == user_id,
                        Action.action_type == "member"
                    ),
                    and_(
                        Action.user_id == user_id,
                        Action.action_type == "owner"
                    ),
                    and_(
                        Action.user_id == user_id,
                        Action.action_type == "admin"
                    )
                )
            ).options(selectinload(Action.company))
        )
        actions = result.scalars().all()
        companies_base_models = [
            CompanyBase(
                company_id=action.company.company_id,
                company_name=action.company.company_name,
                company_avatar=action.company.company_avatar,
                action_id=action.action_id,
                owner_id=action.company.owner_id
            ) for action in actions
        ]
        return companies_base_models

    async def create_admin_action(self, action: Action) -> Action:
        action.action_type = "admin"
        self.session.add(action)
        await self.session.flush()
        await self.session.commit()

        return action

    async def get_all_admins(self, company_id: int) -> list[UserBase]:
        result = await self.session.execute(
            select(Action).where(and_(Action.company_id == company_id, Action.action_type == "admin")
                                 ).options(selectinload(Action.user))
        )
        actions = result.scalars().all()
        user_base_models = [
            UserBase(
                user_id=action.user.user_id,
                user_email=action.user.user_email,
                user_firstname=action.user.user_firstname,
                user_lastname=action.user.user_lastname,
                user_avatar=action.user.user_avatar,
                action_id=action.action_id
            ) for action in actions
        ]
        return user_base_models
