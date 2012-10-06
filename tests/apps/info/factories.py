import datetime

from apps.info.models import Info
from ...common.factories import DjangoFactory


class InfoFactory(DjangoFactory):
    FACTORY_FOR = Info

    text = '*italics* **bold**'

    date_added = datetime.date.today()
