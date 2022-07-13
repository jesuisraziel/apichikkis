--
-- PostgreSQL database dump
--

-- Dumped from database version 10.21 (Ubuntu 10.21-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.21 (Ubuntu 10.21-0ubuntu0.18.04.1)

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

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: cliente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cliente (
    cedula character varying(12) NOT NULL,
    nombre_completo character varying(240) NOT NULL,
    email character varying(140) NOT NULL,
    whatsapp character varying(15) NOT NULL
);


ALTER TABLE public.cliente OWNER TO postgres;

--
-- Name: pedido; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pedido (
    id integer NOT NULL,
    municipio character varying(80) NOT NULL,
    ciudad character varying(140) NOT NULL,
    n_hamburguesas integer NOT NULL,
    monto_delivery numeric(8,4) NOT NULL,
    monto_total numeric(8,4) NOT NULL,
    metodo_pago character varying(10) NOT NULL,
    estado_delivery character varying(12) NOT NULL,
    screenshot bytea,
    fecha timestamp without time zone NOT NULL,
    cedula character varying(12) NOT NULL,
    remark character varying(80)
);


ALTER TABLE public.pedido OWNER TO postgres;

--
-- Name: pedido_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pedido_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pedido_id_seq OWNER TO postgres;

--
-- Name: pedido_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pedido_id_seq OWNED BY public.pedido.id;


--
-- Name: pedido id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedido ALTER COLUMN id SET DEFAULT nextval('public.pedido_id_seq'::regclass);


--
-- Data for Name: cliente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cliente (cedula, nombre_completo, email, whatsapp) FROM stdin;
28074361	Jes£s Raziel Gonz lez Sosa	chokokokyunokibou@gmail.com	584167995554
010206	Enyerck Gomez	elquelolea.com	6969129
12225886	Jesús González Hernández	capatarida@gmail.com	587129904
29668074	Maria Celeste	anika@gmail.com	584162410092
4219872212	Kevin Trevor	kaladan@gmail.com	5941619293
\.


--
-- Data for Name: pedido; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pedido (id, municipio, ciudad, n_hamburguesas, monto_delivery, monto_total, metodo_pago, estado_delivery, screenshot, fecha, cedula, remark) FROM stdin;
5	Arismendi	Atamo Sur	2	2.0000	12.0000	pago_movil	pending	\N	2022-07-13 18:26:46.635135	4219872212	Una sin queso fundido
2	Mariño	Porlamar	3	2.0000	17.0000	pago_movil	pending	\N	2022-07-13 16:51:08.398508	28074361	\N
3	Arismendi	Atamo Sur	1	2.0000	7.0000	efectivo	pending	\N	2022-07-13 17:05:07.028014	28074361	\N
1	Maneiro	Pampatar	2	0.0000	10.0000	pago_movil	completed	\N	2022-07-13 16:48:38.594523	28074361	\N
\.


--
-- Name: pedido_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pedido_id_seq', 5, true);


--
-- Name: cliente cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (cedula);


--
-- Name: pedido pedido_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedido
    ADD CONSTRAINT pedido_pkey PRIMARY KEY (id);


--
-- Name: pedido fk_cedula; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedido
    ADD CONSTRAINT fk_cedula FOREIGN KEY (cedula) REFERENCES public.cliente(cedula) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

