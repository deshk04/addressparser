# G-NAF
To load gnaf data follow the below steps

## Step 1
```
    create database gnaf;
```
## Step 2
```
    download https://github.com/minus34/gnaf-loader in apps folder
```
## Step 3
```
    download and extract the G-NAF data under storage/dump folder
```

## Step 4
```
    python3 ./load-gnaf.py --gnaf-tables-path=/addr/storage/dump/G-NAF_MAY21_AUSTRALIA_GDA2020/ --admin-bdys-path=/addr/storage/dump/MAY21_AdminBounds_ESRIShapefileorDBFfile/ --pghost=addr_database --pgdb=gnaf --pguser=addruser --pgpassword=M1ll4murr4
```
## Step 5
```
    run apps/gnaf/scripts/06_create_view.sql in gnaf database
```

## Step 6
```
    run apps/gnaf/scripts/08_copy_view.sql in addrmain database
```
## Step 7
```
    run apps/gnaf/scripts/09_index_view.sql in addrmain database
```


