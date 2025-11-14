#!/usr/bin/env python3
"""Add multiple products to database from list of IDs"""

import subprocess
import sys

# List of product IDs to add (first 36)
product_ids = [
    597, 3627622, 3620257, 2065545, 154, 845, 220, 1647453, 186, 3473479,
    408, 3175903, 161, 3637759, 998508, 370, 3348115, 3422911, 3453686,
    3575657, 88, 3642724, 909, 3456660, 274053, 969531, 3860361, 1081,
    1268519, 3747033, 1476307, 3417250, 159042, 864032, 3501775, 279
]

success_count = 0
failed = []

for i, product_id in enumerate(product_ids, 1):
    url = f"https://shop.dransay.com/product/placeholder/{product_id}"
    print(f"\n[{i}/{len(product_ids)}] Füge Produkt {product_id} hinzu...")

    try:
        result = subprocess.run(
            ['python3', 'add_product.py', url],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            success_count += 1
            print(f"✅ Produkt {product_id} erfolgreich hinzugefügt")
        else:
            failed.append((product_id, "Fehler beim Hinzufügen"))
            print(f"❌ Produkt {product_id} fehlgeschlagen")

    except subprocess.TimeoutExpired:
        failed.append((product_id, "Timeout"))
        print(f"❌ Produkt {product_id} - Timeout")
    except Exception as e:
        failed.append((product_id, str(e)))
        print(f"❌ Produkt {product_id} - Fehler: {e}")

print(f"\n\n{'='*60}")
print(f"ZUSAMMENFASSUNG")
print(f"{'='*60}")
print(f"Gesamt verarbeitet: {len(product_ids)}")
print(f"Erfolgreich: {success_count}")
print(f"Fehlgeschlagen: {len(failed)}")

if failed:
    print(f"\nFehlgeschlagene Produkte:")
    for prod_id, error in failed:
        print(f"  - {prod_id}: {error}")
