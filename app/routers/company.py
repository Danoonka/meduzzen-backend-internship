from math import ceil
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_postgres_handler import get_session
from app.models.models_user import CompanyCreateUpdate, FullUserResponse, FullCompanyResponse, FullCompanyListResponse, \
    CompanyList, Pagination, DeleteCompanyResponse, CompanyId
from app.routers.authintification import get_current_user
from app.services.company import CompanyService
from app.utils.utils import toFullCompanyResponse

company_router = APIRouter()
token_auth_scheme = HTTPBearer()


async def get_company_service(session: AsyncSession = Depends(get_session)) -> CompanyService:
    return CompanyService(session)


@company_router.get("/", response_model=FullCompanyListResponse)
async def get_companies(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1),
                        company_service: CompanyService = Depends(get_company_service)) -> FullCompanyListResponse:
    company_with_count = await company_service.get_all_companies(page=page, page_size=page_size)
    return FullCompanyListResponse(
        status_code=200,
        detail='Companies list successfully get',
        result=CompanyList(
            companies=company_with_count.company_list
        ),
        pagination=Pagination(
            current_page=page,
            total_page=ceil(company_with_count.total_companies / page_size),
            total_results=company_with_count.total_companies
        )
    )


@company_router.get("/{company_id}", response_model=FullCompanyResponse)
async def get_company(company_id: int,
                      company_service: CompanyService = Depends(get_company_service)) -> FullCompanyResponse:
    company = await company_service.get_company_by_id(company_id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return toFullCompanyResponse(company)


@company_router.post("/", response_model=FullCompanyResponse)
async def create_new_company(company_data: CompanyCreateUpdate,
                             company_service: CompanyService = Depends(get_company_service),
                             current_user: FullUserResponse = Depends(get_current_user)) -> FullCompanyResponse:
    company = await company_service.create_company(companyData=company_data, owner_id=current_user.result.user_id)
    return toFullCompanyResponse(company)


@company_router.put("/{company_id}", response_model=FullCompanyResponse)
async def update_existing_company(
        company_id: int,
        company_data: CompanyCreateUpdate,
        company_service: CompanyService = Depends(get_company_service),
        current_user: FullUserResponse = Depends(get_current_user)) -> FullCompanyResponse:
    company = await company_service.get_company_by_id(company_id=company_id)
    if current_user.result.user_id != company.owner_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    updatedCompany = await company_service.update_company(company=company, company_data=company_data)
    if not updatedCompany:
        raise HTTPException(status_code=404, detail="Company not found")

    return toFullCompanyResponse(updatedCompany)


@company_router.delete("/{company_id}", response_model=DeleteCompanyResponse)
async def delete_existing_company(company_id: int,
                                  company_service: CompanyService = Depends(get_company_service),
                                  current_user: FullUserResponse = Depends(get_current_user)) -> DeleteCompanyResponse:
    company = await company_service.get_company_by_id(company_id=company_id)
    if current_user.result.user_id != company.owner_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    company_id = await company_service.delete_company(company=company)
    if not company_id:
        raise HTTPException(status_code=404, detail="Company not found")
    return DeleteCompanyResponse(
        status_code=200,
        detail="Company delete successfully",
        result=CompanyId(
            company_id=company_id
        )
    )
