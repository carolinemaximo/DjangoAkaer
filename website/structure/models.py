from django.db import models
from django.contrib.auth.models import Group, User
from django.conf import settings


class Topic(models.Model): # Topic = Empresa
    top_name = models.CharField(max_length=264,unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.top_name
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    

 
class Entry(models.Model): # Entry = Projeto
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    collaborators = models.ManyToManyField(User, related_name='permitted_entries')
    group = models.OneToOneField(Group, on_delete=models.CASCADE, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entry_creator')
    class Meta:
        verbose_name_plural = 'entries'
    def __str__(self):
        return self.text[:50] + "..."   
    
    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)
        if creating:
            self.group = Group.objects.create(name=f"entry_{self.pk}")
            self.save()  # Salva o objeto Entry após criar o grupo


    def delete(self, *args, **kwargs):
        if self.group:
            self.group.delete()
        super().delete(*args, **kwargs)