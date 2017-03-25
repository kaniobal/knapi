from django.shortcuts import render
from django.http import Http404

from .models import KnapsackProblemRequest, KnapsackProblem
from .serializers import KnapsackProblemRequestSerializer, KnapsackProblemRequestPresentSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.reverse import reverse
from rest_framework import status

import tasks

import zlib

#########################
# Create your views here.
#########################
class KnapsackProblemRequestList(APIView):
    def post(self, request, format=None):
        serializer = KnapsackProblemRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            task_hash = '%x' % (zlib.crc32(str(serializer.validated_data)) % (1 << 32))
            try:
                # Problem already encountered -- just fetch it
                problem = KnapsackProblem.objects.get(task_hash=task_hash)
            except (KnapsackProblem.DoesNotExist):
                # New problem
                problem = KnapsackProblem.objects.create(
                    task_json=JSONRenderer().render(serializer.validated_data),
                    task_hash=task_hash,
                )
                # Start solving
                tasks.solve_knapsack_problem.delay(problem.id)

            # Save the request
            serializer.save(knapsack_problem=problem)


            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KnapsackProblemRequestDetail(APIView):
    def get_object(self, pk):
        try:
            return KnapsackProblemRequest.objects.get(pk=pk)
        except KnapsackProblemRequest.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        problem_request = self.get_object(pk)
        serializer = KnapsackProblemRequestPresentSerializer(problem_request)

        return Response(serializer.data)
