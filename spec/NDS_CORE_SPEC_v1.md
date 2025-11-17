NDS_CORE_SPEC_v1 — Draft 0.1

این سند قانونِ پایه‌ی پیاده‌سازی NDS است تا تمام کدها (Python/MQL5) با آن هماهنگ باشند. موارد با علامت ◻︎ باید در نسخه‌ی بعدی با رفرنس اصلی تکمیل/قفل شوند.

1) References (living list)

◻︎ Jafarian, I. — Advanced Money Management Strategy Applicable to Nodal Displacement Geometry (نام/سال/لینک دقیق)

◻︎ اسلایدها/دیاگرام‌های NDS (لینک فولدر مرجع)

2) Price Curve & Smoothing

Base curve: پیش‌فرض = HL2 = (High+Low)/2.

Alternatives: Close, HLC3.

Smoothing:

پیش‌فرض: EMA با طول ema_len (مثلاً 7–21).

اختیاری: Savitzky–Golay (window, polyorder) برای نگه‌داشتن مشتق‌ها.

Derivative: مشتق اول با np.gradient روی منحنی اسموت‌شده. (در صورت نیاز مشتق دوم برای تایید انحنا.)

3) Node Definition (Mathematical)

نود به‌صورت ریورسال مشتق‌محور تعریف می‌شود، نه سوئینگ کلاسیک.

کاندید نود:

تغییر علامت مشتق اول در i و موجود بودن انحنای مناسب (دره/قله).

قیود هندسی:

فاصله‌ی حداقل: i - last_idx ≥ min_distance بار.

دامنه‌ی حداقل: |p[i] − p[last]| ≥ k_sigma × σ_local، که σ_local از ATR یا std رولینگ به‌دست می‌آید.

ویژگی‌های نود:

شماره ترتیبی (ID: 1051, 1052, ...)

higher_than_prev برای تحلیل node-to-node.

یادداشت: این تعریف یک working theory است که با رفرنس اصلی NDS تطبیق و قفل می‌شود.

4) Sequences & Roles

توالی‌های پایه‌ی NDS:

صعودی: N1 → S1 → N2 → S2 → N3 → S3

نزولی: S1 → N1 → S2 → N2 → S3 → N3

قواعد:

هر نود نقش می‌گیرد (N/S) بر اساس موقعیت هندسی و روند محلی.

Invalidation: اگر قیود فاصله/دامنه/جهت نقض شوند، توالی fail می‌شود و ری‌لبلینگ لازم است.

5) Hooks & Symmetry

Hook1/Hook2: بازگشت‌های کوتاه/میانی بعد از ریورسال که دارای نسبت‌های شیب/دامنه/زمان مشخص‌اند.

Symmetry: قیود نسبت‌های زمان–قیمت در دو بازوی الگو (◻︎ مقادیر دقیق از رفرنس پر می‌شود).

6) Rally Estimation (Bayesian)

Features: دامنه‌ی نود، نقش در توالی، نسبت‌های هوک/سمتری، σ_t (ولتیلیتی)، شیب‌ها، زمان بین نودها.

Prior: از آمار تاریخی NDS و مدل ولتیلیتی (GARCH/σ_t).

Likelihood: از مدل داده‌محور (مثلاً RF) یا قانون‌های تجربی پایدار.

Posterior: احتمال رسیدن به Target1/2 در افق H بار.

7) Feedback Loop (ΔE)

ΔE (خطا): تفاوت بین rally_predicted و rally_realized.

Loop:

اصلاح آستانه‌ها (thresholds)

وزن‌دهی نمونه‌ها در بازآموزی مدل‌ها

بازتنظیم پارامترهای هندسی (min_distance, k_sigma, smoothing)

8) Volatility & Money Management

Vol model: GARCH/EGARCH برای σ_t.

Position sizing: تابعی از Posterior، σ_t، کیفیت الگو و سقف ریسک حساب.

Risk policy: R ثابت/دینامیک، استاپ بر اساس ساختار نود/هوک.

9) Implementation Conventions

CSV برای MT5:

node_id,bar_index,time,price,node_type,higher_than_prev

Timeframe پایه: US30 M15

نام‌گذاری فایل‌ها:

spec/NDS_CORE_SPEC_v1.md

src/python/nds_core.py

src/python/nds_ml.py

src/mql5/nds_indicator.mq5

src/mql5/nds_ea.mq5

tests/test_nds_core.py

Next Edits (for v0.2)

◻︎ مقادیر دقیق هوک‌ها، نسبت‌های symmetry، و شرایط invalidation از رفرنس اصلی اضافه شوند.

◻︎ پیاده‌سازی classify_nodes_sequence() مطابق الگوی NDS.

◻︎ ماژول nds_ml.py برای feature extraction + RF (node validation & rally strength) با ΔE-logging.

◻︎ یک بک‌تستر مینیمال برای چرخه‌ی Node→Signal→MM.

Appendix A — Data & Repo Layout (Drive ⇄ GitHub)

Drive (NDS_Archive)

NDS_Archive/
  data/
    raw/
      US30/M15/
        US30_M15_ICM_UTC_20240101_20251031.csv
      ...
    processed/
      US30/M15/
        US30_M15_clean_UTC_20240101_20251031.csv
      nds_nodes/
        US30_M15_nodes_v0_2025-11-14.csv
    README.md            # توضیح منبع، تایم‌زون، اسکیمای فایل‌ها
    datasets.yaml        # مانیفست دیتاست‌ها (نمونه زیر)
  patterns_examples/
    images/
      hook_examples/
      sequences/
    videos/
    annotations/
      labels.csv         # برچسب‌گذاری نود/توالی روی تصاویر/ویدئو
  pdfs/
    # مقالات/رفرنس‌ها
  checksums/
    sha256.txt           # هش فایل‌های کلیدی
MANIFEST.md              # نمای کلی لینک‌ها و ساختار

نام‌گذاری استاندارد فایل‌ها

SYMBOL_TIMEFRAME_VENDOR_TZ_STARTDATE_ENDDATE.csv

مثال: US30_M15_ICM_UTC_20240101_20251031.csv

تاریخ‌ها به صورت YYYYMMDD

TZ پیشنهادی: UTC (برای جلوگیری از مشکلات DST)

اسکیمای CSV استاندارد

ستون‌ها: time,open,high,low,close[,volume]

time: ISO‑8601 در UTC، صعودی، بدون تکرار.

داده‌ی «خام» را دست‌نخورده در raw/ نگه دارید؛ پاکسازی/ری‌سمپل در processed/ با توضیح روش.

مانیفست دیتاست‌ها — data/datasets.yaml

datasets:
  - id: us30_m15_icm_2024_2025_raw
    symbol: US30
    timeframe: M15
    vendor: ICMa
