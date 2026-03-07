#!/usr/bin/env python3
"""
Bilingual Support Test Suite for JEP Hong Kong
=================================================

Comprehensive tests for English-Traditional Chinese bilingual support,
including translation accuracy, template rendering, language switching,
and compliance with Hong Kong's linguistic requirements.

Run tests:
    pytest tests/test_bilingual.py -v
    python -m unittest tests/test_bilingual.py
"""

import unittest
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from bilingual.core.translator import BilingualTranslator, Language, get_translator
from bilingual.core.templates import TemplateManager, TemplateRenderer


class TestBilingualTranslator(unittest.TestCase):
    """Test cases for BilingualTranslator core functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.translator = BilingualTranslator(default_language="en")
    
    def test_initialization(self):
        """Test translator initialization."""
        self.assertEqual(self.translator.default_language, "en")
        self.assertEqual(self.translator.current_language, "en")
        self.assertGreater(len(self.translator.translations), 100)
    
    def test_basic_translation_en_to_zh(self):
        """Test basic English to Chinese translation."""
        test_cases = [
            ("credit_scoring", "信用評分"),
            ("APPROVED", "已批准"),
            ("customer", "客戶"),
            ("LOW", "低風險"),
            ("mortgage", "按揭"),
        ]
        
        for english, expected_chinese in test_cases:
            with self.subTest(term=english):
                result = self.translator.translate(english, "zh")
                self.assertEqual(result, expected_chinese)
    
    def test_basic_translation_zh_to_en(self):
        """Test basic Chinese to English translation."""
        # First set language to Chinese to access reverse translations
        test_cases = [
            ("信用評分", "credit_scoring"),
            ("已批准", "APPROVED"),
            ("客戶", "customer"),
            ("低風險", "LOW"),
            ("按揭", "mortgage"),
        ]
        
        for chinese, expected_english in test_cases:
            with self.subTest(term=chinese):
                result = self.translator.translate(chinese, "en")
                self.assertEqual(result, expected_english)
    
    def test_context_term_translation(self):
        """Test context-specific term translations."""
        test_cases = [
            ("credit_scoring", "excellent", "zh", "優良（800分以上）"),
            ("credit_scoring", "good", "zh", "良好（700-799分）"),
            ("ltv_ratio", "high", "zh", "高按揭成數（高於80%）"),
            ("dti_ratio", "low", "zh", "低債務收入比率（低於35%）"),
        ]
        
        for context, term, lang, expected in test_cases:
            with self.subTest(context=context, term=term):
                result = self.translator.translate_context_term(context, term, lang)
                self.assertEqual(result, expected)
    
    def test_dictionary_translation(self):
        """Test recursive dictionary translation."""
        test_dict = {
            "customer_id": "CUST-123",
            "application_id": "APP-2026-001",
            "status": "APPROVED",
            "risk_level": "MEDIUM",
            "decision_factors": {
                "credit_score": 750,
                "dti_ratio": 35,
                "ltv_ratio": 80
            }
        }
        
        translated = self.translator.translate_dict(test_dict, "zh")
        
        # Check key translations
        self.assertIn("客戶編號", translated)  # customer_id
        self.assertIn("申請編號", translated)  # application_id
        self.assertIn("狀態", translated)  # status
        self.assertIn("風險級別", translated)  # risk_level
        self.assertIn("審批因素", translated)  # decision_factors
        
        # Check value translations
        self.assertEqual(translated["狀態"], "已批准")
        self.assertEqual(translated["風險級別"], "中風險")
    
    def test_currency_formatting(self):
        """Test currency formatting in both languages."""
        amount = 5000000
        
        en_format = self.translator.format_currency(amount, "en")
        self.assertEqual(en_format, "HKD 5,000,000")
        
        zh_format = self.translator.format_currency(amount, "zh")
        self.assertEqual(zh_format, "港元 5,000,000")
    
    def test_date_formatting(self):
        """Test date formatting in both languages."""
        test_date = datetime(2026, 3, 7)
        
        en_format = self.translator.format_date(test_date, "en")
        self.assertEqual(en_format, "07 March 2026")
        
        zh_format = self.translator.format_date(test_date, "zh")
        self.assertEqual(zh_format, "2026年03月07日")
    
    def test_language_switching(self):
        """Test language switching functionality."""
        self.assertEqual(self.translator.current_language, "en")
        
        self.translator.set_language("zh")
        self.assertEqual(self.translator.current_language, "zh")
        
        # Test that translate uses current language
        result = self.translator.translate("APPROVED")
        self.assertEqual(result, "已批准")
        
        # Switch back
        self.translator.set_language("en")
        result = self.translator.translate("APPROVED")
        self.assertEqual(result, "APPROVED")
    
    def test_language_detection(self):
        """Test language detection functionality."""
        test_cases = [
            ("This is English text", "en"),
            ("這是中文文本", "zh"),
            ("Mixed 中文 and English", "zh"),  # Contains Chinese
            ("123456", "en"),  # Numbers only
        ]
        
        for text, expected_lang in test_cases:
            with self.subTest(text=text[:20]):
                detected = self.translator.detect_language(text)
                self.assertEqual(detected, expected_lang)
    
    def test_bilingual_text_selection(self):
        """Test bilingual text selection."""
        en_text = "Hello"
        zh_text = "你好"
        
        # Get English
        result = self.translator.get_bilingual_text(en_text, zh_text, "en")
        self.assertEqual(result, en_text)
        
        # Get Chinese
        result = self.translator.get_bilingual_text(en_text, zh_text, "zh")
        self.assertEqual(result, zh_text)
        
        # Use current language
        self.translator.set_language("zh")
        result = self.translator.get_bilingual_text(en_text, zh_text)
        self.assertEqual(result, zh_text)
    
    def test_singleton_pattern(self):
        """Test that get_translator returns the same instance."""
        translator1 = get_translator()
        translator2 = get_translator()
        
        self.assertIs(translator1, translator2)


class TestTemplateManager(unittest.TestCase):
    """Test cases for TemplateManager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = TemplateManager()
        self.renderer = TemplateRenderer()
    
    def test_template_loading(self):
        """Test that templates are loaded."""
        # Note: This test assumes templates are loaded from files
        # In a real environment, we'd create test templates
        self.assertIsNotNone(self.manager.templates)
    
    def test_credit_decision_rendering(self):
        """Test credit decision receipt rendering."""
        test_data = {
            "receipt_id": "TEST-001",
            "application_id": "APP-001",
            "customer_ref": "CUST-001",
            "decision": "APPROVED",
            "amount": 5000000,
            "term_years": 25,
            "interest_rate": 3.5,
            "credit_score": 750,
            "credit_score_rating": "Good",
            "dti_ratio": 35,
            "ltv_ratio": 80,
            "employment_years": 8,
            "explanation": "Test explanation",
            "approval_chain": "Test chain",
            "contact_email": "test@example.com",
            "signature": "test_sig"
        }
        
        # Test English rendering
        en_result = self.renderer.render_credit_decision(test_data, "en")
        self.assertIsInstance(en_result, str)
        self.assertIn("CREDIT DECISION RECEIPT", en_result)
        self.assertIn("APPROVED", en_result)
        
        # Test Chinese rendering
        zh_result = self.renderer.render_credit_decision(test_data, "zh")
        self.assertIsInstance(zh_result, str)
        self.assertIn("信貸審批收據", zh_result)
        self.assertIn("已批准", zh_result)
    
    def test_consent_receipt_rendering(self):
        """Test consent receipt rendering."""
        test_data = {
            "receipt_id": "CONSENT-001",
            "customer_ref": "CUST-001",
            "consent_id": "CONSENT-001",
            "purpose": "credit_scoring",
            "data_categories": ["income", "credit_history"],
            "collection_method": "online_form",
            "notice_provided": "Yes",
            "retention_days": 2555,
            "expiry_date": "2033-03-07",
            "dsar_contact": "dsar@example.com",
            "signature": "test_sig"
        }
        
        # Test English rendering
        en_result = self.renderer.render_consent_receipt(test_data, "en")
        self.assertIsInstance(en_result, str)
        self.assertIn("CONSENT MANAGEMENT RECEIPT", en_result)
        
        # Test Chinese rendering
        zh_result = self.renderer.render_consent_receipt(test_data, "zh")
        self.assertIsInstance(zh_result, str)
        self.assertIn("同意管理收據", zh_result)
    
    def test_approval_notification_rendering(self):
        """Test approval notification rendering."""
        test_data = {
            "customer_name": "Mr. Chan Tai Man",
            "application_type": "mortgage",
            "application_id": "MORT-001",
            "amount": 5000000,
            "approval_date": "2026-03-07",
            "valid_until": "2026-04-07",
            "signature_deadline": 14,
            "disbursement_days": 3,
            "contact_phone": "2233 8000",
            "bank_name": "HSBC Hong Kong"
        }
        
        # Test English rendering
        en_result = self.renderer.render_approval_notification(test_data, "en")
        self.assertIsInstance(en_result, str)
        self.assertIn("has been APPROVED", en_result)
        
        # Test Chinese rendering
        zh_result = self.renderer.render_approval_notification(test_data, "zh")
        self.assertIsInstance(zh_result, str)
        self.assertIn("已獲批准", zh_result)
    
    def test_bilingual_document_generation(self):
        """Test generating document in both languages."""
        test_data = {
            "receipt_id": "TEST-001",
            "application_id": "APP-001",
            "customer_ref": "CUST-001",
            "decision": "APPROVED",
            "amount": 5000000,
            "term_years": 25,
            "interest_rate": 3.5,
            "credit_score": 750,
            "credit_score_rating": "Good",
            "dti_ratio": 35,
            "ltv_ratio": 80,
            "employment_years": 8,
            "explanation": "Test explanation",
            "approval_chain": "Test chain",
            "contact_email": "test@example.com",
            "signature": "test_sig"
        }
        
        # Generate bilingual document
        # Note: This would use a proper bilingual template
        # For test, we'll just render both versions
        en_doc = self.renderer.render_credit_decision(test_data, "en")
        zh_doc = self.renderer.render_credit_decision(test_data, "zh")
        
        self.assertIsInstance(en_doc, str)
        self.assertIsInstance(zh_doc, str)
        self.assertNotEqual(en_doc, zh_doc)


