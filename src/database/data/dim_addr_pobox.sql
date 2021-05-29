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
-- Name: dim_addr_pobox; Type: TABLE; Schema: public; Owner: addruser
--

CREATE TABLE public.dim_addr_pobox (
    pobox character varying(20)
);


ALTER TABLE public.dim_addr_pobox OWNER TO addruser;

--
-- Data for Name: dim_addr_pobox; Type: TABLE DATA; Schema: public; Owner: addruser
--

COPY public.dim_addr_pobox (pobox) FROM stdin;
po box
p o box
letter box
post office box
letter box
\.


--
-- PostgreSQL database dump complete
--

