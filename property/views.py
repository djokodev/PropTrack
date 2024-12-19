from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Property, PropertyImage, PropertyTransfer
from django.core.exceptions import PermissionDenied, ValidationError
from rest_framework.parsers import MultiPartParser
from django.db.models import Q
from .serializers import (
    PropertySerializer,
    PropertyImageSerializer,
    PropertyTransferSerializer,
)


class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retourne les biens de l'utilisateur connecté."""
        return Property.objects.filter(current_owner=self.request.user)

    def perform_create(self, serializer):
        """Associe automatiquement le bien à l'utilisateur connecté."""
        serializer.save(current_owner=self.request.user)

    @action(detail=True, methods=["post"], parser_classes=[MultiPartParser])
    def upload_image(self, request, pk=None):
        """Endpoint pour ajouter une image à un bien."""
        property = self.get_object()

        serializer = PropertyImageSerializer(
            data={
                "property": property.id,
                "image": request.data.get("image"),
            }
        )

        if serializer.is_valid():
            serializer.save(property=property)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyTransferViewSet(viewsets.ModelViewSet):
    serializer_class = PropertyTransferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retourne les transferts où l'utilisateur est impliqué."""
        user = self.request.user
        return PropertyTransfer.objects.filter(Q(from_user=user) | Q(to_user=user))

    def perform_create(self, serializer):
        """Crée un nouveau transfert."""
        property = serializer.validated_data["property"]

        # Vérification que l'utilisateur est bien le propriétaire
        if property.current_owner != self.request.user:
            raise PermissionDenied("Vous n'êtes pas le propriétaire de ce bien")

        # Vérification que le bien est disponible
        if property.status != "available":
            raise ValidationError("Ce bien n'est pas disponible pour le transfert")

        # Mise à jour du statut du bien
        property.status = "transfer_pending"
        property.save()

        serializer.save(from_user=self.request.user, status="pending")

    @action(detail=True, methods=["post"])
    def accept_transfer(self, request, pk=None):
        """Accepter un transfert de propriété."""
        transfer = self.get_object()

        # Vérifications
        if transfer.to_user != request.user:
            raise PermissionDenied("Vous n'êtes pas le destinataire de ce transfert")
        if transfer.status != "pending":
            raise ValidationError("Ce transfert ne peut plus être accepté")

        # Mise à jour du transfert
        transfer.status = "completed"
        transfer.save()

        # Mise à jour du bien
        property = transfer.property
        property.current_owner = transfer.to_user
        property.status = "available"
        property.save()

        return Response({"status": "transfer_accepted"})

    @action(detail=True, methods=["post"])
    def cancel_transfer(self, request, pk=None):
        """Annuler un transfert de propriété."""
        transfer = self.get_object()

        # Vérifications
        if transfer.from_user != request.user:
            raise PermissionDenied("Vous n'êtes pas l'initiateur de ce transfert")
        if transfer.status != "pending":
            raise ValidationError("Ce transfert ne peut plus être annulé")

        # Mise à jour du transfert
        transfer.status = "cancelled"
        transfer.save()

        # Mise à jour du bien
        property = transfer.property
        property.status = "available"
        property.save()

        return Response({"status": "transfer_cancelled"})
