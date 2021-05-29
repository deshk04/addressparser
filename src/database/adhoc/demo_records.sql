--=============================================
-- Author     :  
-- Create date:  
-- Description:  demo sample records
--
--
--
-- Version        Date        Description(of Changes)
-- 1.0        Created
--=============================================

-- object table

INSERT INTO object
(
    record_creation_date,
    record_user, 
    object_id, 
    object_type, 
    object_key, 
    effective_date, 
    expiration_date,
    brand,
    address_id
)
select
    now(),
    'demo',
    object_id,
    object_type,
    object_key,
    effective_date,
    expiration_date,
    'demo',
    address_id
FROM dblink('password=unix11 dbname=pdm',
            'select
                t1.object_id,
                t1.object_type,
                t1.object_key,
                t1.effective_date,
                t1.expiration_date,
                t2.address_id
             from object t1 left join object_address t2
             on t1.object_id = t2.object_id
             and t2.address_type = ''P''
            '
)
AS X
(

    object_id  bigint,
    object_type  text,
    object_key  text,
    effective_date  date,
    expiration_date  date,
    address_id integer
)
;


-- object_address table

-- INSERT INTO object_address
-- (
--     record_creation_date,
--     record_user, 
--     object_id, 
--     address_type,
--     address_id, 
--     effective_date, 
--     expiration_date
-- )
-- select
--     now(),
--     'demo',
--     object_id,
--     'P',
--     address_id,
--     effective_date,
--     expiration_date
-- FROM dblink('password=unix11 dbname=pdm',
--             'select
--                 object_id,
--                 object_type,
--                 object_key,
--                 address_id,
--                 effective_date,
--                 expiration_date
--              from object
--             '
-- )
-- AS X
-- (

--     object_id  bigint,
--     object_type  text,
--     object_key  text,
--     address_id bigint,
--     effective_date  date,
--     expiration_date  date

-- )
-- ;


-- object_relation table

INSERT INTO object_relation
(
    record_creation_date,
    record_user, 
    object_id, 
    relation_type,
    child_object_id, 
    effective_date, 
    expiration_date
)
select
    now(),
    'demo',
    object_id,
    relation_type,
    child_object_id,
    effective_date,
    expiration_date
FROM dblink('password=unix11 dbname=pdm',
            'select
                object_id,
                relation_type,
                child_object_id,
                effective_date,
                expiration_date
             from object_relation
            '
)
AS X
(
    object_id  bigint,
    relation_type  text,
    child_object_id bigint,
    effective_date  date,
    expiration_date  date

)
;


-- provider table

INSERT INTO provider
(
    record_creation_date,
    record_user, 
    object_id,
    provider_number, 
    start_date,
    end_date, 
    status_id
)
select
    now(),
    'demo',
    object_id,
    provider_number,
    start_date,
    end_date,
    cast(provider_status as integer)
FROM dblink('password=unix11 dbname=pdm',
            'select
                object_id,
                provider_number,
                start_date,
                end_date,
                case when status = ''closed''
                then
                    7
                else
                    1
                end as provider_status
             from provider
            '
)
AS X
(
    object_id  bigint,
    provider_number  text,
    start_date date,
    end_date date,
    provider_status  text
)
;


-- person table

INSERT INTO person
(
    record_creation_date,
    record_user, 
    object_id,
    sex, 
    title,
    first_name, 
    middle_name,
    last_name
)
select
    now(),
    'demo',
    object_id,
    sex,
    title,
    first_name,
    middle_name,
    last_name
FROM dblink('password=unix11 dbname=pdm',
            'select
                object_id,
                sex,
                t2.id as title,
                first_name,
                middle_name,
                last_name
             from person t1 left join dim_badf_titles t2
             on t1.title = t2.title_code
            '
)
AS X
(
    object_id  bigint,
    sex  character(1),
    title  integer,
    first_name text,
    middle_name text,
    last_name  text
)
;


-- practice table

INSERT INTO practice
(
    record_creation_date,
    record_user, 
    object_id,

	practice_name,
    abn,
	website,
	trading_hours_mon,
	trading_hours_tue,
	trading_hours_wed,
	trading_hours_thu,
	trading_hours_fri,
	trading_hours_sat,
	trading_hours_sun,
    google_place_id,
    closed_flag
)
select
    now(),
    'demo',
    object_id,

    practice_name,
    abn,
    website,
	trading_hours_mon,
	trading_hours_tue,
	trading_hours_wed,
	trading_hours_thu,
	trading_hours_fri,
	trading_hours_sat,
	trading_hours_sun,
    google_place_id,
    closed_flag

FROM dblink('password=unix11 dbname=pdm',
            'select
                object_id,
                practice_name,
                abn,
                website,
                trading_hours_mon,
                trading_hours_tue,
                trading_hours_wed,
                trading_hours_thu,
                trading_hours_fri,
                trading_hours_sat,
                trading_hours_sun,
                google_place_id,
                closed_flag

             from practice
            '
)
AS X
(
    object_id  bigint,
    practice_name text,
    abn text,
    website text,
    trading_hours_mon text,
    trading_hours_tue text,
    trading_hours_wed text,
    trading_hours_thu text,
    trading_hours_fri text,
    trading_hours_sat text,
    trading_hours_sun text,
    google_place_id text,
    closed_flag character(1)
)
;


