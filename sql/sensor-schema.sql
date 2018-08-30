--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.4
-- Dumped by pg_dump version 9.6.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
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


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: sensor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sensor (
    id integer NOT NULL,
    name character varying,
    lat real,
    long real,
    tempreaturewarning integer,
    tempreaturecritical integer,
    humiditywarning integer,
    humiditycritical integer
);


ALTER TABLE sensor OWNER TO postgres;

--
-- Name: sensor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sensor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sensor_id_seq OWNER TO postgres;

--
-- Name: sensor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sensor_id_seq OWNED BY sensor.id;


--
-- Name: temp_and_humd_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE temp_and_humd_log (
    id bigint NOT NULL,
    tst timestamp without time zone DEFAULT now(),
    name character varying,
    lat real,
    long real,
    sampletime timestamp without time zone,
    status integer,
    message character varying,
    temperature integer,
    humidity integer
);


ALTER TABLE temp_and_humd_log OWNER TO postgres;

--
-- Name: temp_and_humd_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE temp_and_humd_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE temp_and_humd_log_id_seq OWNER TO postgres;

--
-- Name: temp_and_humd_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE temp_and_humd_log_id_seq OWNED BY temp_and_humd_log.id;


--
-- Name: sensor id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sensor ALTER COLUMN id SET DEFAULT nextval('sensor_id_seq'::regclass);


--
-- Name: temp_and_humd_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY temp_and_humd_log ALTER COLUMN id SET DEFAULT nextval('temp_and_humd_log_id_seq'::regclass);


--
-- Name: sensor sensor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sensor
    ADD CONSTRAINT sensor_pkey PRIMARY KEY (id);


--
-- Name: temp_and_humd_log temp_and_humd_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY temp_and_humd_log
    ADD CONSTRAINT temp_and_humd_log_pkey PRIMARY KEY (id);


--
-- Name: i1_temp_and_humd_log; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX i1_temp_and_humd_log ON temp_and_humd_log USING btree (sampletime, name, status);


--
-- Name: sensor; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE sensor TO agent;


--
-- Name: temp_and_humd_log; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE temp_and_humd_log TO agent;


--
-- Name: temp_and_humd_log_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT USAGE ON SEQUENCE temp_and_humd_log_id_seq TO agent;


--
-- PostgreSQL database dump complete
--

