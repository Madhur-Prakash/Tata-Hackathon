CONTIKI_PROJECT = battery-sim
TARGET = sky

all: $(CONTIKI_PROJECT)

CONTIKI = ../..
include $(CONTIKI)/Makefile.include

