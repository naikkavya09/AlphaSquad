from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Career Roadmap API
# =========================

class CareerInput(BaseModel):
    field: str
    level: str

@app.post("/career")
def career(data: CareerInput):

    roadmap = [
        f"Phase 1: Learn fundamentals of {data.field}",
        "Phase 2: Build real-world projects",
        "Phase 3: Certifications & Networking",
        "Phase 4: Apply for internships/jobs"
    ]

    return {
        "title": f"{data.level} {data.field} Roadmap",
        "steps": roadmap
    }


# =========================
# Resume Analyzer API
# =========================

@app.post("/resume")
async def resume_analysis(
        file: UploadFile = File(...),
        job_desc: str = ""
):

    content = (await file.read()).decode(errors="ignore")

    keywords = ["python", "react", "sql", "ai", "ml", "docker"]
    found = [k for k in keywords if k in content.lower()]

    score = 50 + len(found)*8
    score = min(score, 95)

    return {
        "score": score,
        "found_skills": found,
        "suggestion":
        "Add measurable achievements and project outcomes."
    }


# =========================
# Skill Gap API
# =========================

class SkillInput(BaseModel):
    skills: str
    role: str

@app.post("/skillgap")
def skill_gap(data: SkillInput):

    role_data = {
        "AI Engineer": ["python","ml","pytorch","docker","math"],
        "Web Developer": ["javascript","react","css","node","sql"],
        "DevOps Engineer": ["linux","aws","kubernetes","ci/cd","terraform"]
    }

    required = role_data.get(data.role, [])
    user_skills = data.skills.lower()

    stats = []
    missing = []

    for skill in required:
        if skill in user_skills:
            stats.append(100)
        else:
            stats.append(20)
            missing.append(skill)

    return {
        "required": required,
        "stats": stats,
        "missing": missing
    }


# =========================
# Interview Coach API
# =========================

class InterviewInput(BaseModel):
    answer: str

@app.post("/interview")
def interview(data: InterviewInput):

    text = data.answer.lower()
    score = 40

    if "situation" in text:
        score += 15
    if "task" in text:
        score += 15
    if "action" in text:
        score += 15
    if "result" in text:
        score += 15

    feedback = (
        "Great STAR structure!"
        if score >= 70
        else "Mention clear results and outcomes."
    )

    return {
        "score": score,
        "feedback": feedback
    }