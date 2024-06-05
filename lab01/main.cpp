#include <windows.h>
#include <iostream>

typedef int (__stdcall *f_funci)(int a, int b);

int main()
{
  HINSTANCE hGetProcIDDLL = LoadLibrary("MathLibrary.dll");
  f_funci funci = (f_funci)GetProcAddress(hGetProcIDDLL, "suma");


  if (!funci) {
    std::cout << "could not locate the function" << std::endl;
    return EXIT_FAILURE;
  }
  
  int a = 5;
  int b = 10;

  std::cout << "suma() returned " << funci(a, b) << std::endl;

  return EXIT_SUCCESS;
}