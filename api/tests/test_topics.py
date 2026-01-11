"""
Tests for Topic API endpoints.

Tests:
- Topic creation
- Topic retrieval
- Topic update
- Topic deletion
- Topic-subject relationships
"""

import pytest


class TestTopicCreate:
    """Tests for topic creation."""

    def test_create_topic_success(self, client, created_subject, sample_topic_data):
        """Test successful topic creation."""
        data = {**sample_topic_data, "subject_id": created_subject["id"]}
        response = client.post("/api/topics", json=data)
        assert response.status_code == 201

        result = response.json()
        assert result["name"] == sample_topic_data["name"]
        assert result["slug"] == "binary-search-trees"
        assert result["subject_id"] == created_subject["id"]

    def test_create_topic_invalid_subject(self, client, sample_topic_data):
        """Test topic creation with invalid subject."""
        data = {**sample_topic_data, "subject_id": 9999}
        response = client.post("/api/topics", json=data)
        assert response.status_code == 400
        assert "not found" in response.json()["detail"]

    def test_create_topic_duplicate_fails(self, client, created_subject, created_topic):
        """Test that duplicate topic creation fails."""
        response = client.post("/api/topics", json={
            "name": "Binary Search Trees",
            "subject_id": created_subject["id"]
        })
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_create_topic_sanitizes_name(self, client, created_subject):
        """Test that topic name is properly sanitized."""
        response = client.post("/api/topics", json={
            "name": "Hash Tables & Maps",
            "subject_id": created_subject["id"]
        })
        assert response.status_code == 201
        assert response.json()["slug"] == "hash-tables-maps"


class TestTopicRead:
    """Tests for topic retrieval."""

    def test_get_topic_by_id(self, client, created_topic):
        """Test getting topic by ID."""
        topic_id = created_topic["id"]
        response = client.get(f"/api/topics/{topic_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == topic_id
        assert "subject_name" in data

    def test_get_topic_not_found(self, client):
        """Test getting non-existent topic."""
        response = client.get("/api/topics/9999")
        assert response.status_code == 404

    def test_get_topic_includes_subject_info(self, client, created_topic, created_subject):
        """Test that topic detail includes subject info."""
        topic_id = created_topic["id"]
        response = client.get(f"/api/topics/{topic_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["subject_name"] == created_subject["name"]
        assert data["subject_slug"] == created_subject["slug"]


class TestTopicList:
    """Tests for topic listing."""

    def test_list_topics_empty(self, client):
        """Test listing topics when empty."""
        response = client.get("/api/topics")
        assert response.status_code == 200

        data = response.json()
        assert data["topics"] == []
        assert data["total"] == 0

    def test_list_topics_with_data(self, client, created_topic):
        """Test listing topics with data."""
        response = client.get("/api/topics")
        assert response.status_code == 200

        data = response.json()
        assert len(data["topics"]) == 1

    def test_list_topics_filter_by_subject(self, client, created_subject, created_topic):
        """Test filtering topics by subject."""
        response = client.get(f"/api/topics?subject_id={created_subject['id']}")
        assert response.status_code == 200

        data = response.json()
        assert len(data["topics"]) == 1
        assert data["topics"][0]["subject_id"] == created_subject["id"]


class TestTopicUpdate:
    """Tests for topic update."""

    def test_update_topic_name(self, client, created_topic):
        """Test updating topic name."""
        topic_id = created_topic["id"]
        response = client.put(f"/api/topics/{topic_id}", json={
            "name": "AVL Trees"
        })
        assert response.status_code == 200

        data = response.json()
        assert data["name"] == "AVL Trees"
        assert data["slug"] == "avl-trees"

    def test_update_topic_not_found(self, client):
        """Test updating non-existent topic."""
        response = client.put("/api/topics/9999", json={
            "name": "New Name"
        })
        assert response.status_code == 404


class TestTopicDelete:
    """Tests for topic deletion."""

    def test_delete_topic(self, client, created_topic):
        """Test deleting a topic."""
        topic_id = created_topic["id"]
        response = client.delete(f"/api/topics/{topic_id}")
        assert response.status_code == 204

        # Verify deletion
        response = client.get(f"/api/topics/{topic_id}")
        assert response.status_code == 404

    def test_delete_topic_not_found(self, client):
        """Test deleting non-existent topic."""
        response = client.delete("/api/topics/9999")
        assert response.status_code == 404


class TestSubjectTopics:
    """Tests for subject-topic relationships."""

    def test_list_subject_topics(self, client, created_subject, created_topic):
        """Test listing topics for a subject."""
        slug = created_subject["slug"]
        response = client.get(f"/api/subjects/{slug}/topics")
        assert response.status_code == 200

        data = response.json()
        assert len(data["topics"]) == 1
        assert data["topics"][0]["id"] == created_topic["id"]

    def test_list_subject_topics_not_found(self, client):
        """Test listing topics for non-existent subject."""
        response = client.get("/api/subjects/nonexistent/topics")
        assert response.status_code == 404
