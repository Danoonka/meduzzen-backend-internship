from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_postgres_handler import get_session
from app.models.models_actions import FullActionResponse, DeleteActionResponse
from app.models.models_user import FullUserResponse, ListResponse
from app.routers.authintification import get_current_user
from app.routers.company import get_company_service
from app.routers.user import get_user_service
from app.services.actions import ActionsService
from app.services.company import CompanyService
from app.services.user import UserService
from app.utils.utils import toFullActionResponse

action_router = APIRouter()


async def get_action_service(session: AsyncSession = Depends(get_session)) -> ActionsService:
    return ActionsService(session)


@action_router.post('/invite-user/{company_id}/user/{user_id}/', response_model=FullActionResponse)
async def invite_user_endpoint(company_id: int, user_id: int,
                               current_user: FullUserResponse = Depends(get_current_user),
                               actions_service: ActionsService = Depends(get_action_service),
                               company_service: CompanyService = Depends(get_company_service),
                               user_service: UserService = Depends(get_user_service)
                               ) -> FullActionResponse:
    company = await company_service.get_company_by_id(company_id=company_id)
    user = await user_service.get_user_by_id(user_id=user_id)
    if current_user.result.user_id != company.owner_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    action = await actions_service.create_invite_action(user=user, company=company)
    return toFullActionResponse(action)


@action_router.delete('/decline-action', response_model=DeleteActionResponse)
async def decline_action_endpoint(action_id: int, current_user: FullUserResponse = Depends(get_current_user),
                                  actions_service: ActionsService = Depends(get_action_service),
                                  company_service: CompanyService = Depends(
                                      get_company_service)) -> DeleteActionResponse:
    action = await actions_service.get_action_by_id(action_id=action_id)
    company = await company_service.get_company_by_id(company_id=action.company_id)
    if current_user.result.user_id == company.owner_id or current_user.result.user_id == action.user_id:
        await actions_service.decline_action(action_id=action_id)
        return DeleteActionResponse(
            status_code=200,
            detail="Action decline",
            result=action_id
        )
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


@action_router.put('/accept-invite', response_model=FullActionResponse)
async def accept_invite_action_endpoint(action_id: int, current_user: FullUserResponse = Depends(get_current_user),
                                        actions_service: ActionsService = Depends(
                                            get_action_service)) -> FullActionResponse:
    action = await actions_service.get_action_by_id(action_id=action_id)

    if current_user.result.user_id == action.user_id:
        accept_invite = await actions_service.accept_invite_action(action=action)
        return toFullActionResponse(accept_invite)
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


@action_router.post('/request-company/{company_id}/user/{user_id}/', response_model=FullActionResponse)
async def create_request_action_endpoint(company_id: int, user_id: int,
                                         current_user: FullUserResponse = Depends(get_current_user),
                                         actions_service: ActionsService = Depends(
                                             get_action_service)) -> FullActionResponse:
    if current_user.result.user_id == user_id:
        action = await actions_service.create_request_action(user_id=user_id, company_id=company_id)
        return toFullActionResponse(action)
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


@action_router.put('/accept-request/', response_model=FullActionResponse)
async def accept_request(action_id: int, current_user: FullUserResponse = Depends(get_current_user),
                         actions_service: ActionsService = Depends(get_action_service),
                         company_service: CompanyService = Depends(get_company_service)) -> FullActionResponse:
    action = await actions_service.get_action_by_id(action_id=action_id)
    company = await company_service.get_company_by_id(company_id=action.company_id)
    if current_user.result.user_id == company.owner_id:
        accepted_request = await actions_service.accept_invite_action(action=action)
        return toFullActionResponse(accepted_request)
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


@action_router.get("/user-invites-list/{user_id}", response_model=ListResponse)
async def get_all_user_invites(user_id: int, actions_service: ActionsService = Depends(get_action_service),
                               current_user: FullUserResponse = Depends(get_current_user)) -> ListResponse:
    if current_user.result.user_id == user_id:
        invites = await actions_service.get_all_user_invites(user_id=user_id)
        return ListResponse(
            status_code=200,
            details='All invites got',
            result=invites
        )

    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


@action_router.get("/company-invites-list/{company_id}", response_model=ListResponse)
async def get_all_company_invites(company_id: int, actions_service: ActionsService = Depends(get_action_service),
                                  current_user: FullUserResponse = Depends(get_current_user),
                                  company_service: CompanyService = Depends(get_company_service)) -> ListResponse:
    company = await company_service.get_company_by_id(company_id=company_id)
    if current_user.result.user_id == company.owner_id:
        invites = await actions_service.get_all_company_invites(company_id=company_id)
        return ListResponse(
            status_code=200,
            details='All invited users got',
            result=invites
        )
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


@action_router.get("/user-request-list/{user_id}", response_model=ListResponse)
async def get_all_user_request(user_id: int, actions_service: ActionsService = Depends(get_action_service),
                               current_user: FullUserResponse = Depends(get_current_user)) -> ListResponse:
    if current_user.result.user_id == user_id:
        request = await actions_service.get_all_user_request(user_id=user_id)
        return ListResponse(
            status_code=200,
            details='All request got',
            result=request
        )

    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


@action_router.get("/company-request-list/{company_id}", response_model=ListResponse)
async def get_all_company_request(company_id: int, actions_service: ActionsService = Depends(get_action_service),
                                  current_user: FullUserResponse = Depends(get_current_user),
                                  company_service: CompanyService = Depends(get_company_service)) -> ListResponse:
    company = await company_service.get_company_by_id(company_id=company_id)
    if current_user.result.user_id == company.owner_id:
        request = await actions_service.get_all_company_request(company_id=company_id)
        return ListResponse(
            status_code=200,
            details='All users request got',
            result=request
        )
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


@action_router.get("/user-companies-list/{user_id}", response_model=ListResponse)
async def get_all_user_companies_endpoint(user_id: int, actions_service: ActionsService = Depends(get_action_service),
                                          current_user: FullUserResponse = Depends(get_current_user)) -> ListResponse:
    if current_user.result.user_id == user_id:
        companies = await actions_service.get_all_user_companies(user_id=user_id)
        return ListResponse(
            status_code=200,
            details='All companies got',
            result=companies
        )

    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


@action_router.get("/company-users-list/{company_id}", response_model=ListResponse)
async def get_all_members_endpoint(company_id: int,
                                   actions_service: ActionsService = Depends(get_action_service)) -> ListResponse:
    members = await actions_service.get_all_members(company_id=company_id)
    return ListResponse(
        status_code=200,
        details='All members got',
        result=members
    )
