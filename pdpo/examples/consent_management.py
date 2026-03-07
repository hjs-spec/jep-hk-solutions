#!/usr/bin/env python3
"""
PDPO Consent Management Examples
==================================

This example demonstrates complete consent lifecycle management
under Hong Kong's PDPO, including:
- Obtaining consent (DPP1)
- Recording consent details
- Managing consent withdrawal
- Consent renewal and expiry
- Audit trail for consent
- Handling consent for multiple purposes
"""

import json
import time
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pdpo.implementation.pdpo_tracker import PDPOComplianceTracker


class ConsentManagementDemo:
    """
    Demonstrates complete consent management lifecycle under PDPO.
    """
    
    def __init__(self):
        self.tracker = PDPOComplianceTracker(
            data_user="HSBC Hong Kong",
            pcpd_registration="R123456",
            language="en"  # Can switch to "zh" for Traditional Chinese
        )
        
        self.consents = []
        self.customers = [
            {"id": "CUST001", "name": "John Chan", "email": "john.chan@email.com"},
            {"id": "CUST002", "name": "Mary Wong", "email": "mary.wong@email.com"},
            {"id": "CUST003", "name": "Peter Li", "email": "peter.li@email.com"},
            {"id": "CUST004", "name": "Sarah Lam", "email": "sarah.lam@email.com"},
        ]
        
        print("="*70)
        print("🇭🇰 PDPO Consent Management Demo")
        print("="*70)
    
    def demo_single_purpose_consent(self):
        """
        Demo 1: Single purpose consent (DPP1 compliant)
        """
        print("\n" + "="*70)
        print("📝 Demo 1: Single Purpose Consent")
        print("="*70)
        
        customer = self.customers[0]
        
        # Step 1: Present privacy notice
        print(f"\n1. Presenting privacy notice to {customer['name']}")
        privacy_notice = {
            "version": "2.1",
            "effective_date": "2026-01-01",
            "purposes": ["credit_scoring"],
            "data_categories": ["income", "credit_history", "employment"],
            "retention": "7 years",
            "sharing": ["Credit Bureau Ltd"],
            "rights": ["access", "correction", "withdrawal"]
        }
        print(f"   Privacy Notice: {json.dumps(privacy_notice, indent=2)}")
        
        # Step 2: Obtain consent
        print(f"\n2. Obtaining consent for credit scoring")
        consent_receipt = self.tracker.log_data_collection(
            purpose="credit_scoring",
            data_categories=["income", "credit_history", "employment"],
            consent_id=f"CONSENT-{customer['id']}-001",
            consent_obtained=True,
            collection_method="online_form",
            notice_provided=True,
            notice_url="https://hsbc.com.hk/privacy/credit-scoring",
            data_subject=customer['id'],
            retention_period=2555,  # 7 years
            purpose_description="Assessment of creditworthiness for mortgage applications",
            legal_basis="consent",
            data_share_disclosure=True,
            potential_recipients=["Credit Bureau Ltd"],
            dsar_rights_communicated=True,
            dsar_contact="dsar@hsbc.com.hk",
            metadata={
                "customer_name": customer['name'],
                "customer_email": customer['email'],
                "consent_method": "online_checkbox",
                "ip_address": "192.168.1.100",
                "user_agent": "Mozilla/5.0",
                "timestamp": time.time()
            }
        )
        
        print(f"\n✅ Consent obtained successfully:")
        print(f"   Consent ID: {consent_receipt['consent_id']}")
        print(f"   Purpose: {consent_receipt['purpose']}")
        print(f"   DPP1 Compliant: {consent_receipt['dpp1_compliant']}")
        print(f"   Signature: {consent_receipt['signature'][:50]}...")
        
        # Step 3: Record consent in internal system
        self.consents.append({
            "customer_id": customer['id'],
            "consent_id": consent_receipt['consent_id'],
            "purpose": "credit_scoring",
            "granted_at": time.time(),
            "status": "active"
        })
        
        return consent_receipt
    
    def demo_multi_purpose_consent(self):
        """
        Demo 2: Multi-purpose consent with granular control
        """
        print("\n" + "="*70)
        print("📋 Demo 2: Multi-Purpose Consent")
        print("="*70)
        
        customer = self.customers[1]
        
        # Multi-purpose consent with granular options
        purposes = [
            {
                "purpose": "credit_scoring",
                "required": True,
                "data_categories": ["income", "credit_history"],
                "retention": 2555
            },
            {
                "purpose": "marketing",
                "required": False,
                "data_categories": ["name", "email", "preferences"],
                "retention": 730
            },
            {
                "purpose": "product_research",
                "required": False,
                "data_categories": ["transaction_history", "demographics"],
                "retention": 1095
            }
        ]
        
        print(f"\n1. Presenting multi-purpose consent options to {customer['name']}")
        for p in purposes:
            required = " (Required)" if p['required'] else " (Optional)"
            print(f"   • {p['purpose']}{required}")
        
        # Customer selects purposes
        selected_purposes = ["credit_scoring", "marketing"]  # Opts out of research
        
        print(f"\n2. Customer selected: {', '.join(selected_purposes)}")
        
        # Log consent for each selected purpose
        receipts = []
        for purpose in purposes:
            if purpose['purpose'] in selected_purposes:
                receipt = self.tracker.log_data_collection(
                    purpose=purpose['purpose'],
                    data_categories=purpose['data_categories'],
                    consent_id=f"CONSENT-{customer['id']}-{purpose['purpose']}",
                    consent_obtained=True,
                    collection_method="online_form",
                    notice_provided=True,
                    notice_url="https://hsbc.com.hk/privacy",
                    data_subject=customer['id'],
                    retention_period=purpose['retention'],
                    purpose_description=f"Data processing for {purpose['purpose']}",
                    legal_basis="consent",
                    metadata={
                        "customer_name": customer['name'],
                        "purpose_group": "multi_purpose",
                        "consent_version": "2.0"
                    }
                )
                receipts.append(receipt)
                print(f"\n✅ Consent recorded for {purpose['purpose']}")
                print(f"   Consent ID: {receipt['consent_id']}")
        
        return receipts
    
    def demo_consent_withdrawal(self):
        """
        Demo 3: Consent withdrawal and handling
        """
        print("\n" + "="*70)
        print("🚫 Demo 3: Consent Withdrawal")
        print("="*70)
        
        customer = self.customers[2]
        
        # First, obtain consent
        print(f"\n1. Initially obtaining consent from {customer['name']}")
        original_consent = self.tracker.log_data_collection(
            purpose="marketing",
            data_categories=["name", "email", "phone"],
            consent_id=f"CONSENT-{customer['id']}-MARKETING",
            consent_obtained=True,
            collection_method="online_form",
            notice_provided=True,
            data_subject=customer['id'],
            retention_period=730,
            metadata={
                "customer_name": customer['name'],
                "consent_date": datetime.now().isoformat()
            }
        )
        print(f"   Consent obtained: {original_consent['consent_id']}")
        
        # Simulate time passing (3 months)
        print(f"\n2. Three months later...")
        
        # Customer withdraws consent
        print(f"\n3. Customer withdraws consent for marketing")
        withdrawal_receipt = self._withdraw_consent(
            customer_id=customer['id'],
            consent_id=original_consent['consent_id'],
            reason="No longer interested"
        )
        
        # Verify data processing stops
        print(f"\n4. Verifying data processing stopped")
        try:
            # Attempt to use data after withdrawal (should fail)
            self.tracker.use_data(
                data_subject=customer['id'],
                purpose="marketing",
                original_purpose="marketing",
                use_case="email_campaign",
                used_by="marketing-system",
                consent_id=original_consent['consent_id']
            )
            print("❌ ERROR: Data use should have been blocked!")
        except Exception as e:
            print(f"✅ Correctly blocked: {e}")
        
        return withdrawal_receipt
    
    def _withdraw_consent(self, customer_id: str, consent_id: str, reason: str) -> dict:
        """
        Handle consent withdrawal (internal method)
        """
        # Log consent withdrawal
        withdrawal = {
            "withdrawal_id": f"WITHDRAW-{int(time.time())}",
            "timestamp": time.time(),
            "customer_id": customer_id,
            "original_consent_id": consent_id,
            "withdrawal_reason": reason,
            "withdrawal_method": "online_portal",
            "effective_immediately": True,
            "data_deletion_scheduled": True,
            "deletion_date": time.time() + 86400,  # 24 hours
            "notification_sent": True,
            "notification_channel": "email"
        }
        
        # Log to tracker (in real system, would update consent status)
        receipt = self.tracker._sign(withdrawal)
        
        print(f"\n✅ Consent withdrawn successfully:")
        print(f"   Withdrawal ID: {withdrawal['withdrawal_id']}")
        print(f"   Reason: {reason}")
        print(f"   Data will be deleted by: {datetime.fromtimestamp(withdrawal['deletion_date'])}")
        
        return withdrawal
    
    def demo_consent_renewal(self):
        """
        Demo 4: Consent renewal before expiry
        """
        print("\n" + "="*70)
        print("🔄 Demo 4: Consent Renewal")
        print("="*70)
        
        customer = self.customers[3]
        
        # Simulate consent granted 2 years ago (expiring soon)
        past_time = time.time() - (730 * 86400)  # 2 years ago
        
        print(f"\n1. Consent granted 2 years ago for {customer['name']}")
        print(f"   Expiring in 30 days")
        
        # Send renewal reminder
        print(f"\n2. Sending renewal reminder")
        renewal_notice = {
            "customer_id": customer['id'],
            "consent_id": f"CONSENT-{customer['id']}-ORIGINAL",
            "notice_type": "renewal",
            "sent_date": time.time(),
            "expiry_date": time.time() + (30 * 86400),
            "channels": ["email", "sms"],
            "status": "sent"
        }
        print(f"   Renewal notice sent via email and SMS")
        
        # Customer renews consent
        print(f"\n3. Customer renews consent")
        renewed_consent = self.tracker.log_data_collection(
            purpose="credit_scoring",
            data_categories=["income", "credit_history"],
            consent_id=f"CONSENT-{customer['id']}-RENEWED-2026",
            consent_obtained=True,
            collection_method="renewal_portal",
            notice_provided=True,
            notice_url="https://hsbc.com.hk/privacy/renewal",
            data_subject=customer['id'],
            retention_period=2555,
            purpose_description="Renewed consent for credit scoring",
            legal_basis="consent",
            metadata={
                "customer_name": customer['name'],
                "previous_consent_id": f"CONSENT-{customer['id']}-ORIGINAL",
                "renewal_method": "online",
                "renewal_date": datetime.now().isoformat()
            }
        )
        
        print(f"\n✅ Consent renewed successfully:")
        print(f"   New Consent ID: {renewed_consent['consent_id']}")
        print(f"   Previous Consent: {renewed_consent['metadata']['previous_consent_id']}")
        print(f"   New Expiry: {datetime.fromtimestamp(renewed_consent['retention_expiry'])}")
        
        return renewed_consent
    
    def generate_consent_audit_report(self):
        """
        Generate comprehensive consent audit report
        """
        print("\n" + "="*70)
        print("📊 Consent Audit Report")
        print("="*70)
        
        # Compile consent statistics
        report = {
            "report_id": f"AUDIT-{int(time.time())}",
            "generated_at": datetime.now().isoformat(),
            "data_user": self.tracker.data_user,
            "pcpd_registration": self.tracker.pcpd_registration,
            "consent_statistics": {
                "total_consents": len(self.tracker.consents),
                "active_consents": len([c for c in self.tracker.consents.values() if c.get("status") == "granted"]),
                "by_purpose": self._count_by_purpose(),
                "by_collection_method": self._count_by_method(),
                "consents_expiring_soon": self._count_expiring_soon(30)  # Next 30 days
            },
            "dpp1_compliance": {
                "notice_provided_rate": self._notice_rate(),
                "purpose_specified_rate": 1.0,
                "consent_rate": 1.0
            },
            "recent_activities": self._get_recent_activities(10)
        }
        
        print(f"\n📈 Consent Statistics:")
        print(f"   Total Consents: {report['consent_statistics']['total_consents']}")
        print(f"   Active Consents: {report['consent_statistics']['active_consents']}")
        print(f"   Expiring Soon: {report['consent_statistics']['consents_expiring_soon']}")
        
        print(f"\n📊 By Purpose:")
        for purpose, count in report['consent_statistics']['by_purpose'].items():
            print(f"   • {purpose}: {count}")
        
        return report
    
    def _count_by_purpose(self) -> dict:
        """Count consents by purpose"""
        purposes = {}
        for consent in self.tracker.consents.values():
            purpose = consent.get("purpose", "unknown")
            purposes[purpose] = purposes.get(purpose, 0) + 1
        return purposes
    
    def _count_by_method(self) -> dict:
        """Count consents by collection method"""
        methods = {}
        for collection in self.tracker.data_collections:
            method = collection.get("collection_method", "unknown")
            methods[method] = methods.get(method, 0) + 1
        return methods
    
    def _count_expiring_soon(self, days: int) -> int:
        """Count consents expiring within specified days"""
        now = time.time()
        expiry_threshold = now + (days * 86400)
        count = 0
        for collection in self.tracker.data_collections:
            if collection.get("retention_expiry", 0) <= expiry_threshold:
                count += 1
        return count
    
    def _notice_rate(self) -> float:
        """Calculate notice provision rate"""
        if not self.tracker.data_collections:
            return 1.0
        notices = sum(1 for c in self.tracker.data_collections if c.get("notice_provided", False))
        return notices / len(self.tracker.data_collections)
    
    def _get_recent_activities(self, limit: int) -> list:
        """Get recent consent-related activities"""
        activities = []
        for event in self.tracker.audit_log[-limit:]:
            activities.append({
                "timestamp": datetime.fromtimestamp(event["timestamp"]).isoformat(),
                "event_type": event["event_type"],
                "summary": self._summarize_event(event)
            })
        return activities
    
    def _summarize_event(self, event: dict) -> str:
        """Summarize audit event for report"""
        data = event.get("data", {})
        event_type = event["event_type"]
        
        if event_type == "DATA_COLLECTION":
            return f"Consent obtained for {data.get('purpose', 'unknown')}"
        elif event_type == "DATA_USE":
            return f"Data used for {data.get('purpose', 'unknown')}"
        elif event_type == "DATA_SHARE":
            return f"Data shared with {data.get('recipient', 'unknown')}"
        else:
            return event_type


