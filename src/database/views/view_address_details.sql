--=============================================
-- Author     :  
-- Create date:  
-- Description:  view on address details
--
--
--
-- Version        Date        Description(of Changes)
-- 1.0        Created
--=============================================

drop view vw_address_details;

create view vw_address_details
as
select
    address_id,
    pobox_type,
    pobox_number,

    case when building_name is not null and length(trim(building_name)) > 0
    then
        building_name ||', ' ||
        case when flat_type is not null and level_type is not null
        then
            COALESCE(flat_type,'') || ' ' || COALESCE(trim(flat_number::text),'') || ' ' || COALESCE(trim(flat_number_suffix::text),'') || ',' ||
            COALESCE(level_type,'') || ' ' || COALESCE(trim(level_number::text),'') ||' ' || COALESCE(trim(level_number_suffix::text),'')
        when flat_type is not null and level_type is null
        then
                COALESCE(flat_type,'') || ' ' || COALESCE(trim(flat_number::text),'') || ' ' || COALESCE(trim(flat_number_suffix::text),'')
        when flat_type is null and level_type is not null
        then
                COALESCE(level_type,'') || ' ' || COALESCE(trim(level_number::text),'') ||' ' || COALESCE(trim(level_number_suffix::text),'')
        when flat_type is null and level_type is null
        then
            case when number_last is not null
            then
                trim(COALESCE(number_first::text,'')) || '-' || COALESCE(number_last::text,'') || ' '
                || COALESCE(street_name,'') || ' ' || COALESCE(street_type,'')
            else
                trim(COALESCE(number_first::text,'')) || COALESCE(number_suffix,'') || COALESCE(number_last::text,'') || ' '
                || COALESCE(street_name,'') || ' ' || COALESCE(street_type,'')
            end
        end
    else
        case when flat_type is not null and level_type is not null
        then
            COALESCE(flat_type,'') || ' ' || COALESCE(trim(flat_number::text),'') || ' ' || COALESCE(trim(flat_number_suffix::text),'') || ',' ||
            COALESCE(level_type,'') || ' ' || COALESCE(trim(level_number::text),'') ||' ' || COALESCE(trim(level_number_suffix::text),'')
        when flat_type is not null and level_type is null
        then
                COALESCE(flat_type,'') || ' ' || COALESCE(trim(flat_number::text),'') || ' ' || COALESCE(trim(flat_number_suffix::text),'')
        when flat_type is null and level_type is not null
        then
                COALESCE(level_type,'') || ' ' || COALESCE(trim(level_number::text),'') ||' ' || COALESCE(trim(level_number_suffix::text),'')
        when flat_type is null and level_type is null
        then
            case when number_last is not null
            then
                trim(COALESCE(number_first::text,'')) || '-' || COALESCE(number_last::text,'') || ' '
                || COALESCE(street_name,'') || ' ' || COALESCE(street_type,'')
            else
                trim(COALESCE(number_first::text,'')) || COALESCE(number_suffix,'') || COALESCE(number_last::text,'') || ' '
                || COALESCE(street_name,'') || ' ' || COALESCE(street_type,'')
            end
        end
    end as address_line1,
    case when flat_type is not null or level_type is not null
    then
        case when number_last is not null
        then
            trim(COALESCE(number_first::text,'')) || '-' || COALESCE(number_last::text,'') || ' '
            || COALESCE(street_name,'') || ' ' || COALESCE(street_type,'')
        else
            trim(COALESCE(number_first::text,'')) || COALESCE(number_suffix,'') || COALESCE(number_last::text,'') || ' '
            || COALESCE(street_name,'') || ' ' || COALESCE(street_type,'')
        end
    end as address_line2,

    suburb,
    postcode,
    state,
    latitude,
    longitude,
    premises_type

from address_details
;