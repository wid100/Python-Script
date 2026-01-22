# PDF to CSV Converter (Bengali Text)

এই প্রজেক্টটি PDF ফাইল থেকে বাংলা টেক্সট এক্সট্র্যাক্ট করে CSV ফাইলে রূপান্তর করার জন্য তৈরি করা হয়েছে। এটি বিশেষভাবে বিজয় কিবোর্ড লেআউট দিয়ে লেখা বাংলা টেক্সটের জন্য অপ্টিমাইজ করা হয়েছে।

## প্রয়োজনীয় সফটওয়্যার

- Python 3.7 বা তার উপরের ভার্সন
- pip (Python package manager)

## ইনস্টলেশন

1. প্রজেক্ট ফোল্ডারে যান:
```bash
cd PDFtoCSV
```

2. প্রয়োজনীয় প্যাকেজ ইনস্টল করুন:
```bash
pip install -r requirements.txt
```

## ব্যবহার

### মৌলিক ব্যবহার

```bash
python pdf_to_csv.py your_file.pdf
```

এটি `your_file.csv` নামে একটি CSV ফাইল তৈরি করবে।

### আউটপুট ফাইলের নাম নির্দিষ্ট করা

```bash
python pdf_to_csv.py input.pdf output.csv
```

## বৈশিষ্ট্য

- ✅ বাংলা টেক্সট সাপোর্ট (Bengali Unicode)
- ✅ বিজয় কিবোর্ড লেআউট ইস্যু ফিক্স
- ✅ PDF থেকে টেক্সট এক্সট্র্যাকশন
- ✅ টেবিল ডেটা এক্সট্র্যাকশন (যদি PDF-এ টেবিল থাকে)
- ✅ UTF-8 এনকোডিং সহ CSV এক্সপোর্ট
- ✅ মাল্টি-পেজ PDF সাপোর্ট

## ফাইল স্ট্রাকচার

```
PDFtoCSV/
├── pdf_to_csv.py          # মূল কনভার্টার স্ক্রিপ্ট
├── bengali_text_utils.py   # বাংলা টেক্সট প্রসেসিং ইউটিলিটি
├── requirements.txt        # Python প্যাকেজ ডিপেন্ডেন্সি
└── README.md              # এই ফাইল
```

## সমস্যা সমাধান

### বিজয় কিবোর্ড ইস্যু

যদি আপনার PDF-এ বিজয় কিবোর্ড দিয়ে লেখা টেক্সট ভাঙা বা ভুল দেখায়:

1. `bengali_text_utils.py` ফাইলে `_get_bijoy_mappings()` ফাংশনে আপনার স্পেসিফিক ক্যারেক্টার ম্যাপিং যোগ করুন
2. `pdf_to_csv.py` ফাইলে `_fix_bijoy_encoding()` ফাংশন আপডেট করুন

### এনকোডিং সমস্যা

CSV ফাইলটি UTF-8-sig এনকোডিংয়ে সেভ করা হয়, যা Excel এবং অন্যান্য স্প্রেডশীট প্রোগ্রামে বাংলা টেক্সট সঠিকভাবে দেখাবে।

## উন্নত ব্যবহার

### Python কোডে ব্যবহার

```python
from pdf_to_csv import PDFToCSVConverter

# কনভার্টার তৈরি করুন
converter = PDFToCSVConverter("your_file.pdf")

# CSV-তে কনভার্ট করুন
converter.convert_to_csv_simple("output.csv")
```

### কাস্টম টেক্সট প্রসেসিং

```python
from bengali_text_utils import BengaliTextProcessor

processor = BengaliTextProcessor()
cleaned_text = processor.clean_text(raw_text)
```

## নোট

- PDF-এর গুণমানের উপর নির্ভর করে টেক্সট এক্সট্র্যাকশনের ফলাফল পরিবর্তিত হতে পারে
- স্ক্যান করা PDF-এর জন্য OCR প্রয়োজন হতে পারে
- বিজয় কিবোর্ড ইস্যু ফিক্স করার জন্য আপনার স্পেসিফিক সমস্যা অনুযায়ী ম্যাপিং যোগ করতে হতে পারে

## সাহায্য

যদি কোনো সমস্যা হয়, অনুগ্রহ করে:
1. PDF ফাইলের গুণমান চেক করুন
2. Python ভার্সন চেক করুন (3.7+)
3. সব প্যাকেজ সঠিকভাবে ইনস্টল হয়েছে কিনা নিশ্চিত করুন
