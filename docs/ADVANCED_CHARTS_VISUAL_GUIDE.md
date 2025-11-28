# Advanced Charts - Visual Guide

## Interface Overview

### Control Panel
```
┌──────────────────────────────────────────────────────┐
│ Advanced Visualization                                │
├──────────────────────────────────────────────────────┤
│  Select Year Range:  [5 years ▼]                     │
│  Select Country:     [All countries ▼]               │
│                                                        │
│  [Update Charts]                                      │
└──────────────────────────────────────────────────────┘
```

### Stats Cards
```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Total        │ Avg Price    │ YoY Growth   │ Property     │
│ Records      │              │              │ Types        │
│              │              │              │              │
│ 978,768      │ $523K        │ +4.2%        │ 12           │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

## Chart Types

### 1. Monthly Price Trend (Line Chart)
```
Price ($)
  800K │                                    ╱─────
       │                          ╱────────╱
  600K │                  ╱──────╱
       │          ╱──────╱
  400K │  ───────╱
       │
  200K └──────┬──────┬──────┬──────┬──────┬──────
           2020   2021   2022   2023   2024   2025

Legend: ──── Average Price    ─ ─ ─ Median Price
```

**Data Source:** `/api/charts/price-trend`
**Shows:** Average vs Median price trends over time
**Interactive:** Hover for exact values, zoom in/out

### 2. Property Price by Type (Bar Chart)
```
Property Type               Average Price
────────────────────────────────────────────────
Apartment          ████████████████░░░░ $450K
Condo              ██████████████████░░ $620K
House              █████████████████░░░ $580K
Townhouse          ████████████░░░░░░░░ $420K
Villa              ██████████████████████ $750K
```

**Data Source:** `/api/charts/property-type-distribution`
**Shows:** Top 10 property types by average price
**Interactive:** Click to filter by type

### 3. Price Range Distribution (Doughnut Chart)
```
        ╭────────────────╮
      ╱   <$200K: 15%    ╲
    ╱     $200-400K: 35%   ╲
   │      $400-600K: 25%    │
    ╲     $600-800K: 15%   ╱
      ╲   >$800K: 10%    ╱
        ╰────────────────╯
```

**Data Source:** `/api/charts/price-range-distribution`
**Shows:** Percentage of properties in each price bracket
**Interactive:** Click segment to highlight

### 4. Area Distribution (Bar Chart)
```
Area Range        Percentage of Properties
────────────────────────────────────────────────
<50m²             ████░░░░░░░░░░░░░░░ 10%
50-100m²          ████████████████░░░ 40%
100-150m²         ████████████░░░░░░░ 30%
150-200m²         ██████░░░░░░░░░░░░░ 15%
>200m²            ██░░░░░░░░░░░░░░░░░ 5%
```

**Data Source:** `/api/charts/area-distribution`
**Shows:** Distribution of properties by area size
**Interactive:** Hover for count

### 5. Seasonal Patterns (Radar Chart)
```
                    Jan
                     │
         Dec         │         Feb
            ╲        │        ╱
              ╲      │      ╱
     Nov        ╲    │    ╱        Mar
                  ╲  │  ╱
                    ╲│╱
           ─────────────────── Apr
                    ╱│╲
                  ╱  │  ╲
     Oct        ╱    │    ╲        May
              ╱      │      ╲
            ╱        │        ╲
         Sep         │         Jun
                     │
                    Aug
```

**Data Source:** `/api/charts/seasonal-patterns`
**Shows:** Average price patterns by month (Jan-Dec)
**Interactive:** See price fluctuations throughout the year

### 6. Top Cities Comparison (Horizontal Bar)
```
City                    Average Price
──────────────────────────────────────────────────────
San Francisco    ████████████████████████████ $1.2M
New York         ██████████████████████████░░ $950K
Boston           ████████████████████████░░░░ $850K
Seattle          ███████████████████████░░░░░ $780K
Los Angeles      ██████████████████████░░░░░░ $720K
San Diego        █████████████████████░░░░░░░ $680K
Chicago          ████████████████████░░░░░░░░ $620K
Austin           ███████████████████░░░░░░░░░ $580K
Miami            ██████████████████░░░░░░░░░░ $550K
Portland         █████████████████░░░░░░░░░░░ $520K
Denver           ████████████████░░░░░░░░░░░░ $490K
Atlanta          ███████████████░░░░░░░░░░░░░ $450K
Phoenix          ██████████████░░░░░░░░░░░░░░ $420K
Dallas           █████████████░░░░░░░░░░░░░░░ $400K
Houston          ████████████░░░░░░░░░░░░░░░░ $380K
```

**Data Source:** `/api/charts/top-cities`
**Shows:** Top 15 cities by average price
**Interactive:** Sorted by price, hover for details

### 7. Price by Type Trend (Multi-line Chart)
```
Price ($)
  800K │                           ╱Villa
       │                     ╱────╱
  600K │               ╱────╱    ╱Condo
       │         ╱────╱    ╱────╱
  400K │   ─────╱    ╱────╱────╱Apartment
       │            ╱
  200K └──────┬──────┬──────┬──────┬──────
           2020   2021   2022   2023   2024

