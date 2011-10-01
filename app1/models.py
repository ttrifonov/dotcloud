from django.db import models

class Object(models.Model):
    name = models.CharField(max_length=32, unique=True)
    template_name = models.CharField(max_length=256, blank=True)
    sort_order = models.IntegerField()

    def __str__(self):
        return "%s[%s]" % (self.name, self.template_name)

    class Meta:
        ordering = ["sort_order", "name"]
        db_table = 'Object'



