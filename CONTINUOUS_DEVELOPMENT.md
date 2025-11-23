# 持续开发与部署指南

## 🔄 三种开发模式

### 模式 1: 本地开发 + 手动部署
**适合**: 重大更新前测试

```bash
# 本地开发
uvicorn main:app --reload --port 8000

# 测试完成后
git add .
git commit -m "update: 功能描述"
git push origin main

# Demo 会自动更新（Railway/Render）
# 或手动在 Replit 上 git pull
```

### 模式 2: Replit 直接开发
**适合**: 快速迭代

1. 打开 Replit 项目
2. 直接在线编辑代码
3. 点击 Run 测试
4. 保存即更新 Demo
5. （可选）同步到 GitHub：Shell 中运行
   ```bash
   git add .
   git commit -m "update"
   git push
   ```

### 模式 3: 分支开发（专业）
**适合**: 团队协作或重要项目

```bash
# 创建开发分支
git checkout -b dev

# 开发新功能
# ... 修改代码 ...

# 提交到开发分支
git add .
git commit -m "feat: 新功能"
git push origin dev

# 测试通过后合并到 main
git checkout main
git merge dev
git push origin main

# main 分支自动部署到 Demo
```

## 📝 提交规范（推荐）

使用清晰的 commit message：

```bash
feat: 添加语音输入功能
fix: 修复最近记录只显示一条的问题
style: 更新 UI 为 glassmorphism 风格
docs: 更新 README 部署说明
refactor: 重构 Agent 调用逻辑
```

## ⚡ 快速修改检查清单

每次修改前：
- [ ] 本地测试是否正常运行
- [ ] 检查是否有语法错误
- [ ] 确认环境变量设置正确

每次提交前：
- [ ] 测试主要功能是否正常
- [ ] 检查浏览器 Console 无错误
- [ ] 确认 Demo Link 可访问

## 🚨 常见问题

### Q: 我 push 了代码，Demo 没更新？
**A**: 
- Railway: 检查 Deployments 页面，看是否在部署中
- Render: 可能需要 5-10 分钟，检查 Events 页面
- Replit: 需要手动 `git pull` 或在 Version Control 中同步

### Q: 部署失败了怎么办？
**A**:
1. 查看部署日志（Logs）
2. 常见问题：
   - 缺少依赖：更新 `requirements.txt`
   - 端口错误：检查是否使用 `$PORT` 环境变量
   - 环境变量缺失：在平台上添加 `GEMINI_API_KEY`

### Q: 能回退到之前的版本吗？
**A**: 
- Git 回退：`git revert <commit-hash>`
- Railway/Render: 在平台上可以回滚到之前的部署
- Replit: 在 Version Control 中查看历史

## 🎯 最佳实践

### 开发流程
```
1. 本地创建分支
2. 开发新功能
3. 本地测试
4. 提交到 GitHub
5. 自动部署到 Demo
6. 在 Demo 上验证
7. 有问题就修复，重复 2-6
```

### 保持 Demo 稳定
- ✅ 在 `dev` 分支测试新功能
- ✅ 确认无误后合并到 `main`
- ✅ `main` 分支始终保持可用状态
- ✅ Demo 只连接 `main` 分支

### 紧急修复
```bash
# 快速修复 Demo 上的问题
git checkout main
# 直接修改
git add .
git commit -m "hotfix: 紧急修复XXX问题"
git push origin main
# 等待自动部署
```

## 🔐 环境变量管理

### 不同环境的 API Key
- **本地**: `.env` 文件
- **Demo**: 平台的环境变量设置
- **永远不要**: 提交 `.env` 到 Git！

### 更新 API Key
1. 在部署平台更新环境变量
2. 手动重启服务（或等待下次部署）
3. 验证新的 Key 是否生效

## 📊 监控 Demo 状态

### Railway
- Dashboard 查看实时日志
- Metrics 查看访问量
- 设置告警通知

### Render
- Events 查看部署历史
- Logs 查看运行日志
- 免费版可能有休眠（15分钟无访问）

### Replit
- 保持浏览器标签打开避免休眠
- 或升级到付费版获得持续运行

## 💡 提示

- 提交评审期间，**不建议**频繁大改
- 小的 bug 修复可以随时更新
- 记录每次更新的内容
- 保持 GitHub README 更新
- Demo Link 始终指向最新稳定版本

---

**记住**: 有了 Demo Link 后，你仍然完全掌控代码！可以随时修改、优化、修复问题。
