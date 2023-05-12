@echo off

REM Функция запускает набор скриптов и повторяет их выполнение при ошибке с последнего неудачного скрипта
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
set ERROR_SCRIPT=
for %%i in (%SCRIPTS%) do (
    echo Running script "%%i"...
    call %%i
    if errorlevel 1 (
        echo Script "%%i" failed. Marking script for retry...
        set ERROR_SCRIPT=%%i
        goto :retry
    ) else (
        echo Script "%%i" completed successfully.
        timeout /T 5 >nul
    )
)
echo All scripts completed successfully.
exit /b

:retry
echo Retrying script "%ERROR_SCRIPT%"...
call %ERROR_SCRIPT%
if errorlevel 1 (
    echo Script "%ERROR_SCRIPT%" failed again. Retrying in %RETRY_TIMEOUT% seconds...
    timeout /T %RETRY_TIMEOUT% >nul
    goto :retry
) else (
    echo Script "%ERROR_SCRIPT%" completed successfully.
    timeout /T 5 >nul
    set ERROR_SCRIPT=
    goto :loop
)