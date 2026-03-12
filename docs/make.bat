@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

set SOURCEDIR=source
set BUILDDIR=build

if "%1" == "" goto help

python -m sphinx -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:help
python -m sphinx -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd
