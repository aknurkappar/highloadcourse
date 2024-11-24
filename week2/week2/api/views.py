from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Employee, Project
from .serializers import EmployeeSerializer, ProjectSerializer

# Create your views here.

class EmployeeViewSet(viewsets.ViewSet):
    def list(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    def create(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
