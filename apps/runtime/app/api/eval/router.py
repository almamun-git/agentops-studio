from fastapi import APIRouter

router = APIRouter()


@router.post("/run", response_description="Evaluation run status.")
async def run_eval():
    """Run evaluation suite."""
    return {"message": "Evaluation not implemented yet"}


@router.get("/{eval_id}")
async def get_eval(eval_id: str):
    """Get evaluation results."""
    return {"eval_id": eval_id, "status": "pending"}

