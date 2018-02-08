#!/bin/sh
# 2001
#awk "/^<h5>/ {gsub(/href=\"/, \"\"); gsub(/\">Game/, \"\"); print \$5;}" $1 |\
#	awk -F '/' "{print \"curl -o \" \$NF \" https://macalester_ftp.sidearmsports.com/custompages/softball_stats/stats01/\" \$NF;}"

# 2002
#awk "/^<h5>/ {gsub(/href=\"/, \"\"); gsub(/\">Game/, \"\"); print \$5;}" $1 |\
#	awk -F '/' "{print \"curl -o \" \$NF \" https://macalester_ftp.sidearmsports.com/custompages/softball_stats/stats02/\" \$NF;}"

# 2003/4
#awk "/^<h5>/ {gsub(/href=\"/, \"\"); gsub(/\">Game/, \"\"); print \$5;}" $1 |\
#	awk -F '/' "{print \"curl -o \" \$NF \" \" \$_;}"

# 2005
#awk "/^<h5>/ {gsub(/href=\"/, \"\"); gsub(/\">Game/, \"\"); print \$7;}" $1 |\
#	awk -F '/' "{print \"curl -o \" \$NF \" https://macalester_ftp.sidearmsports.com/custompages/softball_stats/stats05/\" \$NF;}"

# 2006
#awk "/^<td.*<a href=/ {gsub(/href=\"/, \"\"); gsub(/\">Box/, \"\"); print \$6;}" $1 |\
#	awk "{print \"curl -o \" \$NF \" https://macalester_ftp.sidearmsports.com/custompages/softball_stats/stats06/\" \$NF;}"

# 2007
#awk "/^<td.*<a href=/ {gsub(/href=\"/, \"\"); gsub(/\">Box/, \"\"); print \$6;}" $1 |\
#	awk "{print \"curl -o \" \$NF \" https://macalester_ftp.sidearmsports.com/custompages/softball_stats/stats07/\" \$NF;}"

# 2008
#awk "/^<td.*<a href=/ {gsub(/href=\"/, \"\"); gsub(/\">Box/, \"\"); print \$6;}" $1 |\
#	awk "{print \"curl -o \" \$NF \" https://macalester_ftp.sidearmsports.com/custompages/softball_stats/stats08/\" \$NF;}"

# 2009
#awk "/^<td.*<a href=/ {gsub(/href=\"/, \"\"); gsub(/\">Box/, \"\"); print \$6;}" $1 |\
#	awk "{print \"curl -o \" \$NF \" https://macalester_ftp.sidearmsports.com/custompages/softball_stats/stats09/\" \$NF;}"

# 2010
#awk "/^<td.*<a href=/ {gsub(/href=\"/, \"\"); gsub(/\">Box/, \"\"); print \$6;}" $1 |\
#	awk "{print \"curl -o \" \$NF \" https://macalester_ftp.sidearmsports.com/custompages/softball_stats/stats10/\" \$NF;}"

# 2011
#awk "/^<td.*<a href=/ {gsub(/href=\"/, \"\"); gsub(/\">Box/, \"\"); print \$6;}" $1 |\
#	awk "{print \"curl -o \" \$NF \" https://macalester_ftp.sidearmsports.com/custompages/softball_stats/stats11/\" \$NF;}"

# 2012
#awk "/^<td.*<a href=/ {gsub(/href=\"/, \"\"); gsub(/\">Box/, \"\"); print \$6;}" $1 |\
#	awk "{print \"curl -o \" \$NF \" https://macalester_ftp.sidearmsports.com/custompages/softball_stats/stats12/\" \$NF;}"

# 2013
#awk "/^<td.*<a href=/ {gsub(/href=\"/, \"\"); gsub(/\">Box/, \"\"); print \$6;}" $1 |\
#	awk "{print \"curl -o \" \$NF \" https://macalester_ftp.sidearmsports.com/custompages/softball_stats/stats13/\" \$NF;}"

# 2014
#awk "/^<td.*<a href=/ {gsub(/href=\"/, \"\"); gsub(/\">Box/, \"\"); print \$6;}" $1 |\
#	awk "{print \"curl -o \" \$NF \" https://macalester_ftp.sidearmsports.com/custompages/softball_stats/stats14/\" \$NF;}"

# 2015/16/17
awk "/<a href='boxscore.aspx/ {tmp=match(\$0, /a href='([^']+)'/, file); if(tmp){match(file[1], /id=([0-9]+)/, id); print \"curl -o \" id[1] \".htm \\\"http://athletics.macalester.edu/\" file[1] \"&clean=true\\\"\"}}" $1 | sort | uniq
