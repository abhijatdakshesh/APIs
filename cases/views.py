from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Case, Visit
from .serializers import CaseSerializer, VisitSerializer

# Create your views here.

class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        case = self.get_object()
        case.visit_status = request.data.get('status', case.visit_status)
        case.save()
        return Response(CaseSerializer(case).data)

class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        visit = self.get_object()
        visit.status = request.data.get('status', visit.status)
        visit.save()
        return Response(VisitSerializer(visit).data)

    @action(detail=True, methods=['post'])
    def save_details(self, request, pk=None):
        visit = self.get_object()
        serializer = VisitSerializer(visit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
