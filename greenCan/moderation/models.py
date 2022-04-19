# # from django.db import models

# # Create your models here.

# from django.db import models
# from recycle.models import ZipCode
# from reuse.models import Post


# class VolunteerLogs(models.Model):
#     id = models.ForeignKey(Post, null=False,on_delete=models.CASCADE)
#     reason = models.CharField(max_length=250, null=False)
#     approved = models.BooleanField(null=True, default=None)


#     def __str__(self):
#         return str(self.id)
