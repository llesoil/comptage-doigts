from django.db import models

class Draw(models.Model):
    file_name = models.TextField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    pred_count = models.IntegerField()
    true_count = models.IntegerField(null=True)

    @classmethod
    def create(cls, file_name, date, pred_count, true_count=None):
        picture = cls(file_name = file_name, date = date, pred_count = pred_count, true_count = true_count)
        return picture

    def __str__(self):
        return self.file_name
