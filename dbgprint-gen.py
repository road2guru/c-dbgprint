import datetime
import argparse
import ntpath

MAX_LINE = 80

FILE_CONTENT_TMPL = """#ifndef __{:s}__
#define __{:s}__

/**
 * GENARATED CODE - BETTER DON'T TOUCH ME
 * @date: {:s}
 */

#ifndef __{:s}__
#define __{:s}__(fmt, id, buff, size, lglv)
#endif /* __{:s}__ */

{:s}
/* data type converter */
#define  __u8(x)                (0xff & (x))
#define __u16(x)      __u8(x),  (0xff & (x >> 8))
#define __u32(x)      __u16(x), (0xff & (x >> 16)), (0xff & (x >> 24))
#define __u64(x)      __u32(x), (0xff & (x >> 32)), (0xff & (x >> 40)), \\
                                (0xff & (x >> 48)), (0xff & (x >> 56))

#endif /* __{:s}__ */
/* ----EOF---- */
"""

class G_:
    def __init__(self):
        pass

    def _(self, name, num):
        prototype_wrapped = "#define __" + name + "_{:03d}".format(num) + "__(loglv,"
        macro_content = " \\\ndo { \\\n"
        content_wrapped = "   __u8 __buffer__[ " + str(num) + " ] = { __TRACE_FILE_ID__"
        if num > 1: # since 1st param is format string
            content_wrapped += ","
            
        macro_prototype = ""
        delimiter = ""

        for i in range(num):
            # wrap macro prototype
            if len(prototype_wrapped + delimiter + "_{:03d}".format(i))  >= MAX_LINE:
                macro_prototype += prototype_wrapped + " \\\n   "
                prototype_wrapped = delimiter + "_{:03d}".format(i)
            else:
                prototype_wrapped += delimiter + "_{:03d}".format(i)

            if i < num - 1:
                # wrap macro body
                if len (content_wrapped + delimiter + "_{:03d}".format(1 + i)) >= MAX_LINE:
                    macro_content += content_wrapped + " \\\n      "
                    content_wrapped = delimiter + "_{:03d}".format(1 + i)
                else:
                    content_wrapped += delimiter + "_{:03d}".format(1 + i)
            
            delimiter = ","
        
        macro_prototype += prototype_wrapped;
        macro_content += content_wrapped + " }; \\\n"
        macro_content += ("   __{:s}__(_000, __LINE__, ((__u8*)__buffer__), " + str(num) + ", loglv); \\\n").format(name)
        macro_content += "   (void)strlen(_000); \\\n"

        return macro_prototype + ")" + macro_content + "} while (0)"

    def _run(self, name, num):
        dispatcher_macro = "#define __" + name + "_000__( \\\n{:s}, __macro__, ...) __macro__"
        main_macros = "#define " + name + "{:s}(...) __" + name + "_000__(__VA_ARGS__, \\\n{:s})({:s}, __VA_ARGS__)"
        delimiter = "    "
        result = ""
        args1 = ""
        args2 = ""

        for i in range(num):
            result += self._(name, i + 1) + "\n"
            args1 += delimiter + "_" + "{:03}".format(i)
            args2 += delimiter + "__" + name + "_" + "{:03}".format(num - i) + "__"

            if (1 + i) % (int(MAX_LINE/(len(name) + 9))) == 0:
                args2 += " \\\n   "

            if (1 + i) % (int(MAX_LINE/5)) == 0:
                args1 += " \\\n   "

            delimiter = ","

        result += dispatcher_macro.format(args1) + "\n"

        for i in ["FATAL", "ERROR", "WARNING", "INFO", "DEBUG", "VERBOSE"]:
            result += main_macros.format(i[0], args2, i) + "\n" 

        return result
    def generate(self, prefix, file, num):
        fname = ntpath.basename(file)
        content = self._run(prefix, num)
        with open(file, "w") as fd:
            fd.write(FILE_CONTENT_TMPL.format(
                fname.upper().replace(".", "_"), 
                fname.upper().replace(".", "_"), 
                str(datetime.datetime.now()),
                prefix,
                prefix,
                prefix,
                content, 
                fname.upper().replace(".", "_"))
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--prefix', help='Logger prefix')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--size', type=int, help='Maximize size (in byte) per print')
    args = parser.parse_args()
    
    if args.prefix == None or args.output == None or args.size == None:
        print('Invalid arguments\n')
        parser.print_help()
    else:
        G_().generate(prefix=args.prefix, file=args.output, num=args.size)