-- ahpra_mapping table

INSERT INTO speciality_mapping
(
    record_creation_date,
    record_user, 
    object_id,
    professionalnumber
    
)
select
    now(),
    'demo',
    object_id,
    professionalnumber
FROM dblink('password=unix11 dbname=pdm',
            'select
                object_id,
                professionalnumber
             from ahpra_mapping
            '
)
AS X
(
    object_id  bigint,
    professionalnumber character varying(13)
)
;


-- address_details table

INSERT INTO address_details
(
    record_creation_date,
    record_user, 

    address_id,
    building_name,                      
    flat_number,              
    flat_type,     
    flat_number_suffix,      
    level_number,              
    level_type,     
    level_number_suffix,      
    number_first,              
    number_suffix,      
    number_last,              
    street_name,    
    street_type,     
    suburb,    
    postcode,      
    state,      
    latitude,             
    longitude,             
    parcel_id,     
    premises_type,
    postal_id         
)
select
    now(),
    'demo',
    address_id,
    building_name,                      
    flat_number,              
    flat_type,     
    flat_number_suffix,      
    level_number,              
    level_type,     
    level_number_suffix,      
    number_first,              
    number_suffix,      
    number_last,              
    street_name,    
    street_type,     
    suburb,    
    postcode,      
    state,      
    latitude,             
    longitude,             
    parcel_id,     
    premises_type,
    postal_id     

FROM dblink('password=unix11 dbname=pdm',
            'select
                address_id,
                postal_id,     
                building_name,                      
                flat_number,              
                flat_type,     
                flat_number_suffix,      
                level_number,              
                level_type,     
                level_number_suffix,      
                number_first,              
                number_suffix,      
                number_last,              
                street_name,    
                street_type,     
                suburb,    
                postcode,      
                state,      
                latitude,             
                longitude,             
                parcel_id,     
                premises_type
             from address_details
            '
)
AS X
(
    address_id        bigint,
    postal_id         text,     
    building_name     text,                      
    flat_number       text,              
    flat_type         text,     
    flat_number_suffix text,      
    level_number      text,              
    level_type        text,     
    level_number_suffix  text,      
    number_first      text,              
    number_suffix     text,      
    number_last       text,              
    street_name       text,    
    street_type       text,     
    suburb            text,    
    postcode          character varying(4),      
    state             character varying(4),      
    latitude          numeric(11,8),             
    longitude         numeric(11,8),             
    parcel_id         text,     
    premises_type     text
)
;



-- contact_details table

INSERT INTO contact_details
(
    record_creation_date,
    record_user, 
    object_id,
	contact_type,
	contact_value    
)
select
    now(),
    'demo',
    object_id,
	contact_type,
	contact_value

FROM dblink('password=unix11 dbname=pdm',
            'select
                object_id,
                contact_type,
                contact_value
             from contact_details
            '
)
AS X
(
 object_id         bigint,                      
 contact_type      text, 
 contact_value     text                        
)
;


-- dimobject table

INSERT INTO dim_object
(
    record_creation_date,
    record_user, 
    object_id,
    object_type          ,
    object_brand         ,
    passport_number      , 
    driving_licence      , 
    medicare_number      , 
    date_of_birth        , 
    first_name           ,
    middle_name          ,
    last_name            ,
    stem                 , 
    practice_name        ,
    practice_postcode    , 
    practice_website     ,
    practice_suburb      ,
    practice_state       , 
    abn                  , 
    ahpra_numbers        ,
    provider_number      ,
    system_id            

)
select
    now(),
    'demo',
    object_id,
    object_type          ,
    object_brand         ,
    passport_number      , 
    driving_licence      , 
    medicare_number      , 
    date_of_birth        , 
    first_name           ,
    middle_name          ,
    last_name            ,
    stem                 , 
    practice_name        ,
    practice_postcode    , 
    practice_website     ,
    practice_suburb      ,
    practice_state       , 
    abn                  , 
    ahpra_numbers        ,
    provider_number      ,
    system_id            

FROM dblink('password=unix11 dbname=pdm',
            'select
                object_id,
                object_type          ,
                object_brand         ,
                passport_number      , 
                driving_licence      , 
                medicare_number      , 
                date_of_birth        , 
                first_name           ,
                middle_name          ,
                last_name            ,
                stem                 , 
                practice_name        ,
                practice_postcode    , 
                practice_website     ,
                practice_suburb      ,
                practice_state       , 
                abn                  , 
                ahpra_numbers        ,
                provider_number      ,
                system_id            

             from dim_object
            '
)
AS X
(

 object_id  bigint,
 object_type text, 
 object_brand text, 
 passport_number text, 
 driving_licence text, 
 medicare_number text, 
 date_of_birth date, 
 first_name text,
 middle_name  text, 
 last_name text, 
 stem text, 
 practice_name text,    
 practice_postcode character varying(4), 
 practice_website text, 
 practice_suburb text,  
 practice_state character varying(4), 
 abn character varying(11),
 ahpra_numbers text[], 
 provider_number text,
 system_id text        
)
;

SELECT setval('"dim_object_object_id_seq"', 
       (SELECT MAX(object_id)+1 
           FROM dim_object
       ) 
);



SELECT setval('"address_details_address_id_seq"', 
       (SELECT MAX(address_id)+1 
           FROM address_details
       ) 
);


