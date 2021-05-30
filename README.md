# addressparser
Australian address parser utility
## What is addressparser?
Addressparser is simple simple tool to transform an address line to Gnaf  address format.
For e.g. if you have below address line input

| Fields      | Values      |
| ----------- | ----------- |
| Line 1      | 102A/LVL 1 151-155 HAWKESBURY RD       |
| Suburb      | WESTMEAD        |
| Postcode      | 2145        |
| State      | NSW        |


Output will be
| Fields      | Values      |
| ----------- | ----------- |
| flat_number   | 102|
| flat_type      | unit        |
| flat_number_suffix      | a        |
| level_number      | 1        |
| level_type      | level       |
| level_number_suffix      |         |
| number_first      | 151        |
| number_suffix      |         |
| number_last      | 155        |
| street_name      | hawkesbury        |
| street_type      | road        |
| postcode      | 2145        |
| state      | nsw        |
| latitude      | -33.8071        |
| longitude      | 150.9882        |


## How to Install
Just run the docker

change directory to addressparser (downloaded repo path) and edit file .env under docker folder. update variable REPO_PATH to folder where addressparser repo is download.
```
REPO_PATH=c:\download\addressparser
```
you can then run docker compose from the docker folder, you are required to download G-NAF data and update the database
* [G-NAF Setup](src/apps/README.md)

## How to use
you can see the test code how the code is used or as simple as something like this
```
    addparser = AddressParser(
        address_line1='12/1-5 IVY ST',
        address_line2='',
        suburb='WOLLSTONECRAFT',
        postcode='2065',
        state='nsw'
    )
    addparser.parse()

```
for G-NAF related variable, pass the data to GnafHandler