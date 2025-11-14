-- WeedDB SQLite Schema (3. Normalform)
-- Cannabis product database with historical pricing and pharmacy tracking

-- Hersteller/Producer Tabelle
CREATE TABLE IF NOT EXISTS producers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    origin TEXT
);

-- Hauptprodukt-Tabelle
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,  -- product_id von shop.dransay.com
    name TEXT NOT NULL,
    variant TEXT,
    genetics TEXT CHECK(genetics IN ('Indica', 'Sativa', 'Hybrid-Sativa', 'Hybrid-Indica', 'Hybrid')),
    thc_percent REAL,
    cbd_percent REAL,
    producer_id INTEGER,
    stock_level INTEGER,
    rating REAL,  -- z.B. 4.1
    review_count INTEGER,  -- z.B. 312
    irradiation TEXT CHECK(irradiation IN ('Yes', 'No')),
    url TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producer_id) REFERENCES producers(id)
);

-- Terpene Master-Tabelle
CREATE TABLE IF NOT EXISTS terpenes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Product-Terpene Junction (Many-to-Many)
CREATE TABLE IF NOT EXISTS product_terpenes (
    product_id INTEGER NOT NULL,
    terpene_id INTEGER NOT NULL,
    percentage REAL,
    PRIMARY KEY (product_id, terpene_id),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (terpene_id) REFERENCES terpenes(id)
);

-- Effekte Master-Tabelle
CREATE TABLE IF NOT EXISTS effects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Product-Effects Junction (Many-to-Many)
CREATE TABLE IF NOT EXISTS product_effects (
    product_id INTEGER NOT NULL,
    effect_id INTEGER NOT NULL,
    strength INTEGER CHECK(strength BETWEEN 0 AND 4),  -- optional: 0-4 Stärke
    PRIMARY KEY (product_id, effect_id),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (effect_id) REFERENCES effects(id)
);

-- Therapeutische Anwendungen Master-Tabelle
CREATE TABLE IF NOT EXISTS therapeutic_uses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Product-Therapeutic Uses Junction (Many-to-Many)
CREATE TABLE IF NOT EXISTS product_therapeutic_uses (
    product_id INTEGER NOT NULL,
    therapeutic_use_id INTEGER NOT NULL,
    strength INTEGER CHECK(strength BETWEEN 0 AND 4),  -- optional: 0-4 Stärke
    PRIMARY KEY (product_id, therapeutic_use_id),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (therapeutic_use_id) REFERENCES therapeutic_uses(id)
);

-- Apotheken/Pharmacies Tabelle
CREATE TABLE IF NOT EXISTS pharmacies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    location TEXT
);

-- Historische Preisdaten
CREATE TABLE IF NOT EXISTS prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    pharmacy_id INTEGER NOT NULL,
    price_per_g REAL NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(id)
);

-- Indices für Performance bei häufigen Queries
CREATE INDEX IF NOT EXISTS idx_products_genetics ON products(genetics);
CREATE INDEX IF NOT EXISTS idx_products_thc ON products(thc_percent);
CREATE INDEX IF NOT EXISTS idx_products_rating ON products(rating);
CREATE INDEX IF NOT EXISTS idx_prices_timestamp ON prices(timestamp);
CREATE INDEX IF NOT EXISTS idx_prices_product ON prices(product_id);
CREATE INDEX IF NOT EXISTS idx_prices_pharmacy ON prices(pharmacy_id);

-- View: Aktuellste Preise pro Produkt und Apotheke
CREATE VIEW IF NOT EXISTS current_prices AS
SELECT
    p1.product_id,
    p1.pharmacy_id,
    p1.price_per_g,
    p1.timestamp
FROM prices p1
INNER JOIN (
    SELECT product_id, pharmacy_id, MAX(timestamp) as max_timestamp
    FROM prices
    GROUP BY product_id, pharmacy_id
) p2 ON p1.product_id = p2.product_id
    AND p1.pharmacy_id = p2.pharmacy_id
    AND p1.timestamp = p2.max_timestamp;

