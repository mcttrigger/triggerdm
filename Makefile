GREEN   = \033[1;32m

WHITE   = \033[0;m

NAME    = T6evdi

CC      = gcc -g

RM      = rm -f

SRCS    = main.c t6usbdongle.c cea_edid.c simclist.c

OBJS    = $(SRCS:.c=.o)

CFLAGS  = -I ./ 

LDFLAGS = -levdi -lusb-1.0 -lturbojpeg -lc -lm -lpthread

all: $(NAME)

$(NAME): $(OBJS)
	@$(CC) $(OBJS) -o $(NAME) $(LDFLAGS)
	@printf "\n[$(GREEN)OK$(WHITE)] Binary : $(NAME)\n"
	@echo "-------------------\n"

%.o :    %.c
	@$(CC) $(CFLAGS) -c -o $@ $<
	@printf "[$(GREEN)OK$(WHITE)] $<\n"


fclean:
	$(RM) $(OBJS)

clean: fclean
	$(RM) $(NAME)
