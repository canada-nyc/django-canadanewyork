from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.contrib.flatpages.models import FlatPage
from django.core.files.base import ContentFile
from django.core.cache import cache

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
        cache.clear()
        Exhibition = ExhibitionFactory.create(artists__n=0)

        exhibition_list = self.app.get(
            reverse('exhibition-list')
        )
        exhibition_list.click(
            unicode(Exhibition),
            href=reverse('exhibition-detail', kwargs={'slug': Exhibition.slug})
        )

    def test_artist_text(self):
        Exhibition = ExhibitionFactory.create(artists__n=1)
        exhibition_list = self.app.get(
            reverse('exhibition-list')
        )

        self.assertIn(Exhibition.join_artists, exhibition_list)


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

    def test_no_press_release_link(self):
        Exhibition = ExhibitionFactory.create()
        exhibition_detail = self.app.get(Exhibition.get_absolute_url())
        with self.assertRaises(IndexError):
            exhibition_detail.click(
                'Press Release',
                href=reverse('exhibition-pressrelease', kwargs={'slug': Exhibition.slug})
            )

    def test_press_release_link(self):
        Exhibition = ExhibitionFactory.create(description='_')
        exhibition_detail = self.app.get(Exhibition.get_absolute_url())

        exhibition_detail.click(
            'Press Release',
            href=reverse('exhibition-pressrelease', kwargs={'slug': Exhibition.slug})
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
        Press.content = '_'
        Press.save()
        exhibition_press_list = self.app.get(
            reverse('exhibition-press-list', kwargs={'slug': Exhibition.slug})
        )

        exhibition_press_list.click(
            unicode(Press),
            href=reverse('press-detail', kwargs={'slug': Press.slug}),
        )

    def test_content_file_link(self):
        Exhibition = ExhibitionFactory.create(press__n=1)
        Press = Exhibition.press.all()[0]

        Press.content_file.save('file.txt', ContentFile("my string content"))
        Press.save()

        exhibition_press_list = self.app.get(
            reverse('exhibition-press-list', kwargs={'slug': Exhibition.slug})
        )
        exhibition_press_list.click(
            unicode(Press),
            href=Press.content_file.url,
        )

    def test_date_text(self):
        Exhibition = ExhibitionFactory.create(press__n=1)
        Press = Exhibition.press.all()[0]
        Press.content = '_'
        Press.date_text ='some text'
        Press.save()

        exhibition_press_list = self.app.get(
            reverse('exhibition-press-list', kwargs={'slug': Exhibition.slug})
        )
        self.assertIn(Press.date_text, exhibition_press_list)


class ExhibitionPressReleaseTest(WebTest):
    def test_parent_link(self):
        Exhibition = ExhibitionFactory.create(description='a press release')
        exhibition_press_release = self.app.get(
            reverse('exhibition-pressrelease', kwargs={'slug': Exhibition.slug})
        )
        exhibition_press_release.click(
            unicode(Exhibition),
            href=Exhibition.get_absolute_url()
        )

    def test_content(self):
        Exhibition = ExhibitionFactory.create(description='a press release')
        exhibition_press_release = self.app.get(
            reverse('exhibition-pressrelease', kwargs={'slug': Exhibition.slug})
        )
        self.assertIn(Exhibition.description, exhibition_press_release)


class ExhibitionCurrentTest(WebTest):
    def test_unicode(self):
        Exhibition = ExhibitionFactory.create()
        exhibition_current = self.app.get(
            reverse('exhibition-current')
        )

        self.assertIn(unicode(Exhibition), exhibition_current)

    def test_artist_text(self):
        Exhibition = ExhibitionFactory.create(artists__n=1)
        exhibition_current = self.app.get(
            reverse('exhibition-current')
        )

        self.assertIn(Exhibition.join_artists, exhibition_current)

    def test_extra_info(self):
        Exhibition = ExhibitionFactory.create(extra_info='some info')
        exhibition_current = self.app.get(
            reverse('exhibition-current')
        )

        self.assertIn(Exhibition.extra_info, exhibition_current)

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

    def test_no_current_exhibition_flatpage_append(self):
        FlatPage_ = FlatPage.objects.create(
            url=reverse('exhibition-current'),
            title='_',
            content='some content',
        )
        exhibition_current = self.app.get(
            reverse('exhibition-current')
        )

        self.assertIn(FlatPage_.content, exhibition_current)
