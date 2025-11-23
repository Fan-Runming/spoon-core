"""
Apify LinkedIn Profile Scraper Integration

使用 Apify API 抓取 LinkedIn 个人资料并提取关键信息。
"""

import httpx
import asyncio
import os
from typing import Optional, Dict, Any


APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "")
ACTOR_ID = "dev_fusion~linkedin-profile-scraper"


async def scrape_linkedin_profile(linkedin_url: str, timeout: int = 120) -> Optional[Dict[str, Any]]:
    """
    使用 Apify LinkedIn Profile Scraper 抓取个人资料。
    
    参数:
        linkedin_url: LinkedIn 个人资料页面 URL（例如 https://www.linkedin.com/in/username）
        timeout: 最长等待时间（秒），默认 120 秒
    
    返回:
        抓取到的个人资料数据字典，失败时返回 None
    """
    
    # 步骤 1: 启动 Actor run（POST 请求带 input JSON）
    run_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs"
    
    # Actor input: 根据 LinkedIn Profile Scraper 文档，通常需要 profileUrls 数组
    actor_input = {
        "profileUrls": [linkedin_url],
        # 可选：其他配置参数（例如 proxy 设置、截图等）
        # "proxy": {"useApifyProxy": True}
    }
    
    headers = {
        "Authorization": f"Bearer {APIFY_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            # 发起 actor run
            run_response = await client.post(run_url, json=actor_input, headers=headers)
            run_response.raise_for_status()
            run_data = run_response.json()
            
            run_id = run_data["data"]["id"]
            default_dataset_id = run_data["data"]["defaultDatasetId"]
            
            print(f"✅ Actor run 已启动: run_id={run_id}, dataset_id={default_dataset_id}")
            
            # 步骤 2: 轮询 run 状态，直到完成或超时
            run_status_url = f"https://api.apify.com/v2/actor-runs/{run_id}"
            max_wait = timeout
            wait_interval = 3  # 每 3 秒检查一次
            elapsed = 0
            
            while elapsed < max_wait:
                await asyncio.sleep(wait_interval)
                elapsed += wait_interval
                
                status_response = await client.get(run_status_url, headers=headers)
                status_response.raise_for_status()
                status_data = status_response.json()
                
                status = status_data["data"]["status"]
                print(f"⏳ Run status: {status} (已等待 {elapsed}s)")
                
                if status in ["SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"]:
                    break
            
            if status != "SUCCEEDED":
                print(f"❌ Actor run 未成功: status={status}")
                return None
            
            # 步骤 3: 从 dataset 获取结果
            dataset_items_url = f"https://api.apify.com/v2/datasets/{default_dataset_id}/items"
            items_response = await client.get(dataset_items_url, headers=headers)
            items_response.raise_for_status()
            items = items_response.json()
            
            if not items or len(items) == 0:
                print("⚠️  Dataset 为空，未抓取到数据")
                return None
            
            # 返回第一条结果（通常只有一个 profile）
            profile = items[0]
            print(f"✅ 成功抓取 LinkedIn 资料: {profile.get('fullName', 'Unknown')}")
            return profile
            
        except httpx.HTTPStatusError as e:
            print(f"❌ HTTP 错误: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            print(f"❌ 抓取失败: {str(e)}")
            return None


def extract_profile_info(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    从 Apify 返回的 LinkedIn 资料中提取关键字段并格式化为 PersonRecord 可用的结构。
    
    返回:
        包含 name, career_tags, interest_tags, summary 等的字典
    """
    if not profile_data:
        return {}
    
    # 根据 Apify LinkedIn scraper 的典型输出字段提取
    extracted = {
        "name": profile_data.get("fullName") or profile_data.get("name"),
        "headline": profile_data.get("headline", ""),
        "location": profile_data.get("location", ""),
        "summary_text": profile_data.get("summary", ""),
        "career_tags": [],
        "interest_tags": [],
        "personality_tags": [],
    }
    
    # 提取职位/公司信息作为 career_tags
    experiences = profile_data.get("experience", []) or profile_data.get("positions", [])
    for exp in experiences[:3]:  # 取前3个职位
        title = exp.get("title") or exp.get("positionTitle", "")
        company = exp.get("companyName") or exp.get("company", "")
        if title:
            extracted["career_tags"].append(title)
        if company:
            extracted["career_tags"].append(company)
    
    # 提取技能作为 interest_tags
    skills = profile_data.get("skills", [])
    if isinstance(skills, list):
        extracted["interest_tags"] = [s.get("name", s) if isinstance(s, dict) else str(s) for s in skills[:8]]
    
    # 提取教育背景
    education = profile_data.get("education", [])
    for edu in education[:2]:
        school = edu.get("schoolName") or edu.get("school", "")
        if school:
            extracted["career_tags"].append(school)
    
    # 去重
    extracted["career_tags"] = list(dict.fromkeys(extracted["career_tags"]))[:5]
    extracted["interest_tags"] = list(dict.fromkeys(extracted["interest_tags"]))[:8]
    
    return extracted


# 示例用法（可以在 main.py 中调用）
async def test_scraper():
    """测试函数"""
    test_url = "https://www.linkedin.com/in/williamhgates/"  # Bill Gates 示例
    result = await scrape_linkedin_profile(test_url)
    if result:
        info = extract_profile_info(result)
        print("提取的信息:")
        print(info)


if __name__ == "__main__":
    # 本地测试
    asyncio.run(test_scraper())
