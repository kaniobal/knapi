from django.contrib import admin

from .models import KnapsackProblem, KnapsackProblemRequest

import datetime

############################
# Register your models here.
############################
class KnapsackProblemRequestInline(admin.TabularInline):
    model = KnapsackProblemRequest
    actions = None
    fields = ('created',)
    readonly_fields = ('created',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class KnapsackProblemAdmin(admin.ModelAdmin):
    actions = None
    fields = ('task_json', 'in_knapsack_json', 'total_value', 'total_weight', 'created', 'finished', 'state', 'seconds_took',)
    readonly_fields = fields
    inlines = [KnapsackProblemRequestInline]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(KnapsackProblem, KnapsackProblemAdmin)
#admin.site.register(KnapsackProblemRequest)
