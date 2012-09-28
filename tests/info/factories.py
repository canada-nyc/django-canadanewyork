import datetime

from canada.apps.info.models import Info
from ..factories import DjangoFactory


class InfoFactory(DjangoFactory):
    FACTORY_FOR = Info

    text = '*italics* **bold**'

    date_added = datetime.date.today()
