# main.py

from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from pydantic import BaseModel

from relationship_spark_agent import create_default_relationship_agent

# ---------- FastAPI 初始化 ----------
app = FastAPI(title="Relationship Spark Agent API")

# CORS（方便本地调试）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 本地开发方便；生产环境建议收紧
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Agent 实例（单例放这里） ----------
agent = create_default_relationship_agent()

# ---------- 简单的“数据库” ----------
class PersonRecord(BaseModel):
    id: int
    scene: str
    context: str  # 对话拼接后的文本

    name: Optional[str] = ""
    main_contact: Optional[str] = ""
    relationship_to_me: Optional[str] = ""
    how_we_met: Optional[str] = ""
    location: Optional[str] = ""
    last_contact: Optional[str] = ""

    personality_tags: List[str] = []
    goal_tags: List[str] = []
    interest_tags: List[str] = []
    career_tags: List[str] = []

    card_title: str
    suggestion: str
    summary: str


class SparkRequest(BaseModel):
    scene: str
    context: str  # 对话内容拼成的一大段文本

    # 用户已知的关键信息（比如通过追问得到的姓名/联系方式）
    name: Optional[str] = None
    main_contact: Optional[str] = None
    relationship_to_me: Optional[str] = None
    how_we_met: Optional[str] = None
    location: Optional[str] = None
    last_contact: Optional[str] = None


class SparkResponse(PersonRecord):
    """/api/spark 返回单个人物的完整卡片"""
    pass


PEOPLE_DB: List[PersonRecord] = []
NEXT_ID: int = 1


# ---------- API: /api/spark ----------
@app.post("/api/spark", response_model=SparkResponse)
async def create_spark(req: SparkRequest):
    global NEXT_ID

    # 调用 Agent 生成结构化结果
    try:
        result = await agent.generate_spark(
            scene=req.scene,
            context=req.context,
            name=req.name,
            main_contact=req.main_contact,
            relationship_to_me=req.relationship_to_me,
            how_we_met=req.how_we_met,
            location=req.location,
            last_contact=req.last_contact,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {e}")

    # 组装 PersonRecord
    record = PersonRecord(
        id=NEXT_ID,
        scene=req.scene,
        context=req.context,
        name=result.get("name", "") or "",
        main_contact=result.get("main_contact", "") or "",
        relationship_to_me=result.get("relationship_to_me", "") or "",
        how_we_met=result.get("how_we_met", "") or "",
        location=result.get("location", "") or "",
        last_contact=result.get("last_contact", "") or "",
        personality_tags=result.get("personality_tags", []) or [],
        goal_tags=result.get("goal_tags", []) or [],
        interest_tags=result.get("interest_tags", []) or [],
        career_tags=result.get("career_tags", []) or [],
        card_title=result.get("card_title", "未命名人物卡片") or "未命名人物卡片",
        suggestion=result.get("suggestion", "") or "",
        summary=result.get("summary", "") or "",
    )

    PEOPLE_DB.append(record)
    NEXT_ID += 1

    return record


# ---------- API: /api/people （列出所有记录的人物） ----------
@app.get("/api/people", response_model=List[PersonRecord])
async def list_people():
    return PEOPLE_DB


# ---------- 静态页面（index.html） ----------
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# 挂载静态文件目录：/static 路径
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    直接返回 static/index.html 的内容作为首页。
    """
    index_file = STATIC_DIR / "index.html"
    return index_file.read_text(encoding="utf-8")
