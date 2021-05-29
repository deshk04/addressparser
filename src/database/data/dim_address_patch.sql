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
-- Name: dim_address_patch; Type: TABLE; Schema: public; Owner: addruser
--

CREATE TABLE public.dim_address_patch (
    sourcestring character varying(80),
    destinationstring character varying(80),
    type character(1)
);


ALTER TABLE public.dim_address_patch OWNER TO addruser;

--
-- Data for Name: dim_address_patch; Type: TABLE DATA; Schema: public; Owner: addruser
--

COPY public.dim_address_patch (sourcestring, destinationstring, type) FROM stdin;
prairievale	prairie vale	A
the kingsway	kingsway	A
the kingswa	kingsway	A
s andrews	st andrews	A
frankston-flinders	frankston-flinders road	A
the ave	the avenue	A
robina town centre	robina town centre drive	A
hawesbury rd	hawkesbury road	A
s/c	shopping centre	A
s/ctr	shopping centre	A
s/town	shopping centre	A
standrews	st andrews	A
good chap	goodchap	A
seventeen mile rocks	seventeen mile rocks road	A
west bourne st	westbourne street	A
frankston/flinders	frankston-flinders	A
frankston flinders	frankston-flinders	A
micarrs-creek	mccarrs creek	A
the bvd	the boulevarde	A
the esp	the esplanade	A
mt gravatt-capalaba	mount gravatt capalaba	A
berwick/cranbourne	berwick-cranbourne	A
norbick	norbrik	A
nambour mapleton	mapleton	A
town ctr	town centre	A
fig tree	figtree	S
compton/calam	compton rd & calam rd	A
glenhuntly rd	glen huntly rd	A
mem ave	memorial avenue	A
s/shine	sunshine	A
center	centre	A
sc	shopping centre	A
shop ctr	shopping centre	A
4thfl	4 fl	A
shpg c	shopping centre	A
calder dr park	calder park drive	A
s/centre	shopping centre	A
cnr captain cook & kenne	captain cook highway	A
mt	mount	A
beverley	beverly	A
st304161	st304 161	A
royal melbourne hospital	parkville	S
royal melb hosp	parkville	S
\.


--
-- PostgreSQL database dump complete
--

