#include <Python.h>
#include <stdio.h>
#include <string.h>
#include <vcruntime.h>

#define PYPATH_SIZE 10000

int main(int argc, char **argv)
{
  char *pythonhome;
  wchar_t *wpythonhome;

  char *repo;
  wchar_t *wrepo;

  char *filename;
  FILE *fp;

  wprintf(L"================= py_file_run.exe ====================\n");

  /* CLI argument parsing ****************************************************/
  if ((argc < 1) || (argc > 4))
  {
    fprintf(stderr, "USAGE: py_file_run.exe C:/Python39 test_filepath.py\n");
    return 1;
  }
  else
  {
    pythonhome = argv[1]; /* e.g. C:\s\eklang\venv\py39 */
    wpythonhome = Py_DecodeLocale(pythonhome, NULL);
    printf("py_file_run: pythonhome = %s\n", pythonhome);

    filename = argv[2]; /* e.g. C:\s\eklang\src\lib\tests\test_m_logic_flex.py */
    printf("py_file_run: filename = %s\n", filename);

    fflush(stdout);
  }

  /* Set python path *********************************************************/
  wchar_t pypath[PYPATH_SIZE];
  printf("py_file_run: Python is NOT a virtual environment\n");
  swprintf(pypath, PYPATH_SIZE,
                                                   /* where {pythondir} C:\hostedtoolcache\windows\Python\3.9.9 */
           L"%s;"                                  // {pythondir}
           L"%s\\DLLs;"                            // {pythondir}\DLLs
           L"%s\\Lib;"                             // {pythondir}\Lib
           L"%s\\Lib\\site-packages;"              // {pythondir}\Lib\site-packages
           L"%s\\Lib\\site-packages\\win32;"       // {pythondir}\Lib\site-packages\win32
           L"%s\\Lib\\site-packages\\win32\\lib;"  // {pythondir}\Lib\site-packages\win32\Lib
           L"%s\\Lib\\site-packages\\Pythonwin;"   // {pythondir}\Lib\site-packages\Pythonwi
           ,
           wpythonhome, wpythonhome, wpythonhome, wpythonhome,
           wpythonhome, wpythonhome, wpythonhome);
  wprintf(L"Py_SetPath = %s\n", pypath);
  wprintf(L"======================================================\n");
  fflush(stdout);

  Py_SetPath(pypath);

  /* Run Python Script *******************************************************/
  Py_Initialize();

  fp = _Py_fopen(filename, "rb");
  PyRun_SimpleFile(fp, filename);

  Py_Finalize();

  return 0;
}
