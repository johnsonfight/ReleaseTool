@echo off
goto start
:usage
@echo off
rem **************************************************************************
rem    System-specefic File for Dell Server 14G BIOS Release Utility - ver 1.0
rem    Copyright (C) 2017 Dell Inc.
rem **************************************************************************
echo    Usage: 
echo       release bios_ver [rev_type] [release_notes]
echo    Example:
echo        release r740 000212
echo        release r740 010000 A release.txt
echo    Input Parameters:
echo       (%%1) = (optional) "c" =^> Show collaterals included in BIOS
echo       (%%1) = Product name (r440/t440/r540)
echo       (%%2) = 6-digit BIOS version (e.g. 010000 for 1.0.0 BIOS)
echo       (%%3) = release type (X= Internal BIOS release, A= External BIOS release) [Default=X]
echo       (%%4) = Customer release notes (to be included Customer Disk Image) [Default=.\release.txt]
rem ************************************************************************
exit /b 0
:start
setlocal 
set codedir=%~dp0
set toolsdir=..\..\..\BuildTools\DellTools\release\
if /I "%1" == "c" goto ShowBiosIncludedCollaterals
rem ************************************************************************
rem Set platform-specefic environment variables 
rem ************************************************************************

set pid=%1

if /I "%pid%"=="r440" goto Taurus
if /I "%pid%"=="r540" goto Taurus
if /I "%pid%"=="t440" goto Taurus
if /I "%pid%"=="r740xd2" goto Spitzer


goto err_name


:Taurus
set project=Taurus
set project_dir=Taurus
set biosver=%2
set rev_type=%3
rem set biosfile=%codedir%%project%.EXE
set projefifile=%codedir%%project%.EFI
set projhdrfile=%codedir%%project%.HDR
set projcapfile=%codedir%%project%.CAP
set projromfile=%codedir%%project%.ROM
set symfile=%codedir%%project%.SYM
rem set pdbfile=%codedir%abios\minitdll.pdb
set location=T:\Projects\14G.TDC.projects\%Project%\Release\%biosver:~0,2%.%biosver:~2,2%.%biosver:~4,2%
rem Size of ROM part (512, 1024, 2048, or 4096 KB)
set size="32768"                  


rem Width of ROM part (8 or 16 bits)
set width="8"				

rem Size of ROM part (512, 1024, 2048, or 4096 KB)
rem set size="2048"				
rem set size="4096"				

rem Padding value for BIN file (00 or FF)
set fill="FF"				

rem Release archive directory
set release=%codedir%release.txt
if "%4" == "" goto start_all
set release=%4

:start_all
call %toolsdir%release2.bat

:ShowBiosIncludedCollaterals
pushd %toolsdir%
BiosIncludedCollaterals Taurus Purley.xml
popd
goto done

:Spitzer
set project_src=Taurus
set project=Spitzer
set project_dir=Spitzer
set biosver=%2
set rev_type=%3
rem set biosfile=%codedir%%project_src%.EXE
set projefifile=%codedir%%project_src%.EFI
set projhdrfile=%codedir%%project_src%.HDR
set projcapfile=%codedir%%project_src%.CAP
set projromfile=%codedir%%project_src%.ROM
set symfile=%codedir%%project_src%.SYM
rem set pdbfile=%codedir%abios\minitdll.pdb
set location=T:\Projects\14G.TDC.projects\%Project%\Release\%biosver:~0,2%.%biosver:~2,2%.%biosver:~4,2%
rem Size of ROM part (512, 1024, 2048, or 4096 KB)
set size="32768"                  


rem Width of ROM part (8 or 16 bits)
set width="8"				

rem Size of ROM part (512, 1024, 2048, or 4096 KB)
rem set size="2048"				
rem set size="4096"				

rem Padding value for BIN file (00 or FF)
set fill="FF"				

rem Release archive directory
set release=%codedir%release.txt
if "%4" == "" goto start_all
set release=%4

:start_all
call %toolsdir%release2.bat

:ShowBiosIncludedCollaterals
pushd %toolsdir%
BiosIncludedCollaterals Taurus Purley.xml
popd
goto done

:err_name
call :usage
:done
endlocal
 
echo.
