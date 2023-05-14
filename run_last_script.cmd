@echo off
chcp 1251 > nul

REM Функция запускает набор скриптов и повторяет их выполнение при ошибке с последнего неудачного скрипта
REM Параметры
REM %1 - директория, в которой будут выполняться сценарии
REM %2 - время задержки перед повторной попыткой выполнения, в секундах
REM %3-%9 - список сценариев, разделенный пробелами

setlocal enabledelayedexpansion
cd /d %1
set RETRY_TIMEOUT=%2
set SCRIPTS=%3 %4 %5 %6 %7 %8 %9
set SUCCESSFUL_SCRIPTS=0
set COUNTER=0

echo Starting main script...

:loop
set ERROR_SCRIPT=
for %%i in (%SCRIPTS%) do (
    set /a COUNTER+=1
    if !SUCCESSFUL_SCRIPTS! GEQ !COUNTER! (
        timeout /T 1 >nul
    ) else (
        echo Running script "%%i"...
        call %%i
        if errorlevel 1 (
            echo Script "%%i" failed. Marking script for retry...
            set ERROR_SCRIPT=%%i
            timeout /T 5
            goto :retry
        ) else (
            set /a SUCCESSFUL_SCRIPTS+=1
            echo Script "%%i" completed successfully.
            timeout /T 5 >nul
        )
    )
)
echo All scripts completed successfully.
exit /b

:retry
echo Retrying script "%ERROR_SCRIPT%"...
call %ERROR_SCRIPT%
if errorlevel 1 (
    echo Script "%ERROR_SCRIPT%" failed again. Retrying in %RETRY_TIMEOUT% seconds...
    timeout /T %RETRY_TIMEOUT%
    goto :retry
) else (
    set /a SUCCESSFUL_SCRIPTS+=1
    echo Script "%ERROR_SCRIPT%" completed successfully.
    timeout /T 5 >nul
    set ERROR_SCRIPT=
    set COUNTER=0
    goto :loop
)
