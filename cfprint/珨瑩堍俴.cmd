@title 康虎云报表系统测试运行
@color 0A

@echo off
@echo =====================================
@echo.
@echo        康虎云报表系统测试运行
@echo               ver 1.3.4
@echo.
@echo.
@echo  本命令是为了方便首次使用该软件者可以
@echo  尽快看到效果而写，而并非表示康虎云报
@echo  的功能仅限于此。
@echo.
@echo.
@echo  !!!!!  请仔细阅读：!!!!!
@echo  《康虎云报表系统概要使用说明.txt》
@echo  和
@echo  《康虎云报表系统最简使用手册.txt》
@echo  两个文件，以学习详细的使用方式。
@echo.
@echo -------------------------------------
@echo.
@echo   作者：康虎软件工作室
@echo   QQ：  360026606
@echo   微信：360026606
@echo.
@echo.
@echo.
@echo 按任意键开始运行...
@pause > NUL

start notepad.exe 康虎云报表系统概要使用说明.txt

start notepad.exe 康虎云报表系统最简使用手册.txt

cd cfprint

start cfprint.exe
start iexplore.exe %CD%\printtest.html

cd ..