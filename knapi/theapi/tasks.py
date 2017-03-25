from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.signals import task_success

from rest_framework.renderers import JSONRenderer

from django.utils import timezone

import time

from .models import KnapsackProblemRequest, KnapsackProblem

from knapsacksolver import KnapsackSolver

@shared_task
def solve_knapsack_problem(knapsack_problem_id):
    knapsack_problem = KnapsackProblem.objects.get(pk=knapsack_problem_id)
    solver = KnapsackSolver.KnapsackSolver()
    solver.load_data_from_json_string(knapsack_problem.task_json)
    solver.solve()
    knapsack_problem.in_knapsack_json = JSONRenderer().render(solver.knapsack)
    knapsack_problem.total_value = solver.v_tot
    knapsack_problem.total_weight = solver.w_tot
    knapsack_problem.finished = timezone.now()
    knapsack_problem.save()

@task_success.connect
def notify_done(sender, result, **kwargs):
    if sender == solve_knapsack_problem:
        pass
