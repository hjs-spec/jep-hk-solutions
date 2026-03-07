#!/usr/bin/env python3
"""
JEP Hong Kong Bilingual Templates
====================================

Template rendering engine for bilingual documents, receipts, and notifications.

This module provides:
- Bilingual template loading and rendering
- Variable substitution in both languages
- Conditional content based on language
- Template inheritance for consistent branding
- Support for all JEP Hong Kong document types
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from string import Template

from .translator import BilingualTranslator, get_translator


class TemplateNotFoundError(Exception):
    """Raised when a template file cannot be found."""
    pass


class TemplateRenderError(Exception):
    """Raised when template rendering fails."""
    pass


class BilingualTemplate:
    """
    Bilingual template with English and Traditional Chinese versions.
    
    Supports:
    - Variable substitution with ${variable} syntax
    - Conditional blocks based on language
    - Nested templates
    - Default values for missing variables
    """
    
    def __init__(self, template_id: str, en_content: str, zh_content: str):
        """
        Initialize bilingual template.
        
        Args:
            template_id: Unique template identifier
            en_content: English template content
            zh_content: Traditional Chinese template content
        """
        self.template_id = template_id
        self.en_template = Template(en_content)
        self.zh_template = Template(zh_content)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def render(self, variables: Dict[str, Any], language: str = "en") -> str:
        """
        Render template in specified language.
        
        Args:
            variables: Dictionary of variables to substitute
            language: Target language ("en" or "zh")
        
        Returns:
            Rendered template string
        
        Raises:
            TemplateRenderError: If rendering fails
        """
        try:
            # Prepare variables with defaults
            safe_vars = self._prepare_variables(variables, language)
            
            # Render appropriate language version
            if language == "zh":
                return self.zh_template.safe_substitute(safe_vars)
            else:
                return self.en_template.safe_substitute(safe_vars)
                
        except Exception as e:
            raise TemplateRenderError(f"Failed to render template {self.template_id}: {e}")
    
    def _prepare_variables(self, variables: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Prepare variables with defaults and language-specific formatting."""
        prepared = variables.copy()
        
        # Add common variables
        prepared.setdefault("current_date", datetime.now().strftime("%Y-%m-%d"))
        prepared.setdefault("current_year", datetime.now().year)
        prepared.setdefault("language", language)
        
        # Format currency if present
        if "amount" in prepared and isinstance(prepared["amount"], (int, float)):
            if language == "zh":
                prepared["amount_formatted"] = f"港元 {prepared['amount']:,.0f}"
            else:
                prepared["amount_formatted"] = f"HKD {prepared['amount']:,.0f}"
        
        return prepared


class TemplateManager:
    """
    Manages all bilingual templates for JEP Hong Kong.
    
    Features:
    - Load templates from files
    - Cache templates in memory
    - Template inheritance
    - Hot reload for development
    """
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize template manager.
        
        Args:
            template_dir: Directory containing template files
        """
        self.translator = get_translator()
        self.template_dir = template_dir or self._get_default_template_dir()
        self.templates: Dict[str, BilingualTemplate] = {}
        self.loaded_at = None
        
        # Load all templates
        self.load_templates()
    
    def _get_default_template_dir(self) -> str:
        """Get default template directory path."""
        base_dir = Path(__file__).parent.parent
        return str(base_dir / "templates")
    
    def load_templates(self) -> None:
        """Load all templates from template directory."""
        template_dir = Path(self.template_dir)
        
        if not template_dir.exists():
            print(f"⚠️ Template directory not found: {self.template_dir}")
            return
        
        # Load receipts
        receipts_dir = template_dir / "receipts"
        if receipts_dir.exists():
            self._load_templates_from_dir(receipts_dir, "receipt")
        
        # Load policies
        policies_dir = template_dir / "policies"
        if policies_dir.exists():
            self._load_templates_from_dir(policies_dir, "policy")
        
        # Load notifications
        notifications_dir = template_dir / "notifications"
        if notifications_dir.exists():
            self._load_templates_from_dir(notifications_dir, "notification")
        
        self.loaded_at = datetime.now()
        print(f"✅ Loaded {len(self.templates)} bilingual templates")
    
    def _load_templates_from_dir(self, directory: Path, prefix: str) -> None:
        """Load all templates from a directory."""
        for file_path in directory.glob("*.json"):
            template_id = f"{prefix}_{file_path.stem}"
            self._load_template_file(file_path, template_id)
    
    def _load_template_file(self, file_path: Path, template_id: str) -> None:
        """Load a single template file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if "en" in data and "zh" in data:
                template = BilingualTemplate(
                    template_id=template_id,
                    en_content=data["en"],
                    zh_content=data["zh"]
                )
                self.templates[template_id] = template
                print(f"   ✓ Loaded: {template_id}")
            else:
                print(f"   ⚠️  Missing language versions: {file_path}")
                
        except Exception as e:
            print(f"   ❌ Failed to load {file_path}: {e}")
    
    def get_template(self, template_id: str) -> Optional[BilingualTemplate]:
        """Get template by ID."""
        return self.templates.get(template_id)
    
    def render_template(self, template_id: str, variables: Dict[str, Any], 
                        language: str = "en") -> str:
        """
        Render a template by ID.
        
        Args:
            template_id: Template identifier
            variables: Variables to substitute
            language: Target language
        
        Returns:
            Rendered template string
        
        Raises:
            TemplateNotFoundError: If template not found
        """
        template = self.get_template(template_id)
        if not template:
            raise TemplateNotFoundError(f"Template not found: {template_id}")
        
        return template.render(variables, language)
    
    def render_bilingual(self, template_id: str, variables: Dict[str, Any]) -> Dict[str, str]:
        """
        Render template in both languages.
        
        Returns:
            Dictionary with 'en' and 'zh' versions
        """
        return {
            "en": self.render_template(template_id, variables, "en"),
            "zh": self.render_template(template_id, variables, "zh")
        }
    
    def reload_templates(self) -> None:
        """Reload all templates from disk."""
        self.templates.clear()
        self.load_templates()


