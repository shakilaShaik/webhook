from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
import pytz
from zoneinfo import ZoneInfo


class GitHubEvent(BaseModel):
    request_id: str
    author: str
    action: Literal["PUSH", "PULL_REQUEST", "MERGE"]
    from_branch: Optional[str] = None
    to_branch: str
    timestamp: str = Field(
        default_factory=lambda: datetime.now(pytz.timezone("Asia/Kolkata")).strftime(
            "%d %B %Y - %I:%M %p IST"
        )
    )


def build_event_from_github_payload(
    event_type: str, data: dict
) -> Optional[GitHubEvent]:
    author = data.get("pusher", {}).get("name") or data.get("sender", {}).get("login")
    timestamp = datetime.now(ZoneInfo("Asia/Kolkata")).strftime(
        "%d %B %Y - %I:%M %p IST"
    )

    if event_type == "push":
        return GitHubEvent(
            request_id=data.get("after"),
            author=author,
            action="PUSH",
            to_branch=data["ref"].split("/")[-1],
            timestamp=timestamp,
        )

    elif event_type == "pull_request":
        pr = data["pull_request"]
        action = (
            "MERGE"
            if (data["action"] == "closed" and pr.get("merged"))
            else "PULL_REQUEST"
        )

        if data["action"] not in ["opened", "closed"]:
            return None  # Ignore PR edits or other actions

        return GitHubEvent(
            request_id=str(pr["id"]),
            author=author,
            action=action,
            from_branch=pr["head"]["ref"],
            to_branch=pr["base"]["ref"],
            timestamp=timestamp,
        )

    return None
