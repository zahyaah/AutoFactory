--
-- PostgreSQL database dump
--

\restrict FmSgGNpsLwhQYx92cHqPLxVk6cO3rzVQeoT5JHqmhIh3Q7Bhwq7KKI3hzcgWh8G

-- Dumped from database version 16.12 (Debian 16.12-1.pgdg13+1)
-- Dumped by pg_dump version 16.12 (Debian 16.12-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: inventory; Type: TABLE; Schema: public; Owner: factory_user
--

CREATE TABLE public.inventory (
    id integer NOT NULL,
    material_name character varying(100),
    current_stock integer,
    reorder_level integer
);


ALTER TABLE public.inventory OWNER TO factory_user;

--
-- Name: inventory_id_seq; Type: SEQUENCE; Schema: public; Owner: factory_user
--

CREATE SEQUENCE public.inventory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.inventory_id_seq OWNER TO factory_user;

--
-- Name: inventory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: factory_user
--

ALTER SEQUENCE public.inventory_id_seq OWNED BY public.inventory.id;


--
-- Name: production_logs; Type: TABLE; Schema: public; Owner: factory_user
--

CREATE TABLE public.production_logs (
    id integer NOT NULL,
    date date NOT NULL,
    machine_id character varying(50),
    units_produced integer,
    downtime_minutes integer
);


ALTER TABLE public.production_logs OWNER TO factory_user;

--
-- Name: production_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: factory_user
--

CREATE SEQUENCE public.production_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.production_logs_id_seq OWNER TO factory_user;

--
-- Name: production_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: factory_user
--

ALTER SEQUENCE public.production_logs_id_seq OWNED BY public.production_logs.id;


--
-- Name: quality_reports; Type: TABLE; Schema: public; Owner: factory_user
--

CREATE TABLE public.quality_reports (
    id integer NOT NULL,
    date date NOT NULL,
    batch_id character varying(50),
    defects integer,
    total_units integer
);


ALTER TABLE public.quality_reports OWNER TO factory_user;

--
-- Name: quality_reports_id_seq; Type: SEQUENCE; Schema: public; Owner: factory_user
--

CREATE SEQUENCE public.quality_reports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.quality_reports_id_seq OWNER TO factory_user;

--
-- Name: quality_reports_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: factory_user
--

ALTER SEQUENCE public.quality_reports_id_seq OWNED BY public.quality_reports.id;


--
-- Name: inventory id; Type: DEFAULT; Schema: public; Owner: factory_user
--

ALTER TABLE ONLY public.inventory ALTER COLUMN id SET DEFAULT nextval('public.inventory_id_seq'::regclass);


--
-- Name: production_logs id; Type: DEFAULT; Schema: public; Owner: factory_user
--

ALTER TABLE ONLY public.production_logs ALTER COLUMN id SET DEFAULT nextval('public.production_logs_id_seq'::regclass);


--
-- Name: quality_reports id; Type: DEFAULT; Schema: public; Owner: factory_user
--

ALTER TABLE ONLY public.quality_reports ALTER COLUMN id SET DEFAULT nextval('public.quality_reports_id_seq'::regclass);


--
-- Data for Name: inventory; Type: TABLE DATA; Schema: public; Owner: factory_user
--

COPY public.inventory (id, material_name, current_stock, reorder_level) FROM stdin;
1	Steel	885	300
2	Plastic	412	350
3	Aluminum	506	250
\.


--
-- Data for Name: production_logs; Type: TABLE DATA; Schema: public; Owner: factory_user
--

COPY public.production_logs (id, date, machine_id, units_produced, downtime_minutes) FROM stdin;
1	2026-01-01	M1	652	43
2	2026-01-01	M2	672	16
3	2026-01-02	M1	678	24
4	2026-01-02	M2	662	50
5	2026-01-03	M1	648	28
6	2026-01-03	M2	623	30
7	2026-01-04	M1	679	17
8	2026-01-04	M2	610	45
9	2026-01-05	M1	600	36
10	2026-01-05	M2	665	19
11	2026-01-06	M1	624	49
12	2026-01-06	M2	633	44
13	2026-01-07	M1	637	37
14	2026-01-07	M2	629	35
15	2026-01-08	M1	662	29
16	2026-01-08	M2	666	47
17	2026-01-09	M1	654	47
18	2026-01-09	M2	660	42
19	2026-01-10	M1	663	26
20	2026-01-10	M2	670	35
21	2026-01-11	M1	601	37
22	2026-01-11	M2	647	44
23	2026-01-12	M1	662	36
24	2026-01-12	M2	622	48
25	2026-01-13	M1	637	29
26	2026-01-13	M2	653	37
27	2026-01-14	M1	614	28
28	2026-01-14	M2	643	46
29	2026-01-15	M1	671	48
30	2026-01-15	M2	635	45
31	2026-01-16	M1	612	16
32	2026-01-16	M2	618	51
33	2026-01-17	M1	612	20
34	2026-01-17	M2	614	31
35	2026-01-18	M1	608	27
36	2026-01-18	M2	630	27
37	2026-01-19	M1	608	49
38	2026-01-19	M2	603	52
39	2026-01-20	M1	666	32
40	2026-01-20	M2	674	45
41	2026-01-21	M1	664	52
42	2026-01-21	M2	667	38
43	2026-01-22	M1	604	15
44	2026-01-22	M2	614	51
45	2026-01-23	M1	657	16
46	2026-01-23	M2	679	46
47	2026-01-24	M1	643	23
48	2026-01-24	M2	632	46
49	2026-01-25	M1	624	26
50	2026-01-25	M2	619	54
51	2026-01-26	M1	646	35
52	2026-01-26	M2	633	17
53	2026-01-27	M1	613	22
54	2026-01-27	M2	650	28
55	2026-01-28	M1	662	40
56	2026-01-28	M2	631	51
57	2026-01-29	M1	678	18
58	2026-01-29	M2	645	19
59	2026-01-30	M1	647	53
60	2026-01-30	M2	648	42
61	2026-01-31	M1	626	36
62	2026-01-31	M2	622	22
\.


--
-- Data for Name: quality_reports; Type: TABLE DATA; Schema: public; Owner: factory_user
--

COPY public.quality_reports (id, date, batch_id, defects, total_units) FROM stdin;
1	2026-01-01	BATCH-01-1	14	619
2	2026-01-01	BATCH-01-2	1	672
3	2026-01-02	BATCH-02-1	1	628
4	2026-01-02	BATCH-02-2	11	660
5	2026-01-03	BATCH-03-1	7	613
6	2026-01-03	BATCH-03-2	2	677
7	2026-01-04	BATCH-04-1	3	637
8	2026-01-04	BATCH-04-2	2	655
9	2026-01-05	BATCH-05-1	2	660
10	2026-01-05	BATCH-05-2	12	671
11	2026-01-06	BATCH-06-1	11	662
12	2026-01-06	BATCH-06-2	3	668
13	2026-01-07	BATCH-07-1	11	633
14	2026-01-07	BATCH-07-2	4	664
15	2026-01-08	BATCH-08-1	11	621
16	2026-01-08	BATCH-08-2	5	633
17	2026-01-09	BATCH-09-1	10	668
18	2026-01-09	BATCH-09-2	9	656
19	2026-01-10	BATCH-10-1	9	664
20	2026-01-10	BATCH-10-2	4	606
21	2026-01-11	BATCH-11-1	10	674
22	2026-01-11	BATCH-11-2	13	638
23	2026-01-12	BATCH-12-1	6	649
24	2026-01-12	BATCH-12-2	8	623
25	2026-01-13	BATCH-13-1	1	638
26	2026-01-13	BATCH-13-2	7	625
27	2026-01-14	BATCH-14-1	0	615
28	2026-01-14	BATCH-14-2	0	628
29	2026-01-15	BATCH-15-1	5	630
30	2026-01-15	BATCH-15-2	9	663
31	2026-01-16	BATCH-16-1	1	652
32	2026-01-16	BATCH-16-2	1	666
33	2026-01-17	BATCH-17-1	4	609
34	2026-01-17	BATCH-17-2	14	678
35	2026-01-18	BATCH-18-1	2	646
36	2026-01-18	BATCH-18-2	2	661
37	2026-01-19	BATCH-19-1	1	647
38	2026-01-19	BATCH-19-2	7	648
39	2026-01-20	BATCH-20-1	1	650
40	2026-01-20	BATCH-20-2	6	660
41	2026-01-21	BATCH-21-1	10	636
42	2026-01-21	BATCH-21-2	1	631
43	2026-01-22	BATCH-22-1	11	644
44	2026-01-22	BATCH-22-2	4	660
45	2026-01-23	BATCH-23-1	6	678
46	2026-01-23	BATCH-23-2	10	603
47	2026-01-24	BATCH-24-1	6	627
48	2026-01-24	BATCH-24-2	4	673
49	2026-01-25	BATCH-25-1	13	657
50	2026-01-25	BATCH-25-2	1	631
51	2026-01-26	BATCH-26-1	0	619
52	2026-01-26	BATCH-26-2	2	641
53	2026-01-27	BATCH-27-1	14	635
54	2026-01-27	BATCH-27-2	2	668
55	2026-01-28	BATCH-28-1	9	608
56	2026-01-28	BATCH-28-2	2	655
57	2026-01-29	BATCH-29-1	14	659
58	2026-01-29	BATCH-29-2	12	612
59	2026-01-30	BATCH-30-1	12	644
60	2026-01-30	BATCH-30-2	11	670
61	2026-01-31	BATCH-31-1	1	621
62	2026-01-31	BATCH-31-2	14	678
\.


--
-- Name: inventory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: factory_user
--

SELECT pg_catalog.setval('public.inventory_id_seq', 3, true);


--
-- Name: production_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: factory_user
--

SELECT pg_catalog.setval('public.production_logs_id_seq', 62, true);


--
-- Name: quality_reports_id_seq; Type: SEQUENCE SET; Schema: public; Owner: factory_user
--

SELECT pg_catalog.setval('public.quality_reports_id_seq', 62, true);


--
-- Name: inventory inventory_pkey; Type: CONSTRAINT; Schema: public; Owner: factory_user
--

ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_pkey PRIMARY KEY (id);


--
-- Name: production_logs production_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: factory_user
--

ALTER TABLE ONLY public.production_logs
    ADD CONSTRAINT production_logs_pkey PRIMARY KEY (id);


--
-- Name: quality_reports quality_reports_pkey; Type: CONSTRAINT; Schema: public; Owner: factory_user
--

ALTER TABLE ONLY public.quality_reports
    ADD CONSTRAINT quality_reports_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict FmSgGNpsLwhQYx92cHqPLxVk6cO3rzVQeoT5JHqmhIh3Q7Bhwq7KKI3hzcgWh8G

