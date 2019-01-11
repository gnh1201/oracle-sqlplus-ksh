#!/bin/ksh

# get tables
(echo "SELECT concat(concat(owner, '.'), table_name) as tablename FROM all_tables WHERE owner = 'DBUSER';" | sqlplus '/as sysdba') > hello.txt

file="hello.txt"
# while loop
while IFS= read -r line
do
        if [[ "$line" != "TABLENAME" && "$line" != "-------------------------------------------------------------" && "$line" != "" ]];then
            echo "@DUMPSTART"
            echo "@TABLENAME $line"
            echo "
                set linesize 30000;
                select * from (select * from $line) t where ROWNUM < 6;
            "  | sqlplus -s '/as sysdba'
            echo "@DUMPEND"
        fi
done <"$file"
