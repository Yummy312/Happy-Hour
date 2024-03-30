from app.companies.models import Company
from app.dao.base import BaseDAO


class CompanyDAO(BaseDAO):
    model = Company
