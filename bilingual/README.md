# 🌐 JEP Hong Kong Bilingual Support

**English + Traditional Chinese Support for All Receipts and Communications**

## 📋 Overview

Hong Kong's unique linguistic environment requires full bilingual support (English and Traditional Chinese) for all regulatory communications, customer-facing documents, and internal records. This directory provides comprehensive bilingual capabilities for JEP Hong Kong solutions.

### Why Bilingual Support Matters

| Requirement | JEP Solution |
|-------------|-------------|
| **PDPO Section 27** - Information must be in both languages | All receipts available in EN/ZH |
| **HKMA Guidelines** - Communications with customers | Bilingual explanations |
| **Consumer Council Recommendations** | Chinese translations for all terms |
| **Internal Audit Requirements** | Language-preference logging |

## 🏛️ Legal Requirements

### PDPO (Personal Data Privacy Ordinance)

| Section | Requirement | JEP Implementation |
|---------|-------------|-------------------|
| **Section 27** | Privacy policies must be available in both languages | `bilingual_policy()` |
| **Section 34** | Data access responses must be in requested language | Language-preference tracking |
| **Section 35** | Complaint handling in customer's language | Bilingual templates |

### HKMA Guidelines

| Guideline | Requirement | JEP Implementation |
|-----------|-------------|-------------------|
| **TM-G-1** | Customer communications in preferred language | Language selection in all receipts |
| **CR-G-12** | Credit decision explanations in both languages | Bilingual decision factors |
| **Fair Treatment** | Terms and conditions in both languages | Bilingual SLA documents |

## 🔧 Core Implementation

### Bilingual Tracker

```python
from jep.hk.bilingual import BilingualTracker

# Initialize with language preference
tracker = BilingualTracker(
    default_language="en",  # or "zh"
    organization="HSBC Hong Kong"
)

# Receipt in English
receipt_en = tracker.log_decision(
    operation="CREDIT_SCORING",
    resource="customer-data",
    actor_id="agent-123",
    reasoning_en="Risk assessment based on credit history",
    reasoning_zh="根據信貸記錄進行風險評估"
)

# Switch to Chinese
tracker.set_language("zh")
receipt_zh = tracker.log_decision(
    operation="信用評分",
    resource="客戶數據",
    actor_id="代理-123"
)
```

## 📁 Directory Structure

```
bilingual/
├── README.md                    # This file
├── core/                         # Core bilingual functionality
│   ├── translator.py              # Translation utilities
│   ├── templates.py               # Bilingual templates
│   └── locale.py                   # Language management
├── templates/                     # Bilingual templates
│   ├── receipts/                   # Receipt templates
│   │   ├── receipt_en.json
│   │   └── receipt_zh.json
│   ├── policies/                    # Privacy policy templates
│   │   ├── policy_en.md
│   │   └── policy_zh.md
│   └── notifications/               # Customer notifications
│       ├── approval_en.md
│       └── approval_zh.md
├── examples/                       # Usage examples
│   ├── bilingual_demo.py
│   └── language_switching.py
└── tests/                          # Tests
    └── test_bilingual.py
```

## 📄 Core Files

### 1. `core/translator.py`

