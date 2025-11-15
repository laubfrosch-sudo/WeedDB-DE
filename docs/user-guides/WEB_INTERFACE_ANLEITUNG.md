# 🌐 Web-Interface Anleitung (v0.1.2)

**GitHub Repository:** [https://github.com/laubfrosch-sudo/WeedDB-DE](https://github.com/laubfrosch-sudo/WeedDB-DE)

Diese Anleitung erklärt, wie du das moderne Web-Interface von WeedDB verwendest, um Cannabis-Produkt-Daten zu erkunden, zu analysieren und zu verwalten.

## 🚀 Schnellstart

### 1. Web-Interface starten

```bash
# Stelle sicher, dass alle Dependencies installiert sind
pip install -r requirements.txt

# Wechsle in das web-Verzeichnis
cd web

# Starte den Entwicklungsserver
python3 -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 2. Zugriff

**Dashboard:** http://localhost:8000
**API-Dokumentation:** http://localhost:8000/docs

## 📊 Dashboard verwenden

### Live-Metriken

Das Dashboard zeigt dir aktuelle Statistiken deiner WeedDB:

- **📦 Produkte:** Anzahl der Cannabis-Sorten in der Datenbank
- **🏭 Produzenten:** Anzahl der verschiedenen Hersteller
- **🏥 Apotheken:** Anzahl der Versandapotheken
- **💰 Preise:** Anzahl der gespeicherten Preisdatensätze

### Schnellaktionen

- **🔄 Preise aktualisieren:** Startet eine Batch-Aktualisierung aller Produktpreise
- **📄 Übersicht generieren:** Erstellt eine neue SORTEN_ÜBERSICHT.md
- **📋 Logs anzeigen:** Zeigt System-Logs an

### Auto-Refresh

Das Dashboard aktualisiert sich automatisch alle 30 Sekunden mit den neuesten Daten.

## 🔍 Produkte erkunden

### Produkte durchsuchen

```bash
# Alle Produkte anzeigen (erste 50)
curl "http://localhost:8000/api/products"

# Nach bestimmten Sorten suchen
curl "http://localhost:8000/api/products?search=sour"

# Begrenze Anzahl der Ergebnisse
curl "http://localhost:8000/api/products?limit=10"

# Kombiniert: Suche + Limit
curl "http://localhost:8000/api/products?search=diesel&limit=5"
```

### Produkt-Details

Jedes Produkt enthält:
- **ID:** Eindeutige Kennung
- **Name:** Produktname (z.B. "Sourdough")
- **THC/CBD:** Cannabinoid-Gehalt in Prozent
- **Genetik:** Indica, Sativa, Hybrid, etc.
- **Produzent:** Hersteller-Name
- **Bewertung:** User-Rating (1-5 Sterne)
- **Reviews:** Anzahl der Bewertungen

## 📈 Preis-Analysen

### Aktuelle Preis-Statistiken

```bash
curl http://localhost:8000/api/analytics/prices
```

**Enthält:**
- Gesamtanzahl der Preisdatensätze
- Durchschnittspreise (Top-Apotheken vs. Alle)
- Preisspanne (Minimum/Maximum)
- Top 5 teuerste Produkte
- Top 5 günstigste Produkte

### Preis-Trends

Die API liefert historische Preisdaten für Trend-Analysen und Marktbeobachtung.

## 🔧 Batch-Operationen

### Preise aktualisieren

```bash
# Über Web-Interface (empfohlen)
# Button "Preise aktualisieren" im Dashboard klicken

# Oder über API
curl -X POST http://localhost:8000/api/batch/update
```

**Was passiert:**
- Alle Produktpreise werden von shop.dransay.com aktualisiert
- Neue Preisdatensätze werden in der Historie gespeichert
- Dashboard zeigt Live-Status der Aktualisierung

### Übersicht generieren

```bash
# Über Web-Interface
# Button "Übersicht generieren" im Dashboard klicken

# Oder manuell
python3 scripts/generate_overview.py
```

**Erstellt:** `docs/SORTEN_ÜBERSICHT.md` mit aktuellen Daten

## 📚 API-Dokumentation

### Swagger UI

Besuche http://localhost:8000/docs für die interaktive API-Dokumentation:

- **Alle Endpunkte** aufgelistet
- **Parameter** und **Response-Schemas** erklärt
- **Test-Interface** direkt im Browser
- **Beispiel-Requests** und Responses

### ReDoc

Alternative Dokumentation: http://localhost:8000/redoc

## 🔧 Erweiterte Features

### System-Monitoring

```bash
# Health-Check
curl http://localhost:8000/health

# Detaillierte System-Informationen
curl http://localhost:8000/api/stats
```

### Datenbank-Status

- **Verbindungsstatus:** Datenbank erreichbar?
- **Letzte Aktualisierung:** Wann wurden Daten zuletzt aktualisiert?
- **Speicherplatz:** Datenbank-Größe
- **Performance-Metriken:** Response-Zeiten

## 🐛 Fehlerbehebung

### Server startet nicht

```bash
# Dependencies prüfen
python3 -c "import fastapi, uvicorn; print('OK')"

# Port-Konflikte prüfen
lsof -i :8000

# Mit Debug-Ausgabe starten
python3 -m uvicorn web.app:app --log-level debug
```

### API funktioniert nicht

```bash
# Health-Check testen
curl http://localhost:8000/health

# Datenbank-Verbindung prüfen
python3 -c "import sqlite3; conn = sqlite3.connect('data/WeedDB.db'); print('DB OK'); conn.close()"
```

### Langsame Performance

- **Datenbank optimieren:** `VACUUM` und `ANALYZE` laufen lassen
- **Cache leeren:** Temporäre Dateien entfernen
- **Server neu starten:** Mit mehr Workern für Production

## 🚀 Production-Deployment

### Mehrere Worker (empfohlen)

```bash
# 4 Worker für bessere Performance
python3 -m uvicorn web.app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Hintergrund-Service

```bash
# Mit systemd (Linux)
# Oder mit launchd (macOS)
# Oder mit screen/tmux
```

### Reverse Proxy (SSL)

```bash
# nginx oder Caddy für SSL-Terminierung
# Beispiel nginx config:
server {
    listen 443 ssl;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 Daten verstehen

### Produkt-Kategorien

- **Indica:** Entspannend, beruhigend
- **Sativa:** Energetisch, fokussierend
- **Hybrid:** Mischung aus beiden
- **THC/CBD:** Wirkstoff-Gehalt in Prozent

### Preis-Unterschiede

- **Top-Apotheken:** Kuriert ausgewählte, vertrauenswürdige Apotheken
- **Alle Apotheken:** Vollständiger Marktüberblick
- **Historische Daten:** Preis-Entwicklung über Zeit

## 🎯 Best Practices

### Regelmäßige Wartung

1. **Tägliche Preis-Updates** für aktuelle Daten
2. **Wöchentliche Übersicht** generieren
3. **Monatliche Backups** und Optimierungen

### Performance-Optimierung

1. **Cache nutzen** für wiederholte Abfragen
2. **Batch-Updates** statt einzelne Requests
3. **API-Limits** respektieren (nicht überlasten)

### Datensicherheit

1. **Regelmäßige Backups** der Datenbank
2. **Logs rotieren** (nicht unendlich wachsen lassen)
3. **API-Zugang** nur über vertrauenswürdige Netzwerke

## 📞 Support

### Häufige Probleme

**Q: Dashboard lädt nicht?**
A: Stelle sicher, dass der Server läuft (`ps aux | grep uvicorn`)

**Q: API gibt Fehler zurück?**
A: Prüfe Datenbank-Verbindung und Logs

**Q: Preise sind veraltet?**
A: Führe Batch-Update durch oder starte Cron-Job

### Logs finden

```bash
# Server-Logs
tail -f /dev/null  # Während Server läuft

# Anwendungs-Logs
tail -f data/logs/web_app.log

# System-Logs
tail -f data/logs/*.log
```

---

## 🎉 Zusammenfassung

Das WeedDB Web-Interface bietet dir:

- **📊 Live-Dashboard** mit aktuellen Metriken
- **🔍 Produkt-Suche** und Filterung
- **📈 Preis-Analysen** und Trends
- **🚀 Batch-Operationen** für Massen-Updates
- **📚 Vollständige API** mit Dokumentation
- **🔧 System-Monitoring** und Health-Checks

**Starte jetzt:** http://localhost:8000

**API-Dokumentation:** http://localhost:8000/docs

**Viel Spaß beim Erkunden deiner Cannabis-Daten! 🌿📊**