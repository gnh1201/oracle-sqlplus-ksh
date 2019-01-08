#!/bin/ksh

# get tables
(echo "SELECT concat(concat(owner, '.'), table_name) as tablename FROM all_tables WHERE owner = 'ORCL';" | sqlplus -s '/as sysdba') > hello.txt

file="hello.txt"
# while loop
while IFS= read -r line
do
        if [[ "$line" != "TABLENAME" && "$line" != "-------------------------------------------------------------" && "$line" != "" ]];then
            echo "$line"
            echo "column column_name format a30;
                set linesize 300;
                select * from (select * from $line) t where ROWNUM < 6);"  | sqlplus -s '/as sysdba'
        fi
done <"$file"