# Pre-defined templates
class ReceiptTemplates:
    """Receipt templates for various document types."""
    
    def __init__(self, manager: TemplateManager):
        self.manager = manager
    
    def credit_decision_receipt(self, data: Dict[str, Any], language: str = "en") -> str:
        """Render credit decision receipt."""
        return self.manager.render_template("receipt_credit_decision", data, language)
    
    def consent_receipt(self, data: Dict[str, Any], language: str = "en") -> str:
        """Render consent receipt."""
        return self.manager.render_template("receipt_consent", data, language)
    
    def dsar_receipt(self, data: Dict[str, Any], language: str = "en") -> str:
        """Render DSAR receipt."""
        return self.manager.render_template("receipt_dsar", data, language)
    
    def mortgage_receipt(self, data: Dict[str, Any], language: str = "en") -> str:
        """Render mortgage application receipt."""
        return self.manager.render_template("receipt_mortgage", data, language)


class PolicyTemplates:
    """Policy templates for privacy and terms."""
    
    def __init__(self, manager: TemplateManager):
        self.manager = manager
    
    def privacy_policy(self, data: Dict[str, Any], language: str = "en") -> str:
        """Render privacy policy."""
        return self.manager.render_template("policy_privacy", data, language)
    
    def terms_of_service(self, data: Dict[str, Any], language: str = "en") -> str:
        """Render terms of service."""
        return self.manager.render_template("policy_terms", data, language)
    
    def cookie_policy(self, data: Dict[str, Any], language: str = "en") -> str:
        """Render cookie policy."""
        return self.manager.render_template("policy_cookie", data, language)


class NotificationTemplates:
    """Notification templates for customer communications."""
    
    def __init__(self, manager: TemplateManager):
        self.manager = manager
    
    def application_approved(self, data: Dict[str, Any], language: str = "en") -> str:
        """Render application approved notification."""
        return self.manager.render_template("notification_approved", data, language)
    
    def application_declined(self, data: Dict[str, Any], language: str = "en") -> str:
        """Render application declined notification."""
        return self.manager.render_template("notification_declined", data, language)
    
    def consent_confirmation(self, data: Dict[str, Any], language: str = "en") -> str:
        """Render consent confirmation."""
        return self.manager.render_template("notification_consent", data, language)
    
    def dsar_completed(self, data: Dict[str, Any], language: str = "en") -> str:
        """Render DSAR completed notification."""
        return self.manager.render_template("notification_dsar", data, language)
    
    def security_alert(self, data: Dict[str, Any], language: str = "en") -> str:
        """Render security alert notification."""
        return self.manager.render_template("notification_security", data, language)


# Example template files content (would be in separate JSON files)

