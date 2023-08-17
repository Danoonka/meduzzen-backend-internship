from typing import Optional

from pydantic import BaseModel


class Pagination(BaseModel):
    current_page: int
    total_page: int
    total_results: int


class CompanyBase(BaseModel):
    company_id: int
    company_name: str
    company_avatar: Optional[str] = None
    action_id: Optional[int] = None
    owner_id: Optional[int] = None


class CompanyCreateUpdate(BaseModel):
    company_name: str
    company_description: str


class Company(CompanyCreateUpdate):
    company_id: int
    owner_id: int
    company_visible: bool
    company_avatar: Optional[str] = None


class GetAllCompanies(BaseModel):
    company_list: list[CompanyBase]
    total_companies: int


class CompanyResponse(BaseModel):
    company_id: int
    company_name: str
    company_description: str
    owner_id: int
    company_visible: bool
    company_avatar: Optional[str] = None


class FullCompanyResponse(BaseModel):
    status_code: int
    detail: str
    result: CompanyResponse


class CompanyList(BaseModel):
    companies: list[CompanyBase]


class FullCompanyListResponse(BaseModel):
    status_code: int
    detail: str
    result: CompanyList
    pagination: Pagination


class CompanyId(BaseModel):
    company_id: int


class DeleteCompanyResponse(BaseModel):
    status_code: int
    detail: str
    result: CompanyId
