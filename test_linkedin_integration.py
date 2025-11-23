#!/usr/bin/env python3
"""
测试 Apify LinkedIn 抓取端点

运行前确保主服务在 http://127.0.0.1:8000 上运行。
"""

import httpx
import asyncio


async def test_enrich_linkedin():
    """测试 /api/enrich_linkedin 端点"""
    
    # 示例 LinkedIn URL（可以换成你要测试的真实 URL）
    linkedin_url = "https://www.linkedin.com/in/williamhgates/"
    
    # 发送请求
    async with httpx.AsyncClient(timeout=180.0) as client:
        print(f"🔍 正在抓取 LinkedIn 资料: {linkedin_url}")
        print("⏳ 这可能需要 30-90 秒，请耐心等待...")
        
        try:
            response = await client.post(
                "http://127.0.0.1:8000/api/enrich_linkedin",
                json={
                    "linkedin_url": linkedin_url,
                    "person_id": None  # 创建新人物；如果要更新现有人物，传入 person_id
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print("\n✅ 成功抓取并创建人物卡片！")
                print(f"ID: {data['id']}")
                print(f"姓名: {data['name']}")
                print(f"职位: {data['relationship_to_me']}")
                print(f"地点: {data['location']}")
                print(f"职业标签: {', '.join(data['career_tags'][:5])}")
                print(f"兴趣/技能: {', '.join(data['interest_tags'][:5])}")
                print(f"\n摘要: {data['summary'][:200]}...")
                
                # 验证该人物已保存
                verify_response = await client.get("http://127.0.0.1:8000/api/people")
                people = verify_response.json()
                print(f"\n📋 当前数据库中共有 {len(people)} 个人物")
                
            else:
                print(f"❌ 请求失败: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"❌ 发生错误: {str(e)}")


async def test_update_existing():
    """测试更新已有人物"""
    
    # 先创建一个测试人物
    async with httpx.AsyncClient(timeout=180.0) as client:
        # 创建初始人物
        create_response = await client.post(
            "http://127.0.0.1:8000/api/spark",
            json={
                "scene": "professional_networking",
                "context": "认识了一位同行专家",
                "name": "测试人物"
            }
        )
        
        if create_response.status_code == 200:
            person = create_response.json()
            person_id = person["id"]
            print(f"✅ 创建了测试人物 (ID: {person_id})")
            
            # 用 LinkedIn 数据丰富该人物
            linkedin_url = "https://www.linkedin.com/in/satyanadella/"
            print(f"\n🔍 用 LinkedIn 数据丰富人物 {person_id}: {linkedin_url}")
            
            enrich_response = await client.post(
                "http://127.0.0.1:8000/api/enrich_linkedin",
                json={
                    "linkedin_url": linkedin_url,
                    "person_id": person_id
                }
            )
            
            if enrich_response.status_code == 200:
                updated = enrich_response.json()
                print(f"\n✅ 成功更新人物！")
                print(f"更新后姓名: {updated['name']}")
                print(f"职位: {updated['relationship_to_me']}")
                print(f"职业标签: {', '.join(updated['career_tags'])}")


if __name__ == "__main__":
    print("=" * 60)
    print("LinkedIn 抓取功能测试")
    print("=" * 60)
    print("\n⚠️  注意事项:")
    print("1. 确保主服务正在 http://127.0.0.1:8000 运行")
    print("2. 抓取过程需要 30-90 秒（Apify actor 执行时间）")
    print("3. 确保 Apify API token 有效且有足够配额")
    print("\n选择测试:")
    print("1. 创建新人物（Bill Gates 示例）")
    print("2. 更新已有人物（Satya Nadella 示例）")
    
    choice = input("\n请输入选择 (1 或 2): ").strip()
    
    if choice == "1":
        asyncio.run(test_enrich_linkedin())
    elif choice == "2":
        asyncio.run(test_update_existing())
    else:
        print("❌ 无效选择")
