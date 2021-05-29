-- \set PGPASSWORD `echo $PGPASSWORD`

DROP TABLE dim_gnaf_address_details;

CREATE TABLE dim_gnaf_address_details
AS
SELECT

 address_detail_pid,
 street_locality_pid,
 locality_pid,
 lower(building_name) building_name,
 lower(lot_number_prefix) lot_number_prefix,
 lot_number,
 lower(lot_number_suffix) lot_number_suffix,
 lower(flat_type) flat_type,
 lower(flat_number_prefix) flat_number_prefix,
 flat_number,
 lower(flat_number_suffix) flat_number_suffix,
 lower(level_type) level_type,
 lower(level_number_prefix) level_number_prefix,
 level_number,
 lower(level_number_suffix) level_number_suffix,
 lower(number_first_prefix) number_first_prefix,
 number_first,
 lower(number_first_suffix) number_first_suffix,
 lower(number_last_prefix) number_last_prefix,
 number_last,
 lower(number_last_suffix) number_last_suffix,
 lower(street_name) street_name,
 lower(street_class_code) street_class_code,
 lower(street_class_type) street_class_type,
 lower(street_type_code) street_type_code,
 lower(street_suffix_code) street_suffix_code,
 lower(street_suffix_type) street_suffix_type,
 lower(locality_name) locality_name,
 lower(state_abbreviation) state_abbreviation,
 postcode,
 latitude,
 longitude,
 lower(geocode_type) geocode_type,
 confidence,
 alias_principal,
 primary_secondary,
 legal_parcel_id,
 date_created

FROM dblink('host=localhost user=addruser password=M1ll4murr4 dbname=gnaf',
'select
 address_detail_pid,  street_locality_pid,  locality_pid,  building_name,  lot_number_prefix,  lot_number,  lot_number_suffix,  flat_type,
 flat_number_prefix,  flat_number,  flat_number_suffix,  level_type,  level_number_prefix,  level_number,  level_number_suffix, number_first_prefix,
 number_first,  number_first_suffix,  number_last_prefix, number_last,  number_last_suffix, street_name,  street_class_code, street_class_type,
 street_type_code, street_suffix_code,  street_suffix_type, locality_name,  state_abbreviation,  postcode,  latitude,  longitude,
 geocode_type,  confidence,  alias_principal,  primary_secondary, legal_parcel_id,  date_created

 from address_view')
AS x(
 address_detail_pid character varying(15) ,
 street_locality_pid character varying(15) ,
 locality_pid       character varying(15) ,
 building_name      text ,
 lot_number_prefix  character varying(2)  ,
 lot_number         character varying(5)  ,
 lot_number_suffix  character varying(2)  ,
 flat_type          character varying(50) ,
 flat_number_prefix character varying(2)  ,
 flat_number        numeric(5,0)          ,
 flat_number_suffix character varying(2)  ,
 level_type         character varying(50) ,
 level_number_prefix character varying(2)  ,
 level_number       numeric(3,0)          ,
 level_number_suffix character varying(2)  ,
 number_first_prefix character varying(3)  ,
 number_first       numeric(6,0)          ,
 number_first_suffix character varying(2)  ,
 number_last_prefix character varying(3)  ,
 number_last        numeric(6,0)          ,
 number_last_suffix character varying(2)  ,
 street_name        character varying(100),
 street_class_code  character(1)          ,
 street_class_type  character varying(50) ,
 street_type_code   character varying(15) ,
 street_suffix_code character varying(15) ,
 street_suffix_type character varying(50) ,
 locality_name      character varying(100),
 state_abbreviation character varying(3)  ,
 postcode           character varying(4)  ,
 latitude           numeric(10,8)         ,
 longitude          numeric(11,8)         ,
 geocode_type       character varying(50) ,
 confidence         numeric(1,0)          ,
 alias_principal    character(1)          ,
 primary_secondary  character varying(1)  ,
 legal_parcel_id    character varying(20) ,
 date_created       date

)
;

-- we also need to create dim_gnaf_postcode and dim_gnaf_streets


DROP TABLE dim_gnaf_postcode;

CREATE TABLE dim_gnaf_postcode
(
  id serial PRIMARY KEY,
  postcode character(4),
  state character(3)
);

INSERT INTO dim_gnaf_postcode
(
  postcode,
  state
)
SELECT
    distinct
        postcode,
        state_abbreviation as state
from dim_gnaf_address_details;

-- CREATE TABLE dim_gnaf_postcode
-- AS
-- SELECT
--     distinct
--         postcode,
--         state_abbreviation as state
-- from dim_gnaf_address_details;

DROP TABLE dim_gnaf_streets;

CREATE TABLE dim_gnaf_streets
(
  id serial PRIMARY KEY
  ,street_name character varying(100)
  ,street_type character varying(15)
  ,suburb  character varying(100)
  ,postcode character varying(4)
  ,state character varying(3)
  ,street_length integer
);

INSERT INTO dim_gnaf_streets
(
  street_name,
  street_type,
  suburb,
  postcode,
  state,
  street_length
)
SELECT distinct
  street_name  as street_name
  ,street_type_code as street_type
  ,locality_name   as suburb
  ,postcode        as postcode
  ,state_abbreviation   as state
  ,length(street_name) as street_length
FROM
  dim_gnaf_address_details;
