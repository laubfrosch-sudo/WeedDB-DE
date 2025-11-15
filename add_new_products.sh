#!/bin/bash
# Add 20 new products to WeedDB
# Generated: 2025-11-15

echo "🚀 Starting batch addition of 20 new products..."
echo "================================================="

products=(
    "Crumbled Lime"
    "Citron Cookies"
    "La Kush Cake"
    "Sunset Strudel"
    "Sunset Serenity"
    "Mango Kush"
    "Sky Berry Kush"
    "Waffle Bites"
    "Ocean Grown Cookies"
    "Do Si Dos"
    "Cinderella Kush"
    "Diamond Mints"
    "Master Kush"
    "Facetz"
    "Kush Mintz"
    "Lemonade Haze"
    "Ghost Train Haze"
    "Amnesia Haze Cake"
    "Liberty Haze"
    "Delahaze"
)

total=${#products[@]}
success=0
failed=0

for i in "${!products[@]}"; do
    num=$((i+1))
    product="${products[$i]}"

    echo ""
    echo "============================================================"
    echo "[$num/$total] Adding: $product"
    echo "============================================================"

    if python3 scripts/add_product.py "$product"; then
        ((success++))
        echo "✅ Successfully added '$product'"
    else
        ((failed++))
        echo "❌ Failed to add '$product'"
    fi

    # Small pause between products
    if [ $num -lt $total ]; then
        echo "⏳ Pause (2 seconds)..."
        sleep 2
    fi
done

echo ""
echo "============================================================"
echo "📊 BATCH ADDITION SUMMARY"
echo "============================================================"
echo "✅ Successful: $success/$total"
echo "❌ Failed: $failed/$total"
echo "✨ Batch addition complete!"
