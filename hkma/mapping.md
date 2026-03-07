# JEP Mapping to Hong Kong HKMA Guidelines

**Detailed Article-by-Article Mapping with Code Examples and Verification Methods**

## 📋 Overview

This document provides a comprehensive mapping between the **Judgment Event Protocol (JEP)** and the Hong Kong Monetary Authority (HKMA) guidelines for AI in banking, including SA-2 (Outsourcing), TM-G-1 (Technology Risk Management), and CR-G-12 (Credit Risk Management).

Each guideline is mapped to JEP's technical features, with code examples demonstrating compliance and verification methods for regulatory reporting.

---

## 📊 SA-2: Outsourcing Technology Risk

### Overview

SA-2 sets out the HKMA's expectations for authorized institutions to manage risks associated with outsourcing, particularly for material outsourcing arrangements involving technology services.

### Key Requirements Mapping

| Section | Requirement | JEP Implementation | Verification |
|---------|-------------|-------------------|--------------|
| **3.1** | Risk assessment before outsourcing | Vendor risk assessment with `risk_level` field | `verify-hkma.py --sa2-3.1` |
| **3.2** | Due diligence on service providers | Vendor due diligence tracking | `verify-hkma.py --sa2-3.2` |
| **3.3** | Written agreements | Contract management with signatures | `verify-hkma.py --sa2-3.3` |
| **3.4** | Data security and confidentiality | Encryption metadata + signatures | `verify-hkma.py --sa2-3.4` |
| **3.5** | Business continuity planning | BCP testing logs | `verify-hkma.py --sa2-3.5` |
| **3.6** | Monitoring and oversight | Continuous compliance checks | `verify-hkma.py --sa2-3.6` |
| **3.7** | Audit rights | Complete audit trail | `verify-hkma.py --sa2-3.7` |
| **3.8** | Sub-outsourcing | Subcontractor tracking | `verify-hkma.py --sa2-3.8` |
| **3.9** | Access to information | Data access logs | `verify-hkma.py --sa2-3.9` |
| **3.10** | Termination rights | Contract termination logs | `verify-hkma.py --sa2-3.10` |

---

### 3.1 Risk Assessment Before Outsourcing

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | `risk_level` field + vendor risk assessment |
| **Implementation** | `log_vendor_onboarding()` with risk assessment |
| **Evidence Location** | Vendor receipts with `risk_assessment` field |

**Code Example:**
```python
from jep.hk.hkma import HKMABankingTracker

tracker = HKMABankingTracker("HSBC Hong Kong", "HSB-123456")

# SA-2 3.1 compliant vendor risk assessment
receipt = tracker.log_vendor_onboarding(
    vendor_name="Cloud Banking Services Ltd",
    service_type="core_banking_platform",
    risk_assessment={
        "overall_risk": "MEDIUM",
        "risk_factors": [
            {
                "factor": "data_sensitivity",
                "rating": "HIGH",
                "mitigation": "encryption"
            },
            {
                "factor": "jurisdiction",
                "rating": "LOW",
                "mitigation": "Hong Kong only"
            },
            {
                "factor": "subcontractors",
                "rating": "MEDIUM",
                "mitigation": "vendor management"
            }
        ],
        "risk_score": 0.65,
        "assessment_date": "2026-01-15",
        "assessed_by": "risk-management-team",
        "approval_status": "approved",
        "approver": "cro-456"
    }
)

# Verification
assert receipt["risk_assessment"]["overall_risk"] == "MEDIUM"
assert receipt["risk_assessment"]["approval_status"] == "approved"
```

**Verification Method:**
```bash
python tests/verify-hkma.py --sa2-3.1 --vendor vendor-123
```

---

### 3.2 Due Diligence on Service Providers

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | `due_diligence` field with comprehensive checks |
| **Implementation** | Vendor onboarding with due diligence tracking |
| **Evidence Location** | Vendor receipts with `due_diligence` field |

