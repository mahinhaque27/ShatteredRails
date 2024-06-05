from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    # create a table in db to store game information
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    game_name = models.CharField(max_length=255)
    health = models.IntegerField(default=50)
    verification = models.CharField(max_length=12, default='unverified')
    completion = models.IntegerField(default=0)
    save_state = models.IntegerField(default=0)
    visited_states = models.TextField(default="")  

    def __str__(self):
        return str(self.user)

    # Add a state to visited_states if it doesn't already exist
    # Completition field will be the sum of the visisted states
    def add_state(self, state):
        if str(state) not in self.visited_states.split(','):
            self.visited_states += ',' + str(state) if self.visited_states else str(state)
            self.completion += 1  
            self.save()
