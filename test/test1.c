#include <stdio.h>
#include <string.h>

#define __TRACE_FILE_ID__ 1
typedef unsigned char __u8;

enum {
    ERROR,
    FATAL,
    WARNING,
    INFO,
    DEBUG,
    VERBOSE
};

#define __DbgPrint_Log__(fmt, id, buff, size, lglv) do { \
    __u8 i; \
    printf("[%3d] %s - log level: %d\n", id, fmt, lglv); \
    printf("%02x | ", buff[0]); \
    for (i = 1; i < size; i++) \
        printf("%02x ", buff[i]); \
    printf("\n"); \
} while(0)

#include "dbprint_types.h"

int main(int argc, char *argv[]) {
    DbgPrint_LogF("This is first line");
    DbgPrint_LogF("This is first line\n"
        "This is 2nd line", __u8(8), __u16(0x0011),
        __u32(0xaabbccdd), __u64(0x1122334455667788));

    DbgPrint_LogE("This is first line");
    DbgPrint_LogE("This is first line\n"
        "This is 2nd line", __u8(8), __u16(0x0011),
        __u32(0xaabbccdd), __u64(0x1122334455667788));

    DbgPrint_LogW("This is first line");
    DbgPrint_LogW("This is first line\n"
        "This is 2nd line", __u8(8), __u16(0x0011),
        __u32(0xaabbccdd), __u64(0x1122334455667788));
    
    DbgPrint_LogI("This is first line");
    DbgPrint_LogI("This is first line\n"
        "This is 2nd line", __u8(8), __u16(0x0011),
        __u32(0xaabbccdd), __u64(0x1122334455667788));

    DbgPrint_LogD("This is first line");
    DbgPrint_LogD("This is first line\n"
        "This is 2nd line", __u8(8), __u16(0x0011),
        __u32(0xaabbccdd), __u64(0x1122334455667788));

    DbgPrint_LogV("This is first line");
    DbgPrint_LogV("This is first line\n"
        "This is 2nd line", __u8(8), __u16(0x0011),
        __u32(0xaabbccdd), __u64(0x1122334455667788));

    return 0;
}
