--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.19
-- Dumped by pg_dump version 9.5.19

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: dim_common_words; Type: TABLE; Schema: public; Owner: addruser
--

CREATE TABLE public.dim_common_words (
    word text
);


ALTER TABLE public.dim_common_words OWNER TO addruser;

--
-- Data for Name: dim_common_words; Type: TABLE DATA; Schema: public; Owner: addruser
--

COPY public.dim_common_words (word) FROM stdin;
hospital
clinic
health
campus
service
centre
medical
medicine
house
the
university
private
for
men
women
theatre
department
unit
care
level
central
surgery
place
floor
\.


--
-- PostgreSQL database dump complete
--

