# شبکه اجتماعی با python + django + postgresql + Docker + MongoDB 


-------------------
## ویژگی ها

* افزودن پست  + قابلیت افزودن تصاویر مختلف  به هر پست
* افزودن کامنت
* افزودن پاسخ به یک کامنت
* لایک پست
* نمایش پست های یک کاربر
* نمایش کاربران لایک کرده
* نمایش کامنت های یک پست
___________________
 * درخواست دوستی
 * قابلیت رد کردن و یا تایید کردن دوستی
 * نمایش دوستان
 * قابیلت حستحو کاربران و پست ها
### نکات
 * پست ها شامل یک متن و تعداد لایک و کامنت هستند
 * کامنت ها شامل متن و نام کاربری شخص نویسنده
 * کاربران شامل نام کاربری می باشند.
 * پیاده سازی برای  پاسخگویی به حجم زیادی از داده
----------
 در پیاده سازی سعی شده که query ها به شکل optimize باشد .

------
### موارد پیشنهادی

* استفاده از cache جهت نمایش پست های محبوب
* استفاده از database sharding برای توزیع داده ها 
* استفاده از CDN ، cloud systems جهت بارگذاری تصاویر

### راه اندازی
جهت راه اندازی میتوانید از docker-compose استفاده کنید :
بعد از clone در دایرکتوری مربوطه دستر زیر را اجرا کنید 

> docker-compose up -d --build 