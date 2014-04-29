# PRAGMAs are specific to SQLite3.
sed -i '/PRAGMA/d' $1
# Convert sequences.
sed -i '/sqlite_sequence/d ; s/integer PRIMARY KEY AUTOINCREMENT/serial PRIMARY KEY/ig' $1
# Convert column types.
sed -i 's/datetime/timestamp/g ; s/integer[(][^)]*[)]/integer/g ; s/text[(]\([^)]*\)[)]/varchar(\1)/g' $1
 