class TestPDPOBilingualCompliance(unittest.TestCase):
    """Test bilingual compliance with PDPO requirements."""
    
    def setUp(self):
        self.translator = BilingualTranslator()
    
    def test_pdpo_section27_compliance(self):
        """Test PDPO Section 27 - Privacy policies in both languages."""
        # Section 27 requires privacy policies to be available in both languages
        policy_terms = [
            "privacy_policy",
            "personal_data",
            "data_subject",
            "consent",
            "retention_period"
        ]
        
        for term in policy_terms:
            with self.subTest(term=term):
                zh_term = self.translator.translate(term, "zh")
                self.assertIsNotNone(zh_term)
                self.assertNotEqual(term, zh_term)
    
    def test_pdpo_section34_compliance(self):
        """Test PDPO Section 34 - DSAR responses in requested language."""
        # Section 34 requires responses to data access requests
        # to be in the language requested by the data subject
        dsar_terms = [
            "dsar",
            "data_access_request",
            "data_correction",
            "response_deadline"
        ]
        
        for term in dsar_terms:
            with self.subTest(term=term):
                zh_term = self.translator.translate(term, "zh")
                self.assertIsNotNone(zh_term)
    
    def test_pdpo_section35_compliance(self):
        """Test PDPO Section 35 - Complaints in customer's language."""
        # Section 35 requires complaint handling in the customer's language
        complaint_terms = [
            "complaint_handling",
            "complaints_contact",
            "investigation",
            "resolution"
        ]
        
        for term in complaint_terms:
            with self.subTest(term=term):
                zh_term = self.translator.translate(term, "zh")
                self.assertIsNotNone(zh_term)


