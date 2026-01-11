"""
Task Management API for the Educational Material Automation System.

This API provides endpoints for:
- Managing subjects (CRUD operations)
- Managing topics per subject
- Tracking generated materials (notes, quizzes, presentations)
- Managing generation tasks and their status
- Utility operations (name sanitization, Bloom's keywords)

Built with:
- FastAPI for REST API
- SQLModel for database models
- Pydantic for request/response validation
"""

__version__ = "1.0.0"
