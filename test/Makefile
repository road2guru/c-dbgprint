
all: prebuild test1

prebuild: ../dbgprint-gen.py
	@python ../dbgprint-gen.py --output=dbprint_types.h --prefix='DbgPrint_Log' --size=100

test1: test1.c
	@gcc -o $@ $<

clean:
	rm -f test1


