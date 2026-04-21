"""
Test suite for OCR Desktop API
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python-api'))

from main import app, ocr_manager

client = TestClient(app)

class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self):
        """Test basic health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "engines" in data
        assert "lite" in data["engines"]
        assert "pro" in data["engines"]

class TestRecognizeEndpoint:
    """Test recognition endpoint"""
    
    def test_recognize_with_valid_request(self):
        """Test recognition with valid request"""
        request_data = {
            "file_path": "/tmp/test_image.png",
            "language": "ch",
            "doc_type": "general",
            "performance_mode": "lite",
            "export_formats": ["txt", "md"],
            "enable_learning": True
        }
        
        response = client.post("/recognize", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert "document_id" in data
        assert "text_content" in data
        assert "confidence" in data
        assert "engine_used" in data
    
    def test_recognize_with_invalid_mode(self):
        """Test recognition with invalid performance mode"""
        request_data = {
            "file_path": "/tmp/test_image.png",
            "performance_mode": "invalid_mode"
        }
        
        response = client.post("/recognize", json=request_data)
        # Should still work with default handling
        assert response.status_code == 200

class TestFeedbackEndpoint:
    """Test feedback endpoint"""
    
    def test_submit_feedback(self):
        """Test submitting feedback"""
        feedback_data = {
            "document_id": "doc_test_123",
            "page_number": 1,
            "original_text": "OCR result",
            "corrected_text": "Corrected result",
            "confidence": 0.85,
            "allow_training": True
        }
        
        response = client.post("/feedback", json=feedback_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

class TestExportEndpoint:
    """Test export endpoint"""
    
    def test_export_supported_format(self):
        """Test export with supported format"""
        response = client.get("/export/doc_test_123/txt")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["format"] == "txt"
    
    def test_export_unsupported_format(self):
        """Test export with unsupported format"""
        response = client.get("/export/doc_test_123/pdf")
        assert response.status_code == 400

class TestEngineDecisionEndpoint:
    """Test engine decision endpoint"""
    
    def test_get_decision_existing_document(self):
        """Test getting decision for existing document"""
        # First create a document
        request_data = {
            "file_path": "/tmp/test.png",
            "performance_mode": "lite"
        }
        response = client.post("/recognize", json=request_data)
        doc_id = response.json()["document_id"]
        
        # Then get decision
        response = client.get(f"/engine/decision/{doc_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["document_id"] == doc_id
        assert "initial_engine" in data
        assert "final_engine" in data
    
    def test_get_decision_nonexistent_document(self):
        """Test getting decision for non-existent document"""
        response = client.get("/engine/decision/nonexistent_doc")
        assert response.status_code == 404

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
