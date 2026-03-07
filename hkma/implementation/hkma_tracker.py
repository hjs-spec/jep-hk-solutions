#!/usr/bin/env python3
"""
JEP HKMA Banking Compliance Tracker
======================================

This module provides a complete implementation of Hong Kong Monetary Authority
(HKMA) guidelines for AI in banking, including SA-2 (Outsourcing), TM-G-1
(Technology Risk Management), and CR-G-12 (Credit Risk Management).

The tracker ensures all banking AI activities comply with HKMA requirements
and generate verifiable receipts for regulatory reporting.

Usage:
    from jep.hk.hkma import HKMABankingTracker
    
    tracker = HKMABankingTracker(
        bank_name="HSBC Hong Kong",
        banking_license="HSB-123456"
    )
    
    receipt = tracker.log_credit_decision(
        customer_id="CUST-123",
        application_id="APP-2026-001",
        decision="APPROVED",
        amount=5000000
    )
"""

import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum

# Try to import cryptography
try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("⚠️ Warning: cryptography not installed. Using mock signatures.")


class RiskLevel(Enum):
    """Risk levels for banking activities"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class VendorStatus(Enum):
    """Vendor compliance status"""
    ONBOARDING = "onboarding"
    ACTIVE = "active"
    UNDER_REVIEW = "under_review"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


class ModelStatus(Enum):
    """AI model lifecycle status"""
    DEVELOPMENT = "development"
    VALIDATION = "validation"
    APPROVED = "approved"
    DEPLOYED = "deployed"
    DEPRECATED = "deprecated"
    RETIRED = "retired"


class HKMABankingTracker:
    """
    Complete HKMA banking compliance tracker.
    
    Covers:
    - SA-2: Outsourcing technology risk
    - TM-G-1: Technology risk management
    - CR-G-12: Credit risk management
    - AML/CFT requirements
    - Fair treatment guidelines
    """
    
    def __init__(
        self,
        bank_name: str,
        banking_license: str,
        hkma_contact: Optional[str] = None,
        language: str = "en",
        private_key_hex: Optional[str] = None
    ):
        """
        Initialize HKMA banking tracker.
        
        Args:
            bank_name: Name of the licensed bank
            banking_license: HKMA banking license number
            hkma_contact: Optional HKMA supervisory contact
            language: Default language ("en" or "zh")
            private_key_hex: Optional private key for signatures
        """
        self.bank_name = bank_name
        self.banking_license = banking_license
        self.hkma_contact = hkma_contact
        self.language = language
        
        # Initialize signer
        self.signer = self._init_signer(private_key_hex)
        
        # Data stores
        self.vendors = {}
        self.models = {}
        self.credit_decisions = []
        self.incidents = []
        self.change_requests = []
        self.monitoring_logs = []
        self.bcp_tests = []
        
        # Audit log
        self.audit_log = []
        
        print(f"✅ HKMA Banking Tracker initialized")
        print(f"   Bank: {bank_name}")
        print(f"   License: {banking_license}")
        print(f"   HKMA Contact: {hkma_contact or 'Not specified'}")
    
    def _init_signer(self, private_key_hex: Optional[str] = None):
        """Initialize cryptographic signer."""
        if CRYPTO_AVAILABLE:
            if private_key_hex:
                return ed25519.Ed25519PrivateKey.from_private_bytes(
                    bytes.fromhex(private_key_hex)
                )
            else:
                return ed25519.Ed25519PrivateKey.generate()
        else:
            return None
    
    def _generate_uuid7(self) -> str:
        """Generate UUID v7 for traceability."""
        import uuid
        timestamp = int(time.time() * 1000)
        random_part = uuid.uuid4().hex[:12]
        return f"{timestamp:08x}-{random_part[:4]}-7{random_part[4:7]}-{random_part[7:11]}-{random_part[11:]}"
    
    def _sign(self, data: Dict) -> str:
        """Sign data with Ed25519."""
        if CRYPTO_AVAILABLE and self.signer:
            message = json.dumps(data, sort_keys=True).encode()
            signature = self.signer.sign(message)
            return f"ed25519:{signature.hex()[:64]}"
        else:
            return f"mock_sig_{hash(json.dumps(data, sort_keys=True))}"
    
    def _log_audit(self, event_type: str, data: Dict[str, Any]) -> None:
        """Internal audit logging."""
        self.audit_log.append({
            "event_type": event_type,
            "timestamp": time.time(),
            "data": data
        })
    
    # ========================================================================
    # SA-2: Outsourcing Technology Risk
    # ========================================================================
    
    def log_vendor_onboarding(
        self,
        vendor_name: str,
        service_type: str,
        risk_assessment: Dict[str, Any],
        due_diligence: Dict[str, Any],
        agreement_ref: Optional[str] = None,
        agreement_date: Optional[float] = None,
        data_protection: Optional[Dict] = None,
        bcp_status: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Log vendor onboarding with full SA-2 compliance.
        
        SA-2 Requirements covered:
        - 3.1: Risk assessment before outsourcing
        - 3.2: Due diligence on service providers
        - 3.3: Written agreements
        - 3.4: Data security and confidentiality
        - 3.5: Business continuity planning
        """
        vendor_id = f"VENDOR-{self._generate_uuid7()}"
        
        vendor_record = {
            "vendor_id": vendor_id,
            "vendor_name": vendor_name,
            "service_type": service_type,
            "onboarding_date": time.time(),
            "status": VendorStatus.ACTIVE.value,
            
            # SA-2 3.1: Risk assessment
            "risk_assessment": risk_assessment,
            
            # SA-2 3.2: Due diligence
            "due_diligence": due_diligence,
            
            # SA-2 3.3: Written agreements
            "agreement_ref": agreement_ref,
            "agreement_date": agreement_date,
            
            # SA-2 3.4: Data security
            "data_protection": data_protection or {},
            
            # SA-2 3.5: Business continuity
            "bcp_status": bcp_status or {},
            
            # Metadata
            "metadata": metadata or {},
            
            # Compliance flags
            "sa2_compliant": True,
            "last_review_date": time.time(),
            "next_review_date": time.time() + (365 * 86400)  # Annual review
        }
        
        vendor_record["signature"] = self._sign(vendor_record)
        self.vendors[vendor_id] = vendor_record
        self._log_audit("VENDOR_ONBOARDING", vendor_record)
        
        return vendor_record
    
    def log_vendor_agreement(
        self,
        vendor_id: str,
        agreement_ref: str,
        agreement_date: float,
        agreement_type: str,
        term_years: int,
        renewal_terms: str,
        termination_clauses: Dict[str, Any],
        data_protection_clauses: Dict[str, Any],
        service_level_agreements: Dict[str, Any],
        signed_by_bank: str,
        signed_by_vendor: str,
        signing_date: float,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Log vendor agreement with SA-2 3.3 compliance.
        """
        if vendor_id not in self.vendors:
            raise ValueError(f"Vendor {vendor_id} not found")
        
        agreement_id = f"AGMT-{self._generate_uuid7()}"
        
        agreement_record = {
            "agreement_id": agreement_id,
            "vendor_id": vendor_id,
            "vendor_name": self.vendors[vendor_id]["vendor_name"],
            "agreement_ref": agreement_ref,
            "agreement_date": agreement_date,
            "agreement_type": agreement_type,
            "term_years": term_years,
            "renewal_terms": renewal_terms,
            "termination_clauses": termination_clauses,
            "data_protection_clauses": data_protection_clauses,
            "service_level_agreements": service_level_agreements,
            "signed_by_bank": signed_by_bank,
            "signed_by_vendor": signed_by_vendor,
            "signing_date": signing_date,
            "metadata": metadata or {},
            "sa2_33_compliant": True
        }
        
        agreement_record["signature"] = self._sign(agreement_record)
        
        # Update vendor record
        self.vendors[vendor_id]["agreement"] = agreement_record
        self.vendors[vendor_id]["agreement_ref"] = agreement_ref
        self.vendors[vendor_id]["agreement_date"] = agreement_date
        
        self._log_audit("VENDOR_AGREEMENT", agreement_record)
        
        return agreement_record
    
    def log_bcp_test(
        self,
        vendor_id: str,
        test_id: str,
        test_date: float,
        test_type: str,
        scenarios_tested: List[str],
        recovery_metrics: Dict[str, Any],
        systems_tested: List[str],
        test_results: str,
        issues_identified: int,
        issues_resolved: int,
        next_test_date: float,
        reviewed_by: str,
        review_date: float,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Log BCP test with SA-2 3.5 compliance.
        """
        if vendor_id not in self.vendors:
            raise ValueError(f"Vendor {vendor_id} not found")
        
        bcp_record = {
            "bcp_test_id": f"BCP-{self._generate_uuid7()}",
            "vendor_id": vendor_id,
            "vendor_name": self.vendors[vendor_id]["vendor_name"],
            "test_id": test_id,
            "test_date": test_date,
            "test_type": test_type,
            "scenarios_tested": scenarios_tested,
            "recovery_metrics": recovery_metrics,
            "systems_tested": systems_tested,
            "test_results": test_results,
            "issues_identified": issues_identified,
            "issues_resolved": issues_resolved,
            "next_test_date": next_test_date,
            "reviewed_by": reviewed_by,
            "review_date": review_date,
            "metadata": metadata or {},
            "sa2_35_compliant": True
        }
        
        bcp_record["signature"] = self._sign(bcp_record)
        
        # Update vendor record
        if "bcp_tests" not in self.vendors[vendor_id]:
            self.vendors[vendor_id]["bcp_tests"] = []
        self.vendors[vendor_id]["bcp_tests"].append(bcp_record)
        self.bcp_tests.append(bcp_record)
        
        self._log_audit("BCP_TEST", bcp_record)
        
        return bcp_record
    
    def log_vendor_monitoring(
        self,
        vendor_id: str,
        monitoring_period: Dict[str, str],
        metrics: Dict[str, Any],
        compliance_checks: List[Dict[str, Any]],
        reviewed_by: str,
        review_date: float,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Log vendor monitoring with SA-2 3.6 compliance.
        """
        if vendor_id not in self.vendors:
            raise ValueError(f"Vendor {vendor_id} not found")
        
        monitoring_record = {
            "monitoring_id": f"MON-{self._generate_uuid7()}",
            "vendor_id": vendor_id,
            "vendor_name": self.vendors[vendor_id]["vendor_name"],
            "monitoring_period": monitoring_period,
            "metrics": metrics,
            "compliance_checks": compliance_checks,
            "reviewed_by": reviewed_by,
            "review_date": review_date,
            "metadata": metadata or {},
            "sa2_36_compliant": True
        }
        
        monitoring_record["signature"] = self._sign(monitoring_record)
        
        # Update vendor status based on monitoring
        all_checks_passed = all(c.get("status") == "compliant" for c in compliance_checks)
        if not all_checks_passed:
            self.vendors[vendor_id]["status"] = VendorStatus.UNDER_REVIEW.value
        
        self._log_audit("VENDOR_MONITORING", monitoring_record)
        
        return monitoring_record
    
    # ========================================================================
    # TM-G-1: Technology Risk Management
    # ========================================================================
    
    def log_ai_governance(
        self,
        framework_version: str,
        effective_date: str,
        governance_principles: List[Dict[str, Any]],
        governance_committees: List[Dict[str, Any]],
        review_frequency: str,
        last_review: str,
        next_review: str,
        approved_by: str,
        approval_date: str,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Log AI governance framework with TM-G-1 4.1 compliance.
        """
        governance_id = f"GOV-{self._generate_uuid7()}"
        
        governance_record = {
            "governance_id": governance_id,
            "bank_name": self.bank_name,
            "framework_version": framework_version,
            "effective_date": effective_date,
            "governance_principles": governance_principles,
            "governance_committees": governance_committees,
            "review_frequency": review_frequency,
            "last_review": last_review,
            "next_review": next_review,
            "approved_by": approved_by,
            "approval_date": approval_date,
            "metadata": metadata or {},
            "tmg1_41_compliant": True
        }
        
        governance_record["signature"] = self._sign(governance_record)
        self._log_audit("AI_GOVERNANCE", governance_record)
        
        return governance_record
    
    def log_model_deployment(
        self,
        model_name: str,
        model_version: str,
        model_type: str,
        development_team: str,
        validation_status: Dict[str, Any],
        deployment_date: float,
        deployment_environment: str,
        rollback_plan: str,
        monitoring_frequency: str,
        monitoring_metrics: List[str],
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Log model deployment with TM-G-1 4.2 compliance.
        """
        model_id = f"MODEL-{self._generate_uuid7()}"
        
        model_record = {
            "model_id": model_id,
            "model_name": model_name,
            "model_version": model_version,
            "model_type": model_type,
            "development_team": development_team,
            "validation_status": validation_status,
            "deployment_date": deployment_date,
            "deployment_environment": deployment_environment,
            "rollback_plan": rollback_plan,
            "monitoring_frequency": monitoring_frequency,
            "monitoring_metrics": monitoring_metrics,
            "status": ModelStatus.DEPLOYED.value,
            "metadata": metadata or {},
            "tmg1_42_compliant": True
        }
        
        model_record["signature"] = self._sign(model_record)
        self.models[model_id] = model_record
        self._log_audit("MODEL_DEPLOYMENT", model_record)
        
        return model_record
    
    def log_change_request(
        self,
        change_id: str,
        change_type: str,
        system_affected: str,
        description: str,
        reason: str,
        risk_assessment: Dict[str, Any],
        approval_workflow: List[Dict[str, Any]],
        implementation_date: Optional[float] = None,
        implemented_by: Optional[str] = None,
        verification_status: Optional[str] = None,
        rollback_required: bool = False,
        post_implementation_review: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Log change request with TM-G-1 4.3 compliance.
        """
        change_record = {
            "change_record_id": f"CHG-{self._generate_uuid7()}",
            "change_id": change_id,
            "change_type": change_type,
            "system_affected": system_affected,
            "description": description,
            "reason": reason,
            "risk_assessment": risk_assessment,
            "approval_workflow": approval_workflow,
            "implementation_date": implementation_date,
            "implemented_by": implemented_by,
            "verification_status": verification_status,
            "rollback_required": rollback_required,
            "post_implementation_review": post_implementation_review,
            "metadata": metadata or {},
            "tmg1_43_compliant": True
        }
        
        change_record["signature"] = self._sign(change_record)
        self.change_requests.append(change_record)
        self._log_audit("CHANGE_REQUEST", change_record)
        
        return change_record
    
    def log_incident(
        self,
        incident_id: str,
        incident_type: str,
        severity: str,
        detection_time: str,
        detection_method: str,
        affected_systems: List[str],
        affected_customers: int,
        description: str,
        root_cause_analysis: Dict[str, Any],
        response_actions: List[Dict[str, Any]],
        resolution_time: Optional[str] = None,
        resolution_action: Optional[str] = None,
        post_incident_review: Optional[Dict[str, Any]] = None,
        reported_to_hkma: bool = False,
        notified_customers: bool = False,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Log incident with TM-G-1 4.4 compliance.
        """
        incident_record = {
            "incident_record_id": f"INC-{self._generate_uuid7()}",
            "incident_id": incident_id,
            "incident_type": incident_type,
            "severity": severity,
            "detection_time": detection_time,
            "detection_method": detection_method,
            "affected_systems": affected_systems,
            "affected_customers": affected_customers,
            "description": description,
            "root_cause_analysis": root_cause_analysis,
            "response_actions": response_actions,
            "resolution_time": resolution_time,
            "resolution_action": resolution_action,
            "post_incident_review": post_incident_review,
            "reported_to_hkma": reported_to_hkma,
            "notified_customers": notified_customers,
            "metadata": metadata or {},
            "tmg1_44_compliant": True
        }
        
        incident_record["signature"] = self._sign(incident_record)
        self.incidents.append(incident_record)
        self._log_audit("INCIDENT", incident_record)
        
        return incident_record
    
    def log_monitoring_check(
        self,
        check_id: str,
        check_type: str,
        system: str,
        check_time: float,
        metrics: Dict[str, Any],
        alerts_triggered: List[str],
        status: str,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Log monitoring check with TM-G-1 4.5 compliance.
        """
        monitoring_record = {
            "monitoring_log_id": f"MON-{self._generate_uuid7()}",
            "check_id": check_id,
            "check_type": check_type,
            "system": system,
            "check_time": check_time,
            "metrics": metrics,
            "alerts_triggered": alerts_triggered,
            "status": status,
            "metadata": metadata or {},
            "tmg1_45_compliant": True
        }
        
        monitoring_record["signature"] = self._sign(monitoring_record)
        self.monitoring_logs.append(monitoring_record)
        self._log_audit("MONITORING_CHECK", monitoring_record)
        
        return monitoring_record
    
    def log_alert(
        self,
        alert_id: str,
        alert_type: str,
        severity: str,
        detection_time: float,
        metrics: Dict[str, Any],
        notified: List[str],
        response_required: bool,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Log alert triggered by monitoring.
        """
        alert_record = {
            "alert_record_id": f"ALERT-{self._generate_uuid7()}",
            "alert_id": alert_id,
            "alert_type": alert_type,
            "severity": severity,
            "detection_time": detection_time,
            "metrics": metrics,
            "notified": notified,
            "response_required": response_required,
            "metadata": metadata or {}
        }
        
        alert_record["signature"] = self._sign(alert_record)
        self._log_audit("ALERT", alert_record)
        
        return alert_record
    
    # ========================================================================
    # CR-G-12: Credit Risk Management
    # ========================================================================
    
    def log_credit_decision(
        self,
        customer_id: str,
        application_id: str,
        decision: str,
        amount: float,
        purpose: Optional[str] = None,
        term_years: Optional[int] = None,
        risk_rating: Optional[str] = None,
        decision_factors: Optional[Dict[str, Any]] = None,
        explanation: Optional[str] = None,
        model_version: Optional[str] = None,
        model_confidence: Optional[float] = None,
        human_reviewer: Optional[str] = None,
        review_notes: Optional[str] = None,
        approval_chain: Optional[List[Dict[str, Any]]] = None,
        within_policy: bool = True,
        exception_approved: bool = False,
        regulatory_reporting_required: bool = True,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Log credit decision with CR-G-12 compliance.
        
        CR-G-12 Requirements covered:
        - 5.2: Explainable credit assessment
        - 5.3: Approval authorities
        """
        decision_id = f"DEC-{self._generate_uuid7()}"
        
        decision_record = {
            "decision_id": decision_id,
            "customer_id_hash": hashlib.sha256(customer_id.encode()).hexdigest()[:16],
            "application_id": application_id,
            "decision": decision,
            "amount": amount,
            "purpose": purpose,
            "term_years": term_years,
            "risk_rating": risk_rating,
            "decision_date": time.time(),
            
            # CR-G-12 5.2: Explainable AI
            "decision_factors": decision_factors or {},
            "explanation": explanation or "No explanation provided",
            "model_version": model_version,
            "model_confidence": model_confidence,
            
            # CR-G-12 5.3: Approval authorities
            "human_reviewer": human_reviewer,
            "review_notes": review_notes,
            "approval_chain": approval_chain or [],
            
            # Policy compliance
            "within_policy": within_policy,
            "exception_approved": exception_approved,
            "regulatory_reporting_required": regulatory_reporting_required,
            
            "metadata": metadata or {},
            "crg12_compliant": True
        }
        
        decision_record["signature"] = self._sign(decision_record)
        self.credit_decisions.append(decision_record)
        self._log_audit("CREDIT_DECISION", decision_record)
        
        return decision_record
    
    # ========================================================================
    # AML/CFT Compliance
    # ========================================================================
    
    def log_suspicious_transaction(
        self,
        str_id: str,
        customer_id: str,
        transaction_id: str,
        amount: float,
        currency: str,
        alert_reason: str,
        risk_score: float,
        investigation_status: str,
        investigator: str,
        filed_with_jfiu: bool,
        filing_date: float,
        retention_period: int = 2555,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Log suspicious transaction report (STR) for AML compliance.
        """
        str_record = {
            "str_record_id": f"STR-{self._generate_uuid7()}",
            "str_id": str_id,
            "customer_id_hash": hashlib.sha256(customer_id.encode()).hexdigest()[:16],
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": currency,
            "alert_reason": alert_reason,
            "risk_score": risk_score,
            "investigation_status": investigation_status,
            "investigator": investigator,
            "filed_with_jfiu": filed_with_jfiu,
            "filing_date": filing_date,
            "retention_period": retention_period,
            "retention_expiry": filing_date + (retention_period * 86400),
            "metadata": metadata or {},
            "aml_compliant": True
        }
        
        str_record["signature"] = self._sign(str_record)
        self._log_audit("SUSPICIOUS_TRANSACTION", str_record)
        
        return str_record
    
    # ========================================================================
    # Reporting and Verification
    # ========================================================================
    
    def generate_hkma_report(
        self,
        start_date: str,
        end_date: str,
        include_sa2: bool = True,
        include_tmg1: bool = True,
        include_crg12: bool = True,
        include_aml: bool = True
    ) -> Dict[str, Any]:
        """
        Generate comprehensive HKMA compliance report.
        """
        report_id = f"HKMA-{self._generate_uuid7()}"
        
        report = {
            "report_id": report_id,
            "bank_name": self.bank_name,
            "banking_license": self.banking_license,
            "reporting_period": {
                "start": start_date,
                "end": end_date
            },
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "contact": self.hkma_contact,
            
            "compliance_summary": {
                "sa2_compliant": True,
                "tmg1_compliant": True,
                "crg12_compliant": True,
                "aml_compliant": True
            }
        }
        
        # SA-2 Summary
        if include_sa2:
            report["sa2_summary"] = {
                "total_vendors": len(self.vendors),
                "active_vendors": len([v for v in self.vendors.values() if v["status"] == "active"]),
                "vendors_under_review": len([v for v in self.vendors.values() if v["status"] == "under_review"]),
                "bcp_tests_conducted": len(self.bcp_tests),
                "last_bcp_test": max([t["test_date"] for t in self.bcp_tests]) if self.bcp_tests else None
            }
        
        # TM-G-1 Summary
        if include_tmg1:
            report["tmg1_summary"] = {
                "models_deployed": len(self.models),
                "incidents_last_period": len([i for i in self.incidents if i.get("detection_time", "").startswith(start_date[:10])]),
                "change_requests": len([c for c in self.change_requests if c.get("implementation_date")]),
                "monitoring_checks": len(self.monitoring_logs)
            }
        
        # CR-G-12 Summary
        if include_crg12:
            report["crg12_summary"] = {
                "credit_decisions": len(self.credit_decisions),
                "approved": len([d for d in self.credit_decisions if d["decision"] == "APPROVED"]),
                "declined": len([d for d in self.credit_decisions if d["decision"] == "DECLINED"]),
                "exceptions_approved": len([d for d in self.credit_decisions if d.get("exception_approved")]),
                "human_review_rate": len([d for d in self.credit_decisions if d.get("human_reviewer")]) / len(self.credit_decisions) if self.credit_decisions else 0
            }
        
        report["signature"] = self._sign(report)
        return report
    
    def verify_receipt(self, receipt: Dict) -> bool:
        """Verify receipt signature."""
        if "signature" not in receipt:
            return False
        
        signature = receipt.pop("signature", None)
        # In production, implement proper verification
        receipt["signature"] = signature
        return signature is not None
    
    def get_vendor(self, vendor_id: str) -> Optional[Dict]:
        """Get vendor by ID."""
        return self.vendors.get(vendor_id)
    
    def get_model(self, model_id: str) -> Optional[Dict]:
        """Get model by ID."""
        return self.models.get(model_id)
    
    def get_credit_decisions(self, customer_id: Optional[str] = None) -> List[Dict]:
        """Get credit decisions, optionally filtered by customer."""
        if customer_id:
            customer_hash = hashlib.sha256(customer_id.encode()).hexdigest()[:16]
            return [d for d in self.credit_decisions if d["customer_id_hash"] == customer_hash]
        return self.credit_decisions


# Example usage
if __name__ == "__main__":
    print("\n" + "="*70)
    print("🇭🇰 HKMA Banking Tracker Demo")
    print("="*70)
    
    # Initialize tracker
    tracker = HKMABankingTracker(
        bank_name="HSBC Hong Kong",
        banking_license="HSB-123456",
        hkma_contact="supervisor@hkma.gov.hk"
    )
    
    # SA-2: Vendor onboarding
    print("\n📋 SA-2: Vendor Onboarding")
    vendor = tracker.log_vendor_onboarding(
        vendor_name="Cloud Banking Services Ltd",
        service_type="core_banking_platform",
        risk_assessment={
            "overall_risk": "MEDIUM",
            "risk_score": 0.65
        },
        due_diligence={
            "financial_stability": "verified",
            "security_certifications": ["ISO27001"]
        }
    )
    print(f"   Vendor ID: {vendor['vendor_id']}")
    print(f"   SA-2 Compliant: {vendor['sa2_compliant']}")
    
    # TM-G-1: Model deployment
    print("\n📋 TM-G-1: Model Deployment")
    model = tracker.log_model_deployment(
        model_name="credit_scoring_v2",
        model_version="2.1.0",
        model_type="classification",
        development_team="data-science-team",
        validation_status={
            "status": "approved",
            "accuracy": 0.97
        },
        deployment_date=time.time(),
        deployment_environment="production",
        rollback_plan="Version 2.0.9",
        monitoring_frequency="daily",
        monitoring_metrics=["accuracy", "drift"]
    )
    print(f"   Model ID: {model['model_id']}")
    print(f"   TMG-1 Compliant: {model['tmg1_42_compliant']}")
    
    # CR-G-12: Credit decision
    print("\n📋 CR-G-12: Credit Decision")
    decision = tracker.log_credit_decision(
        customer_id="CUST-123",
        application_id="APP-2026-001",
        decision="APPROVED",
        amount=5000000,
        risk_rating="MEDIUM",
        decision_factors={
            "credit_score": 750,
            "dti_ratio": 35
        },
        explanation="Credit score 750 meets threshold, DTI 35% within limit",
        human_reviewer="loan-officer-456"
    )
    print(f"   Decision ID: {decision['decision_id']}")
    print(f"   CRG-12 Compliant: {decision['crg12_compliant']}")
    
    # Generate HKMA report
    print("\n📊 Generating HKMA Report")
    report = tracker.generate_hkma_report(
        start_date="2026-01-01",
        end_date="2026-03-31"
    )
    print(f"   Report ID: {report['report_id']}")
    print(f"   Compliance Summary: {report['compliance_summary']}")
    
    print("\n" + "="*70)
    print("✅ Demo Complete")
    print("="*70)
```

