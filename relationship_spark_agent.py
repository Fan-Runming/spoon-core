# relationship_spark_agent.py

from typing import Dict, List, Optional

from pydantic import Field
from spoon_ai.agents import ToolCallAgent
from spoon_ai.tools import ToolManager
from spoon_ai.chat import ChatBot


class RelationshipSparkAgent(ToolCallAgent):
    """
    一个基于 SpoonOS 的关系火花 Agent。
    它不负责建立陌生人关系，而是在已有关系的语境下，
    提取人物信息 + 打标签 + 生成卡片标题 + 给出下一步联系建议。
    """

    # 基本元信息（会被 SpoonOS 用到）
    name: str = "relationship_spark_agent"
    description: str = (
        "Extract structured person info and relationship insights from user's description, "
        "then suggest a lightweight next-step action to deepen or maintain the relationship."
    )

    # 系统提示词：定义 Agent 的「人格」和输出格式
    system_prompt: str = (
        "You are a Relationship Spark Agent. Your job is NOT to sell or optimize KPI.\n"
        "You only help the user:\n"
        "  - Understand a person in their life (from the user's perspective),\n"
        "  - Extract key info & soft tags,\n"
        "  - Suggest one small, kind, non-pushy next step.\n\n"
        "Language rules:\n"
        "1. If the user's context is mainly in Chinese, answer in natural, colloquial Chinese.\n"
        "2. If it's mainly in English, answer in natural, friendly English.\n"
        "3. Do not mix languages unless the user does.\n\n"
        "Information rules:\n"
        "4. Use what the user explicitly tells you as ground truth (do NOT contradict it).\n"
        "5. If some fields cannot be inferred from the user's description, leave them blank "
        "(just after the colon, no placeholder text like 'unknown').\n"
        "6. Tags should be short phrases or single words, comma-separated.\n"
        "7. Personality tags describe HOW this person tends to behave or feel.\n"
        "8. Goal tags describe their personal goals or things they are working towards.\n"
        "9. Interest tags describe what they like to do or care about.\n"
        "10. Career tags describe their profession, role, or academic track.\n\n"
        "Card title rules:\n"
        "11. Card title is NOT the person's name.\n"
        "12. It should be a short phrase capturing the most salient feature of this person "
        "FROM THE USER'S PERSPECTIVE (e.g., 'AI 音乐黑客同学', 'Patient listener in my lab').\n"
        "13. Max 8 Chinese characters OR 5 English words.\n"
        "14. Be specific and vivid, not generic like 'good friend'.\n\n"
        "Suggestion rules:\n"
        "15. Suggest only very lightweight actions (send a short message, share a small update,\n"
        "    invite to a simple activity, etc.).\n"
        "16. Be gentle and non-intrusive, respect boundaries.\n\n"
        "OUTPUT FORMAT (no extra text before or after, no bullet points, no explanations):\n"
        "Name: ...\n"
        "Main contact: ...\n"
        "Relationship to me: ...\n"
        "How we met: ...\n"
        "Location: ...\n"
        "Last contact: ...\n"
        "\n"
        "Personality tags: tag1, tag2, ...\n"
        "Goal tags: tag1, tag2, ...\n"
        "Interest tags: tag1, tag2, ...\n"
        "Career tags: tag1, tag2, ...\n"
        "\n"
        "Card title: ...\n"
        "Suggestion: ...\n"
        "Summary: ...\n"
    )

    # 这里可以用 tools，但我们先不需要工具，给一个空的 ToolManager
    available_tools: ToolManager = Field(
        default_factory=lambda: ToolManager([])
    )

    # 限制一下最大思考步数（如果框架内部有 step 概念）
    max_steps: int = 3

    async def generate_spark(
        self,
        scene: str,
        context: str,
        name: Optional[str] = None,
        main_contact: Optional[str] = None,
        relationship_to_me: Optional[str] = None,
        how_we_met: Optional[str] = None,
        location: Optional[str] = None,
        last_contact: Optional[str] = None,
    ) -> Dict:
        """
        输入场景 + 关系描述 + 已知人物信息，返回完整的 person 结构：
          {
            "name", "main_contact", "relationship_to_me", "how_we_met", "location", "last_contact",
            "personality_tags", "goal_tags", "interest_tags", "career_tags",
            "card_title", "suggestion", "summary"
          }
        """

        # 把已知的信息也告诉模型，让它不要乱改（比如已经从补问中拿到姓名/联系方式）
        known_info_lines = []
        if name:
            known_info_lines.append(f"Known name: {name}")
        if main_contact:
            known_info_lines.append(f"Known main contact: {main_contact}")
        if relationship_to_me:
            known_info_lines.append(f"Known relationship to me: {relationship_to_me}")
        if how_we_met:
            known_info_lines.append(f"Known how we met: {how_we_met}")
        if location:
            known_info_lines.append(f"Known location: {location}")
        if last_contact:
            known_info_lines.append(f"Known last contact: {last_contact}")

        known_info_text = (
            "\n".join(known_info_lines)
            if known_info_lines
            else "Known info: (none provided)."
        )

        user_prompt = (
            "Here is the relationship context (a conversation-like transcript) and any known info "
            "about the person. Use it to fill in the OUTPUT FORMAT fields. "
            "If you cannot infer a field, leave it blank after the colon.\n\n"
            f"Scene: {scene}\n"
            f"{known_info_text}\n\n"
            f"User's description of this person and our relationship (may contain multiple turns):\n{context}\n\n"
            "Remember: respond ONLY in the exact OUTPUT FORMAT defined in the system prompt."
        )

        # 调用 Agent
        result = await self.run(user_prompt)

        # 无论 result 是 dict 还是别的，先转成纯文本
        text = str(result).strip()

        # 解析文本
        parsed = self._parse_output(text)

        # 如果用户已经提供了某些字段，就用用户的覆盖模型的推测
        if name:
            parsed["name"] = name
        if main_contact:
            parsed["main_contact"] = main_contact
        if relationship_to_me:
            parsed["relationship_to_me"] = relationship_to_me
        if how_we_met:
            parsed["how_we_met"] = how_we_met
        if location:
            parsed["location"] = location
        if last_contact:
            parsed["last_contact"] = last_contact

        return parsed

    @staticmethod
    def _split_tags(value: str) -> List[str]:
        if not value:
            return []
        return [t.strip() for t in value.split(",") if t.strip()]

    def _parse_output(self, text: str) -> Dict:
        """
        解析模型输出的多行文本：
        Name: ...
        Main contact: ...
        ...
        Personality tags: ...
        Goal tags: ...
        ...
        Card title: ...
        Suggestion: ...
        Summary: ...
        """
        lines = text.splitlines()
        # 默认值
        data = {
            "name": "",
            "main_contact": "",
            "relationship_to_me": "",
            "how_we_met": "",
            "location": "",
            "last_contact": "",
            "personality_tags": [],
            "goal_tags": [],
            "interest_tags": [],
            "career_tags": [],
            "card_title": "",
            "suggestion": "",
            "summary": "",
        }

        for raw in lines:
            line = raw.strip()
            lower = line.lower()

            def val_after(prefix: str) -> str:
                return line[len(prefix):].strip()

            if lower.startswith("name:"):
                data["name"] = val_after("Name:")
            elif lower.startswith("main contact:"):
                data["main_contact"] = val_after("Main contact:")
            elif lower.startswith("relationship to me:"):
                data["relationship_to_me"] = val_after("Relationship to me:")
            elif lower.startswith("how we met:"):
                data["how_we_met"] = val_after("How we met:")
            elif lower.startswith("location:"):
                data["location"] = val_after("Location:")
            elif lower.startswith("last contact:"):
                data["last_contact"] = val_after("Last contact:")
            elif lower.startswith("personality tags:"):
                data["personality_tags"] = self._split_tags(val_after("Personality tags:"))
            elif lower.startswith("goal tags:"):
                data["goal_tags"] = self._split_tags(val_after("Goal tags:"))
            elif lower.startswith("interest tags:"):
                data["interest_tags"] = self._split_tags(val_after("Interest tags:"))
            elif lower.startswith("career tags:"):
                data["career_tags"] = self._split_tags(val_after("Career tags:"))
            elif lower.startswith("card title:"):
                data["card_title"] = val_after("Card title:")
            elif lower.startswith("suggestion:"):
                data["suggestion"] = val_after("Suggestion:")
            elif lower.startswith("summary:"):
                data["summary"] = val_after("Summary:")

        # 兜底
        if not data["suggestion"]:
            data["suggestion"] = text
        if not data["summary"]:
            data["summary"] = "模型没有按预期格式返回 Summary，这里先用整体输出作为建议的补充。"

        if not data["card_title"]:
            if data["relationship_to_me"]:
                data["card_title"] = data["relationship_to_me"]
            elif data["name"]:
                data["card_title"] = f"关于 {data['name']} 的卡片"
            else:
                data["card_title"] = "未命名人物卡片"

        return data


def create_default_relationship_agent() -> RelationshipSparkAgent:
    """
    工厂函数：创建一个默认配置好的 RelationshipSparkAgent。
    """
    llm = ChatBot(
        llm_provider="gemini",          # ⭐ 根据自己实际环境改
        model_name="gemini-2.5-pro",    # ⭐ 或你想用的模型名称
    )
    return RelationshipSparkAgent(llm=llm)
