# 🇭🇰 JEP for Hong Kong PDPO

**Complete Compliance with Personal Data (Privacy) Ordinance 6 Data Protection Principles**

## 📋 Overview

The Personal Data (Privacy) Ordinance (Cap. 486) (PDPO) is Hong Kong's primary data protection law, consisting of **6 Data Protection Principles (DPPs)**. This directory provides a complete JEP implementation aligned with all 6 principles, ensuring AI systems can demonstrate compliance through verifiable receipts.

### Why PDPO Compliance Matters for AI

| Challenge | JEP Solution |
|-----------|-------------|
| How to prove purpose of data collection? | `purpose` field in every receipt |
| How to ensure data accuracy? | Data hashing + verification |
| How to manage retention periods? | Configurable `retention_days` |
| How to demonstrate security measures? | Ed25519 signatures + encryption |
| How to provide transparency? | JSON-LD machine-readable metadata |
| How to handle access requests? | Complete audit trail |

## 🏛️ The 6 Data Protection Principles

| Principle | Summary | JEP Implementation |
|-----------|---------|-------------------|
| **DPP1 – Purpose & Manner of Collection** | Data must be collected for a lawful purpose with consent | `purpose` field + consent records |
| **DPP2 – Accuracy & Duration** | Data must be accurate and not kept longer than necessary | `retention_days` config + data hashing |
| **DPP3 – Use of Personal Data** | Data can only be used for original purpose or with consent | `purpose_validation` + consent tracking |
| **DPP4 – Data Security** | Reasonable security measures must be in place | Ed25519 signatures + encryption metadata |
| **DPP5 – Transparency** | Data users must provide clear privacy policies | JSON-LD machine-readable metadata |
| **DPP6 – Access & Correction** | Individuals can access and correct their data | Complete audit trail + data lineage |

## 🔧 Core Implementation

### PDPO-Compliant Tracker

```python
from jep.hk.pdpo import PDPOComplianceTracker

# Initialize tracker with PDPO configuration
tracker = PDPOComplianceTracker(
    data_user="HSBC Hong Kong",  # Name of data user
    retention_days=2555,         # 7 years default
    language="en",                # or "zh" for Traditional Chinese
    pcpd_registration_number="R123456"  # Optional PCPD registration
)

# Log a data collection event with full PDPO compliance
receipt = tracker.log_data_collection(
    purpose="credit_scoring",
    data_categories=["name", "income", "credit_history"],
    consent_id="CONSENT-2026-001",
    consent_obtained=True,
    collection_method="online_form",
    data_subject="customer-123",
    retention_period=2555,  # 7 years
    metadata={
        "notice_provided": True,
        "notice_url": "https://hsbc.com.hk/privacy",
        "language_preference": "en"
    }
)

print(f"Receipt ID: {receipt['receipt_id']}")
print(f"DPP1 Compliance: {receipt['dpp1_compliant']}")
print(f"Signature: {receipt['signature'][:30]}...")
```

## 📊 DPP1: Purpose & Manner of Collection

### Requirements

| Requirement | JEP Implementation |
|------------|-------------------|
| Data must be collected for a lawful purpose | `purpose` field with predefined purposes |
| Collection must be necessary and fair | `collection_method` + `necessity_check` |
| Data subject must be informed | `notice_provided` + `notice_url` |
| Consent must be obtained (if required) | `consent_id` + `consent_obtained` |

### Code Example

```python
# Proper data collection with DPP1 compliance
receipt = tracker.log_data_collection(
    purpose="mortgage_application",
    data_categories=["income", "assets", "liabilities"],
    collection_method="in_person",
    notice_provided=True,
    notice_url="https://hsbc.com.hk/privacy/mortgage",
    consent_id="CONSENT-MTG-001",
    consent_obtained=True,
    consent_method="signed_form"
)

# The receipt serves as proof of DPP1 compliance
assert receipt["dpp1_compliant"] == True
assert receipt["consent_obtained"] == True
assert "notice_provided" in receipt["metadata"]
```

## 📊 DPP2: Accuracy & Duration

### Requirements

| Requirement | JEP Implementation |
|------------|-------------------|
| Data must be accurate | Data hashing + verification |
| Data must not be kept longer than necessary | `retention_days` + auto-expiry |
| Data should be deleted when purpose is met | Deletion receipts |

### Code Example

```python
# Data accuracy verification
receipt = tracker.log_data_update(
    data_subject="customer-123",
    field_updated="income",
    old_value_hash="abc123...",
    new_value_hash="def456...",
    verification_method="document_review",
    verified_by="officer-456"
)

# Data retention management
receipt = tracker.set_retention_policy(
    data_categories=["credit_history"],
    retention_days=2555,  # 7 years
    legal_basis="HKMA SA-2",
    auto_delete=True,
    deletion_notification=True
)
```

## 📊 DPP3: Use of Personal Data

### Requirements

