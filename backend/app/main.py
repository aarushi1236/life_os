print("loaded")
from datetime import date

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.models.daily_plan_task import DailyPlanTask
from app.models.daily_plans import DailyPlan

from .database import SessionLocal
from .models.task import Task
from .schemas.task import TaskCreate

from .models.user import User

from .models.reward import Reward
from .models.reward_redemption import RewardRedemption


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Life OS API Running"}

@app.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(**task.model_dump())

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task
    
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@app.patch("/tasks/{task_id}")
def update_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return {"error": "Task not found"}
    return {"message": f"Update task {task_id}"}


@app.post("/daily-plan/generate")
def generate_daily_plan(db: Session = Depends(get_db)):

    existing_plan = (
        db.query(DailyPlan)
        .filter(
            DailyPlan.user_id == 1,
            DailyPlan.plan_date == date.today()
        )
        .first()
    )
    if existing_plan:
        return {
        "message": "Today's plan already exists",
        "plan_id": existing_plan.id
        }
    

    tasks = (
        db.query(Task)
        .filter(Task.status == "pending")
        .all()
    )

    tasks.sort(key=lambda t: t.importance+ t.urgency, reverse=True)

    available_minutes = 240

    selected_tasks = []
    total_time = 0

    for task in tasks:
        if total_time + task.estimated_minutes <= available_minutes:
            selected_tasks.append(task)
            total_time += task.estimated_minutes

    daily_plan = DailyPlan( user_id=1, plan_date=date.today())

    db.add(daily_plan)
    db.commit()
    db.refresh(daily_plan)

    for rank,task in enumerate(selected_tasks, start=1) :
        plan_task = DailyPlanTask(
        plan_id=daily_plan.id,
        task_id=task.id,
        priority_rank=rank,
        completed=False
    )

        db.add(plan_task)


    db.commit()
    return selected_tasks


@app.get("/daily-plan/today")
def get_today_daily_plan(db: Session = Depends(get_db)):

    today_plan = (
        db.query(DailyPlan)
        .filter(
            DailyPlan.user_id == 1,
            DailyPlan.plan_date == date.today()
        )
        .first()
    )
    if not today_plan:
        return {"error": "No daily plan found for today"}

    plan_tasks = (
        db.query(DailyPlanTask)
        .filter(DailyPlanTask.plan_id == today_plan.id)
        .order_by(DailyPlanTask.priority_rank)
        .all()
    )

    result=[]

    for plan_task in plan_tasks:

        task = (
            db.query(Task)
            .filter(Task.id == plan_task.task_id)
            .first()
        )

        result.append({
            "priority_rank": plan_task.priority_rank,
            "completed": plan_task.completed,
            "task": task.title,
            "importance": task.importance,
            "urgency": task.urgency,
            "estimated_minutes": task.estimated_minutes
        })

    return {
        "plan_date": today_plan.plan_date,
        "tasks": result
    }

@app.patch("/tasks/{task_id}/complete")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    try: 
        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            return {"message": "Task not found"}

        task.status = "completed"

        daily_task = (
            db.query(DailyPlanTask)
            .filter(DailyPlanTask.task_id == task_id)
            .first()
        )

        if daily_task:
            daily_task.completed = True

        user = db.query(User).filter(User.id == 1).first()

        user.credits += task.credit_reward

        if not user:
            return {"message": "User not found"}


        db.commit()

        return {
            "message": "Task completed",
            "credits_earned": task.credit_reward
        }
    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}

@app.get("/user/credits")
def get_credits(db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == 1).first()

    if not user:
        return {"message": "User not found"}

    return {
        "user_id": user.id,
        "credits": user.credits
    }

@app.get("/rewards")
def get_rewards(db: Session = Depends(get_db)):
    rewards = db.query(Reward).all()
    return rewards


@app.post("/rewards/redeem/{reward_id}")
def redeem_reward(
    reward_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == 1).first()

    reward = (
        db.query(Reward)
        .filter(Reward.id == reward_id)
        .first()
    )

    if not reward:
        return {"message": "Reward not found"}

    if user.credits < reward.cost:
        return {"message": "Not enough credits"}

    user.credits -= reward.cost

    redemption = RewardRedemption(
        user_id=user.id,
        reward_id=reward.id
    )

    db.add(redemption)
    db.commit()

    return {
        "message": "Reward redeemed",
        "remaining_credits": user.credits
    }



