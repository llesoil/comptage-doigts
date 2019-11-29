from django.db import models

class Audio(models.Model):
    file_name = models.TextField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    pred_count = models.CharField(max_length=10)
    left_hand = models.BooleanField()
    true_count = models.IntegerField(null=True)

    @classmethod
    def create(cls, file_name, date, pred_count, lef_hand, true_count=None):
        audio = cls(file_name = file_name, date = date, pred_count = pred_count, left_hand = left_hand, true_count = true_count)
        return audio

    def __str__(self):
        return self.file_name