| Requirement | JEP Implementation |
|------------|-------------------|
| Data can only be used for original purpose | `purpose_validation` on each use |
| New purposes require fresh consent | Consent versioning |
| Data sharing restrictions | `data_share_log` with purpose check |

### Code Example

```python
# Using data for original purpose
receipt = tracker.use_data(
    data_subject="customer-123",
    purpose="credit_scoring",  # Must match original
    use_case="loan_approval",
    purpose_validated=True
)

# Data sharing with third party
receipt = tracker.log_data_share(
    data_subject="customer-123",
    recipient="Credit Bureau Ltd",
    purpose="credit_checking",
    original_purpose="credit_scoring",
    consent_verified=True,
    sharing_agreement="CB-2026-001"
)
```

## 📊 DPP4: Data Security

### Requirements

| Requirement | JEP Implementation |
|------------|-------------------|
| Reasonable security measures | Ed25519 signatures + encryption |
| Access controls | RBAC + audit logs |
| Security incident response | Incident logging |

### Code Example

```python
# JEP provides cryptographic security by default
receipt = tracker.log_decision(
    operation="ACCESS_SENSITIVE_DATA",
    resource="customer-123",
    actor_id="officer-456",
    access_method="api",
    security_level="high",
    encryption_at_rest="AES-256",
    encryption_in_transit="TLS1.3"
)

# Security incident logging
receipt = tracker.log_security_incident(
    incident_type="unauthorized_access_attempt",
    severity="medium",
    detection_time=time.time(),
    affected_data=["customer-123"],
    response_actions=["blocked_ip", "alerted_admin"]
)
```

## 📊 DPP5: Transparency

### Requirements

| Requirement | JEP Implementation |
|------------|-------------------|
| Clear privacy policies | JSON-LD machine-readable policies |
| Information about data usage | Complete audit trail |
| PICS identifier | PCPD registration field |

### Code Example

```python
# Generate transparency report
report = tracker.generate_transparency_report(
    period_start="2026-01-01",
    period_end="2026-03-31",
    data_categories=["credit_data", "personal_info"],
    purposes=["credit_scoring", "anti_fraud"],
    data_sharing=["Credit Bureau", "HKMA"],
    retention_summary={
        "credit_data": "7 years",
        "personal_info": "2 years"
    }
)

# Machine-readable privacy policy
policy = tracker.generate_privacy_policy_jsonld(
    data_user="HSBC Hong Kong",
    pcpd_registration="R123456",
    purposes=["credit_scoring", "mortgage_approval"],
    data_categories=["name", "income", "credit_history"],
    retention_periods={"default": 2555},
    sharing_countries=["HK", "CN"],
    contact_email="privacy@hsbc.com.hk"
)
```

## 📊 DPP6: Access & Correction

### Requirements

| Requirement | JEP Implementation |
|------------|-------------------|
| Data access rights | Complete audit trail |
| Correction rights | Data lineage + versioning |
| Response within statutory period | SLA tracking |

### Code Example

```python
# Handle data access request
receipt = tracker.handle_access_request(
    requestor="customer-123",
    request_id="DSAR-2026-001",
    received_date=time.time(),
    response_deadline=time.time() + (40 * 86400),  # 40 days
    data_categories=["all"],
    response_format="json"
)

# Data correction
receipt = tracker.handle_correction_request(
    requestor="customer-123",
    correction_id="CORR-2026-001",
    field_corrected="income",
    old_value_hash="abc123...",
    new_value_hash="def456...",
    verification_method="payslip_review",
    approved_by="compliance-officer"
)
```

## 🔍 Verification

```bash
# Verify all 6 PDPO principles
python tests/verify-pdpo.py

# Output:
# ================================
# PDPO COMPLIANCE VERIFICATION
# ================================
# ✅ DPP1: Purpose & Manner of Collection
# ✅ DPP2: Accuracy & Duration
# ✅ DPP3: Use of Personal Data
# ✅ DPP4: Data Security
# ✅ DPP5: Transparency
# ✅ DPP6: Access & Correction
# ================================
# ALL PRINCIPLES COMPLIANT
# ================================
```

## 📁 Directory Contents

| File | Description |
|------|-------------|
| [README.md](README.md) | This file |
| [mapping.md](mapping.md) | Detailed mapping to all 6 PDPO principles |
| [implementation/pdpo_tracker.py](implementation/pdpo_tracker.py) | Core PDPO implementation |
| [examples/consent_management.py](examples/consent_management.py) | Consent lifecycle examples |
| [examples/data_access_request.py](examples/data_access_request.py) | DSAR handling examples |

## 📬 Contact

For PDPO-specific inquiries:
- **Email**: pdpo@humanjudgment.org
- **GitHub**: [hjs-spec/jep-hk-solutions](https://github.com/hjs-spec/jep-hk-solutions)

---

*Last Updated: March 2026*
```
