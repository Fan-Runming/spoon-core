#!/usr/bin/env python3
"""补充翻译脚本 - 处理剩余的中文片段"""

def patch_translate():
    with open('static/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 处理剩余的中文片段
    patches = [
        # 第313行
        ('如果你想从已有人物中"找人"，可以这样说：', 
         'If you want to find someone from your existing contacts, try saying:'),
        
        # 第314行
        ('例如："找有人机交互背景的人聊聊"', 
         'Example: "Find people with HCI background"'),
        
        # 第637行 - 注释
        ('// 判断一句话是"搜索请求"还是"描述人物"', 
         '// Determine if a message is a "search query" or "person description"'),
        
        # 第828行 - 欢迎消息
        ('"嗨～先选一个大致场景，然后用一两句话跟我说说这个人。比如：我们在哪里认识、Ta 是怎样的人，你现在想跟 Ta 保持怎样的关系。\\n\\n如果你想从已经记录的人里"找人"，可以直接说：找有人机交互背景的人聊聊。"',
         '"Hi! First, select a general scene, then tell me about this person in a sentence or two. For example: where you met, what they\'re like, and what kind of relationship you want to maintain.\\n\\nIf you want to find someone from your existing contacts, just say: \'Find people with HCI background.\'"'),
        
        # 处理其他可能遗漏的片段
        ('// 自动发送转写结果', '// Automatically send transcription result'),
        ('照片上传失败。', 'Photo upload failed.'),
    ]
    
    for old, new in patches:
        if old in content:
            content = content.replace(old, new)
            print(f'✓ 修复: {old[:40]}...')
        else:
            print(f'✗ 未找到: {old[:40]}...')
    
    with open('static/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'\n✅ 补充翻译完成！')

if __name__ == '__main__':
    patch_translate()
