from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Property(models.Model):
    """Modèle représentant un bien personnel."""

    PROPERTY_STATUS = (
        ("available", "Disponible"),
        ("transfer_pending", "Transfert en cours"),
        ("archived", "Archivé"),
    )

    name = models.CharField(_("Nom du bien"), max_length=255)
    description = models.TextField(_("Description"))
    # serial_number = models.CharField(_("Numéro de série"), max_length=100, blank=True)
    value = models.DecimalField(
        _("Valeur estimée"),
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    purchase_date = models.DateField(_("Date d'acquisition"), null=True, blank=True)
    current_owner = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="owned_properties"
    )
    status = models.CharField(
        max_length=20, choices=PROPERTY_STATUS, default="available"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Bien")
        verbose_name_plural = _("Biens")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.current_owner}"


class PropertyImage(models.Model):
    """Modèle pour gérer les images associées à un bien."""

    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to="property_images/%Y/%m/%d/", verbose_name=_("Image")
    )
    # is_primary = models.BooleanField(_("Image principale"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Image du bien")
        verbose_name_plural = _("Images des biens")

    def __str__(self):
        return f"{self.property} {self.image.name}"


class PropertyTransfer(models.Model):
    """Modèle pour gérer l'historique des transferts de propriété."""

    TRANSFER_STATUS = (
        ("pending", "En attente"),
        ("completed", "Complété"),
        ("cancelled", "Annulé"),
    )

    property = models.ForeignKey(
        Property, on_delete=models.PROTECT, related_name="transfers"
    )
    from_user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="transfers_sent"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="transfers_received"
    )
    transfer_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=TRANSFER_STATUS, default="pending")
    transfer_notes = models.TextField(blank=True)
    transfer_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Transfert de propriété")
        verbose_name_plural = _("Transferts de propriétés")
        ordering = ["-transfer_date"]

    def __str__(self):
        return f"Transfert de {self.property.name} de {self.from_user} à {self.to_user}"
