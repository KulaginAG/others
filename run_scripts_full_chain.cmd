@echo off

REM Функция запускает набор сценариев и повторяет их выполнение при ошибке полностью с самого начала
REM Параметры
REM %1 - директория, в которой будут выполняться сценарии
REM %2 - список сценариев, разделенный пробелами
REM %3 - время задержки перед повторной попыткой выполнения, в секундах

:run_scripts
setlocal
echo Starting main script...
cd /d %1
set RETRY_TIMEOUT=%2
set SCRIPTS=%3 %4 %5 %6 %7 %8 %9
:loop
for %%i in (%SCRIPTS%) do (
    echo Running script "%%i"...
    call %%i
    if errorlevel 1 (
        echo Script "%%i" failed. Retrying in %RETRY_TIMEOUT% seconds...
        timeout /T %RETRY_TIMEOUT% >nul
        goto loop
    ) else (
        echo Script "%%i" completed successfully.
        timeout /T 5 >nul
    )
)
echo All scripts completed successfully.
endlocal
goto :eof