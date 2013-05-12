from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.contrib.flatpages.models import FlatPage

from .factories import ExhibitionFactory


class ExhibitionListTest(WebTest):
    def test_reverse(self):
        self.app.get(
            reverse('exhibition-list')
        )

    def test_nav_click(self):
        exhibition_list = self.app.get(
            reverse('exhibition-list')
        )
        exhibition_list.click(
            'Exhibitions',
            href=reverse('exhibition-list')
        )

    def test_detail_link(self):
        Exhibition = ExhibitionFactory.create()
        exhibition_list = self.app.get(
            reverse('exhibition-list')
        )

        exhibition_list.click(
            unicode(Exhibition),
            href=reverse('exhibition-detail', kwargs={'slug': Exhibition.slug})
        )


class ExhibitionDetailTest(WebTest):
    def test_unicode(self):
        Exhibition = ExhibitionFactory.create()
        exhibition_detail = self.app.get(Exhibition.get_absolute_url())
        self.assertIn(unicode(Exhibition), exhibition_detail)

    def test_description(self):
        Exhibition = ExhibitionFactory.create(description='description')
        exhibition_detail = self.app.get(Exhibition.get_absolute_url())
        self.assertIn(Exhibition.description, exhibition_detail)

    def test_artist_link(self):
        Exhibition = ExhibitionFactory.create(artists__n=1)
        Artist = Exhibition.artists.all()[0]
        exhibition_detail = self.app.get(Exhibition.get_absolute_url())

        exhibition_detail.click(
            unicode(Artist),
            href=Artist.get_absolute_url()
        )

    def test_invisible_artist_no_link(self):
        Exhibition = ExhibitionFactory.create(artists__n=1, artists__visible=False)
        Artist = Exhibition.artists.all()[0]
        exhibition_detail = self.app.get(Exhibition.get_absolute_url())

        self.assertIn(unicode(Artist), exhibition_detail)
        with self.assertRaises(IndexError):
            exhibition_detail.click(
                unicode(Artist),
                href=Artist.get_absolute_url()
            )

    def test_no_press_link(self):
        Exhibition = ExhibitionFactory.create()
        exhibition_detail = self.app.get(Exhibition.get_absolute_url())
        with self.assertRaises(IndexError):
            exhibition_detail.click(
                'Press',
                href=reverse('exhibition-press-list', kwargs={'slug': Exhibition.slug})
            )

    def test_press_link(self):
        Exhibition = ExhibitionFactory.create(press__n=1)
        exhibition_detail = self.app.get(Exhibition.get_absolute_url())

        exhibition_detail.click(
            'Press',
            href=reverse('exhibition-press-list', kwargs={'slug': Exhibition.slug})
        )


class ExhibitionPressListTest(WebTest):
    def test_parent_link(self):
        Exhibition = ExhibitionFactory.create()
        exhibition_press_list = self.app.get(
            reverse('exhibition-press-list', kwargs={'slug': Exhibition.slug})
        )

        exhibition_press_list.click(
            unicode(Exhibition),
            href=Exhibition.get_absolute_url()
        )

    def test_detail_link(self):
        Exhibition = ExhibitionFactory.create(press__n=1)
        Press = Exhibition.press.all()[0]
        exhibition_press_list = self.app.get(
            reverse('exhibition-press-list', kwargs={'slug': Exhibition.slug})
        )

        exhibition_press_list.click(
            unicode(Press),
            href=reverse('press-detail', kwargs={'slug': Press.slug}),
        )


class ExhibitionCurrentTest(WebTest):
    def test_unicode(self):
        Exhibition = ExhibitionFactory.create()
        exhibition_current = self.app.get(
            reverse('exhibition-current')
        )

        self.assertIn(unicode(Exhibition), exhibition_current)

    def test_link_to_exhibition(self):
        Exhibition = ExhibitionFactory.create()
        exhibition_current = self.app.get(
            reverse('exhibition-current')
        )
        exhibition_current.click(
            href=Exhibition.get_absolute_url()
        )

    def test_flatpage_append(self):
        ExhibitionFactory.create()
        FlatPage_ = FlatPage.objects.create(
            url=reverse('exhibition-current'),
            title='_',
            content='some content',
        )
        exhibition_current = self.app.get(
            reverse('exhibition-current')
        )

        self.assertIn(FlatPage_.content, exhibition_current)
