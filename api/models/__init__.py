"""
Database models for the Task Management API.

Models:
- Subject: Academic subjects (e.g., "Data Structures and Algorithms")
- Topic: Topics within subjects (e.g., "Binary Search Trees")
- Material: Generated educational materials (notes, quizzes, presentations)
- Task: Generation task tracking
- CLO: Course Learning Outcomes for quiz alignment
"""

from api.models.base import (
    MaterialType,
    TaskStatus,
    EducationalLevel,
    OutputFormat,
    BloomLevel,
)
from api.models.subject import Subject, SubjectCreate, SubjectUpdate
from api.models.topic import Topic, TopicCreate, TopicUpdate
from api.models.material import Material, MaterialCreate, MaterialUpdate
from api.models.task import Task, TaskCreate, TaskUpdate
from api.models.clo import CLO, CLOCreate

__all__ = [
    # Enums
    "MaterialType",
    "TaskStatus",
    "EducationalLevel",
    "OutputFormat",
    "BloomLevel",
    # Subject
    "Subject",
    "SubjectCreate",
    "SubjectUpdate",
    # Topic
    "Topic",
    "TopicCreate",
    "TopicUpdate",
    # Material
    "Material",
    "MaterialCreate",
    "MaterialUpdate",
    # Task
    "Task",
    "TaskCreate",
    "TaskUpdate",
    # CLO
    "CLO",
    "CLOCreate",
]
