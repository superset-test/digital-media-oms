# Instructions to Complete Implementation

This document provides copy-paste templates for all remaining files.

## Remaining Repositories

Create these files in `backend/src/app/repositories/`:

### advertiser_repository.py
Copy from `agency_repository.py` and replace:
- "Agency" → "Advertiser"
- "agencies" → "advertisers"
- Add "industry" field handling

### contact_repository.py
Key methods needed:
- `create()` - validate agency_id XOR advertiser_id
- `get_by_id()`
- `list_by_agency()`
- `list_by_advertiser()`
- `list_by_tenant()`
- `get_primary_contact()` - WHERE is_primary = true
- `update()`
- `delete()`

### placement_repository.py, ad_unit_repository.py
Follow the tenant/agency pattern with appropriate fields.

### rate_card_repository.py
Additional method:
- `get_active_rate()` - WHERE effective_date <= $2 AND (expiration_date IS NULL OR >= $2)

### order_repository.py
Additional methods:
- `get_by_order_number()`
- `generate_order_number()` - Get max for year, format as 'ORD-{year}-{seq:05d}'
- `update_total_amount()` - SUM line_items.subtotal

### line_item_repository.py
Additional methods:
- `get_next_line_number()` - MAX(line_number) + 1 for order
- In `create()` and `update()`, calculate subtotal: quantity * unit_price * (1 - discount/100)

