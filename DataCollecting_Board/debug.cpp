/*
	This source file defines the DEBUG function used
	for the potential debugging requirements considering
	that there is not a user-friendly Arduino IDE and
	debugger under Liunx and MacOS like Visual Micro working
	with Visual Studio under Windows.
	My implementation refers to the idea of the printf
	function in C standard library.

  Last modified date: 17 March, 2017
  Author: Xiangyi Meng
  E-Mail: xymeng16@gmail.com
*/
#ifndef _DEBUG_H_
#define _DEBUG_H_
#include <stdarg.h>
#include <string.h>
#include "Arduino.h"
#define _DEBUG
int _vDEBUG(char *fmt, va_list args)
{
  char ch, tmp_ch, *tmp_str;
  int len = 0, tmp_int;
  double tmp_dbl;
  char buf[512];
  bool new_line = false;
  while (ch = *fmt++)
  {
    if ('%' == ch)
    {
      switch (ch = *fmt++)
      {
        case '%':
          {
            Serial.print('%');
            len++;
            break;
          }
        case 'c':
          {
            tmp_ch = va_arg(args, int);
            Serial.print(tmp_ch);
            len++;
            break;
          }
        case 'd':
          {
            tmp_int = va_arg(args, int);
            Serial.print(tmp_int);
            while (tmp_int /= 10)
              len++;
            len++;
            break;
          }
        case 'x':
          {
            tmp_int = va_arg(args, int);
            Serial.print(tmp_int, HEX);
            while (tmp_int /= 16)
              len++;
            len++;
            break;
          }
        case 'f':
          {
            tmp_dbl = va_arg(args, double);
            Serial.print((float)tmp_dbl);
            len += 2; // Serial.print has a fixed width 2 for float and double type variable.
            tmp_int = tmp_dbl;
            while (tmp_int /= 10)
              len++;
            break;
          }
        case 's':
          {
            tmp_str = va_arg(args, char *);
            Serial.print(tmp_str);
            len += strlen(tmp_str);
            break;
          }
        case 'b':
          {
            tmp_int = va_arg(args, int);
            if (tmp_int == 0)
            {
              Serial.print("false");
            }
            else
            {
              Serial.print("true");
            }
            break;
          }
      }
    }
    else
    {
      Serial.print(ch);
      len++;
    }
  }
  return len;
}

int DEBUG(char *format, ...)
{
  // int vDEBUG(char *, va_list);
  {
    va_list arguments;
    int len;

    va_start(arguments, format);
    len = _vDEBUG(format, arguments);
    va_end(arguments);

    return len;
  }

}
#endif