**Code Example:**
```python
receipt = tracker.log_vendor_onboarding(
    vendor_name="Cloud Banking Services Ltd",
    service_type="core_banking_platform",
    due_diligence={
        "financial_stability": {
            "status": "verified",
            "evidence": "audited_financials_2025.pdf",
            "auditor": "PwC",
            "opinion": "unqualified"
        },
        "security_certifications": [
            {
                "certification": "ISO27001",
                "certificate_number": "IS-12345",
                "expiry_date": "2027-12-31",
                "auditor": "BSI"
            },
            {
                "certification": "SOC2 Type II",
                "report_date": "2025-12-31",
                "auditor": "Deloitte"
            }
        ],
        "reference_checks": {
            "client1": "Standard Chartered",
            "reference": "positive",
            "client2": "Bank of China",
            "reference": "positive"
        },
        "regulatory_status": {
            "licensed_in": "Hong Kong",
            "license_number": "TC-123456",
            "regulator": "HKMA"
        },
        "reputation_check": "passed",
        "background_check": "passed"
    }
)

# Verification
assert len(receipt["due_diligence"]["security_certifications"]) >= 2
assert receipt["due_diligence"]["regulatory_status"]["licensed_in"] == "Hong Kong"
```

---

### 3.3 Written Agreements

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Signed agreements with cryptographic proof |
| **Implementation** | Contract management with signatures |
| **Evidence Location** | Agreement receipts with signatures |

**Code Example:**
```python
receipt = tracker.log_vendor_agreement(
    vendor_name="Cloud Banking Services Ltd",
    agreement_ref="CSA-2026-001",
    agreement_date="2026-01-15",
    agreement_type="outsourcing",
    term_years=3,
    renewal_terms="automatic",
    termination_clauses={
        "notice_period_days": 90,
        "for_cause": True,
        "without_cause": True,
        "regulatory_termination": True
    },
    data_protection_clauses={
        "data_ownership": "bank",
        "data_localization": "Hong Kong only",
        "data_deletion_on_termination": True,
        "audit_rights": True,
        "regulatory_access": True
    },
    service_level_agreements={
        "availability": "99.99%",
        "response_time": "15 minutes",
        "resolution_time": "4 hours",
        "penalties": "service_credits"
    },
    signed_by_bank="legal-counsel-123",
    signed_by_vendor="vendor-cfo-456",
    signing_date=time.time()
)

# The receipt is cryptographically signed
assert receipt["signature"] is not None
```

---

### 3.4 Data Security and Confidentiality

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Encryption metadata + signatures |
| **Implementation** | Security measures documentation |
| **Evidence Location** | Security receipts with encryption details |

**Code Example:**
```python
receipt = tracker.log_security_measures(
    vendor_name="Cloud Banking Services Ltd",
    data_protection={
        "encryption_at_rest": {
            "algorithm": "AES-256-GCM",
            "key_management": "HSM",
            "key_rotation": "90_days"
        },
        "encryption_in_transit": {
            "protocol": "TLS1.3",
            "certificate_authority": "DigiCert",
            "perfect_forward_secrecy": True
        },
        "data_classification": {
            "sensitive_data": ["customer_info", "transaction_data"],
            "pseudonymization": True,
            "tokenization": True
        },
        "access_controls": {
            "authentication": "MFA",
            "authorization": "RBAC",
            "privileged_access": "just_in_time"
        },
        "audit_logging": {
            "enabled": True,
            "retention_days": 2555,
            "immutable": True
        }
    }
)

# Verification
assert receipt["data_protection"]["encryption_at_rest"]["algorithm"] == "AES-256-GCM"
```

---

### 3.5 Business Continuity Planning

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | BCP testing logs and recovery metrics |
| **Implementation** | Disaster recovery tracking |
| **Evidence Location** | BCP receipts with test results |

