#!/bin/zsh
# Build a self-contained Desktop .app. Run from this project directory.
set -euo pipefail

project_root="$(cd "$(dirname "$0")/../.." && pwd)"
app="$HOME/Desktop/Papier Parade.app"
contents="$app/Contents"
resources="$contents/Resources"
mkdir -p "$resources" "$contents/MacOS"

cp "$project_root/tools/macos_launcher/launch_game.sh" "$contents/MacOS/Papier Parade"
chmod +x "$contents/MacOS/Papier Parade"
cp "$project_root/assets/characters/tech_billionaire/portrait.png" "$resources/TechBillionaireCover.png"

cat > "$contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>CFBundleName</key><string>Papier Parade</string>
  <key>CFBundleDisplayName</key><string>Papier Parade</string>
  <key>CFBundleExecutable</key><string>Papier Parade</string>
  <key>CFBundleIdentifier</key><string>com.grummpy.papierparade.launcher</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleVersion</key><string>1.0</string>
  <key>LSUIElement</key><false/>
</dict></plist>
PLIST

echo "Created $app"
