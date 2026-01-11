"""
Tests for Material API endpoints.

Tests:
- Material creation
- Material retrieval
- Material update
- Material version management
"""

import pytest
from api.models.base import MaterialType, OutputFormat


class TestMaterialCreate:
    """Tests for material creation."""

    def test_create_material_success(self, client, created_topic):
        """Test successful material creation."""
        response = client.post("/api/materials", json={
            "topic_id": created_topic["id"],
            "material_type": "notes",
            "output_format": "pdf",
            "file_path": "subjects/test/notes/test/test.pdf",
            "version": "v1.0"
        })
        assert response.status_code == 201

        data = response.json()
        assert data["topic_id"] == created_topic["id"]
        assert data["material_type"] == "notes"
        assert data["version"] == "v1.0"

    def test_create_material_invalid_topic(self, client):
        """Test material creation with invalid topic."""
        response = client.post("/api/materials", json={
            "topic_id": 9999,
            "material_type": "quiz",
            "output_format": "docx",
            "file_path": "subjects/test/quizzes/test/test-quiz.docx"
        })
        assert response.status_code == 400

    def test_create_quiz_material(self, client, created_topic):
        """Test creating quiz material."""
        response = client.post("/api/materials", json={
            "topic_id": created_topic["id"],
            "material_type": "quiz",
            "output_format": "docx",
            "file_path": "subjects/test/quizzes/test/test-quiz.docx",
            "metadata_json": '{"clos": ["CLO1", "CLO2"], "time_duration": 60}'
        })
        assert response.status_code == 201

        data = response.json()
        assert data["material_type"] == "quiz"
        assert data["output_format"] == "docx"


class TestMaterialRead:
    """Tests for material retrieval."""

    @pytest.fixture
    def created_material(self, client, created_topic):
        """Create and return a material."""
        response = client.post("/api/materials", json={
            "topic_id": created_topic["id"],
            "material_type": "notes",
            "output_format": "pdf",
            "file_path": "subjects/test/notes/test/test.pdf"
        })
        return response.json()

    def test_get_material_by_id(self, client, created_material):
        """Test getting material by ID."""
        material_id = created_material["id"]
        response = client.get(f"/api/materials/{material_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == material_id

    def test_get_material_not_found(self, client):
        """Test getting non-existent material."""
        response = client.get("/api/materials/9999")
        assert response.status_code == 404

    def test_get_material_includes_topic_info(self, client, created_material, created_topic):
        """Test that material detail includes topic info."""
        material_id = created_material["id"]
        response = client.get(f"/api/materials/{material_id}")
        assert response.status_code == 200

        data = response.json()
        assert "topic_name" in data
        assert "subject_name" in data


class TestMaterialList:
    """Tests for material listing."""

    def test_list_materials_empty(self, client):
        """Test listing materials when empty."""
        response = client.get("/api/materials")
        assert response.status_code == 200

        data = response.json()
        assert data["materials"] == []

    def test_list_materials_filter_by_type(self, client, created_topic):
        """Test filtering materials by type."""
        # Create notes material
        client.post("/api/materials", json={
            "topic_id": created_topic["id"],
            "material_type": "notes",
            "output_format": "pdf",
            "file_path": "test.pdf"
        })

        # Create quiz material
        client.post("/api/materials", json={
            "topic_id": created_topic["id"],
            "material_type": "quiz",
            "output_format": "docx",
            "file_path": "test-quiz.docx"
        })

        # Filter by notes
        response = client.get("/api/materials?material_type=notes")
        assert response.status_code == 200

        data = response.json()
        assert all(m["material_type"] == "notes" for m in data["materials"])


class TestMaterialVersions:
    """Tests for material version management."""

    @pytest.fixture
    def created_material(self, client, created_topic):
        """Create and return a material."""
        response = client.post("/api/materials", json={
            "topic_id": created_topic["id"],
            "material_type": "notes",
            "output_format": "pdf",
            "file_path": "test.pdf",
            "metadata_json": '{"version_history": [{"version": "v1.0", "date": "2026-01-11", "changes": "Initial"}]}'
        })
        return response.json()

    def test_get_version_history(self, client, created_material):
        """Test getting material version history."""
        material_id = created_material["id"]
        response = client.get(f"/api/materials/{material_id}/versions")
        assert response.status_code == 200

        data = response.json()
        assert data["material_id"] == material_id
        assert "current_version" in data

    def test_increment_version(self, client, created_material):
        """Test incrementing material version."""
        material_id = created_material["id"]
        response = client.post(
            f"/api/materials/{material_id}/increment-version",
            params={"changes_description": "Added new section"}
        )
        assert response.status_code == 200

        data = response.json()
        assert data["version"] == "v1.1"