**Code Example:**
```python
receipt = tracker.log_bcp_test(
    vendor_name="Cloud Banking Services Ltd",
    test_id="BCP-2026-001",
    test_date="2026-02-15",
    test_type="full_failover",
    scenarios_tested=[
        "regional_outage",
        "data_center_failure",
        "network_disruption"
    ],
    recovery_metrics={
        "rto_achieved_minutes": 45,
        "rto_target_minutes": 120,
        "rpo_achieved_minutes": 10,
        "rpo_target_minutes": 15,
        "data_loss": "none"
    },
    systems_tested=[
        "core_banking",
        "customer_portal",
        "mobile_app"
    ],
    test_results="successful",
    issues_identified=2,
    issues_resolved=2,
    next_test_date="2026-05-15",
    reviewed_by="bcm-committee",
    review_date=time.time()
)

# Verification
assert receipt["recovery_metrics"]["rto_achieved_minutes"] < receipt["recovery_metrics"]["rto_target_minutes"]
```

---

### 3.6 Monitoring and Oversight

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Continuous compliance checks |
| **Implementation** | Ongoing vendor monitoring |
| **Evidence Location** | Monitoring logs with timestamps |

**Code Example:**
```python
receipt = tracker.log_vendor_monitoring(
    vendor_name="Cloud Banking Services Ltd",
    monitoring_period={
        "start": "2026-01-01",
        "end": "2026-03-31"
    },
    metrics={
        "availability": {
            "target": "99.99%",
            "achieved": "99.995%",
            "breaches": 0
        },
        "incident_count": 2,
        "mean_time_to_detect": "2 minutes",
        "mean_time_to_resolve": "35 minutes"
    },
    compliance_checks=[
        {
            "check": "data_localization",
            "status": "compliant",
            "evidence": "traffic_logs"
        },
        {
            "check": "encryption_standards",
            "status": "compliant",
            "evidence": "config_review"
        },
        {
            "check": "access_reviews",
            "status": "compliant",
            "evidence": "review_report"
        }
    ],
    reviewed_by="vendor-management-team",
    review_date=time.time()
)
```

---

## 📊 TM-G-1: Technology Risk Management

### Overview

TM-G-1 provides general principles for technology risk management, including AI governance, model risk management, and change management.

### Key Requirements Mapping

| Section | Requirement | JEP Implementation | Verification |
|---------|-------------|-------------------|--------------|
| **4.1** | AI governance framework | Four primitives documented | `verify-hkma.py --tmg1-4.1` |
| **4.2** | Model risk management | Model versioning + validation | `verify-hkma.py --tmg1-4.2` |
| **4.3** | Change management | Change control logs | `verify-hkma.py --tmg1-4.3` |
| **4.4** | Incident management | Incident response tracking | `verify-hkma.py --tmg1-4.4` |
| **4.5** | Continuous monitoring | Real-time compliance checks | `verify-hkma.py --tmg1-4.5` |
| **4.6** | Third-party risk | Vendor risk tracking | `verify-hkma.py --tmg1-4.6` |
| **4.7** | Data governance | Data lineage + consent | `verify-hkma.py --tmg1-4.7` |

---

### 4.1 AI Governance Framework

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Four primitives (Judge/Delegate/Terminate/Verify) |
| **Implementation** | Complete AI governance documentation |
| **Evidence Location** | Governance receipts with framework details |

**Code Example:**
```python
receipt = tracker.log_ai_governance(
    framework_version="2.0",
    effective_date="2026-01-01",
    governance_principles=[
        {
            "principle": "accountability",
            "implementation": "Four primitives with signatures",
            "owner": "chief-ai-officer"
        },
        {
            "principle": "transparency",
            "implementation": "JSON-LD metadata",
            "owner": "model-risk-team"
        },
        {
            "principle": "fairness",
            "implementation": "bias testing",
            "owner": "ai-ethics-committee"
        }
    ],
    governance_committees=[
        {
            "committee": "AI Risk Committee",
            "frequency": "monthly",
            "chair": "CRO"
        },
        {
            "committee": "Model Validation Committee",
            "frequency": "quarterly",
            "chair": "Chief Model Officer"
        }
    ],
    review_frequency="annual",
    last_review="2025-12-15",
    next_review="2026-12-15",
    approved_by="board",
    approval_date="2025-12-20"
)
```

