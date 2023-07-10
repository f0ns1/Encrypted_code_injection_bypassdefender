@ECHO OFF

cl.exe /nologo /Ox /MT /W0 /GS- /DNDEBUG /Tcreverse.cpp /link /OUT:reverse.exe /SUBSYSTEM:CONSOLE /MACHINE:x64
