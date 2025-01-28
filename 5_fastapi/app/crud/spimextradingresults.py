from crud.base import CRUDBase
from models import SpimexTradingResults


class CRUDSpimexTradingResults(CRUDBase): pass


spimextradingresults_crud = CRUDSpimexTradingResults(SpimexTradingResults)