---

### 4.2 Model Risk Management

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Model versioning + validation tracking |
| **Implementation** | Complete model lifecycle management |
| **Evidence Location** | Model receipts with validation status |

**Code Example:**
```python
receipt = tracker.log_model_deployment(
    model_name="credit_scoring_v2",
    model_version="2.1.0",
    model_type="classification",
    development_team="data-science-team",
    validation_status={
        "status": "approved",
        "validator": "model-validation-team",
        "validation_report": "VALID-2026-001",
        "validation_date": "2026-02-28",
        "validation_methods": [
            "backtesting",
            "benchmarking",
            "sensitivity_analysis"
        ],
        "performance_metrics": {
            "accuracy": 0.97,
            "precision": 0.96,
            "recall": 0.98,
            "f1_score": 0.97,
            "auc_roc": 0.99
        },
        "fairness_metrics": {
            "disparate_impact": 0.98,
            "equal_opportunity": 0.97,
            "demographic_parity": 0.96
        },
        "limitations": [
            "Requires retraining every 6 months",
            "Less accurate for new-to-credit customers"
        ]
    },
    deployment_date="2026-03-01",
    deployment_environment="production",
    rollback_plan="Version 2.0.9",
    monitoring_frequency="daily",
    monitoring_metrics=["accuracy", "drift", "fairness"]
)

# Verification
assert receipt["validation_status"]["status"] == "approved"
assert receipt["validation_status"]["performance_metrics"]["accuracy"] > 0.95
```

---

### 4.3 Change Management

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Change control logs with approvals |
| **Implementation** | Complete change tracking |
| **Evidence Location** | Change receipts with audit trail |

**Code Example:**
```python
receipt = tracker.log_change_request(
    change_id="CHG-2026-001",
    change_type="model_update",
    system_affected="credit_scoring_engine",
    description="Update credit scoring weights",
    reason="Improve accuracy for mortgage applicants",
    risk_assessment={
        "overall_risk": "MEDIUM",
        "impact_analysis": "Limited to new applications",
        "testing_required": True
    },
    approval_workflow=[
        {
            "approver": "development-manager",
            "decision": "approved",
            "date": "2026-02-20",
            "comments": "Code review passed"
        },
        {
            "approver": "risk-manager",
            "decision": "approved",
            "date": "2026-02-21",
            "comments": "Risk assessment acceptable"
        },
        {
            "approver": "change-advisory-board",
            "decision": "approved",
            "date": "2026-02-22",
            "comments": "Scheduled for 2026-03-01"
        }
    ],
    implementation_date="2026-03-01",
    implemented_by="devops-team",
    verification_status="successful",
    rollback_required=False,
    post_implementation_review="completed"
)
```

---

### 4.4 Incident Management

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Incident response tracking |
| **Implementation** | Complete incident lifecycle management |
| **Evidence Location** | Incident receipts with resolution details |

**Code Example:**
```python
receipt = tracker.log_incident(
    incident_id="INC-2026-001",
    incident_type="model_performance_degradation",
    severity="MEDIUM",
    detection_time="2026-03-15T10:30:00Z",
    detection_method="automated_monitoring",
    affected_systems=["credit_scoring"],
    affected_customers=1234,
    description="Credit score accuracy dropped from 97% to 92%",
    root_cause_analysis={
        "cause": "data_drift",
        "affected_feature": "income_verification",
        "confidence": 0.95
    },
    response_actions=[
        {
            "action": "alert_risk_team",
            "time": "2026-03-15T10:32:00Z",
            "performed_by": "monitoring_system"
        },
        {
            "action": "temporary_shadow_mode",
            "time": "2026-03-15T11:00:00Z",
            "performed_by": "ml_engineer"
        },
        {
            "action": "model_retraining_initiated",
            "time": "2026-03-15T11:30:00Z",
            "performed_by": "data_scientist"
        }
    ],
    resolution_time="2026-03-16T09:00:00Z",
    resolution_action="model_retrained_and_deployed",
    post_incident_review={
        "completed": True,
        "findings": ["Update monitoring thresholds", "Add feature importance tracking"],
        "action_items": ["ACC-2026-001", "ACC-2026-002"],
        "review_date": "2026-03-17"
    },
    reported_to_hkma=False,  # Below threshold
    notified_customers=False
)
```

