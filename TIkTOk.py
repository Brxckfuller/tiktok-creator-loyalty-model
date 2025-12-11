#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 22:23:03 2025

@author: brockfuller
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="white", context="talk")
np.random.seed(42)

# =====================================================
# 1. Creators with tiers
# =====================================================

tiers = ["nano", "micro", "mid", "macro", "mega"]
tier_dist = [0.40, 0.30, 0.15, 0.10, 0.05]

n_creators = 300

creators = pd.DataFrame({
    "creator_id": np.arange(1, n_creators+1),
    "tier": np.random.choice(tiers, size=n_creators, p=tier_dist)
})

loyalty_weight = {"nano":1.0, "micro":1.4, "mid":1.9, "macro":2.4, "mega":3.0}
creators["loyalty_weight"] = creators["tier"].map(loyalty_weight)

# =====================================================
# 2. Viewers with assigned home creator
# =====================================================

n_viewers = 40_000

viewers = pd.DataFrame({"viewer_id": np.arange(1, n_viewers+1)})
viewers["home_creator"] = np.random.choice(
    creators["creator_id"],
    size=n_viewers,
    p=creators["loyalty_weight"]/creators["loyalty_weight"].sum()
)

# =====================================================
# 3. Events (with controlled repeat exposure)
# =====================================================

n_events = 250_000

events = pd.DataFrame({
    "viewer_id": np.random.choice(viewers["viewer_id"], size=n_events)
})

events = events.merge(viewers, on="viewer_id", how="left")

# loyalty probability based on tier
events = events.merge(creators[["creator_id","tier","loyalty_weight"]],
                      left_on="home_creator", right_on="creator_id", how="left")

events["p_loyal"] = (
    events["loyalty_weight"] / events["loyalty_weight"].max() * 0.60
)

mask = np.random.rand(n_events) < events["p_loyal"]

events["creator_id"] = np.where(
    mask,
    events["home_creator"],
    np.random.choice(creators["creator_id"], size=n_events)
)

# overwrite tier cleanly
events = events.merge(creators[["creator_id","tier"]], on="creator_id", how="left",
                      suffixes=("","_fresh"))

events = events.drop(columns=["tier_fresh"])  # only one tier now

# =====================================================
# 4. Define rejoin_flag (THIS is the single final column)
# =====================================================

pair = events.groupby(["viewer_id","creator_id"]).size().reset_index(name="views")
pair["rejoin_flag"] = (pair["views"] > 1).astype(int)

pair = pair.merge(creators[["creator_id","tier"]], on="creator_id", how="left")

# single canonical metric
rejoin_by_tier = pair.groupby("tier")["rejoin_flag"].mean().reindex(tiers)
print("\nLoyalty (Rejoin Probability) by Tier:\n", rejoin_by_tier)

# =====================================================
# 5. Bar Chart
# =====================================================

plt.figure(figsize=(9,5))
sns.barplot(x=rejoin_by_tier.index, y=rejoin_by_tier.values, palette="rocket_r")
for i, v in enumerate(rejoin_by_tier.values):
    plt.text(i, v+0.015, f"{v:.2f}", ha="center")
plt.title("Creator-Tier Loyalty & Return Probability")
plt.ylabel("Rejoin Probability")
plt.ylim(0, max(rejoin_by_tier.values) + 0.1)
sns.despine()
plt.show()

# =====================================================
# 6. Retention Step Curve (now guaranteed to work)
# =====================================================

tiers = rejoin_by_tier.index.tolist()
loyalty = rejoin_by_tier.values

days = np.arange(0, 30)
curves = {}

for i, tier in enumerate(tiers):
    start = loyalty[i]
    k = 0.18 - (start * 0.25)
    curves[tier] = start * np.exp(-k * days)

plt.figure(figsize=(9,5))
for tier in tiers:
    plt.step(days, curves[tier], where='mid', lw=2, label=tier)

plt.title("30-Day Return Survival by Creator Tier")
plt.xlabel("Days Since Last Session")
plt.ylabel("Retention Probability")
plt.ylim(0, max(loyalty)+0.1)
plt.xlim(0, 30)
plt.legend(title="Tier", bbox_to_anchor=(1.05,1), loc="upper left")
plt.grid(alpha=0.15)
sns.despine()
plt.tight_layout()
plt.show()
























