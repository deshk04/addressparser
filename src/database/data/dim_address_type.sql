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
-- Name: dim_address_type; Type: TABLE; Schema: public; Owner: addruser
--

CREATE TABLE public.dim_address_type (
    address_type character(1) NOT NULL,
    address_type_desc character varying(60)
);


ALTER TABLE public.dim_address_type OWNER TO addruser;

--
-- Data for Name: dim_address_type; Type: TABLE DATA; Schema: public; Owner: addruser
--

COPY public.dim_address_type (address_type, address_type_desc) FROM stdin;
P	Practice address
C	Correspondence address
B	Billing address
O	Organisation address
\.


--
-- Name: dim_address_type_pkey; Type: CONSTRAINT; Schema: public; Owner: addruser
--

ALTER TABLE ONLY public.dim_address_type
    ADD CONSTRAINT dim_address_type_pkey PRIMARY KEY (address_type);


--
-- PostgreSQL database dump complete
--

