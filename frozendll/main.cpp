#include "main.h"


BOOL WINAPI DllMain(HINSTANCE hinstDLL,DWORD fdwReason,LPVOID lpvReserved)
{
	int     size_of_first_handle = sizeof(int);
	const char*   name_of_first_handle = "frozen_trigger";
	int     size_of_second_handle = sizeof(double)*4;
	const char*   name_of_second_handle = "frozen_prices";

	HANDLE handleOne;
	HANDLE handleTwo;
	LPCTSTR bufOne;
	LPCTSTR bufTwo;

	switch(fdwReason)
	{
		case DLL_PROCESS_ATTACH:
		{
// first map ------------------------------------------------------------------------------------------------
// trigger - int type ---------------------------------------------------------------------------------------
			handleOne = CreateFileMapping(
			                INVALID_HANDLE_VALUE,    // use paging file
			                NULL,                    // default security
			                PAGE_READWRITE,          // read/write access
			                0,                       // maximum object size (high-order DWORD)
			                size_of_first_handle,                // maximum object size (low-order DWORD)
			                name_of_first_handle);
			bufOne = (LPTSTR) MapViewOfFile(
							handleOne,   // handle to map object
		                    FILE_MAP_ALL_ACCESS, // read/write permission
		                    0,
		                    0,
		                    size_of_first_handle);
			triggers = (int*) bufOne;
// second map ------------------------------------------------------------------------------------------------
			handleTwo = CreateFileMapping(
			                INVALID_HANDLE_VALUE,    // use paging file
			                NULL,                    // default security
			                PAGE_READWRITE,          // read/write access
			                0,                       // maximum object size (high-order DWORD)
			                size_of_second_handle,                // maximum object size (low-order DWORD)
			                name_of_second_handle);
			bufTwo = (LPTSTR) MapViewOfFile(
					handleTwo,   // handle to map object
					FILE_MAP_ALL_ACCESS, // read/write permission
					0,
					0,
					size_of_second_handle);
			values = (double*) bufTwo;
			break;
		}
		case DLL_PROCESS_DETACH:
		{
			UnmapViewOfFile(bufTwo);
			CloseHandle(handleTwo);
			UnmapViewOfFile(bufOne);
			CloseHandle(handleOne);
			break;
		}
		case DLL_THREAD_ATTACH:
		{
			break;
		}
		case DLL_THREAD_DETACH:
		{
			break;
		}
	}

	/* Return TRUE on success, FALSE on failure */
	return TRUE;
}


void	SetTrigger(int values)
{
	triggers[0] = values;
}

int	GetTrigger()
{
	return triggers[0];
}

void	SetValues(double open, double high, double low, double close)
{
	values[0] = open;
	values[1] = high;
	values[2] = low;
	values[3] = close;
}

double	GetValues(int index)
{
	return values[index];
}
