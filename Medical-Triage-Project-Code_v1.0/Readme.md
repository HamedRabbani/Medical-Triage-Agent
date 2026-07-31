#### **Overview:**



این پروژه یک نمونه اولیه از سیستم تریاژ پزشکی مبتنی بر هوش مصنوعی

است که در فاز اول روی هسته اصلی مکالمه و تریاژ  پایه تمرکز دارد.

هدف این فاز، دریافت اطلاعات اولیه بیمار، شناسایی اطلاعات ناقص، پرسیدن سؤالات تکمیلی و اجرای یک فرآیند اولیه برای ارزیابی سطح خطر است در این فاز از



* &#x20;RAG
* &#x20;Database
* &#x20;External Search 
* &#x20;Long-term Memory

استفاده نشده است



#### **Objectives of this Phase:**



* دریافت علائم بیمار
* استخراج سن، علائم، مدت و شدت علائم
* مدیریت اطلاعات ناقص
* پرسیدن سؤالات تکمیلی
* حفظ اطلاعات جمع‌آوری‌شده در طول سشن
* تشخیص رِد فِلگ های اولیه
* Executed Rule-Based Triage
* بررسی نتیجه توسط  سوپروایزر
* نمایش نتیجه در یک رابط گرافیکی ساده





#### **Phase 1:**

###### **Conversation Layer:** 



با ساخت این لایه سیستم می تواند از کاربر اطلاعات بگیرد اطلاعاتی مثل: 

* سن
* علائم
* مدت زمان
* شدت



###### **Symptom Agent:**



در این مرحله پیام طبیعی کاربر را دریافت می کند و اطلاعات را استخراج میکند مثلا:



"I'm 30 and I've had a mild headache for 3 days"

و بعد در خروجی تبدیل می شود به 

age = 30

symptoms = \["headache"]

duration = "3 days"

severity = "mild"



###### 

###### **State Management:**



این مرحله برسی میکند آیا اطلاعات کافی داریم یا نه مثلا:

Symptoms 

Age 

Duration 

Severity 





#### **Replanning / Feedback Loop:**



&#x20;اگر اطلاعات ناقص باشد مراحل زیر طی میشود



**Planner>Question>User Answer>Symptom Agent>Planner**

&#x20;با این روش سیستم مجدد وضعیت را برسی میکند.





#### **Risk Assessment:**

وقتی اطلاعات کامل شد، سیستم وارد ارزیابی ریسک میشود 

**Risk Agent>Triage Rules>Red Flag Detection>Risk Level**



&#x20;    



#### **Streamlit UI:**

در نهایت یک رابط کاربری ساده ساختم برای چت، نمایش سوال، دریافت پاسخ، نمایش نتیجه و دکمه شروع ارزیابی مجدد. 



##### **مراحل زیر اجرا شده در فاز اول:**



* LangGraph Workflow
* Symptom Agent
* Planner Agent
* Risk Assessment
* Rule-Based Triage
* Red Flag Detection
* Supervisor
* State Management
* Streamlit Chat UI
* Multi-turn Conversation
* Basic Scenario Testing



##### **مراحل زیر در فازهای بعدی اجرا خواهد شد:**



* RAG
* Vector Database
* Medical Knowledge Database
* External Search
* Long-term Memory
* Patient History Database
* Advanced Clinical Validation
* Full ESI Clinical Implementation



#### **Medical Validation:**



در فاز اول  تمرکز بر ساخت و تست مراحل اجرای تریاژ و جریان تصمیم‌گیری مبتنی بر قواعد است.

منطق پزشکی و سطح‌بندی ESI

&#x20;در مراحل بعدی بر اساس منابع و دستورالعمل‌های بالینی معتبر بازبینی و اعتبارسنجی خواهد شد.

بنابراین خروجی فعلی نباید به‌عنوان تشخیص پزشکی یا جایگزین ارزیابی پزشک استفاده شود



##### **نصب وابستگی‌ها:**



**pip install -r requirements.txt**

**اجرای برنامه:**

**streamlit run app.py**

**سپس رابط کاربری در مرورگر باز می‌شود.**