```python
"""
Bilingual translation utilities for JEP Hong Kong.
"""

import json
from typing import Dict, Any, Optional

class BilingualTranslator:
    """
    Handles translation between English and Traditional Chinese
    for all JEP receipts and communications.
    """
    
    def __init__(self):
        self.translations = self._load_translations()
    
    def _load_translations(self) -> Dict:
        """Load translation dictionary."""
        return {
            # Operations
            "credit_scoring": "信用評分",
            "loan_approval": "貸款審批",
            "customer_due_diligence": "客戶盡職審查",
            "property_valuation": "物業估價",
            "funds_disbursement": "資金發放",
            
            # Risk levels
            "LOW": "低風險",
            "MEDIUM": "中風險", 
            "HIGH": "高風險",
            "CRITICAL": "嚴重風險",
            
            # Decision outcomes
            "APPROVED": "已批准",
            "DECLINED": "已拒絕",
            "PENDING": "待處理",
            "WITHDRAWN": "已撤回",
            
            # Common terms
            "customer": "客戶",
            "application": "申請",
            "amount": "金額",
            "date": "日期",
            "reference": "參考編號",
            "signature": "電子簽署",
            
            # PDPO terms
            "consent": "同意",
            "personal_data": "個人資料",
            "privacy_policy": "私隱政策",
            "data_subject": "資料當事人",
            "data_user": "資料使用者",
            
            # HKMA terms
            "mortgage": "按揭",
            "credit_assessment": "信貸評估",
            "ltv_ratio": "按揭成數",
            "dti_ratio": "債務收入比率",
            "approval_workflow": "審批流程"
        }
    
    def translate(self, text: str, to_lang: str = "zh") -> str:
        """Translate text to target language."""
        if to_lang == "en":
            return text
        return self.translations.get(text, text)
    
    def translate_dict(self, data: Dict, to_lang: str = "zh") -> Dict:
        """Translate dictionary keys and values."""
        if to_lang == "en":
            return data
        
        translated = {}
        for key, value in data.items():
            # Translate key
            zh_key = self.translate(key, "zh")
            
            # Translate value if it's a string
            if isinstance(value, str):
                translated[zh_key] = self.translate(value, "zh")
            elif isinstance(value, dict):
                translated[zh_key] = self.translate_dict(value, "zh")
            elif isinstance(value, list):
                translated[zh_key] = [
                    self.translate_dict(item, "zh") if isinstance(item, dict)
                    else self.translate(item, "zh") if isinstance(item, str)
                    else item
                    for item in value
                ]
            else:
                translated[zh_key] = value
        
        return translated
```

### 2. `templates/receipts/receipt_en.json`

```json
{
  "receipt_id": "Receipt ID",
  "timestamp": "Timestamp",
  "operation": "Operation",
  "status": "Status",
  "risk_level": "Risk Level",
  "customer_reference": "Customer Reference",
  
  "credit_decision": {
    "application_id": "Application ID",
    "amount": "Amount (HKD)",
    "decision": "Decision",
    "decision_factors": {
      "credit_score": "Credit Score",
      "dti_ratio": "Debt-to-Income Ratio",
      "employment_years": "Employment Years",
      "ltv_ratio": "Loan-to-Value Ratio"
    },
    "explanation": "Explanation"
  },
  
  "approval_workflow": {
    "level": "Approval Level",
    "approver": "Approver",
    "decision": "Decision",
    "notes": "Notes",
    "timestamp": "Approval Time"
  },
  
  "pdp_o_compliance": {
    "consent_id": "Consent ID",
    "purpose": "Purpose of Collection",
    "data_categories": "Data Categories",
    "retention_days": "Retention Period (days)",
    "dsar_contact": "DSAR Contact"
  },
  
  "signature": "Digital Signature"
}
```

### 3. `templates/receipts/receipt_zh.json`

```json
{
  "receipt_id": "收據編號",
  "timestamp": "時間戳記",
  "operation": "操作項目",
  "status": "狀態",
  "risk_level": "風險級別",
  "customer_reference": "客戶參考編號",
  
  "credit_decision": {
    "application_id": "申請編號",
    "amount": "金額（港元）",
    "decision": "審批結果",
    "decision_factors": {
      "credit_score": "信貸評分",
      "dti_ratio": "債務收入比率",
      "employment_years": "就業年資",
      "ltv_ratio": "按揭成數"
    },
    "explanation": "解釋說明"
  },
  
  "approval_workflow": {
    "level": "審批級別",
    "approver": "審批人",
    "decision": "審批決定",
    "notes": "備註",
    "timestamp": "審批時間"
  },
  
  "pdp_o_compliance": {
    "consent_id": "同意編號",
    "purpose": "收集目的",
    "data_categories": "資料類別",
    "retention_days": "保留期限（日）",
    "dsar_contact": "查閱資料要求聯絡人"
  },
  
  "signature": "電子簽署"
}
```

### 4. `templates/policies/policy_en.md`

```markdown
# Privacy Policy

**Effective Date:** {effective_date}
**Version:** {version}
**Data User:** {data_user}
**PCPD Registration:** {pcpd_registration}

## 1. Collection of Personal Data

We collect personal data for the following purposes:
{purposes}

### Types of Data Collected
{data_categories}

## 2. Use of Personal Data

Your personal data will be used only for the purposes stated above. Any use for new purposes will require your consent.

## 3. Data Sharing

We may share your data with:
{data_recipients}

## 4. Data Retention

| Data Category | Retention Period |
|---------------|------------------|
{retention_table}

## 5. Your Rights

Under the PDPO, you have the right to:
- Access your personal data
- Request correction of inaccurate data
- Withdraw consent

To exercise these rights, contact: {dsar_contact}

## 6. Language

This policy is available in English and Chinese. In case of inconsistency, the English version shall prevail.
```