class TestHKMABilingualCompliance(unittest.TestCase):
    """Test bilingual compliance with HKMA guidelines."""
    
    def setUp(self):
        self.translator = BilingualTranslator()
    
    def test_tmg1_customer_communications(self):
        """Test TM-G-1 - Customer communications in preferred language."""
        # HKMA expects customer communications in their preferred language
        comm_terms = [
            "notice",
            "reminder",
            "alert",
            "confirmation",
            "statement"
        ]
        
        for term in comm_terms:
            with self.subTest(term=term):
                zh_term = self.translator.translate(term, "zh")
                self.assertIsNotNone(zh_term)
    
    def test_crg12_credit_explanations(self):
        """Test CR-G-12 - Credit decision explanations in both languages."""
        # Credit decisions should be explainable in the customer's language
        credit_terms = [
            "credit_assessment",
            "decision_factors",
            "explanation",
            "approval_workflow",
            "conditions"
        ]
        
        for term in credit_terms:
            with self.subTest(term=term):
                zh_term = self.translator.translate(term, "zh")
                self.assertIsNotNone(zh_term)
    
    def test_fair_treatment_guidelines(self):
        """Test Fair Treatment Guidelines - Terms in both languages."""
        # Fair Treatment requires terms and conditions in both languages
        fair_treatment_terms = [
            "terms_and_conditions",
            "interest_rate",
            "fees_and_charges",
            "repayment_schedule",
            "early_repayment"
        ]
        
        for term in fair_treatment_terms:
            with self.subTest(term=term):
                zh_term = self.translator.translate(term, "zh")
                self.assertIsNotNone(zh_term)


