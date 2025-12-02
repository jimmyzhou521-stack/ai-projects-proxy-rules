@echo off
echo ================================
echo AI代理规则项目部署脚本
echo ================================
echo.

echo [1/5] 初始化Git仓库...
git init
if %errorlevel% neq 0 (
    echo 错误：Git初始化失败，请确保已安装Git
    pause
    exit /b 1
)

echo [2/5] 添加所有文件...
git add .

echo [3/5] 创建初始提交...
git commit -m "Initial commit: AI websites proxy rules generator"

echo [4/5] 设置主分支...
git branch -M main

echo [5/5] 请输入你的GitHub用户名：
set /p USERNAME=GitHub用户名: 

echo.
echo 正在添加远程仓库...
git remote add origin https://github.com/%USERNAME%/ai-projects-proxy-rules.git

echo.
echo ================================
echo 接下来需要推送到GitHub
echo 请在弹出的窗口中登录你的GitHub账号
echo ================================
echo.
pause

git push -u origin main

echo.
echo ================================
echo 部署完成！
echo 仓库地址：https://github.com/%USERNAME%/ai-projects-proxy-rules
echo.
echo 下一步：
echo 1. 访问 https://github.com/%USERNAME%/ai-projects-proxy-rules/settings/actions
echo 2. 启用 GitHub Actions
echo 3. 手动触发第一次更新（Actions标签页）
echo ================================
pause
