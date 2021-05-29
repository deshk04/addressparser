DROP INDEX dim_gnaf_address_details_all_idx;
DROP INDEX dim_gnaf_address_details_geo_idx;
DROP INDEX dim_gnaf_address_details_state_post_idx;
DROP INDEX dim_gnaf_address_details_state_loc_idx;

CREATE UNIQUE INDEX dim_gnaf_address_details_all_idx 
ON dim_gnaf_address_details USING btree (address_detail_pid, street_name,locality_name, 
state_abbreviation, postcode,latitude, longitude);
CREATE INDEX dim_gnaf_address_details_geo_idx 
ON dim_gnaf_address_details USING btree (latitude, longitude);
CREATE INDEX dim_gnaf_address_details_state_post_idx 
ON dim_gnaf_address_details USING btree (state_abbreviation, postcode);
CREATE INDEX dim_gnaf_address_details_state_loc_idx 
ON dim_gnaf_address_details USING btree (state_abbreviation, locality_name);

