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

    async def get_action_by_id(self, action_id: int) -> ActionBase:
        action = await self.session.scalar(
            select(Action).where(Action.action_id == action_id))

        return toActionResponse(action)

    async def decline_action(self, action_id: int) -> int:
        action = await self.get_action_by_id(action_id=action_id)
        if action:
            await self.session.delete(action)
            await self.session.flush()
            await self.session.commit()
        return action_id

    async def accept_invite_action(self, action: Action) -> ActionBase:
        action.action_type = "member"
        self.session.add(action)
        await self.session.flush()
        await self.session.commit()

        return  toActionResponse(action)

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
        companies = [action.company for action in actions if action.company]

        companies_base_models = [
            CompanyBase(
                company_id=company.company_id,
                company_name=company.company_name,
                company_avatar=company.company_avatar
            ) for company in companies
        ]
        return companies_base_models

    async def get_all_company_invites(self, company_id: int) -> list[UserBase]:
        result = await self.session.execute(
            select(Action).where(Action.company_id == company_id).where(Action.action_type == "invite").options(
                selectinload(Action.user))
        )
        actions = result.scalars().all()
        users = [action.user for action in actions if action.user]
        user_base_models = [
            UserBase(
                user_id=user.user_id,
                user_email=user.user_email,
                user_firstname=user.user_firstname,
                user_lastname=user.user_lastname,
                user_avatar=user.user_avatar
            ) for user in users
        ]
        return user_base_models

    async def get_all_user_request(self, user_id: int) -> list[CompanyBase]:
        result = await self.session.execute(
            select(Action).where(Action.user_id == user_id).where(Action.action_type == "request").options(
                selectinload(Action.company))
        )
        actions = result.scalars().all()
        companies = [action.company for action in actions if action.company]

        companies_base_models = [
            CompanyBase(
                company_id=company.company_id,
                company_name=company.company_name,
                company_avatar=company.company_avatar
            ) for company in companies
        ]
        return companies_base_models

    async def get_all_company_request(self, company_id: int) -> list[UserBase]:
        result = await self.session.execute(
            select(Action).where(Action.company_id == company_id).where(Action.action_type == "request").options(
                selectinload(Action.user))
        )
        actions = result.scalars().all()
        users = [action.user for action in actions if action.user]
        user_base_models = [
            UserBase(
                user_id=user.user_id,
                user_email=user.user_email,
                user_firstname=user.user_firstname,
                user_lastname=user.user_lastname,
                user_avatar=user.user_avatar
            ) for user in users
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
                    )
                )
            ).options(selectinload(Action.user))
        )
        actions = result.scalars().all()
        users = [action.user for action in actions if action.user]
        user_base_models = [
            UserBase(
                user_id=user.user_id,
                user_email=user.user_email,
                user_firstname=user.user_firstname,
                user_lastname=user.user_lastname,
                user_avatar=user.user_avatar
            ) for user in users
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
                    )
                )
            ).options(selectinload(Action.company))
        )
        actions = result.scalars().all()
        companies = [action.company for action in actions if action.company]
        companies_base_models = [
            CompanyBase(
                company_id=company.company_id,
                company_name=company.company_name,
                company_avatar=company.company_avatar
            ) for company in companies
        ]
        return companies_base_models
