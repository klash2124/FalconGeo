[Falcon Geo_ Geo-Intelligence Tool.md](https://github.com/user-attachments/files/27981362/Falcon.Geo_.Geo-Intelligence.Tool.md)
# Falcon Geo: Geo-Intelligence Tool

```
  /\\      / \\
 / /\\    / /\\ \\
[ FALCON GEO: GEO-INTELLIGENCE ]
/ /  \\  / /  \\ \\
[ MAPPING & TRACKING ]
/ /    \\/ /    \\ \\
[ STATUS: ACTIVE ]
/ /      \\ \\
/ /        \\ \\
/_/          \\_\\
\ \        / /
 \ \      / /
  \ \    / /
   \ \  / /
    \ \/ /
     \/ /

[+] Falcon Geo is LIVE & READY [+] الصقر الجغرافي نشط وجاهز
```

## الوصف (Description)

Falcon Geo هي أداة متقدمة ومتعددة المنصات (Windows و Kali Linux) مصممة لجمع وتحليل المعلومات الجغرافية والاستخباراتية. تهدف الأداة إلى توفير رؤية شاملة للبيانات الجغرافية، بدءًا من تحديد مواقع عناوين IP وصولاً إلى رسم خرائط لشبكات Wi-Fi المحيطة.

## الميزات (Features)

تتكون Falcon Geo من وحدات رئيسية مصممة لأداء مهام استخباراتية جغرافية محددة:

### 1. وحدة تحديد الموقع وتتبع المسار (IP Geolocation & Traceroute)
*   **تحديد الموقع الجغرافي لـ IP/النطاق:** للحصول على معلومات مفصلة عن الموقع الجغرافي (البلد، المدينة، مزود الخدمة، خطوط الطول والعرض) لأي عنوان IP أو اسم نطاق.
*   **تتبع مسار البيانات (Traceroute):** لتتبع المسار الذي تسلكه حزم البيانات من جهازك إلى أي هدف (IP أو نطاق)، مما يساعد في فهم البنية التحتية للشبكة.

### 2. وحدة رادار ورسم خرائط Wi-Fi (WiFi Radar & Mapping)
*   **فحص شبكات Wi-Fi:** لاكتشاف وعرض تفاصيل شبكات Wi-Fi المحيطة (SSID, BSSID, قوة الإشارة، نوع الحماية).
*   **تصدير الشبكات الممسوحة إلى KML:** لإنشاء ملف KML يمكن فتحه باستخدام Google Earth أو برامج الخرائط الأخرى لعرض المواقع الجغرافية التقريبية للشبكات الممسوحة.

## التثبيت (Installation)

### المتطلبات الأساسية (Prerequisites)
*   Python 3.x
*   نظام تشغيل Windows أو Kali Linux

### تثبيت Falcon Geo
1.  **استنساخ المستودع (Clone the repository):**
    ```bash
    git clone https://github.com/YOUR_USERNAME/FalconGeo.git
    cd FalconGeo
    ```

2.  **تثبيت مكتبات Python المطلوبة:**
    ```bash
    pip install requests simplekml
    ```

### تثبيت الأدوات الخارجية (External Tools)
تتطلب بعض ميزات Falcon Geo تثبيت أدوات إضافية على نظامك:

#### على Kali Linux:
*   **Traceroute (لتتبع المسار):**
    ```bash
    sudo apt update
    sudo apt install traceroute
    ```
*   **Network Manager CLI (nmcli) أو Wireless Tools (iwlist) (لفحص Wi-Fi):**
    عادة ما تكون مثبتة مسبقًا في Kali Linux. إذا لم تكن كذلك:
    ```bash
    sudo apt install network-manager
    # أو
    sudo apt install wireless-tools
    ```

#### على Windows:
*   **Tracert (لتتبع المسار):** مدمج في Windows.
*   **Netsh WLAN (لفحص Wi-Fi):** مدمج في Windows.

## الاستخدام (Usage)

لتشغيل Falcon Geo، افتح Terminal (على Kali Linux) أو Command Prompt/PowerShell (على Windows) وانتقل إلى مجلد Falcon Geo، ثم قم بتشغيل السكريبت:

```bash
python FalconGeo.py
```

ستظهر لك القائمة الرئيسية للأداة، ومنها يمكنك التنقل بين الوحدات المختلفة:

```
--- Falcon Geo Main Menu ---
1. Display System Info
2. IP Geolocation & Traceroute
3. WiFi Radar & Mapping
4. Exit
```

اتبع التعليمات التي تظهر على الشاشة لاستخدام كل ميزة.

## إخلاء مسؤولية (Disclaimer)

تم تطوير Falcon Geo لأغراض تعليمية وبحثية فقط في مجال الأمن السيبراني. لا تتحمل Manus AI أو مطورو الأداة أي مسؤولية عن أي استخدام غير قانوني أو غير أخلاقي لهذه الأداة. يتحمل المستخدم المسؤولية الكاملة عن أي أضرار أو انتهاكات قد تنجم عن استخدام Falcon Geo. يرجى استخدام هذه الأداة بمسؤولية وفي إطار القانون والأخلاق.
