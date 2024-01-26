from typing import AsyncContextManager

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from moneyroundup.database import get_async_session_context_manager
from moneyroundup.models import Goal
from moneyroundup.schemas import GoalUpdate, NewGoal
from moneyroundup.users import current_active_user

router = APIRouter(prefix="/goal", tags=["Goals"])


@router.post("", status_code=201)
async def create_goal(
    payload: NewGoal,
    session=Depends(get_async_session_context_manager),
    user=Depends(current_active_user),
):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    g = Goal(user_id=payload.user_id, goal=payload.goal)

    async with session as session:
        session.add(g)
        await session.commit()

    return {"goal_created": True, "id": g.id}


@router.get("", status_code=200)
async def get_goals(
    session: AsyncContextManager[AsyncSession] = Depends(
        get_async_session_context_manager
    ),
    user=Depends(current_active_user),
):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    async with session as session:
        query = select(Goal)
        goals = await session.execute(query)
        goal_list = [{"id": g.id, "goal": g.goal} for g in goals.scalars().all()]

    return {"goals": goal_list}


@router.patch("/{goal_id}", status_code=200)
async def update_goal(
    goal_id: str,
    payload: GoalUpdate,
    session: AsyncContextManager[AsyncSession] = Depends(
        get_async_session_context_manager
    ),
    user=Depends(current_active_user),
):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    async with session as session:
        query = select(Goal).where(Goal.id == goal_id)
        goal = await session.execute(query)
        goal = goal.scalar_one_or_none()

        if goal:
            goal.goal = payload.goal
            await session.commit()

            return goal

    raise HTTPException(status_code=404, detail="Goal not found")


@router.delete("/{goal_id}", status_code=200)
async def delete_goal(
    goal_id: str,
    session: AsyncContextManager[AsyncSession] = Depends(
        get_async_session_context_manager
    ),
    user=Depends(current_active_user),
):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    async with session as session:
        query = select(Goal).where(Goal.id == goal_id)
        goal = await session.execute(query)
        goal = goal.scalar_one_or_none()

        if goal:
            await session.delete(goal)
            await session.commit()

            return {"goal_deleted": True}

    raise HTTPException(status_code=404, detail="Goal not found")
