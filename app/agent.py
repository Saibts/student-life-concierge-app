# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pydantic import BaseModel
from google.adk.agents import LlmAgent
from google.adk.apps import App


class CalendarEventSchema(BaseModel):
    title: str
    date: str
    duration_hours: float
    user_id: str


def extract_email_deadlines(user_id: str) -> str:
    """Mimics checking the inbox for academic deadlines.

    Args:
        user_id: The ID of the user.

    Returns:
        A string indicating the extracted deadlines.
    """
    return "Extracted: Capstone Project deadline found on July 06, 2026."


def book_calendar_focus_block(event: CalendarEventSchema) -> str:
    """Mimics booking a focus block on the user's calendar.

    Args:
        event: The calendar event details containing title, date, duration, and user ID.

    Returns:
        A success message.
    """
    return "Success: Focus block booked for the assignment."


AcademicTaskExtractor = LlmAgent(
    name="AcademicTaskExtractor",
    instruction="Extract academic deadlines from the user's emails.",
    tools=[extract_email_deadlines],
)

SchedulerCoordinator = LlmAgent(
    name="SchedulerCoordinator",
    instruction="Book calendar focus blocks for assignments and deadlines.",
    tools=[book_calendar_focus_block],
)

# Set sub_agents correctly on AcademicTaskExtractor
AcademicTaskExtractor.sub_agents = [SchedulerCoordinator]

app = App(
    name="app",
    root_agent=AcademicTaskExtractor,
)