Legend: 
──── Villa    ──── Condo    ──── Apartment
──── House    ──── Townhouse
```

**Data Source:** `/api/charts/price-by-type-trend`
**Shows:** Price trends for top 5 property types over time
**Interactive:** Toggle property type visibility, hover for values

## Filter Examples

### By Country
```
All Countries → Shows global aggregate
Singapore → Shows Singapore market only
USA → Shows US market only
Australia → Shows Australian market only
```

### By Year Range
```
5 years → Last 5 years of data (2020-2025)
10 years → Last 10 years (2015-2025)
15 years → Last 15 years (2010-2025)
All years → Complete dataset (1990-2025)
```

## Color Scheme

### Light Theme
- Primary: #00D4FF (Cyan Blue)
- Accent: #8B5CF6 (Purple)
- Success: #00C9A7 (Teal)
- Warning: #FFB020 (Orange)
- Danger: #FF6B6B (Red)

### Dark Theme
- Primary: #1E90FF (Dodger Blue)
- Accent: #9F7AEA (Light Purple)
- Success: #48BB78 (Green)
- Warning: #ECC94B (Yellow)
- Danger: #FC8181 (Light Red)

## Chart Interactions

### All Charts Support:
- ✓ **Hover** - Show exact values in tooltip
- ✓ **Legend Click** - Toggle dataset visibility
- ✓ **Animation** - Smooth transitions on load/update
- ✓ **Responsive** - Auto-resize on window change

### Additional Features:
- **Line Charts** - Zoom in/out, pan
- **Bar Charts** - Click to filter/highlight
- **Doughnut** - Rotate to focus
- **Radar** - Scale adjustment

## Loading States

### Before Data Loads
```
┌──────────────────────────────────┐
│                                   │
│      🔄 Loading data...           │
│                                   │
│      Please wait...               │
│                                   │
└──────────────────────────────────┘
```

### After Data Loads
```
┌──────────────────────────────────┐
│  [Chart visualizations display]   │
│                                   │
│  ✓ All charts loaded              │
│  ✓ 978,768 records processed      │
└──────────────────────────────────┘
```

### Error State
```
┌──────────────────────────────────┐
│                                   │
│  ⚠️ Error loading data            │
│                                   │
│  Please try again                 │
│                                   │
└──────────────────────────────────┘
```

## API Response Examples

### Overview Endpoint
```json
{
  "success": true,
  "data": {
    "total_records": 978768,
    "avg_price": 523420.50,
    "median_price": 425000.00,
    "min_price": 75000.00,
    "max_price": 7700000.00,
    "yoy_growth": 4.2,
    "property_types_count": 12
  }
}
```

### Price Trend Endpoint
```json
{
  "success": true,
  "data": {
    "labels": [2020, 2021, 2022, 2023, 2024, 2025],
    "mean": [450000, 475000, 500000, 520000, 540000, 563000],
    "median": [380000, 395000, 410000, 425000, 440000, 458000],
    "count": [150000, 155000, 160000, 165000, 170000, 178768]
  }
}
```

### Top Cities Endpoint
```json
{
  "success": true,
  "data": {
    "cities": ["San Francisco", "New York", "Boston", ...],
    "avg_prices": [1200000, 950000, 850000, ...]
  }
}
```

## Performance Metrics

- **API Response Time:** < 500ms per endpoint
- **Chart Render Time:** < 1s for all 7 charts
- **Data Processing:** 978K records in < 2s
- **Memory Usage:** ~150MB for complete visualization
- **Network:** 8 parallel requests, ~200KB total payload

## Browser Console Output (Success)

```
✓ Countries loaded: ["Singapore", "USA", "Australia"]
✓ Fetching visualization data...
✓ Overview: 978,768 records, $523K avg
✓ Price trend: 6 years of data
✓ Property types: 12 types found
✓ All charts rendered successfully
✓ Visualization ready in 2.3s
```

---
*This guide shows the visual structure and interactions of the Advanced Charts feature*