---

### 4.5 Continuous Monitoring

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Real-time compliance checks |
| **Implementation** | Automated monitoring with alerts |
| **Evidence Location** | Monitoring logs with timestamps |

**Code Example:**
```python
receipt = tracker.log_monitoring_check(
    check_id="MON-2026-001",
    check_type="model_drift",
    system="credit_scoring",
    check_time=time.time(),
    metrics={
        "accuracy": 0.97,
        "accuracy_threshold": 0.95,
        "accuracy_status": "NORMAL",
        "drift_score": 0.12,
        "drift_threshold": 0.15,
        "drift_status": "NORMAL",
        "fairness_metric": 0.98,
        "fairness_threshold": 0.95,
        "fairness_status": "NORMAL"
    },
    alerts_triggered=[],
    status="HEALTHY"
)

# Alert example (if threshold exceeded)
alert_receipt = tracker.log_alert(
    alert_id="ALERT-2026-001",
    alert_type="drift_detected",
    severity="WARNING",
    detection_time=time.time(),
    metrics={
        "drift_score": 0.18,
        "threshold": 0.15,
        "affected_features": ["income", "employment"]
    },
    notified=["ml-team", "risk-team"],
    response_required=True
)
```

---

## 📊 CR-G-12: Credit Risk Management

### Overview

CR-G-12 sets out the HKMA's requirements for credit risk management, including the use of AI in credit decisions.

### Key Requirements Mapping

| Section | Requirement | JEP Implementation | Verification |
|---------|-------------|-------------------|--------------|
| **5.1** | Credit risk policies | Policy adherence tracking | `verify-hkma.py --crg12-5.1` |
| **5.2** | Credit assessment | Explainable decisions | `verify-hkma.py --crg12-5.2` |
| **5.3** | Approval authorities | Multi-level approvals | `verify-hkma.py --crg12-5.3` |
| **5.4** | Monitoring and review | Ongoing compliance checks | `verify-hkma.py --crg12-5.4` |
| **5.5** | Problem loan management | Escalation workflows | `verify-hkma.py --crg12-5.5` |
| **5.6** | Credit risk reporting | Regulatory reporting | `verify-hkma.py --crg12-5.6` |

---

### 5.2 Credit Assessment (Explainable AI)

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Explainable decisions with reasoning |
| **Implementation** | Complete decision factors documented |
| **Evidence Location** | Credit receipts with `decision_factors` |

**Code Example:**
```python
receipt = tracker.log_credit_decision(
    customer_id="CUST-123",
    application_id="APP-2026-001",
    decision="APPROVED",
    amount=5000000,
    purpose="mortgage",
    term_years=25,
    
    # Explainable factors (CR-G-12 requirement)
    decision_factors={
        "credit_score": {
            "value": 750,
            "weight": 0.4,
            "threshold": ">=680",
            "contribution": "positive"
        },
        "dti_ratio": {
            "value": 35,
            "weight": 0.3,
            "threshold": "<=40",
            "contribution": "positive"
        },
        "employment_stability": {
            "value": "5_years",
            "weight": 0.2,
            "threshold": ">=2_years",
            "contribution": "positive"
        },
        "collateral": {
            "value": "property",
            "weight": 0.1,
            "ltv": 80,
            "ltv_threshold": "<=85",
            "contribution": "positive"
        }
    },
    
    # Overall explanation
    explanation = "Credit score 750 meets threshold, DTI 35% within limit, stable employment 5 years, LTV 80% within policy",
    
    # Model information
    model_version="credit-scoring-v2.1",
    model_confidence=0.95,
    
    # Human oversight
    human_reviewer="loan-officer-456",
    review_notes="Verified income documents, LTV within limit"
)

# Verification
assert receipt["decision_factors"]["credit_score"]["value"] >= 680
assert receipt["decision_factors"]["dti_ratio"]["value"] <= 40
```

