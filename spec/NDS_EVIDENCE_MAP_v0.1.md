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
- [PDF: NDS ALL resources.pdf | p=p49(6), p48(5)]
- [PDF: NDS  Advanced Trading Model.pdf | p=p1(2), p2(2)]
- [IMG: ._Screenshot 2024-06-07 at 00.06.44.PNG]
- [IMG: ._Screenshot 2024-08-14 at 23.54.22 copy.jpg]
- [VID: ._Rec 0006.mp4 | t=?]
**یادداشت انطباق:** Deadzone برای حذف فلیپ‌های میکرو؛ آستانه‌های دامنه برحسب σ/ATR.  
**وضعیت:** ☐

## B) توالی مجاز و قواعد ابطال (I1..I4)
**بند SPEC:** 3) ترتیب‌ها و ابطال‌ها  
**شواهد (PDF/IMG/VID):**
- [PDF: AI-NDS.Final.pdf | p=p5(12), p6(9)]
- [PDF: NDS ALL resources.pdf | p=p21(12), p38(12)]
- [IMG: ._IMG_0725.jpg]
- [IMG: ._IMG_0726.jpg]
- [VID: ._Rec 0006.mp4 | t=?]
**یادداشت انطباق:** پرچم `higher_than_prev` مستقل ثبت شود؛ نگهبان ری‌پینت w کندل.  
**وضعیت:** ☐

## C) کیفیت هوک (H0..H3) و تحمل‌ها (α/β/ε_hook)
**بند SPEC:** 4) Hook Quality  
**شواهد (PDF/IMG/VID):**
- [PDF: NDS_Strategy_English_Version.pdf | p=p11(5), p2(4)]
- [PDF: AI-NDS.Final.pdf | p=p5(6), p4(4)]
- [VID: ._Algorithmic Trading.mov | t=?]
**یادداشت انطباق:** α_low..α_high، β_low..β_high، ε_hook.  
**وضعیت:** ☐

## D) پیش‌بینی رالی با بیزین و حلقهٔ بازخورد
**بند SPEC:** (مطابق توضیح مدل شما)  
**شواهد (PDF/IMG/VID):**
- [PDF: AI-NDS.Final.pdf | p=p3(3), p1(2)]
- [PDF: Advanced_Quantitative_Trading_Integratin.pdf | p=p3(3), p1(2)]
**یادداشت انطباق:** استفاده از ΔE و hill-climbing برای اصلاح تخمین.  
**وضعیت:** ☐

## E) Random Forest به‌عنوان متافیلتر
**بند SPEC:** (مطابق توضیح مدل شما)  
**شواهد (PDF/IMG/VID):**
- [PDF: AI-NDS.Final.pdf | p=p3(8), p4(8)]
- [PDF: Advanced_Quantitative_Trading_Integratin.pdf | p=p5(8), p3(7)]
**یادداشت انطباق:** RF به‌عنوان متافیلتر کیفیت سیگنال.  
**وضعیت:** ☐

## F) GARCH + Money Management
**بند SPEC:** پیوند مدیریت ریسک/ولتیلیتی با خروجی نودها  
**شواهد (PDF/IMG/VID):**
- [PDF: Advanced_Money_Management_Strategy_Appli.pdf | p=p4(21), p2(14)]
- [PDF: Simple Money Management.pdf | p=p3(22), p2(21)]
**یادداشت انطباق:** σ̂_t (GARCH/ATR) برای SL/TP و سایز پوزیشن.  
**وضعیت:** ☐

## G) خروجی استاندارد و هم‌ترازی با MT5
**بند SPEC:** 5) ستون‌های خروجی و سازگاری Python/MT5  
**شواهد (PDF/IMG/VID):**
- [PDF: Advanced_Quantitative_Trading_Integratin.pdf | p=?]
- [VID: ._export_1731148455677.MOV | t=?]
**یادداشت انطباق:** ستون‌های نهایی میان Python/MT5 هم‌تراز بماند.  
**وضعیت:** ☐
