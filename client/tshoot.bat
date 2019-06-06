<<<<<<< HEAD
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: This file will need to pushed AppData\Local\NetLog folder on users'		::
:: computers, so that all logs can be locally saved in the same directory	::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

echo off
echo Gathering information, this window will close once completed.

:: Initializing variables to be used
set datef=%DATE:~10,4%%DATE:~4,2%%DATE:~7,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
set ipAdd=ipconfig /all
set lanStat=netsh lan show interfaces
set wlanStat=netsh wlan show interfaces
set pgPubDns=ping 8.8.8.8
set pgSdcDns=ping 10.15.98.64
set pgNdcDns=ping 10.23.98.64
set pgTnGov=ping tn.gov
set trcRtPubDns=tracert -d -h 15 8.8.8.8
set trcRtSdcDns=tracert -d -h 10 10.15.98.64
set trcRtNdcDns=tracert -d -h 10 10.23.98.64
set trcRtTnGov=tracert -d -h 10 tn.gov
set topAppMem=tasklist /fi "memusage gt 40000"

:: Create a dictionnary to be used for data parsing
echo { >> svr.json 
echo "ip" >> svr.json : "[
%ipAdd% >> svr.json
echo ] >> svr.json ", "lanStat" : "[
%lanStat% >> svr.json
echo ] >> svr.json ", "wlanStat" : "[
%wlanStat% >> svr.json
echo ] >> svr.json ", "pgPubDns" : "[
%pgPubDNS% >> svr.json
echo ] >> svr.json ", "pgSdcDns" : "[
%pgSdcDNS% >> svr.json
echo ] >> svr.json ", "pgNdcDns" : "[
%pgNdcDNS% >> svr.json
echo ] >> svr.json ", "pgTnGov" : "[
%pgTnGov% >> svr.json
echo ] >> svr.json ", "trcRtPubDns" : "[
%trcRtPubDNS% >> svr.json
echo ] >> svr.json ", "trcRtSdcDns" : "[
%trcRtSdcDns% >> svr.json
echo ] >> svr.json ", "trcRtNdcDns" : "[
%trcRtNdcDns% >> svr.json
echo ] >> svr.json ", "trcRtTnGov" : "[
%trcRtTnGov% >> svr.json
echo ] >> svr.json ", "topAppMem" : "[
%topAppMem% >> svr.json
echo ] >> svr.json "
echo } >> svr.json

:: Gathering computer info, and saving on local computer.
%ipAdd% >> TEST_%datef%_%computername%-%username%.txt
%lanStat% >> TEST_%datef%_%computername%-%username%.txt
%wlanStat% >> TEST_%datef%_%computername%-%username%.txt
%pgPubDNS% >> TEST_%datef%_%computername%-%username%.txt
%pgSdcDns% >> TEST_%datef%_%computername%-%username%.txt
%pgNdcDns% >> TEST_%datef%_%computername%-%username%.txt
%pgTnGov% >> TEST_%datef%_%computername%-%username%.txt
%trcRtPubDNS% >> TEST_%datef%_%computername%-%username%.txt
%trcRtSdcDns% >> TEST_%datef%_%computername%-%username%.txt
%trcRtNdcDns% >> TEST_%datef%_%computername%-%username%.txt
%trcRtTnGov% >> TEST_%datef%_%computername%-%username%.txt
:: The below command will only fetch those processes whose memory is greater than 40MB
%topAppMem% >> TEST_%datef%_%computername%-%username%.txt		

				
:: Time stamp end of script
echo %date%_%time% >> TEST_%datef%_%computername%-%username%.txt

::this will copy files in batch script across network
::copy c:\folder\file.ext \\dest-machine\destfolder /Z /Y

=======
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: This file will need to pushed AppData\Local\NetLog folder on users'		::
:: computers, so that all logs can be locally saved in the same directory	::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@echo off

del /Q svr.json

echo This utility is only to be used under direction of STS.
echo The running of this script is monitored by STS. It really is.
echo.
echo Hit enter to continue.  If you ran by accident, close the window.
echo.
PAUSE


echo Gathering information, this window will close once completed.


SET /P _username= Please enter your userid(ie agXXXX):
SET /P _tcktNum= Please enter ticket number(ask tech for it):

for /F "tokens=2" %%i in ('date /t') do set mydate=%%i
set mytime=%time%

:: Initializing variables to be used
set datef=%DATE:~10,4%%DATE:~4,2%%DATE:~7,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%

set ipAdd=ipconfig /all
set lanStat=netsh lan show interfaces
set wlanStat=netsh wlan show interfaces
set pgPubDns=ping 8.8.8.8
set pgSdcDns=ping 10.15.98.64
set pgNdcDns=ping 10.23.98.64
set pgTnGov=ping tn.gov
set trcRtPubDns=tracert -d -h 15 8.8.8.8
set trcRtSdcDns=tracert -d -h 10 10.15.98.64
set trcRtNdcDns=tracert -d -h 10 10.23.98.64
set trcRtTnGov=tracert -d -h 10 tn.gov
set topAppMem=tasklist /fi "memusage gt 40000"

:: Create a dictionnary to be used for data parsing

echo {"userId" >> svr.json : "
echo %_username% >> svr.json
echo  >> svr.json ", "ticketNum" : "
echo %_tcktNum% >> svr.json
echo  >> svr.json ", "runTmStmp" : "
echo %mydate%:%mytime% >> svr.json
echo  >> svr.json ", "ip" : "
%ipAdd% >> svr.json
echo  >> svr.json ", "wlanStat" : "
%wlanStat% >> svr.json
echo  >> svr.json ",  "pgPubDns" : "
%pgPubDNS% >> svr.json
echo  >> svr.json ", "pgSdcDns" : "
%pgSdcDNS% >> svr.json
echo  >> svr.json ", "pgNdcDns" : "
%pgNdcDNS% >> svr.json
echo  >> svr.json ", "pgTnGov" : "
%pgTnGov% >> svr.json
echo  >> svr.json ", "trcRtPubDns" : "
%trcRtPubDNS% >> svr.json
echo  >> svr.json ", "trcRtSdcDns" : "
%trcRtSdcDns% >> svr.json
echo  >> svr.json ", "trcRtNdcDns" : "
%trcRtNdcDns% >> svr.json
echo  >> svr.json ", "trcRtTnGov" : "
%trcRtTnGov% >> svr.json
echo  >> svr.json ", "topAppMem" : "
%topAppMem% >> svr.json
echo  >> svr.json "}

net use \\10.8.4.126\netDiag netDiag /user:netDiag

copy svr.json \\10.8.4.126\netDiag\diag-%_tcktNum%.json /Z /Y

copy svr.json %HOMEPATH%\Desktop\diag-%_tcktNum%.json

rm svr.json

::this will copy files in batch script across network
::copy c:\folder\file.ext \\dest-machine\destfolder /Z /Y
>>>>>>> 96c1bae83f0094a3677fdb0a9cf79a89f1c251fd
