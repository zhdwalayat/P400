"""
Tests for Task API endpoints.

Tests:
- Task creation
- Task retrieval
- Task status updates
- Task statistics
"""

import pytest
from api.models.base import TaskStatus, MaterialType


class TestTaskCreate:
    """Tests for task creation."""

    def test_create_task_success(self, client, created_subject, sample_task_data):
        """Test successful task creation."""
        data = {**sample_task_data, "subject_id": created_subject["id"]}
        response = client.post("/api/tasks", json=data)
        assert response.status_code == 201

        result = response.json()
        assert result["subject_id"] == created_subject["id"]
        assert result["material_type"] == "quiz"
        assert result["status"] == "pending"

    def test_create_task_invalid_subject(self, client, sample_task_data):
        """Test task creation with invalid subject."""
        data = {**sample_task_data, "subject_id": 9999}
        response = client.post("/api/tasks", json=data)
        assert response.status_code == 400

    def test_create_task_with_topic_id(self, client, created_subject, created_topic):
        """Test task creation with existing topic."""
        response = client.post("/api/tasks", json={
            "subject_id": created_subject["id"],
            "topic_id": created_topic["id"],
            "material_type": "notes"
        })
        assert response.status_code == 201

        data = response.json()
        assert data["topic_id"] == created_topic["id"]


class TestTaskRead:
    """Tests for task retrieval."""

    @pytest.fixture
    def created_task(self, client, created_subject, sample_task_data):
        """Create and return a task."""
        data = {**sample_task_data, "subject_id": created_subject["id"]}
        response = client.post("/api/tasks", json=data)
        return response.json()

    def test_get_task_by_id(self, client, created_task):
        """Test getting task by ID."""
        task_id = created_task["id"]
        response = client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == task_id
        assert "subject_name" in data

    def test_get_task_not_found(self, client):
        """Test getting non-existent task."""
        response = client.get("/api/tasks/9999")
        assert response.status_code == 404


class TestTaskList:
    """Tests for task listing."""

    def test_list_tasks_empty(self, client):
        """Test listing tasks when empty."""
        response = client.get("/api/tasks")
        assert response.status_code == 200

        data = response.json()
        assert data["tasks"] == []

    def test_list_tasks_filter_by_status(self, client, created_subject, sample_task_data):
        """Test filtering tasks by status."""
        # Create a task
        data = {**sample_task_data, "subject_id": created_subject["id"]}
        client.post("/api/tasks", json=data)

        # Filter by pending
        response = client.get("/api/tasks?status=pending")
        assert response.status_code == 200

        data = response.json()
        assert all(t["status"] == "pending" for t in data["tasks"])

    def test_get_pending_tasks(self, client, created_subject, sample_task_data):
        """Test getting pending tasks endpoint."""
        data = {**sample_task_data, "subject_id": created_subject["id"]}
        client.post("/api/tasks", json=data)

        response = client.get("/api/tasks/pending")
        assert response.status_code == 200

        tasks = response.json()
        assert isinstance(tasks, list)
        assert all(t["status"] == "pending" for t in tasks)


class TestTaskStatusUpdate:
    """Tests for task status updates."""

    @pytest.fixture
    def created_task(self, client, created_subject, sample_task_data):
        """Create and return a task."""
        data = {**sample_task_data, "subject_id": created_subject["id"]}
        response = client.post("/api/tasks", json=data)
        return response.json()

    def test_update_status_to_in_progress(self, client, created_task):
        """Test updating task status to in_progress."""
        task_id = created_task["id"]
        response = client.put(f"/api/tasks/{task_id}/status", json={
            "status": "in_progress"
        })
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "in_progress"
        assert data["started_at"] is not None

    def test_update_status_to_completed(self, client, created_task):
        """Test updating task status to completed."""
        task_id = created_task["id"]

        # First move to in_progress
        client.put(f"/api/tasks/{task_id}/status", json={"status": "in_progress"})

        # Then complete
        response = client.put(f"/api/tasks/{task_id}/status", json={
            "status": "completed"
        })
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "completed"
        assert data["completed_at"] is not None

    def test_update_status_to_failed(self, client, created_task):
        """Test updating task status to failed with error message."""
        task_id = created_task["id"]
        response = client.put(f"/api/tasks/{task_id}/status", json={
            "status": "failed",
            "error_message": "Generation failed due to invalid input"
        })
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "failed"
        assert data["error_message"] == "Generation failed due to invalid input"


class TestTaskStatistics:
    """Tests for task statistics."""

    def test_get_task_statistics(self, client, created_subject, sample_task_data):
        """Test getting task statistics."""
        # Create some tasks
        data = {**sample_task_data, "subject_id": created_subject["id"]}
        client.post("/api/tasks", json=data)
        client.post("/api/tasks", json=data)

        response = client.get("/api/tasks/stats")
        assert response.status_code == 200

        stats = response.json()
        assert "total_tasks" in stats
        assert "pending" in stats
        assert "completed" in stats
        assert "by_material_type" in stats


class TestTaskDelete:
    """Tests for task deletion."""

    @pytest.fixture
    def created_task(self, client, created_subject, sample_task_data):
        """Create and return a task."""
        data = {**sample_task_data, "subject_id": created_subject["id"]}
        response = client.post("/api/tasks", json=data)
        return response.json()

    def test_delete_task(self, client, created_task):
        """Test deleting a task."""
        task_id = created_task["id"]
        response = client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 204

        # Verify deletion
        response = client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 404

    def test_delete_task_not_found(self, client):
        """Test deleting non-existent task."""
        response = client.delete("/api/tasks/9999")
        assert response.status_code == 404
