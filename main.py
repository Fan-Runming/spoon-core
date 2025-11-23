# main.py

from pathlib import Path
from typing import List, Optional
import shutil

from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from pydantic import BaseModel

from relationship_spark_agent import create_default_relationship_agent

# ---------- FastAPI 初始化 ----------
app = FastAPI(title="Relationship Spark Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 本地开发方便；生产环境建议收紧
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Agent 实例 ----------
agent = create_default_relationship_agent()

# ---------- 简单“数据库” ----------
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
    photo_url: Optional[str] = None  # 头像照片 URL


class SparkRequest(BaseModel):
    # ⭐ 新增：如果传入 id，就更新对应的人，而不是新建
    id: Optional[int] = None

    scene: str
    context: str  # 对话内容拼成的一大段文本

    # 追问得到的关键信息
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

    # 如果带了 id，就尝试查找已有记录（更新模式）
    existing_record = None
    if req.id is not None:
        for p in PEOPLE_DB:
            if p.id == req.id:
                existing_record = p
                break

    # 调用 Agent
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

    if existing_record is None:
        # 新建记录
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
    else:
        # 更新已有记录（id 不变）
        existing_record.scene = req.scene
        existing_record.context = req.context
        existing_record.name = result.get("name", "") or ""
        existing_record.main_contact = result.get("main_contact", "") or ""
        existing_record.relationship_to_me = result.get("relationship_to_me", "") or ""
        existing_record.how_we_met = result.get("how_we_met", "") or ""
        existing_record.location = result.get("location", "") or ""
        existing_record.last_contact = result.get("last_contact", "") or ""
        existing_record.personality_tags = result.get("personality_tags", []) or []
        existing_record.goal_tags = result.get("goal_tags", []) or []
        existing_record.interest_tags = result.get("interest_tags", []) or []
        existing_record.career_tags = result.get("career_tags", []) or []
        existing_record.card_title = result.get("card_title", "未命名人物卡片") or "未命名人物卡片"
        existing_record.suggestion = result.get("suggestion", "") or ""
        existing_record.summary = result.get("summary", "") or ""
        return existing_record


# ---------- API: /api/people （列出所有记录的人物） ----------
@app.get("/api/people", response_model=List[PersonRecord])
async def list_people():
    return PEOPLE_DB


# ---------- API: /api/search_people?q=... （搜索已有卡片） ----------
@app.get("/api/search_people", response_model=List[PersonRecord])
async def search_people(q: str = Query(..., description="搜索关键词")):
    """
    简单关键词搜索：
    在 card_title / name / relationship_to_me / how_we_met / location / summary / suggestion
    和 四类 tags 中做子串匹配。
    """
    query = q.strip().lower()
    if not query:
        return []

    def match_text(text: Optional[str]) -> bool:
        return bool(text) and query in text.lower()

    def match_tags(tags: List[str]) -> bool:
        return any(query in t.lower() for t in tags)

    results: List[PersonRecord] = []
    for p in PEOPLE_DB:
        if (
            match_text(p.card_title)
            or match_text(p.name)
            or match_text(p.relationship_to_me)
            or match_text(p.how_we_met)
            or match_text(p.location)
            or match_text(p.summary)
            or match_text(p.suggestion)
            or match_tags(p.personality_tags)
            or match_tags(p.goal_tags)
            or match_tags(p.interest_tags)
            or match_tags(p.career_tags)
        ):
            results.append(p)

    return results


# ---------- API: /api/upload_photo ----------
@app.post("/api/upload_photo")
async def upload_photo(
    file: UploadFile = File(...),
    id: Optional[int] = Form(None)
):
    """
    上传头像照片
    - 如果提供 id，将照片关联到该人物
    - 照片保存到 static/uploads/ 目录
    """
    # 创建 uploads 目录
    UPLOAD_DIR = STATIC_DIR / "uploads"
    UPLOAD_DIR.mkdir(exist_ok=True)

    # 生成安全的文件名
    import uuid
    file_ext = Path(file.filename).suffix if file.filename else ".jpg"
    safe_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / safe_filename

    # 保存文件
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    finally:
        file.file.close()

    # 生成可访问的 URL
    photo_url = f"/static/uploads/{safe_filename}"

    # 如果提供了 id，更新对应人物的照片
    if id is not None:
        for person in PEOPLE_DB:
            if person.id == id:
                person.photo_url = photo_url
                return {"success": True, "photo_url": photo_url, "id": id}
        raise HTTPException(status_code=404, detail=f"Person with id {id} not found")

    # 如果没有提供 id，只返回上传成功的 URL
    return {"success": True, "photo_url": photo_url, "id": None}


# ---------- 静态页面（index.html） ----------
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    index_file = STATIC_DIR / "index.html"
    return index_file.read_text(encoding="utf-8")
