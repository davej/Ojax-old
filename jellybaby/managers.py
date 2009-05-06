import datetime
from django.db import models
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from tagging.fields import TagField

class ItemManager(models.Manager):
    
    def __init__(self):
        super(ItemManager, self).__init__()
        self.models_by_name = {}
    
    def create_or_update(self, instance, timestamp=None, tags="", source="INTERACTIVE", source_id="", username="", **kwargs):
        """
        Create or update an Item from some instace.
        """
        # If the instance hasn't already been saved, save it first. This
        # requires disconnecting the post-save signal that might be sent to
        # this function (otherwise we could get an infinite loop).
        if instance._get_pk_val() is None:
            try:
                signals.post_save.disconnect(self.create_or_update, sender=type(instance))
            except Exception, err:
                reconnect = False
            else:
                reconnect = True
            instance.save()
            if reconnect:
                signals.post_save.connect(self.create_or_update, sender=type(instance))
        
        # Make sure the item "should" be registered.
        if not getattr(instance, "jellybabyable", True):
            return
        
        # Check to see if the timestamp is being updated, possibly pulling
        # the timestamp from the instance.
        if hasattr(instance, "timestamp"):
            timestamp = instance.timestamp
        if timestamp is None:
            update_timestamp = False
            timestamp = datetime.datetime.now()
        else:
            update_timestamp = True
                    
        # Ditto for tags.
        if not tags:
            for f in instance._meta.fields:
                if isinstance(f, TagField):
                    tags = getattr(instance, f.attname)
                    break
        
        # Create the Item object.
        ctype = ContentType.objects.get_for_model(instance)
        item, created = self.get_or_create(
            content_type = ctype, 
            object_id = force_unicode(instance._get_pk_val()),
            defaults = dict(
                timestamp = timestamp,
                source = source,
                source_id = source_id,
                tags = tags,
                username = username,
            )
        )        
        item.tags = tags
        item.source = source
        item.source_id = source_id
        item.username = username
        if update_timestamp:
            item.timestamp = timestamp
            
        # Save and return the item.
        item.save()
        return item
        
    def follow_model(self, model):
        """
        Follow a particular model class, updating associated Items automatically.
        """
        self.models_by_name[model.__name__.lower()] = model
        signals.post_save.connect(self.create_or_update, sender=model)
        
    def get_for_model(self, model):
        """
        Return a QuerySet of only items of a certain type.
        """
        return self.filter(content_type=ContentType.objects.get_for_model(model))
        
    def get_last_update_of_model(self, model, **kwargs):
        """
        Return the last time a given model's items were updated. Returns the
        epoch if the items were never updated.
        """
        qs = self.get_for_model(model)
        if kwargs:
            qs = qs.filter(**kwargs)
        try:
            return qs.order_by('-timestamp')[0].timestamp
        except IndexError:
            return datetime.datetime.fromtimestamp(0)