RECEIPT_CREDIT_DECISION = {
    "en": """
╔══════════════════════════════════════════════════════════════╗
║                 CREDIT DECISION RECEIPT                      ║
╚══════════════════════════════════════════════════════════════╝

Receipt ID: ${receipt_id}
Date: ${current_date}
Application ID: ${application_id}
Customer Reference: ${customer_ref}

DECISION SUMMARY
────────────────────────────────────────────────────────────────
Decision: ${decision}
Amount: ${amount_formatted}
Term: ${term_years} years
Interest Rate: ${interest_rate}% p.a.

DECISION FACTORS
────────────────────────────────────────────────────────────────
Credit Score: ${credit_score} (${credit_score_rating})
DTI Ratio: ${dti_ratio}%
LTV Ratio: ${ltv_ratio}%
Employment Years: ${employment_years}

EXPLANATION
────────────────────────────────────────────────────────────────
${explanation}

APPROVAL WORKFLOW
────────────────────────────────────────────────────────────────
${approval_chain}

This receipt serves as official record of the credit decision.
For questions, contact: ${contact_email}

────────────────────────────────────────────────────────────────
Signature: ${signature}
    """,
    
    "zh": """
╔══════════════════════════════════════════════════════════════╗
║                      信貸審批收據                             ║
╚══════════════════════════════════════════════════════════════╝

收據編號：${receipt_id}
日期：${current_date}
申請編號：${application_id}
客戶參考：${customer_ref}

審批結果概要
────────────────────────────────────────────────────────────────
審批結果：${decision_zh}
貸款金額：${amount_formatted}
貸款年期：${term_years}年
年利率：${interest_rate}厘

審批因素
────────────────────────────────────────────────────────────────
信貸評分：${credit_score}（${credit_score_rating_zh}）
債務收入比率：${dti_ratio}%
按揭成數：${ltv_ratio}%
就業年資：${employment_years}年

解釋說明
────────────────────────────────────────────────────────────────
${explanation_zh}

審批流程
────────────────────────────────────────────────────────────────
${approval_chain_zh}

此收據為信貸審批的正式記錄。
如有查詢，請聯絡：${contact_email_zh}

────────────────────────────────────────────────────────────────
電子簽署：${signature}
    """
}


RECEIPT_CONSENT = {
    "en": """
╔══════════════════════════════════════════════════════════════╗
║                    CONSENT MANAGEMENT RECEIPT                ║
╚══════════════════════════════════════════════════════════════╝

Receipt ID: ${receipt_id}
Date: ${current_date}
Customer Reference: ${customer_ref}

CONSENT DETAILS
────────────────────────────────────────────────────────────────
Consent ID: ${consent_id}
Purpose: ${purpose}
Data Categories: ${data_categories}
Collection Method: ${collection_method}
Notice Provided: ${notice_provided}

RETENTION PERIOD
────────────────────────────────────────────────────────────────
Retention Days: ${retention_days}
Expiry Date: ${expiry_date}

YOUR RIGHTS
────────────────────────────────────────────────────────────────
• Right to withdraw consent at any time
• Right to access your personal data
• Right to request correction

To exercise your rights, contact: ${dsar_contact}

────────────────────────────────────────────────────────────────
Signature: ${signature}
    """,
    
    "zh": """
╔══════════════════════════════════════════════════════════════╗
║                      同意管理收據                             ║
╚══════════════════════════════════════════════════════════════╝

收據編號：${receipt_id}
日期：${current_date}
客戶參考：${customer_ref}

同意詳情
────────────────────────────────────────────────────────────────
同意編號：${consent_id}
收集目的：${purpose_zh}
資料類別：${data_categories_zh}
收集方式：${collection_method_zh}
已提供通知：${notice_provided_zh}

保留期限
────────────────────────────────────────────────────────────────
保留日數：${retention_days}日
屆滿日期：${expiry_date}

您的權利
────────────────────────────────────────────────────────────────
• 隨時撤回同意
• 查閱您的個人資料
• 要求更正資料

行使權利請聯絡：${dsar_contact_zh}

────────────────────────────────────────────────────────────────
電子簽署：${signature}
    """
}


NOTIFICATION_APPROVED = {
    "en": """
Dear ${customer_name},

We are pleased to inform you that your ${application_type} application
(Ref: ${application_id}) has been APPROVED.

APPROVAL DETAILS
────────────────────────────────────────────────────────────────
Approved Amount: ${amount_formatted}
Approval Date: ${approval_date}
Valid Until: ${valid_until}

NEXT STEPS
────────────────────────────────────────────────────────────────
1. Review the loan agreement in your online banking portal
2. Sign the agreement electronically within ${signature_deadline} days
3. Funds will be disbursed within ${disbursement_days} working days
   after signing

If you have any questions, please contact our customer service
at ${contact_phone} or visit any branch.

Thank you for choosing ${bank_name}.

────────────────────────────────────────────────────────────────
This is an automated message. Please do not reply.
    """,
    
    "zh": """
尊敬的${customer_name_zh}：

我們很高興通知您，您的${application_type_zh}申請
（編號：${application_id}）已獲批准。

批准詳情
────────────────────────────────────────────────────────────────
批准金額：${amount_formatted}
批准日期：${approval_date}
有效期限：${valid_until}

下一步行動
────────────────────────────────────────────────────────────────
1. 請登入網上銀行查閱貸款協議
2. 請於${signature_deadline}日內以電子方式簽署協議
3. 簽署後${disbursement_days}個工作天內發放貸款

如有任何查詢，請致電客戶服務熱線${contact_phone}
或親臨任何分行。

多謝選用${bank_name_zh}。

────────────────────────────────────────────────────────────────
此為自動訊息，請勿回覆。
    """
}


