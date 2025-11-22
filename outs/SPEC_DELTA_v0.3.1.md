# SPEC_DELTA_v0.3.1

این نسخه تغییرات زیر را نسبت به v0.3 تثبیت می‌کند:

## A) تشخیص نود مشتق‌محور
- افزودن **Derivative Deadzone**: اگر |P′(t)| < δ ⇒ صفر تلقی می‌شود (δ برحسب σ_local یا ATR تعریف می‌شود).
- **Prominence/Thresholds**: پذیرش نود وقتی |Δp| ≥ max(k_sigma·σ_local, k_atr·ATR(m)); کف ولتیلیتی ε_floor.
- **Smoothing ملایم** قبل از مشتق (eg. EMA/Gauss) برای کاهش نویز.

## B) توالی و ابطال‌ها
- توالی‌های مجاز: صعودی N1→S1→N2→S2→N3→S3 ، نزولی S1→N1→S2→N2→S3→N3.
- ابطال‌ها:
  - **I1: Separation breach** — Δt < τ_min یا Δp < ε_min.
  - **I2: Sequence violation** — خارج از ترتیب مجاز.
  - **I3: Repaint guard** — نود تا w کندل «موقت» است؛ تأیید بعد از بسته‌شدن کندل w.
  - **I4: Structural conflict** — فیلد `higher_than_prev` همیشه مستقل ثبت می‌شود.

## C) کیفیت هوک
- سطوح: **H0/H1/H2/H3** بر اساس تقارن قیمت/زمان.
- تحمل‌ها: α_low..α_high برای قیمت، β_low..β_high برای زمان، و ε_hook برای کیفیت نهایی (مقادیر اولیه قابل‌کالیبراسیون).

## D) خروجی استاندارد (Python/MT5 parity)
`node_id, bar_index, time, price, node_type, higher_than_prev, hook_quality, seq_label?, σ_t, R̂, SL, TP, quality_score`

## E) اتصال به شواهد
- تمام بندهای بالا باید در `spec/NDS_EVIDENCE_MAP_v0.1.md` به صفحات PDF/تایم‌کد ویدیو/تصاویر ارجاع داده شوند.