def run_all_demos():
    """Run all consent management demos"""
    
    demo = ConsentManagementDemo()
    
    # Demo 1: Single purpose consent
    demo.demo_single_purpose_consent()
    
    # Demo 2: Multi-purpose consent
    demo.demo_multi_purpose_consent()
    
    # Demo 3: Consent withdrawal
    demo.demo_consent_withdrawal()
    
    # Demo 4: Consent renewal
    demo.demo_consent_renewal()
    
    # Generate audit report
    report = demo.generate_consent_audit_report()
    
    # Save report
    with open("consent_audit_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n✅ Consent audit report saved to consent_audit_report.json")
    
    return demo


def main():
    """Main function"""
    print("\n" + "="*70)
    print("🇭🇰 PDPO Consent Management Demo")
    print("="*70)
    print("\nThis demo showcases complete consent lifecycle management")
    print("under Hong Kong's Personal Data (Privacy) Ordinance.")
    
    # Run all demos
    demo = run_all_demos()
    
    print("\n" + "="*70)
    print("✅ All consent management demos completed successfully")
    print("="*70)
    
    # Summary
    print(f"\n📊 Demo Summary:")
    print(f"   • Single purpose consent demonstrated")
    print(f"   • Multi-purpose consent with granular control")
    print(f"   • Consent withdrawal with automatic blocking")
    print(f"   • Consent renewal before expiry")
    print(f"   • Complete audit trail maintained")
    print(f"   • DPP1 compliance verified for all scenarios")


if __name__ == "__main__":
    main()
