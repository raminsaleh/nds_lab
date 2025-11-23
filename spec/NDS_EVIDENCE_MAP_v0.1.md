# NDS Evidence Map (v0.1)

این سند هر بند اصلی SPEC را به مدارک (PDF/تصویر/ویدیو) وصل می‌کند تا SPEC «منبع‌محور» باشد.

---

## Tag Schema (استاندارد ارجاع)
- PDF: `[PDF: <filename.pdf> | p=12-14]`  ← صفحه یا بازه صفحه
- IMG: `[IMG: <image_name.ext>]`          ← نام فایل تصویر
- VID: `[VID: <video_name.ext> | t=00:03:15-00:03:50]` ← بازه زمانی
- پس از هر تگ، یک جملهٔ کوتاه دربارهٔ آنچه مدرک نشان می‌دهد.

> نام دقیق فایل‌ها را از:
> - `outs/PDF_CATALOG.md`
> - `spec/IMAGES_INDEX.md`
> - `spec/VIDEOS_INDEX.md`
> بردارید.

---

## A) مشتق، Deadzone و فیلترها
**بند SPEC:** 2) تشخیص نود مشتق‌محور + Deadzone + Prominence  
**شواهد (PDF/IMG/VID):**
- [PDF: NDS ALL resources.pdf | p=?] — تعریف ریورسال با مشتق و پیش‌نیاز هموارسازی
- [PDF: NDS  Advanced Trading Model.pdf | p=?] — جزئیات عملی روی تشخیص نقطه
- [IMG: Screenshot 2024-06-07 at 00.06.44.PNG] — نمونه ناحیه ریورسال و تقارن محلی
- [VID: Rec 0006.mp4 | t=?] — مشاهدهٔ صفرشدن مشتق و تأیید بصری
**یادداشت انطباق:** Deadzone برای حذف فلیپ‌های میکرو؛ آستانه‌های دامنه برحسب σ/ATR.  
**وضعیت:** ☐

## B) توالی مجاز و قواعد ابطال (I1..I4)
**بند SPEC:** 3) ترتیب‌ها و ابطال‌ها  
**شواهد:**
- [PDF: AI-NDS.Final.pdf | p=?] — تعریف ترتیب صعودی/نزولی و قیود
- [PDF: NDS ALL resources.pdf | p=?] — نمونه‌های ابطال (separation/repaint)
- [IMG: IMG_0725.jpg] — مثال تصویری نقض جدایش
- [VID: Rec 0012.mp4 | t=?] — کیس نقض ترتیب و ابطال
**یادداشت انطباق:** پرچم `higher_than_prev` مستقل ثبت شود؛ نگهبان ری‌پینت w کندل.  
**وضعیت:** ☐

## C) کیفیت هوک (H0..H3) و تحمل‌ها (α/β/ε_hook)
**بند SPEC:** 4) Hook Quality  
**شواهد:**
- [PDF: NDS_Strategy_English_Version.pdf | p=?] — تعریف تقارن قیمت/زمان و بازه تحمل
- [PDF: AI-NDS.Final.pdf | p=?] — مثال‌های عملی H1/H2/H3
- [VID: Algorithmic Trading.mov | t=?] — نمونه هوک کامل (H3) با هر دو تقارن
**یادداشت انطباق:** α_low..α_high، β_low..β_high، ε_hook.  
**وضعیت:** ☐

## D) پیش‌بینی رالی با بیزین و حلقهٔ بازخورد
**بند SPEC:** (مطابق توضیح مدل شما)  
**شواهد:**
- [PDF: AI-NDS.Final.pdf | p=?] — چارچوب بیزین برای اندازهٔ رالی
- [PDF: Advanced_Quantitative_Trading_Integratin.pdf | p=?] — اتصال به تخمین خطا و فیدبک
**یادداشت انطباق:** استفاده از ΔE و hill-climbing برای اصلاح تخمین.  
**وضعیت:** ☐

## E) Random Forest به‌عنوان متافیلتر
**بند SPEC:** (مطابق توضیح مدل شما)  
**شواهد:**
- [PDF: AI-NDS.Final.pdf | p=?] — انتخاب ویژگی‌ها از نودها و ولتیلیتی
- [PDF: Advanced_Quantitative_Trading_Integratin.pdf | p=?] — ارزیابی کیفیت سیگنال
**وضعیت:** ☐

## F) GARCH + Money Management
**بند SPEC:** پیوند مدیریت ریسک/ولتیلیتی با خروجی نودها  
**شواهد:**
- [PDF: Advanced_Money_Management_Strategy_Appli.pdf | p=?] — منطق سایز پوزیشن و قیود عملی
- [PDF: Simple Money Management.pdf | p=?] — قوانین ساده مکمل
**یادداشت انطباق:** استفاده از σ̂_t (GARCH/ATR) برای SL/TP و پوزیشن‌سایز.  
**وضعیت:** ☐

## G) خروجی استاندارد و هم‌ترازی با MT5
**بند SPEC:** 5) ستون‌های خروجی و سازگاری Python/MT5  
**شواهد:**
- [PDF: Advanced_Quantitative_Trading_Integratin.pdf | p=?] — فرمت خروجی/انتگره‌یشن
- [VID: export_1731148455677.MOV | t=?] — نمایش خروجی/اکسپورت
**یادداشت انطباق:** ستون‌های نهایی: node_id, time, price, node_type, higher_than_prev, hook_quality, seq_label?, σ_t, R̂, SL, TP, quality_score.  
**وضعیت:** ☐
