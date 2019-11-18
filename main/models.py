from django.db import models


# Create your models here.


class Questions(models.Model):
    QuestionKeywords = models.CharField(max_length=500)
    Response = models.CharField(max_length=2500)
    Attachment = models.CharField(max_length=500)
    ResponseLink = models.IntegerField()
    MinMatchScore = models.IntegerField(default=0)
    FuzzyResponse = models.CharField(default=0,max_length=2500)

    def __str__(self):
        #return  {"id" : self.id, "Keys": self.QuestionKeywords, "Response": self.Response}
        return "Question "+ str(self.id) + " : " + self.QuestionKeywords

