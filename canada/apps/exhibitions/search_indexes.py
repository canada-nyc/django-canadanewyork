from haystack import indexes
from .models import Exhibition


class ExhibitionIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Exhibition
