from rest_framework import serializers

from .models import KnapsackProblemRequest, KnapsackProblem

class KnapsackProblemRequestSerializer(serializers.ModelSerializer):
    items = serializers.ListField(child=serializers.DictField())

    def validate(self, data, *args, **kwargs):
        actual_count = len(data['items'])
        if data['num_items'] != actual_count:
            raise serializers.ValidationError('Declared number of items (%d) different from supplied number of items (%d).' % (data['num_items'], actual_count))

        invalid_items = False
        for item in data['items']:
            requireds = ['index', 'value', 'weight']
            for required in requireds:
                if not required in item or not isinstance(item[required], (int, long)):
                    valid_format = '{"num_items":2,"capacity":10,"items":[{"index":0,"value":8,"weight":4},{"index":1,"value":10,"weight":5}]}'
                    raise serializers.ValidationError('Invalid items supplied. Correct format:' + valid_format)
                    invalid_items = True
                    break

            if invalid_items:
                break

        return super(KnapsackProblemRequestSerializer, self).validate(data, *args, **kwargs)

    class Meta:
        model = KnapsackProblemRequest
        fields = ('url', 'num_items', 'capacity', 'items')


class KnapsackProblemPresentSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnapsackProblem
        fields = ('in_knapsack_json', 'total_value', 'total_weight', 'state', 'seconds_took',)


class KnapsackProblemRequestPresentSerializer(serializers.ModelSerializer):
    knapsack_problem = KnapsackProblemPresentSerializer(read_only=True)

    class Meta:
        model = KnapsackProblemRequest
        fields = ('time_elapsed', 'num_items', 'capacity', 'items', 'knapsack_problem')
