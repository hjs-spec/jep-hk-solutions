#!/usr/bin/env python3
"""
HKMA Mortgage Application Workflow Example
=============================================

This example demonstrates a complete mortgage application workflow
with full HKMA compliance, including:

- Customer due diligence (CDD)
- Credit assessment with explainable AI
- Property valuation
- Multi-level approval workflow
- Funds disbursement
- Complete audit trail
- HKMA regulatory reporting

All steps are recorded with cryptographic receipts that can be
presented to HKMA examiners.
"""

import json
import time
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from hkma.implementation.hkma_tracker import HKMABankingTracker


class MortgageApplication:
    """
    Represents a mortgage application with full lifecycle tracking.
    """
    
    def __init__(self, application_id: str, customer_id: str, amount: float,
                 property_value: float, customer_name: str):
        self.application_id = application_id
        self.customer_id = customer_id
        self.amount = amount
        self.property_value = property_value
        self.customer_name = customer_name
        self.ltv_ratio = (amount / property_value) * 100
        
        self.status = "initiated"
        self.steps = []
        self.receipts = {}
        self.approvals = []
        
    def to_dict(self) -> dict:
        return {
            "application_id": self.application_id,
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "amount": self.amount,
            "property_value": self.property_value,
            "ltv_ratio": self.ltv_ratio,
            "status": self.status,
            "steps": self.steps,
            "receipts": self.receipts,
            "approvals": self.approvals
        }


