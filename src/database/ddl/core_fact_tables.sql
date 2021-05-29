----=============================================
---- Author     :
---- Create date:
---- Description:  Main address database
----
----
----
---- Version		Date        Description(of Changes)
---- 1.0		Created
----=============================================


----=============================================
--  Create statements for FACT tables
----=============================================

----=============================================
--   Drop statements
----=============================================

DROP TABLE address_details;
DROP TABLE staging_input_data cascade;
DROP TABLE staging_processed_address;

DROP SEQUENCE address_details_address_id_seq;
DROP SEQUENCE staging_input_data_id_seq;

----=============================================
--  Fact tables
----=============================================


CREATE SEQUENCE address_details_address_id_seq INCREMENT BY 1 MINVALUE 100 MAXVALUE 99999999;

CREATE TABLE address_details
(
    id serial PRIMARY KEY,
    system_creation_date timestamp without time zone,
    system_update_date timestamp without time zone,
    user_id text,

    address_id bigint default nextval('address_details_address_id_seq') not null,
    pobox_type text,
    pobox_number text,
	building_name text,
	department_name text,
	flat_number text,
	flat_type   text,
	flat_number_suffix text,
	level_number   text,
	level_type     text,
	level_number_suffix text,
	number_first   text,
	number_suffix  text,
	number_last    text,
	street_name     text,
	street_type     text,
	suburb          text,
	postcode     character varying(4),
	state        character varying(4),
	latitude     numeric(11,8),
	longitude    numeric(11,8),
	parcel_id    text,
	premises_type text,
	postal_id text,

	UNIQUE (address_id)
 )
WITH (
    OIDS = FALSE
);


----=============================================
--  staging area where different system will supply input data
----=============================================

-- CREATE SEQUENCE staging_input_data_id_seq INCREMENT BY 1 MINVALUE 100 MAXVALUE 99999999;

CREATE TABLE staging_input_data
(
    -- id integer default nextval('staging_input_data_id_seq'),
    id serial PRIMARY KEY,
    system_creation_date timestamp without time zone,
    system_update_date timestamp without time zone,
    user_id text,
    system_type text,
    source_key text,
    address_type text,
    address_line1 text,
    address_line2 text,
    suburb character varying(100),
    postcode character varying(4),
    state  character varying(4)
)
WITH (
    OIDS = FALSE
);


CREATE TABLE staging_processed_address
(
    id serial PRIMARY KEY,
    system_creation_date timestamp without time zone,
    system_update_date timestamp without time zone,
    user_id text,
    source_input_id bigint references staging_input_data(id),
    pobox_type text,
    pobox_number text,
	building_name text,
	department_name text,
	flat_number text,
	flat_type   text,
	flat_number_suffix text,
	level_number   text,
	level_type     text,
	level_number_suffix text,
	number_first   text,
	number_suffix  text,
	number_last    text,
	street_name     text,
	street_type     text,
	suburb          text,
	postcode     character varying(4),
	state        character varying(4),
	latitude     numeric(11,8),
	longitude    numeric(11,8),
	parcel_id    text,
	premises_type text,
	postal_id text,
    rank integer,
    exception_flag char(1)
 )
WITH (
    OIDS = FALSE
);



CREATE TABLE google_places
(
    id  serial PRIMARY KEY,
    place_id text,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id character varying(30),
    street_number text,
    street_name text,
    state text,
    suburb text,
    county text,
    country text,
    postcode text,
    neighborhood text,
    sublocality text,
    housenumber text,
    town text,
    subpremise text,
    latitude text,
    longitude text,
    location_type text,
    postal_code_suffix text,
    business_name text,
    formatted_phone_number text,
    international_phone_number text,
    trading_hours_mon text,
    trading_hours_tue text,
    trading_hours_wed text,
    trading_hours_thu text,
    trading_hours_fri text,
    trading_hours_sat text,
    trading_hours_sun text,
    web_website text,
    permanently_closed text,
    rating numeric(2),
    price_level text,
    scope text,
    types text[],
    exception_flag character (1),
    UNIQUE (place_id)
 )
WITH (
    OIDS = FALSE
);
