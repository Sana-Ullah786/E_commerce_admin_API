from src.endpoints.inventory.GET.get_inventory_status import (
    get_all_inventory,
    get_status_by_category,
    get_status_by_merchant,
    get_status_by_product_id,
)
from src.endpoints.inventory.GET.get_inventory_track import get_track_by_product_id
from src.endpoints.inventory.POST.create_new_inventory import create_inventory
from src.endpoints.inventory.PUT.update_inventory_by_product_id import (
    update_inventory_by_product_id,
)
from src.endpoints.inventory.router_init import router
