from pydantic import BaseModel, Field


class TaskAllocationResponse(BaseModel):
    """
    Task allocation response for assigning the correct agent based on the query.
    """

    score: int = Field(
        ...,
        description=(
            "1 if the task should be assigned to Agent 1 (Prospecting Agent), "
            "2 if the task should be assigned to Agent 2 (Prospect Insights Agent), "
            "3 if the task should be assigned to Agent 3 (Communication Agent), "
            "and -1 if the query is nonsensical or not relevant to the task allocation."
        ),
    )
