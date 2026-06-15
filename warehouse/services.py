from decimal import Decimal

from django.db.models import Sum

from .models import inventrories


ZERO = Decimal("0")


def to_decimal(value):
    return Decimal(str(value or 0))


def clamp_zero(value):
    value = to_decimal(value)
    return value if value > ZERO else ZERO


def get_product_stock(product_instance, warehouse_instance=None):
    inventory = inventrories.objects.filter(product_foerignkey=product_instance)
    if warehouse_instance is not None:
        inventory = inventory.filter(warehouse_foerignkey=warehouse_instance)

    in_totals = inventory.filter(in_and_out="IN").aggregate(
        total_quantity=Sum("Quantity"),
        total_weight=Sum("weight_field"),
    )
    out_totals = inventory.filter(in_and_out="OUT").aggregate(
        total_quantity=Sum("Quantity"),
        total_weight=Sum("weight_field"),
    )

    total_quantity_in = to_decimal(in_totals["total_quantity"])
    total_weight_in = to_decimal(in_totals["total_weight"])
    total_quantity_out = to_decimal(out_totals["total_quantity"])
    total_weight_out = to_decimal(out_totals["total_weight"])
    raw_available_quantity = total_quantity_in - total_quantity_out
    raw_available_weight = total_weight_in - total_weight_out

    return {
        "total_quantity_in": total_quantity_in,
        "total_weight_in": total_weight_in,
        "total_quantity_out": total_quantity_out,
        "total_weight_out": total_weight_out,
        "raw_available_quantity": raw_available_quantity,
        "raw_available_weight": raw_available_weight,
        "available_quantity": clamp_zero(raw_available_quantity),
        "available_weight": clamp_zero(raw_available_weight),
    }


def has_enough_stock(product_instance, warehouse_instance, quantity, weight):
    stock = get_product_stock(product_instance, warehouse_instance)
    return (
        to_decimal(quantity) <= stock["available_quantity"]
        and to_decimal(weight) <= stock["available_weight"]
    )
