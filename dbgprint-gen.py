import datetime

MAX_LINE = 120

FILE_HEADER_TMPL = """#ifndef __DBGPRINT_TYPES_H__\n"
"#define __DBGPRINT_TYPES_H__\n"
"/**\n"
" * GENARATED CODE - BETTER DON'T TOUCH ME\n"
" * @date: {:s}\n"
" */\n"""

class G_:
    def __init__(self, module, context, session):
        self._module = module
        self._context = context
        self._session = session

    def _(self, name, num):
        prototype_wrapped = "#define __" + name + "_{:03d}".format(num) + "__(loglv,"
        macro_content = " \\\ndo { \\\n"
        content_wrapped = "   __u8 __buffer__[ " + str(num) + " ] = { __TRACE_FILE_ID__,"
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
        macro_content += "   __LOG__(_000, __LINE__, (__u8*)__buffer__, " + str(num) + ", loglv); \\\n"
        macro_content += "   (void)strlen(_000); \\\n"

        return macro_prototype + ")" + macro_content + "} while (0)"

    def _run(self, name, num):
        dispatcher_macro = "#define __" + name + "__( \\\n{:s}, __macro__, ...) __macro__"
        main_macros = "#define " + name + "{:s}(...) __" + name + "__(__VA_ARGS__, \\\n{:s})({:s}, __VA_ARGS__)"
        result = ""
        args1 = ""
        args2 = ""
        number_of_element = int(MAX_LINE/(len(name) + 8))

        delimiter = "    "

        result += FILE_HEADER_TMPL.format(str(datetime.datetime.now()))
        result += "#define __LOG__(fmt, id, buff, size, lglv) \n"

        for i in range(num):
            result += self._(name, i + 1) + "\n"
            args1 += delimiter + "_" + "{:03}".format(i)
            args2 += delimiter + "__" + name + "_" + "{:03}".format(num - i) + "__"

            if (1 + i) % number_of_element == 0:
                args2 += " \\\n   "

            if (1 + i) % 14 == 0:
                args1 += " \\\n   "

            delimiter = ","

        result += dispatcher_macro.format(args1) + "\n"

        for i in ["ERROR", "DEBUG", "INFO"]:
            result += main_macros.format(i[0], args2, i) + "\n" 
        
        result += "#endif /* __DBGPRINT_TYPES_H__ */\n"
        return result
    def generate(self, prefix, file, num):
        
        content = self._run(prefix, num)
        with open(file, "w") as fd:
            fd.write(str(content))

if __name__ == "__main__":
    dlt = G_("MOD_ID", "Ctx", "Sess")
    dlt.generate("DbgPrint_Log", "dbgprint_types.h", 128)
