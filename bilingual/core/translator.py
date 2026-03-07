#!/usr/bin/env python3
"""
JEP Hong Kong Bilingual Translator
=====================================

Core translation utilities for English-Traditional Chinese support
across all JEP Hong Kong components.

This module provides:
- Translation dictionaries for all common terms
- Dynamic translation of receipts and documents
- Language preference management
- Bilingual template rendering
"""

import json
import re
from typing import Dict, Any, Optional, List, Union
from enum import Enum
from datetime import datetime


class Language(Enum):
    """Supported languages"""
    ENGLISH = "en"
    TRADITIONAL_CHINESE = "zh"


class BilingualTranslator:
    """
    Core translator for English-Traditional Chinese bilingual support.
    
    Features:
    - Bidirectional translation (EN ↔ ZH)
    - Context-aware term translation
    - Dynamic template rendering
    - Language preference management
    """
    
    def __init__(self, default_language: str = "en"):
        """
        Initialize translator with language preference.
        
        Args:
            default_language: Default language ("en" or "zh")
        """
        self.default_language = default_language
        self.current_language = default_language
        
        # Load translation dictionaries
        self.translations = self._load_translations()
        self.reverse_translations = self._build_reverse_index()
        
        # Load context-specific terms
        self.context_terms = self._load_context_terms()
        
        # Currency and number formatting
        self.currency_formats = {
            "en": "HKD {amount:,.0f}",
            "zh": "港元 {amount:,.0f}"
        }
        
        self.date_formats = {
            "en": "%d %B %Y",
            "zh": "%Y年%m月%d日"
        }
        
        print(f"✅ Bilingual Translator initialized")
        print(f"   Default Language: {default_language}")
        print(f"   Terms loaded: {len(self.translations)}")
    
    def _load_translations(self) -> Dict[str, str]:
        """
        Load master translation dictionary.
        
        Returns:
            Dictionary mapping English terms to Traditional Chinese
        """
        return {
            # =================================================================
            # Common Operations
            # =================================================================
            "credit_scoring": "信用評分",
            "loan_approval": "貸款審批",
            "mortgage_application": "按揭申請",
            "customer_due_diligence": "客戶盡職審查",
            "property_valuation": "物業估價",
            "funds_disbursement": "資金發放",
            "account_opening": "開立戶口",
            "transaction_monitoring": "交易監察",
            "risk_assessment": "風險評估",
            "compliance_check": "合規審查",
            "identity_verification": "身份驗證",
            "document_verification": "文件核實",
            "consent_management": "同意管理",
            "data_access_request": "查閱資料要求",
            "data_correction": "資料更正",
            "data_deletion": "資料刪除",
            "complaint_handling": "投訴處理",
            "audit_trail": "審計追蹤",
            "regulatory_reporting": "監管申報",
            
            # =================================================================
            # Risk Levels
            # =================================================================
            "LOW": "低風險",
            "MEDIUM": "中風險",
            "HIGH": "高風險",
            "CRITICAL": "嚴重風險",
            
            # =================================================================
            # Decision Outcomes
            # =================================================================
            "APPROVED": "已批准",
            "DECLINED": "已拒絕",
            "PENDING": "待處理",
            "WITHDRAWN": "已撤回",
            "EXPIRED": "已逾期",
            "CANCELLED": "已取消",
            "UNDER_REVIEW": "審核中",
            "AWAITING_APPROVAL": "待審批",
            
            # =================================================================
            # Common Terms
            # =================================================================
            "customer": "客戶",
            "application": "申請",
            "amount": "金額",
            "date": "日期",
            "time": "時間",
            "reference": "參考編號",
            "receipt_id": "收據編號",
            "transaction_id": "交易編號",
            "signature": "電子簽署",
            "timestamp": "時間戳記",
            "status": "狀態",
            "remarks": "備註",
            "notes": "備註",
            "details": "詳情",
            "summary": "摘要",
            "report": "報告",
            
            # =================================================================
            # PDPO Terms
            # =================================================================
            "personal_data": "個人資料",
            "sensitive_data": "敏感資料",
            "data_subject": "資料當事人",
            "data_user": "資料使用者",
            "data_processor": "資料處理者",
            "consent": "同意",
            "consent_id": "同意編號",
            "consent_withdrawn": "同意已撤回",
            "privacy_policy": "私隱政策",
            "privacy_notice": "私隱通知",
            "pcpd": "私隱專員公署",
            "pcpd_registration": "私隱專員公署登記號碼",
            "dsar": "查閱資料要求",
            "dsar_contact": "查閱資料要求聯絡人",
            "data_breach": "資料外洩",
            "data_protection_officer": "資料保障主任",
            "collection_purpose": "收集目的",
            "data_categories": "資料類別",
            "retention_period": "保留期限",
            "data_sharing": "資料共享",
            "cross_border_transfer": "跨境資料轉移",
            
            # =================================================================
            # HKMA Terms
            # =================================================================
            "hkma": "香港金融管理局",
            "banking_license": "銀行牌照",
            "authorized_institution": "認可機構",
            "mortgage": "按揭",
            "loan": "貸款",
            "credit_assessment": "信貸評估",
            "credit_score": "信貸評分",
            "credit_history": "信貸紀錄",
            "credit_limit": "信貸限額",
            "interest_rate": "利率",
            "loan_term": "貸款年期",
            "repayment_schedule": "還款時間表",
            "monthly_repayment": "每月還款額",
            "down_payment": "首期付款",
            "property_value": "物業價值",
            "ltv_ratio": "按揭成數",
            "dti_ratio": "債務收入比率",
            "dsr": "供款與入息比率",
            "employment_years": "就業年資",
            "income_verification": "收入核實",
            "asset_verification": "資產核實",
            "approval_workflow": "審批流程",
            "approval_level": "審批級別",
            "loan_officer": "貸款主任",
            "senior_manager": "高級經理",
            "department_head": "部門主管",
            "credit_committee": "信貸委員會",
            "board_approval": "董事會批准",
            
            # =================================================================
            # AML/CFT Terms
            # =================================================================
            "aml": "打擊洗錢",
            "cft": "反恐怖分子資金籌集",
            "cdd": "客戶盡職審查",
            "edd": "加強盡職審查",
            "pep": "政治人物",
            "sanctions": "制裁",
            "adverse_media": "負面新聞",
            "source_of_funds": "資金來源",
            "source_of_wealth": "財富來源",
            "transaction_monitoring": "交易監察",
            "suspicious_transaction": "可疑交易",
            "str": "可疑交易報告",
            "jfiu": "聯合財富情報組",
            
            # =================================================================
            # Status Indicators
            # =================================================================
            "active": "有效",
            "inactive": "無效",
            "suspended": "暫停",
            "terminated": "終止",
            "expired": "逾期",
            "valid": "有效",
            "invalid": "無效",
            "verified": "已核實",
            "unverified": "未核實",
            "pending": "待處理",
            "processing": "處理中",
            "completed": "已完成",
            "failed": "失敗",
            "success": "成功",
            "error": "錯誤",
            "warning": "警告",
            
            # =================================================================
            # Months
            # =================================================================
            "January": "一月",
            "February": "二月",
            "March": "三月",
            "April": "四月",
            "May": "五月",
            "June": "六月",
            "July": "七月",
            "August": "八月",
            "September": "九月",
            "October": "十月",
            "November": "十一月",
            "December": "十二月",
            
            # =================================================================
            # Common Phrases
            # =================================================================
            "thank_you": "謝謝",
            "please_contact": "請聯絡",
            "for_more_information": "了解更多資訊",
            "if_you_have_any_questions": "如有任何疑問",
            "this_is_an_automated_message": "此為自動訊息",
            "do_not_reply": "請勿回覆",
            "confidential": "保密",
            "urgent": "緊急",
            "important": "重要",
            "notice": "通知",
            "reminder": "提醒",
            "confirmation": "確認",
            "receipt": "收據",
            "certificate": "證明書",
        }
    
    def _build_reverse_index(self) -> Dict[str, str]:
        """Build reverse index for Chinese to English translation."""
        return {v: k for k, v in self.translations.items()}
    
    def _load_context_terms(self) -> Dict[str, Dict[str, str]]:
        """Load context-specific term translations."""
        return {
            "credit_scoring": {
                "en": {
                    "excellent": "Excellent (800+)",
                    "good": "Good (700-799)",
                    "fair": "Fair (600-699)",
                    "poor": "Poor (below 600)"
                },
                "zh": {
                    "excellent": "優良（800分以上）",
                    "good": "良好（700-799分）",
                    "fair": "一般（600-699分）",
                    "poor": "較差（600分以下）"
                }
            },
            "ltv_ratio": {
                "en": {
                    "low": "Low LTV (below 60%)",
                    "medium": "Medium LTV (60-80%)",
                    "high": "High LTV (above 80%)"
                },
                "zh": {
                    "low": "低按揭成數（低於60%）",
                    "medium": "中按揭成數（60-80%）",
                    "high": "高按揭成數（高於80%）"
                }
            },
            "dti_ratio": {
                "en": {
                    "low": "Low DTI (below 35%)",
                    "medium": "Medium DTI (35-45%)",
                    "high": "High DTI (above 45%)"
                },
                "zh": {
                    "low": "低債務收入比率（低於35%）",
                    "medium": "中債務收入比率（35-45%）",
                    "high": "高債務收入比率（高於45%）"
                }
            }
        }
    
    def translate(self, text: str, to_lang: Optional[str] = None) -> str:
        """
        Translate text to target language.
        
        Args:
            text: Text to translate
            to_lang: Target language ("en" or "zh"), defaults to current language
        
        Returns:
            Translated text
        """
        if to_lang is None:
            to_lang = self.current_language
        
        # If target is English and text is already English, return as is
        if to_lang == "en" and text.isascii():
            return text
        
        # If target is Chinese, translate from English
        if to_lang == "zh":
            # Check if text is a known term
            if text in self.translations:
                return self.translations[text]
            
            # Check if text contains known patterns
            for eng, chi in self.translations.items():
                if eng.lower() in text.lower():
                    return text.replace(eng, chi)
            
            # Return original if no translation found
            return text
        
        # If target is English, translate from Chinese
        if to_lang == "en" and text in self.reverse_translations:
            return self.reverse_translations[text]
        
        return text
    
    def translate_dict(self, data: Dict[str, Any], to_lang: Optional[str] = None) -> Dict[str, Any]:
        """
        Recursively translate dictionary keys and values.
        
        Args:
            data: Dictionary to translate
            to_lang: Target language
        
        Returns:
            Translated dictionary
        """
        if to_lang is None:
            to_lang = self.current_language
        
        if to_lang == "en":
            return data
        
        translated = {}
        for key, value in data.items():
            # Translate key
            zh_key = self.translate(key, "zh")
            
            # Translate value based on type
            if isinstance(value, dict):
                translated[zh_key] = self.translate_dict(value, "zh")
            elif isinstance(value, list):
                translated[zh_key] = [
                    self.translate_dict(item, "zh") if isinstance(item, dict)
                    else self.translate(str(item), "zh") if isinstance(item, str)
                    else item
                    for item in value
                ]
            elif isinstance(value, str):
                translated[zh_key] = self.translate(value, "zh")
            else:
                translated[zh_key] = value
        
        return translated
    
    def translate_context_term(self, context: str, term: str, to_lang: Optional[str] = None) -> str:
        """
        Translate context-specific terms.
        
        Args:
            context: Context category (e.g., "credit_scoring")
            term: Term to translate (e.g., "excellent")
            to_lang: Target language
        
        Returns:
            Context-appropriate translation
        """
        if to_lang is None:
            to_lang = self.current_language
        
        if context in self.context_terms:
            if term in self.context_terms[context][to_lang]:
                return self.context_terms[context][to_lang][term]
        
        return self.translate(term, to_lang)
    
    def format_currency(self, amount: float, to_lang: Optional[str] = None) -> str:
        """
        Format currency according to language.
        
        Args:
            amount: Amount in HKD
            to_lang: Target language
        
        Returns:
            Formatted currency string
        """
        if to_lang is None:
            to_lang = self.current_language
        
        format_str = self.currency_formats.get(to_lang, self.currency_formats["en"])
        return format_str.format(amount=amount)
    
    def format_date(self, dt: datetime, to_lang: Optional[str] = None) -> str:
        """
        Format date according to language.
        
        Args:
            dt: Datetime object
            to_lang: Target language
        
        Returns:
            Formatted date string
        """
        if to_lang is None:
            to_lang = self.current_language
        
        format_str = self.date_formats.get(to_lang, self.date_formats["en"])
        return dt.strftime(format_str)
    
    def set_language(self, language: str) -> None:
        """Set current language for subsequent translations."""
        if language in ["en", "zh"]:
            self.current_language = language
        else:
            raise ValueError(f"Unsupported language: {language}")
    
    def get_bilingual_text(self, en_text: str, zh_text: str, lang: Optional[str] = None) -> str:
        """
        Get text in specified language, falling back to English if not available.
        
        Args:
            en_text: English text
            zh_text: Traditional Chinese text
            lang: Requested language
        
        Returns:
            Text in requested language
        """
        if lang is None:
            lang = self.current_language
        
        if lang == "zh" and zh_text:
            return zh_text
        return en_text
    
    def detect_language(self, text: str) -> str:
        """
        Detect whether text is English or Traditional Chinese.
        
        Args:
            text: Text to analyze
        
        Returns:
            "en" or "zh"
        """
        # Check for Chinese characters (Unicode range)
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        if len(chinese_chars) > len(text) * 0.3:  # >30% Chinese characters
            return "zh"
        return "en"
    
    def create_bilingual_receipt(self, en_data: Dict[str, Any], zh_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a bilingual receipt with both language versions.
        
        Args:
            en_data: English version data
            zh_data: Traditional Chinese version data
        
        Returns:
            Bilingual receipt with both versions
        """
        return {
            "en": en_data,
            "zh": zh_data,
            "languages": ["en", "zh"],
            "default_language": self.default_language,
            "generated_at": datetime.now().isoformat()
        }
    
    def extract_language_version(self, bilingual_receipt: Dict[str, Any], lang: str) -> Dict[str, Any]:
        """
        Extract single language version from bilingual receipt.
        
        Args:
            bilingual_receipt: Bilingual receipt with both versions
            lang: Requested language
        
        Returns:
            Receipt in requested language
        """
        if lang in bilingual_receipt:
            return bilingual_receipt[lang]
        return bilingual_receipt.get(self.default_language, {})


# Singleton instance for global use
_default_translator = None


def get_translator(default_language: str = "en") -> BilingualTranslator:
    """Get or create default translator instance."""
    global _default_translator
    if _default_translator is None:
        _default_translator = BilingualTranslator(default_language)
    return _default_translator


# Example usage
if __name__ == "__main__":
    translator = BilingualTranslator()
    
    # Test basic translation
    print("\n🔤 Basic Translation Tests:")
    print(f"   'credit_scoring' → {translator.translate('credit_scoring', 'zh')}")
    print(f"   'APPROVED' → {translator.translate('APPROVED', 'zh')}")
    print(f"   'customer' → {translator.translate('customer', 'zh')}")
    
    # Test context terms
    print("\n🎯 Context Term Tests:")
    print(f"   'excellent' (credit) → {translator.translate_context_term('credit_scoring', 'excellent', 'zh')}")
    print(f"   'high' (LTV) → {translator.translate_context_term('ltv_ratio', 'high', 'zh')}")
    
    # Test formatting
    print("\n💰 Formatting Tests:")
    print(f"   Currency: {translator.format_currency(5000000, 'zh')}")
    print(f"   Date: {translator.format_date(datetime.now(), 'zh')}")
    
    # Test dictionary translation
    test_dict = {
        "customer_id": "CUST-123",
        "application_id": "APP-2026-001",
        "amount": 5000000,
        "status": "APPROVED",
        "credit_score": 750,
        "decision_factors": {
            "dti_ratio": 35,
            "ltv_ratio": 80
        }
    }
    
    print("\n📚 Dictionary Translation:")
    translated = translator.translate_dict(test_dict, "zh")
    print(json.dumps(translated, indent=2, ensure_ascii=False))
    
    print("\n✅ Translator tests complete")
