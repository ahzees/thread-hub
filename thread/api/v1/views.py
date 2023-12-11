from django.shortcuts import render
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework import serializers
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, inline_serializer

from authentication.permisions import IsMember
from thread.models import Thread, Messages
from thread.api.v1.serializers import CreateThreadSerializer, ViewThreadSerializer, AddMembersSerializer, MessageSerializer
from authentication.models import CustomUser



class ThreadApiView(CreateAPIView):
    queryset = Thread.objects.all()
    serializer_class = CreateThreadSerializer
    permission_classes = [IsAuthenticated]


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                thread = Thread.objects.get(pk=serializer.data['pk'])
                thread.members.add(request.user.pk)
                return Response(
                    {"status": "created", "name": serializer.data["name"]},
                    status=status.HTTP_201_CREATED,
                )
            except IntegrityError as e:
                return Response(
                    {"status": "error - name is invalid"},
                    status=status.HTTP_409_CONFLICT,
                )
    
class ViewThreadApiView(RetrieveAPIView):
    queryset = Thread.objects.all()
    serializer_class = ViewThreadSerializer
    permission_classes = [IsAuthenticated, IsMember]

class DeleteThreadApiView(DestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = ViewThreadSerializer
    permission_classes = [IsAuthenticated, IsMember]

class ViewAllThreadApiView(ListAPIView):
    queryset = Thread.objects.all()
    serializer_class = ViewThreadSerializer
    permission_classes = [IsAuthenticated,]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(members__pk = request.user.pk)
        serializer = self.get_serializer(data=queryset, many=True)
        serializer.is_valid()
        return Response({"threads":serializer.data})
    
class AddMembersApiView(UpdateAPIView):
    queryset = Thread.objects.all()
    serializer_class = AddMembersSerializer
    permission_classes = [IsAuthenticated, IsMember]


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        list_of_members = [CustomUser.objects.get(email=i).pk for i in request.data['members']]
        instance.members.add(*list_of_members)
        instance.save()
        return Response({*instance.members.all().values_list('email', flat=True)})
    

class ViewMessagesThreadApiView(RetrieveAPIView):
    queryset = Thread.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        queryset = self.get_queryset().get(pk=pk).messages
        if queryset:
            serializer = self.serializer_class(data=queryset.all(), many=True)
            serializer.is_valid()
            return Response({"messages": serializer.data})
        return Response({"messages":"Empty"})



class AddMessageThreadApiView(UpdateAPIView):
    queryset = Thread.objects.all()
    serializer_class = MessageSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        message = Messages.objects.create(user=request.user, content=request.data['content'], thread=instance)
        return Response({"message": message.content})