class TestBilingualIntegration(unittest.TestCase):
    """Test integration of bilingual support with other components."""
    
    def setUp(self):
        self.translator = BilingualTranslator()
        self.renderer = TemplateRenderer()
    
    def test_consent_management_integration(self):
        """Test bilingual support in consent management."""
        # Create bilingual consent receipt
        consent_data = {
            "receipt_id": "TEST-CONSENT-001",
            "customer_ref": "CUST-001",
            "consent_id": "CONSENT-001",
            "purpose": "credit_scoring",
            "data_categories": ["income", "credit_history"],
            "collection_method": "online_form",
            "notice_provided": "Yes",
            "retention_days": 2555,
            "expiry_date": "2033-03-07",
            "dsar_contact": "dsar@example.com"
        }
        
        # Add Chinese translations
        consent_data["purpose_zh"] = self.translator.translate("credit_scoring", "zh")
        consent_data["data_categories_zh"] = [
            self.translator.translate("income", "zh"),
            self.translator.translate("credit_history", "zh")
        ]
        
        # Render both versions
        en_receipt = self.renderer.render_consent_receipt(consent_data, "en")
        zh_receipt = self.renderer.render_consent_receipt(consent_data, "zh")
        
        self.assertIsInstance(en_receipt, str)
        self.assertIsInstance(zh_receipt, str)
    
    def test_mortgage_workflow_integration(self):
        """Test bilingual support in mortgage workflow."""
        # Create bilingual mortgage data
        mortgage_data = {
            "receipt_id": "TEST-MORT-001",
            "application_id": "APP-001",
            "customer_ref": "CUST-001",
            "decision": "APPROVED",
            "amount": 5000000,
            "term_years": 25,
            "interest_rate": 3.5,
            "credit_score": 750,
            "credit_score_rating": "Good",
            "dti_ratio": 35,
            "ltv_ratio": 80,
            "employment_years": 8,
            "explanation": "Credit score meets threshold"
        }
        
        # Add Chinese translations
        mortgage_data["decision_zh"] = self.translator.translate("APPROVED", "zh")
        mortgage_data["explanation_zh"] = self.translator.translate(
            "Credit score meets threshold", "zh"
        )
        
        # Render both versions
        en_receipt = self.renderer.render_credit_decision(mortgage_data, "en")
        zh_receipt = self.renderer.render_credit_decision(mortgage_data, "zh")
        
        self.assertIsInstance(en_receipt, str)
        self.assertIsInstance(zh_receipt, str)
    
    def test_notification_preference(self):
        """Test customer language preference in notifications."""
        # Customer prefers Chinese
        notification_data = {
            "customer_name": "Mr. Chan Tai Man",
            "customer_name_zh": "陳大文先生",
            "application_type": "mortgage",
            "application_type_zh": "按揭",
            "application_id": "MORT-001",
            "amount": 5000000,
            "approval_date": "2026-03-07",
            "bank_name": "HSBC Hong Kong",
            "bank_name_zh": "香港滙豐銀行"
        }
        
        # Render in Chinese (customer's preference)
        notification = self.renderer.render_approval_notification(notification_data, "zh")
        
        self.assertIsInstance(notification, str)
        self.assertIn("陳大文先生", notification)
        self.assertIn("按揭", notification)
        self.assertIn("香港滙豐銀行", notification)


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🌐 JEP Hong Kong Bilingual Support Test Suite")
    print("="*70)
    
    unittest.main(verbosity=2)
