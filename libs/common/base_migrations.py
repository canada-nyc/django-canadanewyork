import os

from django.db.models import Max


class BasePhotoMigration(object):
    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        OldPhoto = orm['photos.Photo']
        Objects = orm[orm.default_app + '.' + self.model_name]
        for photo in OldPhoto.objects.all():
            if photo.content_type.model == self.model_name.lower():
                instance = Objects.objects.get(pk=photo.object_id)
                max_pk = instance.new_photos.model.objects.aggregate(Max('id')).values()[0] or 0
                new_photo = instance.new_photos.create(id=max_pk + 1)
                new_photo.image.field.generate_filename = lambda instance, filename: os.path.join(
                    unicode(instance.content_object._meta.app_label),
                    unicode(instance.content_object.pk),
                    'photos',
                    'original',
                    filename
                )
                new_name = os.path.basename(photo.image.name)
                new_photo.image.save(new_name, photo.image.file, save=False)

                get_name = lambda _: _.name
                for field_name in map(get_name, photo._meta.fields):
                    if field_name in map(get_name, new_photo._meta.fields):
                        if 'image' not in field_name:
                            setattr(new_photo, field_name, getattr(photo, field_name))
                new_photo.save()

    def backwards(self, orm):
        "Write your backwards methods here."
        NewPhoto = orm[orm.default_app + '.' + self.model_name + 'Photo']
        NewPhoto.objects.all().delete()

    depends_on = (
        ("photos", "0002_add_artist_field"),
    )
