# tiktok-creator-loyalty-model


TikTok Creator Loyalty & Engagement Simulation

This project builds a synthetic TikTok ecosystem to explore how creator size, viewer behavior, and content exposure shape loyalty, re-engagement, and retention curves.

It simulates:

300 creators across 5 tiers (nano → mega)

40,000 viewers with probabilistic loyalty

250,000 watch events

Return probability (rejoin rate) based on creator tier

A 30-day retention step-curve for each tier

The goal is to model how creator scale affects viewer stickiness.

What the simulation shows

1. Larger creators generate stronger loyalty

Rejoin probability by tier might look like:

Tier	Rejoin Probability
Nano	low
Micro	rising
Mid	solid loyalty
Macro	high loyalty
Mega	strongest loyalty

This matches real TikTok dynamics:
Bigger creators win more repeat views even with identical content.

2. Retention curves reveal how fast viewers drop off

A 30-day exponential retention curve is generated for each tier.

Higher tiers decay slower, meaning viewers come back longer and more reliably.
Smaller creators lose almost all engagement by ~Day 10.

This reflects how TikTok’s algorithm rewards content with stable return probability, not just one-off spikes.

 Why this project matters

This repo demonstrates that you can:

Build large-scale synthetic behavioral datasets

Model probability-driven user systems

Analyze loyalty, retention, and tier effects

Visualize creator–viewer interaction dynamics

Think like a product scientist studying virality and engagement

This is exactly the type of modeling used by TikTok, ByteDance, and social media data science teams.

Included Outputs

Bar chart: Loyalty (rejoin probability) by creator tier

Retention curves: 30-day return survival forecasts

Simulation code: Clean, documented Python model

 Tech Stack

Python, NumPy, Pandas, Seaborn, Matplotlib
