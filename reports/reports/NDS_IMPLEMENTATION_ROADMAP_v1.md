# NDS Implementation Roadmap v1

## Purpose

This document defines the implementation roadmap for the NDS trading-system project.

## Core Implementation Principle

Do not start with trade signals. Start with structure.

Correct order:

1. Source alignment
2. Data preparation
3. Structural labeling
4. Visual template validation
5. Core data models
6. Sequence state machine
7. 123 / Point 3 detector
8. ND detector
9. Flag detector
10. Hook / Rally detectors
11. 86% reference engine
12. Multi-timeframe engine
13. GARCH risk module
14. AI residual refinement
15. Backtesting
16. MT5 integration
17. Reporting

## Phase 0 — Repository Specification Update

Create all source-aligned spec files and changelog. Exit when every planned spec exists and uncertain rules are marked validation-required.

## Phase 1 — Data Inventory and Standardization

Prepare US30/Dow Jones M15, M5, and M1 data. Validate timezone, missing candles, duplicate timestamps, bad OHLC values, weekend gaps, source/broker, and timeframe alignment.

## Phase 2 — Source-Based Labeling Framework

Create a label schema for Z, N, S, Cycle, 123, Point 3, ND, Flag, Hook A/B, Rally, 86% context, and parent/child timeframe relation.

## Phase 3 — Visual Template Validation

Extract templates from NDS visual examples: positive/negative cycle, flag, Hook A/B, Rally 123, Point 3 decision, ND, and 86% references.

## Phase 4 — Core Data Structures

Create Python data models for NDSNode, NDSCycle, NDS123Structure, NDSNearDeath, NDSFlag, NDSHook, NDSRally, NDS86Reference, NDSMultiTimeframeContext, and NDSRiskPlan.

## Phase 5 — Sequence State Machine Prototype

Implement WAIT_Z through CYCLE_COMPLETE plus extended states for point 3, ND, flag, multi-timeframe confirmation, and risk approval.

## Phase 6–11 — Structural Detectors and Context Engines

Implement 123/Point3, ND, Flag, Hook/Rally, 86% reference, multi-timeframe and nested-cycle engines in that order.

## Phase 12 — GARCH Risk Module

Implement GARCH volatility, ATR fallback, position sizing, broker point value conversion, midpoint trailing, and risk approval.

## Phase 13 — AI Residual Refinement

Add AI only after NDS structural features exist. AI must refine residuals, not create direct buy/sell signals.

## Phase 14 — Backtesting

Separate structural detection outcomes from trade/risk outcomes. Report node accuracy, ND confirmation, point3 decisions, hook classification, flag continuation, sequence validity, multi-timeframe alignment, 86% deviation, drawdown, expectancy, and GARCH behavior.

## Phase 15 — MT5 Integration

Export validated signals and risk plans to MT5. EA must not override risk plan or execute invalid context.

## Non-Negotiable Rules

Do not start with buy/sell signals, raw AI prediction, generic swing nodes, universal 86%, flag-only ND, merged Hook A/B, single-timeframe context, or trades before GARCH risk approval.
