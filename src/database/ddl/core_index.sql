----=============================================
---- Author     :
---- Create date:
---- Description:  index
----
----
----
---- Version		Date        Description(of Changes)
---- 1.0		Created
----=============================================


----=============================================
--  Create index statements for FACT tables
----=============================================

----=============================================
--   Drop statements
----=============================================

DROP index address_details_address_id_idx;
DROP index address_details_long_lat_idx;
DROP index dim_gnaf_address_details_postcode_idx;

CREATE index address_details_address_id_idx ON address_details(address_id);
CREATE index address_details_long_lat_idx ON address_details(latitude, longitude);
CREATE index dim_gnaf_address_details_postcode_idx ON dim_gnaf_address_details(postcode);

