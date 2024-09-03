#
#  Copyright (c) 2016-2024 Magic Control Technology Corp.
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
#   author: louis@mct.com.tw



GREEN   = \033[1;32m

WHITE   = \033[0;m

NAME    = triggerdm

CC      = gcc -g

RM      = rm -f

SRCS    = main.c t6usbdongle.c cea_edid.c simclist.c

OBJS    = $(SRCS:.c=.o)

CFLAGS  = -I ./ 

LDFLAGS = -levdi -lusb-1.0 -lturbojpeg -lc -lpthread

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
