from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

import zlib

##########################
# Create your models here.
##########################


class KnapsackProblem(models.Model):
    """Specific knapsack problem model"""
    created = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(null=True)
    task_json = models.TextField()
    task_hash = models.CharField(max_length=8)
    in_knapsack_json = models.TextField()
    total_value = models.IntegerField(default=0)
    total_weight = models.IntegerField(default=0)

    @property
    def seconds_took(self):
        if self.finished:
            return (self.finished - self.created).total_seconds()
        else:
            return 'Still running'

    @property
    def state(self):
        return 'FINISHED' if self.finished else 'RUNNING'

    class Meta:
        ordering = ('created',)


class KnapsackProblemRequest(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    #created.editable = True
    knapsack_problem = models.ForeignKey(KnapsackProblem)
    num_items = models.IntegerField()
    capacity = models.IntegerField()
    items = models.TextField()

    @property
    def time_elapsed(self):
        if self.knapsack_problem.finished:
            # solution was fetched instantly
            if self.knapsack_problem.finished < self.created:
                return 0
            else:
                return max(self.knapsack_problem.seconds_took, (self.knapsack_problem.finished - self.created).total_seconds())
        else:
            return (timezone.now() - self.created).total_seconds()

    class Meta:
        ordering = ('created',)