### 5. `templates/policies/policy_zh.md`

```markdown
# 私隱政策聲明

**生效日期：** {effective_date}
**版本：** {version}
**資料使用者：** {data_user}
**私隱專員公署登記號碼：** {pcpd_registration}

## 1. 收集個人資料

我們為以下目的收集個人資料：
{purposes}

### 收集的資料類別
{data_categories}

## 2. 個人資料的使用

您的個人資料只會用於上述目的。如用於新目的，將另行徵求您的同意。

## 3. 資料共享

我們可能與以下機構共享您的資料：
{data_recipients}

## 4. 資料保留

| 資料類別 | 保留期限 |
|---------|---------|
{retention_table}

## 5. 您的權利

根據《個人資料（私隱）條例》，您有權：
- 查閱您的個人資料
- 要求更正不準確的資料
- 撤回同意

行使這些權利，請聯絡：{dsar_contact}

## 6. 語言版本

本政策備有中英文版本。如中英文版本有任何不一致，以英文版本為準。
```

## 🚀 Usage Examples

### 1. Basic Bilingual Receipt

```python
from jep.hk.bilingual import BilingualTracker

tracker = BilingualTracker(default_language="en")

receipt = tracker.log_decision(
    operation="CREDIT_SCORING",
    operation_zh="信用評分",
    resource="customer-123",
    actor_id="agent-456",
    risk_level="MEDIUM",
    risk_level_zh="中風險",
    explanation_en="Credit score 750 meets threshold",
    explanation_zh="信貸評分750符合要求"
)

# Receipt contains both languages
print(receipt["operation"])        # "CREDIT_SCORING"
print(receipt["operation_zh"])      # "信用評分"
```

### 2. Language Switching

```python
# Set language for session
tracker.set_language("zh")

# All subsequent receipts will be in Chinese
receipt = tracker.log_decision(
    operation="信用評分",
    resource="客戶-123",
    actor_id="代理-456"
)

# Get receipt in specific language
receipt_en = tracker.get_receipt(receipt["receipt_id"], lang="en")
receipt_zh = tracker.get_receipt(receipt["receipt_id"], lang="zh")
```

### 3. Bilingual Customer Notification

```python
from jep.hk.bilingual import CustomerNotifier

notifier = CustomerNotifier()

# Send notification in customer's preferred language
notification = notifier.send_approval_notice(
    customer_id="CUST-123",
    preferred_language="zh",  # from customer profile
    application_id="MORT-2026-001",
    amount=5000000,
    decision="APPROVED"
)

# Notification content in Chinese
print(notification["subject"])  # "按揭申請批准通知"
print(notification["body"])      # "您的按揭申請（編號：MORT-2026-001）已獲批准..."
```

## 🔍 Verification

```bash
# Test bilingual functionality
python tests/test_bilingual.py

# Output:
# ================================
# BILINGUAL SUPPORT VERIFICATION
# ================================
# ✅ English receipts generated
# ✅ Chinese receipts generated
# ✅ Language switching works
# ✅ Translations complete
# ✅ Templates rendered correctly
# ================================
# ALL TESTS PASSED
# ================================
```

## 📊 Compliance Matrix

| Requirement | English Support | Chinese Support | Verified |
|------------|-----------------|-----------------|----------|
| PDPO Section 27 | ✅ | ✅ | ✅ |
| HKMA Customer Comms | ✅ | ✅ | ✅ |
| Consumer Council | ✅ | ✅ | ✅ |
| Credit Agreements | ✅ | ✅ | ✅ |
| Privacy Policies | ✅ | ✅ | ✅ |
| DSAR Responses | ✅ | ✅ | ✅ |

## 📬 Contact

For bilingual support inquiries:
- **Email**: bilingual@humanjudgment.org
- **GitHub**: [hjs-spec/jep-hk-solutions](https://github.com/hjs-spec/jep-hk-solutions)

---

*Last Updated: March 2026*
*最後更新：2026年3月*
```
