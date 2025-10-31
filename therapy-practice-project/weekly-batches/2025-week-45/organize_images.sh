#!/bin/bash

# Quick script to organize Canva exports into images folder
# Usage: bash organize_images.sh

echo "🖼️  Organizing Week 45 images..."
echo ""

WEEK_FOLDER="/Users/Coding Projects/Claude_Agents_Meta/therapy-practice-project/weekly-batches/2025-week-45"
IMAGES_FOLDER="$WEEK_FOLDER/images"
DOWNLOADS="$HOME/Downloads"

# Find recent Canva downloads (last hour)
echo "Looking for recent Canva downloads..."
echo ""

# Look for common Canva export patterns
CANVA_FILES=$(find "$DOWNLOADS" -name "*.jpg" -o -name "*.png" -mmin -60 2>/dev/null | grep -i -E "(canva|design|untitled)" | head -10)

if [ -z "$CANVA_FILES" ]; then
    echo "❌ No recent Canva files found in Downloads"
    echo ""
    echo "💡 Options:"
    echo "   1. Export from Canva again"
    echo "   2. Manually drag files to:"
    echo "      $IMAGES_FOLDER"
    echo ""
    exit 1
fi

echo "Found these files:"
echo "$CANVA_FILES" | nl
echo ""

# Ask user to confirm
read -p "Move these files to images folder? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 0
fi

# Move files
COUNT=0
while IFS= read -r file; do
    if [ -f "$file" ]; then
        BASENAME=$(basename "$file")

        # Try to auto-rename based on dimensions
        DIMS=$(sips -g pixelWidth -g pixelHeight "$file" 2>/dev/null | grep -E "pixelWidth|pixelHeight" | awk '{print $2}' | tr '\n' 'x')

        # Suggest name based on dimensions
        if [[ "$DIMS" == "1200x630"* ]]; then
            NEWNAME="w45-blog-caregiving.jpg"
        elif [[ "$DIMS" == "1080x1080"* ]]; then
            NEWNAME="w45-instagram-feed-caregiving.jpg"
        elif [[ "$DIMS" == "1080x1920"* ]]; then
            NEWNAME="w45-instagram-story-caregiving.jpg"
        elif [[ "$DIMS" == "1200x1200"* ]]; then
            NEWNAME="w45-facebook-caregiving.jpg"
        else
            NEWNAME="w45-$(echo $BASENAME | sed 's/[^a-zA-Z0-9.-]/_/g')"
        fi

        mv "$file" "$IMAGES_FOLDER/$NEWNAME"
        echo "✓ Moved to: $NEWNAME"
        ((COUNT++))
    fi
done <<< "$CANVA_FILES"

echo ""
echo "✅ Moved $COUNT files to images folder"
echo ""
echo "📁 View images:"
echo "   cd \"$IMAGES_FOLDER\""
echo "   open ."
echo ""

# Open folder automatically
open "$IMAGES_FOLDER"
