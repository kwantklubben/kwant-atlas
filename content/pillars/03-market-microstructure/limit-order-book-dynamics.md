---
title: "Limit Order Book (LOB) Dynamics"
tags: [microstructure, lob, orderbook]
---

# Limit Order Book (LOB) Dynamics

Electronic exchanges match buyers and sellers using continuous double auctions organized in Limit Order Books.

## Market Data Tiers
- **Level 1 (Top of Book):** Best Bid and Best Ask price and quantity.
- **Level 2 (Market Depth):** Aggregated order quantities at each price level (typically 5–20 levels).
- **Level 3 (Full Order Log / Tick Data):** Every individual order submission, cancellation, modification, and fill (e.g. NASDAQ ITCH feed).

## Order Flow Imbalance (OFI)
Order Flow Imbalance measures net changes in supply and demand at the best bid and ask quotes. High OFI reliably predicts immediate tick price moves over subsequent microsecond-to-second intervals.
