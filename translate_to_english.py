#!/usr/bin/env python3
"""
批量将 static/index.html 中的中文文本替换为英文
"""

def translate_html():
    # 读取原文件
    with open('static/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 定义所有需要替换的中文到英文的映射
    translations = [
        # HTML lang attribute
        ('lang="zh-CN"', 'lang="en"'),
        
        # 注释
        ('<!-- 左侧：对话式输入 -->', '<!-- Left panel: Conversational input -->'),
        ('<!-- 右侧：卡片展示 + 列表 -->', '<!-- Right panel: Card display + List -->'),
        ('<!-- 隐藏的文件选择器 -->', '<!-- Hidden file input -->'),
        ('/* 固定高度，避免聊天框随内容不断拉长。内部可滚动 */', '/* Fixed height to prevent chat window from growing infinitely. Scrollable inside */'),
        ('/* 左右行内：输入框 + 语音/上传/发送按钮 */', '/* Input row: text input + voice/upload/send buttons */'),
        ('// 对话历史', '// Chat history'),
        ('// 追问得到的关键信息', '// Extracted key information'),
        ('// 当前是否在等用户回答某个追问字段', '// Currently waiting for user to answer a specific question'),
        ('// ⭐ 当前正在编辑的人物 id（用于更新同一张卡片）', '// ⭐ Currently editing person ID (for updating the same card)'),
        ('// 判断一句话是"搜索请求"还是"描述人物"', '// Determine if a message is a "search query" or "person description"'),
        ('// ⭐ 搜索模式：不修改当前人物，直接在已有卡片中找人', '// ⭐ Search mode: Don\'t modify current person, search existing cards'),
        ('// 普通描述：更新 / 创建人物卡片', '// Normal description: Update / create profile card'),
        ('// 如果当前在等用户回答姓名 / 联系方式，就把这一句当成答案', '// If currently waiting for user to answer name / contact, treat this as the answer'),
        ('// ---- 语音输入 & 照片上传支持 ----', '// ---- Voice input & Photo upload support ----'),
        ('// 上传图片并（如果有 currentPersonId）关联', '// Upload image and associate with currentPersonId if exists'),
        ('// 重新加载人物列表并尝试把该人物展示出来', '// Reload people list and try to display this person'),
        ('// reset so same file can be selected again', '// reset so same file can be selected again'),
        ('// 语音识别（Web Speech API）', '// Voice recognition (Web Speech API)'),
        ('// 自动发送转写结果', '// Automatically send transcription result'),
        ('// 页面加载时，引导 + 加载已有卡片列表', '// On page load, show welcome message + load existing cards list'),
        ('// ⭐ 保存当前人的 id，以便后续更新同一张卡片', '// ⭐ Save current person\'s ID for future updates to the same card'),
        ('// ⭐ 告诉后端当前是更新哪个人（第一次为 null）', '// ⭐ Tell backend which person to update (null for first time)'),
        ('// 检查是否缺少关键信息：姓名 / 主要联系方式', '// Check if key information is missing: name / main contact'),
        ('// 图片展示（如果有的话）', '// Photo display (if any)'),
        ('// 拼一段推荐话', '// Compose recommendation message'),
        ('// 把第一个匹配的人展示在右侧卡片区', '// Display the first matching person in the right card area'),
        ('// 重新绑定点击', '// Re-bind click events'),
        ('// 点击 mini card 展示到当前卡片区域（初始绑定）', '// Click mini card to display in current card area (initial binding)'),
        ('// 只显示最近的 5 条记录（数据已在后端按时间倒序返回）', '// Display only the most recent 5 records (data already sorted by backend)'),
        
        # UI文本
        ('通过一段对话，把你和 Ta 的故事说出来。', 'Tell me about someone in your life through a conversation.'),
        ('Agent 会自动抽取姓名、联系方式、关系标签，并在缺失时向你追问。', 'The Agent will automatically extract names, contact info, and relationship tags, asking follow-up questions when needed.'),
        ('如果你想从已有人物中"找人"，可以这样说：', 'If you want to find someone from your existing contacts, try saying:'),
        ('例如："找有人机交互背景的人聊聊"', 'Example: "Find people with HCI background"'),
        ('Scene / 场景', 'Scene'),
        ('保持联系（stay in touch）', 'Stay in Touch'),
        ('初次认识（first meeting）', 'First Meeting'),
        ('很久没联系（long time no see）', 'Long Time No See'),
        ('想修复关系（repair tension）', 'Repair Tension'),
        ('不确定，只是想记录（uncertain）', 'Uncertain / Just Recording'),
        ('跟我说说 Ta 吧，或者直接说：找有人机交互背景的人。', 'Tell me about them, or say: \'Find people with HCI background.\''),
        ('语音输入', 'Voice input'),
        ('上传照片', 'Upload photo'),
        ('发送', 'Send'),
        ('✨ 当前人物卡片', '✨ Current Profile Card'),
        ('还没有卡片', 'No card yet'),
        ('在左边开始一段对话，然后我会帮你生成关于 Ta 的人物卡片。', 'Start a conversation on the left, and I\'ll help you create a profile card.'),
        ('📒 我最近记录的人', '📒 Recently Added'),
        ('Personality / 性格', 'Personality'),
        ('Goals / 目标', 'Goals'),
        ('Interests / 兴趣', 'Interests'),
        ('Career / 职业/专业', 'Career / Education'),
        ('未命名人物卡片', 'Untitled Profile'),
        ('（未填写姓名）', '(Name not provided)'),
        ('联系方式：', 'Contact: '),
        ('相识方式：', 'How we met: '),
        ('Ta 大概在：', 'Location: '),
        ('上次联系：', 'Last contact: '),
        ('Relationship Summary / 关系小结', 'Relationship Summary'),
        ('Next Step Suggestion / 下一步可以怎么联系 Ta', 'Next Step Suggestion'),
        ('还没有填写姓名/关系', 'Name/relationship not provided'),
        ('还没有记录任何人。', 'No records yet.'),
        ('显示最近 ${data.length} 条中的前 5 条，点击查看全部', 'Showing 5 of ${data.length} recent records. Click to view all.'),
        ('加载人物列表失败。', 'Failed to load people list.'),
        ('先跟我说一点关于 Ta 的事情吧～', 'Tell me a bit about them first~'),
        ('生成中…', 'Generating…'),
        ('我正在消化你说的内容，帮你整理这段关系。', 'I\'m processing what you said and organizing this relationship.'),
        ('完成 ✔ 这张卡片已经被记录在右下角列表中～', 'Done ✔ This card has been saved to the list below~'),
        ('我还不知道 Ta 的名字，你方便告诉我吗？', 'I don\'t know their name yet. Could you tell me?'),
        ('那通常你是通过什么方式联系 Ta 的？可以给一个你习惯使用的联系方式（比如微信号、手机号或邮箱）。', 'How do you usually contact them? Please provide your preferred contact method (e.g., WeChat, phone, or email).'),
        ('我已经帮你记录好 Ta 啦～之后你也可以继续补充关于 Ta 的故事。', 'I\'ve recorded them for you! Feel free to add more about their story anytime.'),
        ('调用失败了，检查一下后端是否在运行（uvicorn main:app --reload）。', 'Call failed. Please check if the backend is running (uvicorn main:app --reload).'),
        ('出错了', 'Error occurred'),
        ('请在终端查看错误信息，或稍后重试。', 'Please check the terminal for error messages or try again later.'),
        ('我在你的人物卡片里帮你找找看…', 'Searching through your profile cards…'),
        ('我在你已经记录的人物里暂时没有找到和这句话特别相关的人。你可以换个关键词试试，比如具体一点的方向、城市或学校。', 'I couldn\'t find anyone matching this in your records. Try different keywords like a specific field, city, or school.'),
        ('我觉得你可以考虑联系这些人：', 'I think you could reach out to these people:'),
        ('（未命名）', '(Unnamed)'),
        ('我已经根据你的描述推荐了几个人，也把其中一个展示在右边卡片里了～', 'I\'ve recommended a few people based on your description and displayed one in the card on the right~'),
        ('搜索失败了，可能是后端没有运行或网络问题。', 'Search failed. The backend might not be running or there\'s a network issue.'),
        ('好的，我记下来了，Ta 的名字是 ${text}。我再帮你更新一下人物卡片～', 'Got it! Their name is ${text}. Let me update the profile card~'),
        ('好的，我会用这个作为主要联系方式。让我再更新一下这张卡片。', 'Got it! I\'ll use this as the primary contact method. Let me update the card.'),
        ('正在上传照片…', 'Uploading photo…'),
        ('上传失败', 'Upload failed'),
        ('照片上传并已保存到该人物卡片。', 'Photo uploaded and saved to the profile card.'),
        ('照片已上传（未关联到人物）。你可以在创建/更新卡片时保存。', 'Photo uploaded (not associated with anyone). You can save it when creating/updating a card.'),
        ('照片上传失败。', 'Photo upload failed.'),
        ('r.lang = "zh-CN";', 'r.lang = "en-US";'),
        ('正在听写，点击停止或再次点击麦克风。', 'Listening… Click again to stop.'),
        ('语音识别失败（请检查浏览器权限）。', 'Voice recognition failed (please check browser permissions).'),
        ('当前浏览器不支持语音识别（试试 Chrome/Edge）。', 'Voice recognition not supported in this browser (try Chrome/Edge).'),
        ('嗨～先选一个大致场景，然后用一两句话跟我说说这个人。比如：我们在哪里认识、Ta 是怎样的人，你现在想跟 Ta 保持怎样的关系。\\n\\n如果你想从已经记录的人里"找人"，可以直接说：找有人机交互背景的人聊聊。', 'Hi! First, select a general scene, then tell me about this person in a sentence or two. For example: where you met, what they\'re like, and what kind of relationship you want to maintain.\\n\\nIf you want to find someone from your existing contacts, just say: \'Find people with HCI background.\''),
    ]
    
    # 执行所有替换
    for chinese, english in translations:
        content = content.replace(chinese, english)
    
    # 写回文件
    with open('static/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Translation completed! All Chinese text has been replaced with English.")
    print(f"   Total replacements: {len(translations)}")

if __name__ == '__main__':
    translate_html()
