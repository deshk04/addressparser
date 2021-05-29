----=============================================
---- Author     :
---- Create date:
---- Description:  dim tables
----
----
----
---- Version		Date        Description(of Changes)
---- 1.0		Created
----=============================================


----=============================================
--  Create statements for DIM tables
----=============================================


----=============================================
--   Drop statements
----=============================================

DROP TABLE dim_addr_abbr_words;
DROP TABLE dim_word_dictionary;
DROP TABLE dim_gnaf_streets;
DROP TABLE dim_addr_commonwords;
DROP TABLE dim_addr_pobox;
DROP TABLE dim_addr_patch;
DROP TABLE dim_gnaf_postcode;

DROP TABLE dim_premises_type;
DROP TABLE dim_name_abbr;

----=============================================
--   Dim tables
----=============================================

CREATE TABLE dim_addr_abbr_words
(
	suffixword character varying(30),
	primaryword character varying(60),
    typeFlag character (1),
    primary key(suffixword, primaryword)
)
WITH (
	OIDS = FALSE
);
--\copy dim_addr_abbr_words from '/addr/src/database/data/dim_addr_abbr_words.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE dim_gnaf_streets
(
  street_name      character varying(100),
  street_type character varying(15),
  suburb    character varying(100),
  postcode         character varying(4),
  state   character varying(3),
  street_length integer
)
WITH (
	OIDS = FALSE
);

/*
CREATE TABLE dim_gnaf_streets
AS
SELECT distinct
  street_name  as street_name
  ,street_type_code as street_type
  ,locality_name   as suburb
  ,postcode        as postcode
  ,state_abbreviation   as state
  ,length(street_name) as street_length
FROM
  addr.gnaf_address_details
 ;

*/

CREATE TABLE dim_addr_commonwords
(
  word      character varying(100)
)
WITH (
    OIDS = FALSE
);


CREATE TABLE dim_addr_pobox
(
  pobox      character varying(20)
)
WITH (
    OIDS = FALSE
);


CREATE TABLE dim_addr_patch
(
  sourcestring      character varying(80),
  destinationstring character varying(80),
  type character (1)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE dim_gnaf_postcode
(
  postcode  character varying(4),
  state   character varying(3)
)
WITH (
  OIDS = FALSE
);


CREATE TABLE dim_premises_type
(
	premises_type text primary key,
	description text
)
WITH (
    OIDS = FALSE
);


CREATE TABLE dim_name_abbr
(
	name  text,
	shortname  text
)
WITH (
    OIDS = FALSE
);