class TemplateRenderer:
    """
    High-level template renderer for common document types.
    """
    
    def __init__(self):
        self.manager = TemplateManager()
        self.receipts = ReceiptTemplates(self.manager)
        self.policies = PolicyTemplates(self.manager)
        self.notifications = NotificationTemplates(self.manager)
        self.translator = get_translator()
    
    def render_credit_decision(self, decision_data: Dict[str, Any], 
                               language: str = "en") -> str:
        """Render credit decision receipt."""
        # Prepare language-specific fields
        if language == "zh":
            decision_data["decision_zh"] = self.translator.translate(
                decision_data.get("decision", ""), "zh"
            )
            decision_data["explanation_zh"] = decision_data.get("explanation_zh", 
                self.translator.translate(decision_data.get("explanation", ""), "zh"))
        
        return self.receipts.credit_decision_receipt(decision_data, language)
    
    def render_consent_receipt(self, consent_data: Dict[str, Any],
                               language: str = "en") -> str:
        """Render consent receipt."""
        if language == "zh":
            consent_data["purpose_zh"] = self.translator.translate(
                consent_data.get("purpose", ""), "zh"
            )
            consent_data["data_categories_zh"] = [
                self.translator.translate(cat, "zh") 
                for cat in consent_data.get("data_categories", [])
            ]
        
        return self.receipts.consent_receipt(consent_data, language)
    
    def render_approval_notification(self, approval_data: Dict[str, Any],
                                     language: str = "en") -> str:
        """Render approval notification."""
        if language == "zh":
            approval_data["customer_name_zh"] = approval_data.get("customer_name_zh",
                self.translator.translate(approval_data.get("customer_name", ""), "zh"))
            approval_data["application_type_zh"] = self.translator.translate(
                approval_data.get("application_type", ""), "zh"
            )
            approval_data["bank_name_zh"] = approval_data.get("bank_name_zh",
                self.translator.translate(approval_data.get("bank_name", ""), "zh"))
        
        return self.notifications.application_approved(approval_data, language)
    
    def render_bilingual_document(self, template_id: str, 
                                  data: Dict[str, Any]) -> Dict[str, str]:
        """Render document in both languages."""
        return self.manager.render_bilingual(template_id, data)


# Example usage
if __name__ == "__main__":
    renderer = TemplateRenderer()
    
    # Test credit decision receipt
    credit_data = {
        "receipt_id": "RCP-2026-001",
        "application_id": "APP-2026-001",
        "customer_ref": "CUST-123",
        "decision": "APPROVED",
        "amount": 5000000,
        "term_years": 25,
        "interest_rate": 3.5,
        "credit_score": 750,
        "credit_score_rating": "Good",
        "dti_ratio": 35,
        "ltv_ratio": 80,
        "employment_years": 8,
        "explanation": "Credit score meets threshold, DTI within limit",
        "approval_chain": "Loan Officer → Senior Manager",
        "contact_email": "mortgage@hsbc.com.hk",
        "signature": "ed25519:abc123..."
    }
    
    print("\n📄 English Credit Decision Receipt:")
    print(renderer.render_credit_decision(credit_data, "en"))
    
    print("\n📄 Chinese Credit Decision Receipt:")
    print(renderer.render_credit_decision(credit_data, "zh"))
    
    # Test consent receipt
    consent_data = {
        "receipt_id": "CONSENT-2026-001",
        "customer_ref": "CUST-123",
        "consent_id": "CONSENT-001",
        "purpose": "credit_scoring",
        "data_categories": ["income", "credit_history"],
        "collection_method": "online_form",
        "notice_provided": "Yes",
        "retention_days": 2555,
        "expiry_date": "2033-03-07",
        "dsar_contact": "dsar@hsbc.com.hk"
    }
    
    print("\n📄 English Consent Receipt:")
    print(renderer.render_consent_receipt(consent_data, "en"))
    
    print("\n📄 Chinese Consent Receipt:")
    print(renderer.render_consent_receipt(consent_data, "zh"))
    
    # Test approval notification
    notification_data = {
        "customer_name": "Mr. Chan Tai Man",
        "application_type": "mortgage",
        "application_id": "MORT-2026-001",
        "amount": 5000000,
        "approval_date": "2026-03-07",
        "valid_until": "2026-04-07",
        "signature_deadline": 14,
        "disbursement_days": 3,
        "contact_phone": "2233 8000",
        "bank_name": "HSBC Hong Kong"
    }
    
    print("\n📧 English Approval Notification:")
    print(renderer.render_approval_notification(notification_data, "en"))
    
    print("\n📧 Chinese Approval Notification:")
    print(renderer.render_approval_notification(notification_data, "zh"))
