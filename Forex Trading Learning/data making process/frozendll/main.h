#ifndef __MAIN_H__
#define __MAIN_H__

#include <windows.h>

/*  To use this exported function of dll, include this header
 *  in your project.
 */

#ifdef BUILD_DLL
    #define DLL_EXPORT __declspec(dllexport)
#else
    #define DLL_EXPORT __declspec(dllimport)
#endif


#ifdef __cplusplus
extern "C"
{
#endif
#ifdef __cplusplus
void	SetTrigger(int value);
int		GetTrigger();
void	SetValues(double open, double high, double low, double close);
double	GetValues(int index);

}
#endif

int* 		triggers;
double*  	values;

#endif // __MAIN_H__