class MortgageWorkflowDemo:
    """
    Complete mortgage application workflow with HKMA compliance.
    """
    
    def __init__(self):
        self.tracker = HKMABankingTracker(
            bank_name="HSBC Hong Kong",
            banking_license="HSB-123456",
            hkma_contact="mortgage-supervisor@hkma.gov.hk"
        )
        
        self.applications = []
        self.completed_applications = []
        
        print("="*80)
        print("🏦 HKMA Mortgage Application Workflow Demo")
        print("="*80)
        print(f"Bank: {self.tracker.bank_name}")
        print(f"License: {self.tracker.banking_license}")
        print(f"HKMA Contact: {self.tracker.hkma_contact}")
    
    def run_complete_workflow(self):
        """
        Run a complete mortgage application workflow with multiple scenarios.
        """
        
        # Scenario 1: Standard mortgage approval (within limits)
        print("\n" + "="*80)
        print("📋 Scenario 1: Standard Mortgage Approval (HKD 5M)")
        print("="*80)
        
        app1 = MortgageApplication(
            application_id="MORT-2026-001",
            customer_id="CUST-001",
            amount=5000000,
            property_value=6250000,
            customer_name="Mr. Chan Tai Man"
        )
        
        self._process_mortgage_application(app1)
        self.applications.append(app1)
        
        # Scenario 2: High-value mortgage requiring additional approvals
        print("\n" + "="*80)
        print("📋 Scenario 2: High-Value Mortgage (HKD 12M)")
        print("="*80)
        
        app2 = MortgageApplication(
            application_id="MORT-2026-002",
            customer_id="CUST-002",
            amount=12000000,
            property_value=15000000,
            customer_name="Ms. Wong Sau Lan"
        )
        
        self._process_mortgage_application(app2)
        self.applications.append(app2)
        
        # Scenario 3: Mortgage requiring exception approval
        print("\n" + "="*80)
        print("📋 Scenario 3: Exception Mortgage (High LTV)")
        print("="*80)
        
        app3 = MortgageApplication(
            application_id="MORT-2026-003",
            customer_id="CUST-003",
            amount=8500000,
            property_value=10000000,
            customer_name="Mr. Lee Ka Fai"
        )
        
        self._process_mortgage_application(app3, high_ltv=True)
        self.applications.append(app3)
        
        # Generate HKMA report
        self._generate_hkma_report()
    
    def _process_mortgage_application(self, app: MortgageApplication, high_ltv: bool = False):
        """
        Process a complete mortgage application through all steps.
        """
        
        # Step 1: Customer Due Diligence
        print(f"\n1️⃣  Step 1: Customer Due Diligence - {app.customer_name}")
        cdd_receipt = self._perform_cdd(app)
        app.receipts["cdd"] = cdd_receipt["receipt_id"]
        app.steps.append({
            "step": "CDD",
            "timestamp": cdd_receipt["timestamp"],
            "status": "completed"
        })
        
        # Step 2: Credit Assessment
        print(f"\n2️⃣  Step 2: Credit Assessment")
        credit_receipt = self._assess_credit(app, high_ltv)
        app.receipts["credit_assessment"] = credit_receipt["decision_id"]
        app.steps.append({
            "step": "Credit Assessment",
            "timestamp": credit_receipt["decision_date"],
            "status": credit_receipt["decision"]
        })
        
        # Step 3: Property Valuation
        print(f"\n3️⃣  Step 3: Property Valuation")
        valuation_receipt = self._value_property(app)
        app.receipts["valuation"] = valuation_receipt["receipt_id"]
        app.steps.append({
            "step": "Valuation",
            "timestamp": valuation_receipt["timestamp"],
            "status": "completed"
        })
        
        # Step 4: Approval Workflow
        print(f"\n4️⃣  Step 4: Approval Workflow")
        approvals = self._obtain_approvals(app, credit_receipt)
        app.approvals = approvals
        app.receipts["approvals"] = [a["receipt_id"] for a in approvals]
        
        # Step 5: Funds Disbursement
        if all(a["decision"] == "APPROVED" for a in approvals):
            print(f"\n5️⃣  Step 5: Funds Disbursement")
            disbursement_receipt = self._disburse_funds(app)
            app.receipts["disbursement"] = disbursement_receipt["receipt_id"]
            app.status = "completed"
            self.completed_applications.append(app)
        else:
            app.status = "declined"
            print(f"\n❌ Application {app.application_id} declined")
        
        # Summary
        print(f"\n📊 Application {app.application_id} Summary:")
        print(f"   Status: {app.status}")
        print(f"   LTV Ratio: {app.ltv_ratio:.1f}%")
        print(f"   Approvals: {len([a for a in approvals if a['decision'] == 'APPROVED'])}/{len(approvals)}")
        print(f"   Receipts: {list(app.receipts.keys())}")
    
    def _perform_cdd(self, app: MortgageApplication) -> dict:
        """
        Perform Customer Due Diligence (HKMA AML requirements).
        """
        print(f"   Verifying identity for {app.customer_name}...")
        
        receipt = self.tracker.log_decision(
            operation="CDD_VERIFICATION",
            resource=f"customer/{app.customer_id}",
            actor_id="cdd-system",
            risk_level="MEDIUM",
            metadata={
                "customer_name": app.customer_name,
                "id_verified": True,
                "id_type": "HKID",
                "id_number": hashlib.sha256(f"ID-{app.customer_id}".encode()).hexdigest()[:8],
                "address_verified": True,
                "address_proof": "utility_bill",
                "income_verified": True,
                "income_proof": "payslip_3_months",
                "source_of_funds": "employment",
                "pep_check": "passed",
                "sanctions_check": "passed",
                "adverse_media": "none",
                "cdd_completed_by": "officer-123",
                "cdd_completion_date": time.time()
            }
        )
        
        print(f"   ✅ CDD completed - Receipt: {receipt['receipt_id'][:16]}...")
        return receipt
    
    def _assess_credit(self, app: MortgageApplication, high_ltv: bool = False) -> dict:
        """
        Perform credit assessment with explainable AI (CR-G-12).
        """
        print(f"   Assessing credit for HKD {app.amount:,.0f}...")
        
        # Simulate credit scoring
        credit_score = 680 if high_ltv else 750
        dti_ratio = 45 if high_ltv else 35
        employment_years = 2 if high_ltv else 8
        
        decision = "APPROVED" if not high_ltv else "APPROVED_WITH_CONDITIONS"
        
        receipt = self.tracker.log_credit_decision(
            customer_id=app.customer_id,
            application_id=app.application_id,
            decision=decision,
            amount=app.amount,
            purpose="mortgage",
            term_years=25,
            risk_rating="HIGH" if high_ltv else "MEDIUM",
            
            # Explainable factors (CR-G-12 requirement)
            decision_factors={
                "credit_score": {
                    "value": credit_score,
                    "weight": 0.4,
                    "threshold": ">=680",
                    "contribution": "positive" if credit_score >= 680 else "negative"
                },
                "dti_ratio": {
                    "value": dti_ratio,
                    "weight": 0.3,
                    "threshold": "<=40",
                    "contribution": "positive" if dti_ratio <= 40 else "negative"
                },
                "employment_stability": {
                    "value": f"{employment_years}_years",
                    "weight": 0.2,
                    "threshold": ">=2_years",
                    "contribution": "positive" if employment_years >= 2 else "negative"
                },
                "ltv_ratio": {
                    "value": app.ltv_ratio,
                    "weight": 0.1,
                    "threshold": "<=80",
                    "contribution": "negative" if high_ltv else "positive"
                }
            },
            
            # Human-readable explanation
            explanation=(
                f"Credit score {credit_score} meets threshold, "
                f"DTI {dti_ratio}% within limit, "
                f"employment {employment_years} years, "
                f"LTV {app.ltv_ratio:.1f}% {'exceeds' if high_ltv else 'within'} policy"
            ),
            
            # Model information
            model_version="mortgage-scoring-v2.1",
            model_confidence=0.95,
            
            # Policy compliance
            within_policy=not high_ltv,
            exception_approved=high_ltv,
            regulatory_reporting_required=True,
            
            metadata={
                "property_type": "residential",
                "occupancy": "owner",
                "first_time_buyer": True
            }
        )
        
        print(f"   ✅ Credit assessment completed - Decision: {decision}")
        print(f"   Credit Score: {credit_score}, DTI: {dti_ratio}%, LTV: {app.ltv_ratio:.1f}%")
        
        return receipt
    
    def _value_property(self, app: MortgageApplication) -> dict:
        """
        Perform property valuation.
        """
        print(f"   Valuing property at HKD {app.property_value:,.0f}...")
        
        receipt = self.tracker.log_decision(
            operation="PROPERTY_VALUATION",
            resource=f"property/{hash(app.customer_id)}",
            actor_id="valuation-system",
            risk_level="LOW",
            metadata={
                "property_address": f"{hash(app.customer_id)} Nathan Road, Kowloon",
                "property_type": "residential",
                "valuation_amount": app.property_value,
                "valuation_method": "automated_valuation_model",
                "avm_confidence": 0.95,
                "comparable_sales_used": 12,
                "valuation_date": time.time(),
                "valuer": "system",
                "review_required": app.ltv_ratio > 80
            }
        )
        
        print(f"   ✅ Property valuation completed")
        return receipt
    
    def _obtain_approvals(self, app: MortgageApplication, credit_receipt: dict) -> list:
        """
        Obtain required approvals based on amount and risk (CR-G-12 5.3).
        """
        approvals = []
        
        # Determine approval levels based on amount
        if app.amount <= 3000000:
            levels = ["loan_officer"]
        elif app.amount <= 8000000:
            levels = ["loan_officer", "senior_manager"]
        elif app.amount <= 15000000:
            levels = ["loan_officer", "senior_manager", "department_head"]
        else:
            levels = ["loan_officer", "senior_manager", "department_head", "credit_committee"]
        
        print(f"   Required approvals: {', '.join(levels)}")
        
        # Simulate approval workflow
        for level in levels:
            print(f"   → Obtaining {level} approval...")
            
            if level == "loan_officer":
                approver = "officer-456"
                decision = "APPROVED"
                notes = "All documents verified, within policy"
                
            elif level == "senior_manager":
                approver = "manager-789"
                decision = "APPROVED"
                notes = "Risk assessment acceptable"
                
            elif level == "department_head":
                approver = "head-012"
                decision = "APPROVED_WITH_CONDITIONS" if app.ltv_ratio > 80 else "APPROVED"
                notes = f"Approved with conditions: LTV {app.ltv_ratio:.1f}% requires higher downpayment"
                
            else:  # credit_committee
                approver = "committee-chair"
                decision = "APPROVED"
                notes = "Credit committee approved on 2026-03-15"
            
            approval = self.tracker.log_decision(
                operation="APPROVAL",
                resource=f"application/{app.application_id}",
                actor_id=level,
                risk_level="MEDIUM" if level in ["loan_officer", "senior_manager"] else "HIGH",
                human_approver=approver,
                reasoning=notes,
                metadata={
                    "approval_level": level,
                    "application_id": app.application_id,
                    "amount": app.amount,
                    "credit_decision_id": credit_receipt["decision_id"],
                    "approval_notes": notes,
                    "approval_date": time.time()
                }
            )
            
            approvals.append({
                "level": level,
                "approver": approver,
                "decision": decision,
                "timestamp": approval["timestamp"],
                "receipt_id": approval["receipt_id"]
            })
            
            print(f"      ✅ {level} approved by {approver}")
        
        return approvals
    
    def _disburse_funds(self, app: MortgageApplication) -> dict:
        """
        Disburse mortgage funds.
        """
        print(f"   Disbursing HKD {app.amount:,.0f}...")
        
        receipt = self.tracker.log_decision(
            operation="FUNDS_DISBURSEMENT",
            resource=f"application/{app.application_id}",
            actor_id="payment-system",
            risk_level="LOW",
            metadata={
                "amount": app.amount,
                "currency": "HKD",
                "disbursement_method": "telegraphic_transfer",
                "recipient_account": "123-456-789",
                "recipient_name": app.customer_name,
                "disbursement_date": time.time(),
                "reference": f"LOAN-{app.application_id}",
                "settlement_date": time.time() + 86400,
                "confirmed_by": "settlement-officer"
            }
        )
        
        print(f"   ✅ Funds disbursed - Reference: LOAN-{app.application_id}")
        return receipt
    
    def _generate_hkma_report(self):
        """
        Generate HKMA compliance report for all applications.
        """
        print("\n" + "="*80)
        print("📊 Generating HKMA Compliance Report")
        print("="*80)
        
        # Calculate statistics
        total_applications = len(self.applications)
        completed = len([a for a in self.applications if a.status == "completed"])
        declined = len([a for a in self.applications if a.status == "declined"])
        total_amount = sum(a.amount for a in self.applications)
        
        # Generate report
        report = self.tracker.generate_hkma_report(
            start_date="2026-01-01",
            end_date="2026-03-31"
        )
        
        # Add mortgage-specific metrics
        report["mortgage_statistics"] = {
            "total_applications": total_applications,
            "completed_applications": completed,
            "declined_applications": declined,
            "total_amount_disbursed": total_amount,
            "average_ltv": sum(a.ltv_ratio for a in self.applications) / total_applications,
            "approval_rate": f"{(completed/total_applications)*100:.1f}%"
        }
        
        # Add application summaries
        report["applications"] = [a.to_dict() for a in self.applications]
        
        # Save report
        filename = f"hkma_mortgage_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n📈 Mortgage Statistics:")
        print(f"   Total Applications: {total_applications}")
        print(f"   Completed: {completed}")
        print(f"   Declined: {declined}")
        print(f"   Total Amount: HKD {total_amount:,.0f}")
        print(f"   Average LTV: {report['mortgage_statistics']['average_ltv']:.1f}%")
        print(f"   Approval Rate: {report['mortgage_statistics']['approval_rate']}")
        
        print(f"\n✅ HKMA report saved to: {filename}")
        
        return report
    
    def verify_application(self, application_id: str) -> dict:
        """
        Verify a specific application's compliance.
        """
        app = next((a for a in self.applications if a.application_id == application_id), None)
        if not app:
            return {"error": "Application not found"}
        
        verification = {
            "application_id": app.application_id,
            "status": app.status,
            "compliance_checks": {
                "cdd_completed": "cdd" in app.receipts,
                "credit_assessment_completed": "credit_assessment" in app.receipts,
                "valuation_completed": "valuation" in app.receipts,
                "approvals_obtained": len(app.approvals) > 0,
                "disbursement_completed": "disbursement" in app.receipts if app.status == "completed" else True
            },
            "all_receipts_present": len(app.receipts) == (5 if app.status == "completed" else 4),
            "verification_time": time.time()
        }
        
        verification["fully_compliant"] = all(verification["compliance_checks"].values())
        
        return verification


def run_demo():
    """Run the complete mortgage workflow demo."""
    
    demo = MortgageWorkflowDemo()
    demo.run_complete_workflow()
    
    # Verify applications
    print("\n" + "="*80)
    print("🔍 Application Verification")
    print("="*80)
    
    for app in demo.applications:
        verification = demo.verify_application(app.application_id)
        status = "✅ COMPLIANT" if verification["fully_compliant"] else "❌ ISSUES FOUND"
        print(f"\n{app.application_id}: {status}")
        for check, passed in verification["compliance_checks"].items():
            mark = "✅" if passed else "❌"
            print(f"  {mark} {check}")
    
    print("\n" + "="*80)
    print("✅ Mortgage Workflow Demo Complete")
    print("="*80)
    print("\nThis demo demonstrated:")
    print("  • Complete mortgage application lifecycle")
    print("  • HKMA CR-G-12 credit risk compliance")
    print("  • Explainable AI for credit decisions")
    print("  • Multi-level approval workflow")
    print("  • Cryptographic receipts for all steps")
    print("  • Regulatory report generation")


if __name__ == "__main__":
    run_demo()