-- View: Günstigste aktuelle Preise pro Produkt
CREATE VIEW IF NOT EXISTS cheapest_current_prices AS
SELECT
    cp.product_id,
    MIN(cp.price_per_g) as cheapest_price,
    ph.name as cheapest_pharmacy,
    ph.location as pharmacy_location
FROM current_prices cp
JOIN pharmacies ph ON cp.pharmacy_id = ph.id
GROUP BY cp.product_id
HAVING cp.price_per_g = MIN(cp.price_per_g);

-- ============================================================================
-- MULTI-PHARMACY ANALYSIS VIEWS
-- ============================================================================

-- View: Alle Preise pro Produkt mit Apotheken-Details (sortiert nach Preis)
-- Zeigt alle verfügbaren Apotheken und Preise für jedes Produkt (letzte 7 Tage)
CREATE VIEW IF NOT EXISTS product_pharmacy_prices AS
SELECT
    p.id as product_id,
    p.name as product_name,
    p.genetics,
    p.thc_percent,
    ph.id as pharmacy_id,
    ph.name as pharmacy_name,
    pr.price_per_g,
    pr.timestamp,
    RANK() OVER (PARTITION BY p.id ORDER BY pr.price_per_g ASC) as price_rank
FROM products p
JOIN prices pr ON p.id = pr.product_id
JOIN pharmacies ph ON pr.pharmacy_id = ph.id
WHERE pr.timestamp >= datetime('now', '-7 days');

-- View: Preisspanne pro Produkt (min, max, avg, Anzahl Apotheken)
-- Zeigt Preisstatistiken für umfassenden Preisvergleich
CREATE VIEW IF NOT EXISTS product_price_stats AS
SELECT
    p.id as product_id,
    p.name as product_name,
    p.genetics,
    p.thc_percent,
    COUNT(DISTINCT ph.id) as pharmacy_count,
    MIN(pr.price_per_g) as min_price,
    MAX(pr.price_per_g) as max_price,
    ROUND(AVG(pr.price_per_g), 2) as avg_price,
    ROUND(MAX(pr.price_per_g) - MIN(pr.price_per_g), 2) as price_spread,
    MAX(pr.timestamp) as last_updated
FROM products p
JOIN prices pr ON p.id = pr.product_id
JOIN pharmacies ph ON pr.pharmacy_id = ph.id
WHERE pr.timestamp >= datetime('now', '-7 days')
GROUP BY p.id;

-- View: Apotheken-Ranking (günstigste Apotheken insgesamt)
-- Zeigt welche Apotheken am häufigsten die günstigsten Preise haben
CREATE VIEW IF NOT EXISTS pharmacy_price_ranking AS
SELECT
    ph.id as pharmacy_id,
    ph.name as pharmacy_name,
    ph.location,
    COUNT(DISTINCT pr.product_id) as products_offered,
    ROUND(AVG(pr.price_per_g), 2) as avg_price_per_g,
    ROUND(MIN(pr.price_per_g), 2) as min_price_per_g,
    ROUND(MAX(pr.price_per_g), 2) as max_price_per_g,
    COUNT(CASE WHEN rank_table.price_rank = 1 THEN 1 END) as times_cheapest
FROM pharmacies ph
JOIN prices pr ON ph.id = pr.pharmacy_id
LEFT JOIN (
    SELECT
        pr.pharmacy_id,
        pr.product_id,
        RANK() OVER (PARTITION BY pr.product_id ORDER BY pr.price_per_g ASC) as price_rank
    FROM prices pr
    WHERE pr.timestamp >= datetime('now', '-7 days')
) rank_table ON ph.id = rank_table.pharmacy_id
WHERE pr.timestamp >= datetime('now', '-7 days')
GROUP BY ph.id
ORDER BY times_cheapest DESC, avg_price_per_g ASC;