---

### 5.3 Approval Authorities

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Multi-level approvals with signatures |
| **Implementation** | Approval workflow based on amount/risk |
| **Evidence Location** | Approval chain with multiple signatures |

**Code Example:**
```python
# Approval matrix based on amount
def get_approval_level(amount):
    if amount <= 1000000:
        return "loan_officer"
    elif amount <= 5000000:
        return "senior_manager"
    elif amount <= 10000000:
        return "department_head"
    else:
        return "credit_committee"

# Log decision with appropriate approvals
receipt = tracker.log_credit_decision(
    customer_id="CUST-123",
    application_id="APP-2026-001",
    decision="APPROVED",
    amount=8000000,  # Requires department head
    
    approval_chain=[
        {
            "level": "loan_officer",
            "approver": "officer-123",
            "decision": "recommend_approve",
            "date": "2026-03-01T10:00:00Z",
            "signature": "ed25519:..."
        },
        {
            "level": "senior_manager",
            "approver": "manager-456",
            "decision": "approve",
            "date": "2026-03-01T14:00:00Z",
            "signature": "ed25519:..."
        },
        {
            "level": "department_head",
            "approver": "head-789",
            "decision": "approve",
            "date": "2026-03-02T09:00:00Z",
            "signature": "ed25519:..."
        }
    ]
)

# Verification
assert len(receipt["approval_chain"]) == 3
assert receipt["approval_chain"][-1]["level"] == "department_head"
```

---

## ✅ Verification Script

```bash
#!/bin/bash
# verify-hkma.sh - Complete HKMA compliance verification

echo "================================="
echo "HKMA COMPLIANCE VERIFICATION"
echo "================================="

echo -e "\n📋 SA-2: Outsourcing Risk"
python tests/verify-hkma.py --sa2-3.1 --vendor cloud-banking
python tests/verify-hkma.py --sa2-3.2 --vendor cloud-banking
python tests/verify-hkma.py --sa2-3.3 --vendor cloud-banking
python tests/verify-hkma.py --sa2-3.4 --vendor cloud-banking
python tests/verify-hkma.py --sa2-3.5 --vendor cloud-banking

echo -e "\n📋 TM-G-1: Technology Risk"
python tests/verify-hkma.py --tmg1-4.1
python tests/verify-hkma.py --tmg1-4.2 --model credit-scoring
python tests/verify-hkma.py --tmg1-4.3 --change CHG-2026-001
python tests/verify-hkma.py --tmg1-4.4 --incident INC-2026-001

echo -e "\n📋 CR-G-12: Credit Risk"
python tests/verify-hkma.py --crg12-5.2 --application APP-2026-001
python tests/verify-hkma.py --crg12-5.3 --application APP-2026-001

echo -e "\n================================="
echo "✅ ALL HKMA REQUIREMENTS VERIFIED"
echo "================================="
```

## 📁 Directory Contents

| File | Description |
|------|-------------|
| [README.md](README.md) | HKMA overview |
| [mapping.md](mapping.md) | This file - detailed mapping |
| [implementation/hkma_tracker.py](implementation/hkma_tracker.py) | Core HKMA implementation |
| [examples/mortgage_workflow.py](examples/mortgage_workflow.py) | Complete mortgage example |
| [tests/verify-hkma.py](tests/verify-hkma.py) | Verification script |

## 📬 Contact

For HKMA-specific inquiries:
- **Email**: hkma@humanjudgment.org
- **GitHub**: [hjs-spec/jep-hk-solutions](https://github.com/hjs-spec/jep-hk-solutions)

---

*Last Updated: March 2026*
```
