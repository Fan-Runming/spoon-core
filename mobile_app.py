from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Relationship Spark — Mobile Preview")

# 挂载 static 文件夹以便直接访问静态资源
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    # 返回 mobile.html
    return FileResponse("static/mobile.html")

# 说明：
# 在另一个终端运行：
#   uvicorn mobile_app:app --reload --host 127.0.0.1 --port 8001
# 然后在浏览器打开 http://127.0.0.1:8001/ 即可看到移动端预览页面（它会通过 iframe 加载主服务的 /static/index.html）。
