@echo off
cd /d "C:\Users\lian1\Documents\Work\core\lian_company"
set PYTHONUTF8=1
.\venv\Scripts\python.exe -m core.ops_loop weekly "사장님도구함" >> "C:\Users\lian1\Documents\Work\core\lian_company\logs\weekly.log" 2>&1
.\venv\Scripts\python.exe -m core.ops_loop weekly "스마트스토어 셀러 AI 콘텐츠 납품" >> "C:\Users\lian1\Documents\Work\core\lian_company\logs\weekly.log" 2>&1
