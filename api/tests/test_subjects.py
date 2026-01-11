"""
Tests for Subject API endpoints.

Tests:
- Subject creation
- Subject retrieval
- Subject update
- Subject deletion
- Subject listing
- Name sanitization
"""

import pytest


class TestSubjectCreate:
    """Tests for subject creation."""

    def test_create_subject_success(self, client, sample_subject_data):
        """Test successful subject creation."""
        response = client.post("/api/subjects", json=sample_subject_data)
        assert response.status_code == 201

        data = response.json()
        assert data["name"] == sample_subject_data["name"]
        assert data["slug"] == "data-structures-and-algorithms"
        assert "id" in data
        assert "created_at" in data

    def test_create_subject_with_description(self, client):
        """Test subject creation with description."""
        response = client.post("/api/subjects", json={
            "name": "Organic Chemistry",
            "description": "Study of carbon compounds"
        })
        assert response.status_code == 201

        data = response.json()
        assert data["description"] == "Study of carbon compounds"

    def test_create_subject_sanitizes_name(self, client):
        """Test that subject name is properly sanitized to slug."""
        test_cases = [
            ("Data Structures and Algorithms", "data-structures-and-algorithms"),
            ("The French Revolution (1789-1799)", "the-french-revolution-1789-1799"),
            ("Alkene Reactions & Mechanisms", "alkene-reactions-mechanisms"),
            ("Machine   Learning", "machine-learning"),
        ]

        for name, expected_slug in test_cases:
            response = client.post("/api/subjects", json={"name": name})
            if response.status_code == 201:
                assert response.json()["slug"] == expected_slug

    def test_create_subject_duplicate_fails(self, client, created_subject):
        """Test that duplicate subject creation fails."""
        response = client.post("/api/subjects", json={
            "name": "Data Structures and Algorithms"
        })
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]


class TestSubjectRead:
    """Tests for subject retrieval."""

    def test_get_subject_by_slug(self, client, created_subject):
        """Test getting subject by slug."""
        slug = created_subject["slug"]
        response = client.get(f"/api/subjects/{slug}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == created_subject["id"]
        assert data["name"] == created_subject["name"]

    def test_get_subject_not_found(self, client):
        """Test getting non-existent subject."""
        response = client.get("/api/subjects/nonexistent")
        assert response.status_code == 404

    def test_get_subject_includes_statistics(self, client, created_subject):
        """Test that subject detail includes statistics."""
        slug = created_subject["slug"]
        response = client.get(f"/api/subjects/{slug}")
        assert response.status_code == 200

        data = response.json()
        assert "topic_count" in data
        assert "notes_count" in data
        assert "quiz_count" in data
        assert "presentation_count" in data


class TestSubjectList:
    """Tests for subject listing."""

    def test_list_subjects_empty(self, client):
        """Test listing subjects when empty."""
        response = client.get("/api/subjects")
        assert response.status_code == 200

        data = response.json()
        assert data["subjects"] == []
        assert data["total"] == 0

    def test_list_subjects_with_data(self, client, created_subject):
        """Test listing subjects with data."""
        response = client.get("/api/subjects")
        assert response.status_code == 200

        data = response.json()
        assert len(data["subjects"]) == 1
        assert data["total"] == 1

    def test_list_subjects_pagination(self, client):
        """Test subject listing pagination."""
        # Create multiple subjects
        for i in range(5):
            client.post("/api/subjects", json={"name": f"Subject {i}"})

        # Test pagination
        response = client.get("/api/subjects?page=1&page_size=2")
        assert response.status_code == 200

        data = response.json()
        assert len(data["subjects"]) == 2
        assert data["page"] == 1
        assert data["page_size"] == 2

    def test_list_subjects_search(self, client):
        """Test subject search."""
        client.post("/api/subjects", json={"name": "Computer Science"})
        client.post("/api/subjects", json={"name": "Political Science"})
        client.post("/api/subjects", json={"name": "Mathematics"})

        response = client.get("/api/subjects?search=Science")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 2


class TestSubjectUpdate:
    """Tests for subject update."""

    def test_update_subject_name(self, client, created_subject):
        """Test updating subject name."""
        slug = created_subject["slug"]
        response = client.put(f"/api/subjects/{slug}", json={
            "name": "Advanced Data Structures"
        })
        assert response.status_code == 200

        data = response.json()
        assert data["name"] == "Advanced Data Structures"
        assert data["slug"] == "advanced-data-structures"

    def test_update_subject_description(self, client, created_subject):
        """Test updating subject description."""
        slug = created_subject["slug"]
        response = client.put(f"/api/subjects/{slug}", json={
            "description": "Updated description"
        })
        assert response.status_code == 200

        data = response.json()
        assert data["description"] == "Updated description"

    def test_update_subject_not_found(self, client):
        """Test updating non-existent subject."""
        response = client.put("/api/subjects/nonexistent", json={
            "name": "New Name"
        })
        assert response.status_code == 404


class TestSubjectDelete:
    """Tests for subject deletion."""

    def test_delete_subject(self, client, created_subject):
        """Test deleting a subject."""
        slug = created_subject["slug"]
        response = client.delete(f"/api/subjects/{slug}")
        assert response.status_code == 204

        # Verify deletion
        response = client.get(f"/api/subjects/{slug}")
        assert response.status_code == 404

    def test_delete_subject_not_found(self, client):
        """Test deleting non-existent subject."""
        response = client.delete("/api/subjects/nonexistent")
        assert response.status_code == 404
