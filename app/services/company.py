from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models_user import CompanyDB, CompanyBase, GetAllCompanies, CompanyCreateUpdate, CompanyResponse


class CompanyService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_companies(self, page: int = 1, page_size: int = 10) -> GetAllCompanies:
        query = select(CompanyDB)
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        result = await self.session.execute(query)
        companies = result.scalars().all()

        total_companies = await self.session.scalar(select(func.count()).select_from(CompanyDB))
        companies_base_models = [
            CompanyBase(
                company_id=company.company_id,
                company_name=company.company_name,
                company_avatar=company.company_avatar
            ) for company in companies
        ]
        return GetAllCompanies(
            company_list=companies_base_models,
            total_companies=total_companies
        )

    async def get_company_by_id(self, company_id: int) -> CompanyDB:
        company = await self.session.scalar(
            select(CompanyDB).where(CompanyDB.company_id == company_id)
        )
        return company

    async def create_company(self, companyData: CompanyCreateUpdate, owner_id: int) -> CompanyResponse:
        company = CompanyDB(
            owner_id=owner_id,
            company_name=companyData.company_name,
            company_description=companyData.company_description
        )
        self.session.add(company)
        await self.session.flush()
        await self.session.commit()

        return company

    async def update_company(self, company: CompanyResponse, company_data: CompanyCreateUpdate) -> CompanyResponse:
        if company:
            for field, value in company_data.dict(exclude_unset=True).items():
                setattr(company, field, value)
            await self.session.flush()
            await self.session.commit()
            return company

    async def delete_company(self, company: CompanyResponse) -> int:
        if company:
            await self.session.delete(company)
            await self.session.flush()
            await self.session.commit()
        return company.company_id
