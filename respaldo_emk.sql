--
-- PostgreSQL database dump
--

\restrict hWn8X2m287poF0rDj2vZr8au6DhJ2Kb9X2mnq9iln6zqCrVIDgcJ80dZ6IfjeFg

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: alimentos_preparados; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alimentos_preparados (
    descripcion character varying(255) NOT NULL,
    cantidad double precision NOT NULL,
    unidad character varying(50) NOT NULL,
    equipo character varying(100) NOT NULL,
    fecha date NOT NULL,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone
);


--
-- Name: alimentos_preparados_componentes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alimentos_preparados_componentes (
    alimento_preparado_id integer NOT NULL,
    donacion_materia_id integer NOT NULL,
    cantidad_usada double precision NOT NULL,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone
);


--
-- Name: alimentos_preparados_componentes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.alimentos_preparados_componentes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: alimentos_preparados_componentes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.alimentos_preparados_componentes_id_seq OWNED BY public.alimentos_preparados_componentes.id;


--
-- Name: alimentos_preparados_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.alimentos_preparados_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: alimentos_preparados_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.alimentos_preparados_id_seq OWNED BY public.alimentos_preparados.id;


--
-- Name: areas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.areas (
    area character varying(100) NOT NULL,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone
);


--
-- Name: areas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.areas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: areas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.areas_id_seq OWNED BY public.areas.id;


--
-- Name: asistencia_servidores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.asistencia_servidores (
    id_persona integer CONSTRAINT asistencia_servidores_id_servidor_not_null NOT NULL,
    fecha date NOT NULL,
    rol character varying(50) NOT NULL,
    categoria_contexto character varying(50) NOT NULL,
    referencia_id integer,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone
);


--
-- Name: asistencia_servidores_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.asistencia_servidores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: asistencia_servidores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.asistencia_servidores_id_seq OWNED BY public.asistencia_servidores.id;


--
-- Name: aulas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.aulas (
    condicion character varying NOT NULL,
    ninos integer NOT NULL,
    ninas integer NOT NULL,
    fecha date NOT NULL,
    id_salon integer,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone,
    id_maestra integer,
    id_auxiliar integer
);


--
-- Name: aulas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.aulas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: aulas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.aulas_id_seq OWNED BY public.aulas.id;


--
-- Name: auxiliares; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auxiliares (
    nombre character varying(100) NOT NULL,
    edad integer NOT NULL,
    fecha_nacimiento date,
    cedula integer NOT NULL,
    celular character varying(20),
    correo character varying(100),
    numero_equipo integer,
    id_capitan integer,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone
);


--
-- Name: auxiliares_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auxiliares_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auxiliares_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auxiliares_id_seq OWNED BY public.auxiliares.id;


--
-- Name: capitanes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.capitanes (
    nombre character varying(100) NOT NULL,
    edad integer NOT NULL,
    fecha_nacimiento date,
    cedula integer NOT NULL,
    celular character varying(20),
    correo character varying(100),
    id_coordinador integer,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone
);


--
-- Name: capitanes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.capitanes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: capitanes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.capitanes_id_seq OWNED BY public.capitanes.id;


--
-- Name: colaboradores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.colaboradores (
    nombre character varying(100) NOT NULL,
    edad integer NOT NULL,
    fecha_nacimiento date,
    cedula integer NOT NULL,
    celular character varying(20),
    correo character varying(100),
    numero_equipo integer,
    id_capitan integer,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone
);


--
-- Name: colaboradores_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.colaboradores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: colaboradores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.colaboradores_id_seq OWNED BY public.colaboradores.id;


--
-- Name: coordinadores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.coordinadores (
    nombre character varying(100) NOT NULL,
    edad integer NOT NULL,
    fecha_nacimiento date,
    cedula integer NOT NULL,
    celular character varying(20),
    correo character varying(100),
    id_lider integer,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone,
    id_area integer
);


--
-- Name: coordinadores_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.coordinadores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: coordinadores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.coordinadores_id_seq OWNED BY public.coordinadores.id;


--
-- Name: distribuciones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.distribuciones (
    donacion_id integer,
    alimento_preparado_id integer,
    salon_id integer,
    area_id integer,
    recepcion_id integer,
    cantidad double precision NOT NULL,
    unidad character varying(50) NOT NULL,
    fecha date NOT NULL,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone
);


--
-- Name: distribuciones_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.distribuciones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: distribuciones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.distribuciones_id_seq OWNED BY public.distribuciones.id;


--
-- Name: docentes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.docentes (
    nombre character varying(100) NOT NULL,
    edad integer NOT NULL,
    fecha_nacimiento date,
    cedula integer NOT NULL,
    celular character varying(20),
    correo character varying(100),
    numero_equipo integer,
    id_capitan integer,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone
);


--
-- Name: docentes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.docentes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: docentes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.docentes_id_seq OWNED BY public.docentes.id;


--
-- Name: donaciones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.donaciones (
    descripcion character varying(255) NOT NULL,
    cantidad double precision NOT NULL,
    unidad character varying(50) NOT NULL,
    equipo character varying(100),
    fecha date NOT NULL,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone
);


--
-- Name: donaciones_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.donaciones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: donaciones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.donaciones_id_seq OWNED BY public.donaciones.id;


--
-- Name: ensenanzas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ensenanzas (
    capitan character varying,
    subcapitan integer,
    fecha date,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone
);


--
-- Name: ensenanzas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ensenanzas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ensenanzas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ensenanzas_id_seq OWNED BY public.ensenanzas.id;


--
-- Name: lideres; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lideres (
    nombre character varying(100) NOT NULL,
    edad integer NOT NULL,
    fecha_nacimiento date,
    cedula integer NOT NULL,
    celular character varying(20),
    correo character varying(100),
    id_pastor integer,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone
);


--
-- Name: lideres_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.lideres_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: lideres_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.lideres_id_seq OWNED BY public.lideres.id;


--
-- Name: logisticas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.logisticas (
    almacen integer,
    capitan integer,
    distribucion integer,
    hidratacion integer,
    pasillo integer,
    secretaria integer,
    fecha date NOT NULL,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone,
    id_capitan integer,
    observaciones text
);


--
-- Name: logisticas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.logisticas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: logisticas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.logisticas_id_seq OWNED BY public.logisticas.id;


--
-- Name: otrasareas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.otrasareas (
    alabanza integer,
    protocolo integer,
    semillitas integer,
    sonido integer,
    teatro integer,
    tv integer,
    ujier integer,
    seguridad integer,
    fecha date,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone
);


--
-- Name: otrasareas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.otrasareas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: otrasareas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.otrasareas_id_seq OWNED BY public.otrasareas.id;


--
-- Name: pastores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pastores (
    nombre character varying(100) NOT NULL,
    iglesia character varying(100) NOT NULL,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone
);


--
-- Name: pastores_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.pastores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: pastores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.pastores_id_seq OWNED BY public.pastores.id;


--
-- Name: permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.permissions (
    codigo character varying(100) NOT NULL,
    descripcion character varying(255),
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone
);


--
-- Name: permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.permissions_id_seq OWNED BY public.permissions.id;


--
-- Name: recepciones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.recepciones (
    nombre character varying,
    fecha date,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone
);


--
-- Name: recepciones_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.recepciones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: recepciones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.recepciones_id_seq OWNED BY public.recepciones.id;


--
-- Name: role_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.role_permissions (
    role_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles (
    nombre character varying(50) NOT NULL,
    descripcion character varying(255),
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone
);


--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: salones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salones (
    salon character varying NOT NULL,
    edad character varying NOT NULL,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone,
    id_area integer
);


--
-- Name: salones_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.salones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: salones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.salones_id_seq OWNED BY public.salones.id;


--
-- Name: servidores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.servidores (
    nombre character varying(100) NOT NULL,
    edad integer NOT NULL,
    cedula integer NOT NULL,
    celular character varying(20),
    correo character varying(100),
    numero_equipo integer,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone,
    fecha_nacimiento date,
    id_capitan integer
);


--
-- Name: servidores_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.servidores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: servidores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.servidores_id_seq OWNED BY public.servidores.id;


--
-- Name: sync_queue; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sync_queue (
    entity_name character varying(80) NOT NULL,
    entity_sync_id character varying(36) NOT NULL,
    operation character varying(20) NOT NULL,
    payload_json text NOT NULL,
    status character varying(20) NOT NULL,
    attempts integer NOT NULL,
    last_error text,
    processed_at timestamp without time zone,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone
);


--
-- Name: sync_queue_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sync_queue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sync_queue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sync_queue_id_seq OWNED BY public.sync_queue.id;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usuarios (
    username character varying(60) NOT NULL,
    password character varying(255) NOT NULL,
    activo boolean NOT NULL,
    reset_token character varying(100),
    reset_token_expiry timestamp without time zone,
    rol_id integer NOT NULL,
    id integer NOT NULL,
    sync_id character varying(36) NOT NULL,
    is_deleted boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_sync timestamp without time zone
);


--
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- Name: alimentos_preparados id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alimentos_preparados ALTER COLUMN id SET DEFAULT nextval('public.alimentos_preparados_id_seq'::regclass);


--
-- Name: alimentos_preparados_componentes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alimentos_preparados_componentes ALTER COLUMN id SET DEFAULT nextval('public.alimentos_preparados_componentes_id_seq'::regclass);


--
-- Name: areas id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.areas ALTER COLUMN id SET DEFAULT nextval('public.areas_id_seq'::regclass);


--
-- Name: asistencia_servidores id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asistencia_servidores ALTER COLUMN id SET DEFAULT nextval('public.asistencia_servidores_id_seq'::regclass);


--
-- Name: aulas id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aulas ALTER COLUMN id SET DEFAULT nextval('public.aulas_id_seq'::regclass);


--
-- Name: auxiliares id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auxiliares ALTER COLUMN id SET DEFAULT nextval('public.auxiliares_id_seq'::regclass);


--
-- Name: capitanes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.capitanes ALTER COLUMN id SET DEFAULT nextval('public.capitanes_id_seq'::regclass);


--
-- Name: colaboradores id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.colaboradores ALTER COLUMN id SET DEFAULT nextval('public.colaboradores_id_seq'::regclass);


--
-- Name: coordinadores id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.coordinadores ALTER COLUMN id SET DEFAULT nextval('public.coordinadores_id_seq'::regclass);


--
-- Name: distribuciones id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.distribuciones ALTER COLUMN id SET DEFAULT nextval('public.distribuciones_id_seq'::regclass);


--
-- Name: docentes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.docentes ALTER COLUMN id SET DEFAULT nextval('public.docentes_id_seq'::regclass);


--
-- Name: donaciones id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.donaciones ALTER COLUMN id SET DEFAULT nextval('public.donaciones_id_seq'::regclass);


--
-- Name: ensenanzas id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ensenanzas ALTER COLUMN id SET DEFAULT nextval('public.ensenanzas_id_seq'::regclass);


--
-- Name: lideres id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lideres ALTER COLUMN id SET DEFAULT nextval('public.lideres_id_seq'::regclass);


--
-- Name: logisticas id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.logisticas ALTER COLUMN id SET DEFAULT nextval('public.logisticas_id_seq'::regclass);


--
-- Name: otrasareas id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.otrasareas ALTER COLUMN id SET DEFAULT nextval('public.otrasareas_id_seq'::regclass);


--
-- Name: pastores id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pastores ALTER COLUMN id SET DEFAULT nextval('public.pastores_id_seq'::regclass);


--
-- Name: permissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permissions ALTER COLUMN id SET DEFAULT nextval('public.permissions_id_seq'::regclass);


--
-- Name: recepciones id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recepciones ALTER COLUMN id SET DEFAULT nextval('public.recepciones_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: salones id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salones ALTER COLUMN id SET DEFAULT nextval('public.salones_id_seq'::regclass);


--
-- Name: servidores id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.servidores ALTER COLUMN id SET DEFAULT nextval('public.servidores_id_seq'::regclass);


--
-- Name: sync_queue id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sync_queue ALTER COLUMN id SET DEFAULT nextval('public.sync_queue_id_seq'::regclass);


--
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
751a47a06aaa
\.


--
-- Data for Name: alimentos_preparados; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alimentos_preparados (descripcion, cantidad, unidad, equipo, fecha, id, sync_id, is_deleted, created_at, updated_at, last_sync) FROM stdin;
Jugo de guayaba	237	Vaso(s)	N. 2	2026-05-03	1	271bc578-5609-47c4-90da-af2edffb52f7	f	2026-05-10 19:29:37.444635	2026-05-10 19:29:37.44464	\N
\.


--
-- Data for Name: alimentos_preparados_componentes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alimentos_preparados_componentes (alimento_preparado_id, donacion_materia_id, cantidad_usada, id, sync_id, is_deleted, created_at, updated_at, last_sync) FROM stdin;
1	3	3	1	f8438bb5-5362-46be-bad9-185a60394dc5	f	2026-05-10 19:29:37.482923	2026-05-10 19:29:37.482929	\N
1	2	3	2	5ebdf9da-bb7c-4464-a243-a2ebd141097e	f	2026-05-10 19:29:37.482942	2026-05-10 19:29:37.482944	\N
\.


--
-- Data for Name: areas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.areas (area, id, sync_id, is_deleted, created_at, updated_at, last_sync) FROM stdin;
Logistica	1	0f169ead-bb6a-44a9-9c91-63c37de3db0b	f	2026-05-10 19:04:09.641126	2026-05-10 19:04:09.641135	\N
Almacén	2	dfdb89e7-4043-4002-b94c-59754dbc36ee	f	2026-05-10 19:04:31.115682	2026-05-10 19:04:31.115687	\N
Secretaría	3	b36d362b-96b4-4f04-8040-3cf9ed1de78b	f	2026-05-10 19:04:40.810793	2026-05-10 19:04:40.8108	\N
Distribución de Alimentos	4	beb47f4f-756c-4259-b5ce-9c165ef2909e	f	2026-05-10 19:04:58.415163	2026-05-10 19:04:58.415169	\N
Maternal	5	be378141-898b-49e6-a307-1b49612e0363	f	2026-05-14 14:56:43.761711	2026-05-14 14:56:43.761716	\N
Infantil	6	88243cda-291e-4651-b20e-79c9dc5a2e5b	f	2026-05-14 14:56:49.42182	2026-05-14 14:56:49.421825	\N
Pre-Juvenil	7	a717ff7c-efa3-41d2-adf2-b8e6053a67a4	f	2026-05-14 14:56:54.880864	2026-05-14 14:56:54.880869	\N
Logistica-pasillo	8	bf29f61f-9fe9-45bc-9a1a-20ea9d625195	f	2026-05-19 02:31:07.948163	2026-05-19 02:31:07.948169	\N
Logistica-hidratación	9	e2a6b53f-da2d-4eb9-aae6-403261d8e2e5	f	2026-05-19 02:31:16.527641	2026-05-19 02:31:16.527646	\N
\.


--
-- Data for Name: asistencia_servidores; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.asistencia_servidores (id_persona, fecha, rol, categoria_contexto, referencia_id, id, sync_id, is_deleted, created_at, updated_at, last_sync) FROM stdin;
\.


--
-- Data for Name: aulas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.aulas (condicion, ninos, ninas, fecha, id_salon, id, sync_id, is_deleted, created_at, updated_at, last_sync, id_maestra, id_auxiliar) FROM stdin;
Abierto	1	1	2026-05-03	2	1	d27b0487-c559-4506-9ee7-44fe0f617046	f	2026-05-10 19:19:54.890844	2026-05-10 19:19:54.89085	\N	\N	\N
Abierto	3	1	2026-05-03	3	2	66777813-816b-4983-8d85-18d9e204d109	f	2026-05-10 19:22:50.807202	2026-05-10 19:22:50.807209	\N	\N	\N
\.


--
-- Data for Name: auxiliares; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auxiliares (nombre, edad, fecha_nacimiento, cedula, celular, correo, numero_equipo, id_capitan, id, sync_id, is_deleted, created_at, updated_at, last_sync) FROM stdin;
\.


--
-- Data for Name: capitanes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.capitanes (nombre, edad, fecha_nacimiento, cedula, celular, correo, id_coordinador, id, sync_id, is_deleted, created_at, updated_at, last_sync) FROM stdin;
Flavio García	19	2007-03-02	33411494	4244605084	flaviogarciaoriginal35@gmail.com	1	1	30213e04-ddc0-479a-bf11-c6db6f40593a	f	2026-05-14 20:16:29.383775	2026-05-14 20:16:29.383779	\N
Marcos Jimenez	18	2007-08-22	32349262	04144012640	\N	1	2	a600c738-f60b-409b-bb85-aaf5a3aef662	f	2026-05-14 20:17:12.047199	2026-05-14 20:17:12.047203	\N
Reina Torres	52	1974-03-09	12101243	04244035469	\N	6	6	2483edf8-dbf6-4acd-a653-3a9e2a332152	f	2026-05-14 20:23:04.989606	2026-05-14 20:23:04.989609	\N
Davis Jesús García Rodríguez 	46	1979-05-17	13194143	0424418118	\N	9	9	8c9b0bfd-b5f3-4341-9e87-61918c64a952	f	2026-05-14 20:25:23.522468	2026-05-14 20:25:23.522472	\N
Crisálida Rojas	58	1967-05-21	8668243	04128864207	\N	10	13	a58ac00b-db58-4d0c-8e9f-905c846d8655	f	2026-05-14 20:29:23.600222	2026-05-14 20:29:23.600227	\N
Liyeira Ochoa 	52	1974-03-07	11526448	04165406041 	\N	1	14	f9e8cd0a-5a76-468c-8bc7-40b4be9b296f	f	2026-05-14 20:30:09.881666	2026-05-14 20:30:09.881671	\N
 Yohana González	46	\N	15657098	0412.755.4175	\N	5	3	69a397a8-37cd-4438-8d95-22bea36050b1	f	2026-05-14 20:18:38.232796	2026-05-14 20:47:39.838221	\N
Martha Navarro 	52	\N	11354526	0424-4560239	\N	5	4	200a5db3-1613-400c-92a5-8acd4798feeb	f	2026-05-14 20:19:40.501717	2026-05-14 20:48:06.933656	\N
Rebeca Del Valle Valdespino	40	\N	17513136	414-5845023	\N	5	5	594aa52f-d05d-405a-8e3f-6e69464e190b	f	2026-05-14 20:20:20.569346	2026-05-14 20:48:23.208918	\N
Rosana Angélica Zumeta Viñas	39	\N	17613359	0414-4105673	\N	8	7	91142301-3ebf-4ffd-b586-6a5e545ce1cb	f	2026-05-14 20:23:59.362162	2026-05-14 20:49:16.819118	\N
Orlairis del Valle Patti Rodriguez	36	\N	20697541	0424-4995846	\N	8	8	2b56e3b2-f61f-4abe-a855-6c5fd57cefe7	f	2026-05-14 20:24:45.236067	2026-05-14 20:49:34.124212	\N
Yorkhatreen Yanez	27	1998-06-01	27925147	424-4095793	\N	6	15	d02592f9-c18d-44b6-9b5e-29cc18836073	f	2026-05-14 20:56:22.652276	2026-05-14 20:56:22.65228	\N
María Carrillo	41	\N	17257952	 04144314626 	\N	13	10	91d7f153-4dbc-469f-bcd6-a62168b6f712	f	2026-05-14 20:26:17.703728	2026-05-14 21:00:21.447748	\N
Alicia García 	60	\N	9525964	04244298347	\N	13	12	0b1e9196-5b82-4995-a1e2-56c4eaefc602	f	2026-05-14 20:28:35.716678	2026-05-14 21:00:32.80572	\N
Richard José Giménez Meléndez 	41	\N	17613006	0412-4107719	\N	13	11	cec30d5a-b241-4a43-b165-769aa968862d	f	2026-05-14 20:27:03.67715	2026-05-14 21:00:48.991789	\N
\.


--
-- Data for Name: colaboradores; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.colaboradores (nombre, edad, fecha_nacimiento, cedula, celular, correo, numero_equipo, id_capitan, id, sync_id, is_deleted, created_at, updated_at, last_sync) FROM stdin;
\.


--
-- Data for Name: coordinadores; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.coordinadores (nombre, edad, fecha_nacimiento, cedula, celular, correo, id_lider, id, sync_id, is_deleted, created_at, updated_at, last_sync, id_area) FROM stdin;
Dina Carreño	50	\N	13254487	0424-4370301	dina.m.c@hotmail.com	1	1	8bae3ac8-9814-45e5-91e8-dd2ffb877b55	f	2026-05-13 19:15:47.925392	2026-05-14 19:44:41.893849	\N	\N
Noreidis Rada 	33	1992-11-24	21017972	04262468973	\N	1	6	d58cc795-0193-45a1-a9b4-e6f5878c457b	f	2026-05-14 20:08:34.823654	2026-05-14 20:08:34.82366	\N	\N
Vanessa Sánchez 	35	1990-05-20	20180218	04128664432	\N	1	7	8269663c-b3f6-4dab-9239-d851eb002e6a	f	2026-05-14 20:12:51.615495	2026-05-14 20:12:51.615499	\N	\N
Dina Rodriguez 	44	1981-06-22	15901226	04128380443	\N	1	8	f15d3489-9a4f-4c37-b4df-f0350252c61c	f	2026-05-14 20:13:27.69409	2026-05-14 20:13:27.694093	\N	\N
Elizabeth Solemni Pérez Padrón 	36	1989-06-21	18973052	04143492253	\N	1	9	84d66673-851d-4b60-84e2-4a64aae71461	f	2026-05-14 20:14:09.40626	2026-05-14 20:14:09.406266	\N	\N
Rafael Garcia	35	1990-08-14	20091488	0412.1470380	\N	1	10	70ab4c4d-cfc8-4170-a82a-27027c6fb479	f	2026-05-14 20:14:54.082272	2026-05-14 20:14:54.082276	\N	\N
Mariana Alcalá de Malavé	37	1988-12-26	18781089	0412413000	\N	1	11	3cc2f257-edd8-4c5d-bee8-5833bb45e2bb	f	2026-05-14 20:58:26.08442	2026-05-14 20:58:26.084424	\N	\N
Carlos Enrique Malavé	44	1981-07-17	15824189	04244494489	\N	1	12	0e92faf0-7d2c-4b61-be4e-40e59dd8f59c	f	2026-05-14 20:59:10.681315	2026-05-14 20:59:10.681319	\N	\N
Jesús María Silva Terán	54	1971-12-02	11155867	04128861314	\N	1	13	ce761b99-567e-4923-8d37-1f2677c4a3fe	f	2026-05-14 20:59:45.480812	2026-05-14 20:59:45.480816	\N	\N
Andrea González (md)	29	\N	24458183	0424-4965738	\N	1	3	d7958258-4e2b-4d58-bbf2-4fc4abb1fef6	f	2026-05-14 19:46:51.212916	2026-05-15 03:21:20.343983	\N	\N
Sulma Ines Arango Loboa	44	1981-09-28	22212426	04244491781	\N	1	5	813a4009-bddd-45d2-90cb-92f6df72de52	f	2026-05-14 20:04:03.315374	2026-05-19 21:53:42.593199	\N	5
\.


--
-- Data for Name: distribuciones; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.distribuciones (donacion_id, alimento_preparado_id, salon_id, area_id, recepcion_id, cantidad, unidad, fecha, id, sync_id, is_deleted, created_at, updated_at, last_sync) FROM stdin;
\N	1	2	\N	\N	5	Vaso(s)	2026-05-03	1	515185c7-7062-4126-94b9-a2deeedba91a	f	2026-05-10 19:30:50.71222	2026-05-10 19:30:50.712226	\N
\.


--
-- Data for Name: docentes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.docentes (nombre, edad, fecha_nacimiento, cedula, celular, correo, numero_equipo, id_capitan, id, sync_id, is_deleted, created_at, updated_at, last_sync) FROM stdin;
Yrene del Carmen Escobar Hernandez	50	1976-05-28	14392872	0412 9658152	\N	1	3	1	8c4bb78b-4298-4af7-826d-3756f0c763f8	f	2026-06-08 18:07:59.103312	2026-06-08 18:07:59.103317	\N
Gloria Isabel  Manzanilla Carreño	20	2006-05-27	32047347	0414 4092307	\N	1	3	2	aedce09f-82d9-424e-ae5f-3282c7aefeab	f	2026-06-08 18:09:30.552141	2026-06-08 18:09:30.552146	\N
Joselyn Karina Bravo Suárez	22	2003-07-07	30195494	0412 4411774	\N	1	3	3	d178b5f7-016e-4751-970c-39ffde0f5a70	f	2026-06-08 18:13:26.798667	2026-06-08 18:13:26.798673	\N
Yelimar Pérez	32	1993-10-05	21241340	0414 4023117	\N	1	3	4	86e53a61-1ecc-49f4-84cb-749e7f8d9f3b	f	2026-06-08 18:14:24.747303	2026-06-08 18:14:24.747306	\N
Francisca del Carmen Alvarez de Medina 	70	1955-12-03	5319246	0424 4104403	\N	1	3	5	d38cfc88-fb21-4bc3-b715-08b70f871165	f	2026-06-08 18:15:45.060593	2026-06-08 18:15:45.060598	\N
Aurelia Carrasco de Galvis	63	1962-12-05	7726073	0414 4307685	\N	1	3	6	61ff2f2f-729a-4557-8f28-35ae6038bc73	f	2026-06-08 18:16:44.006633	2026-06-08 18:16:44.006637	\N
Isbeth Tovar	0	\N	11057227	0412 7464577	\N	3	4	7	abaa9573-3d0e-49ac-8f9f-5cf84db0714a	f	2026-06-08 18:21:17.58246	2026-06-08 18:21:17.582465	\N
Marianys Conde	22	2003-06-25	29915272	0412 4086768	\N	3	4	8	f1d6a1c9-92a1-4474-a91e-a98a558faaa4	f	2026-06-08 18:22:13.023206	2026-06-08 18:22:13.02321	\N
Angelys Gutierrez	25	2000-09-28	27877616	0414 9426627	\N	2	4	9	91bbe9d6-db7c-4fea-a101-6462781a5c5d	f	2026-06-08 18:23:00.992523	2026-06-08 18:23:00.992526	\N
Nurbia Sanchez	38	1987-07-21	19425901	0424 4054264	\N	3	4	10	7583dac4-4868-4003-9fe7-80edff311f8d	f	2026-06-08 18:23:43.105468	2026-06-08 18:23:43.105472	\N
Eluzai Rodriguez	-1	2026-07-11	32842330	0424 5064234	\N	3	4	11	2e5b49f5-30cf-41f9-ac57-562883a36595	f	2026-06-08 18:24:20.597585	2026-06-08 18:24:20.597588	\N
Analia Perez	0	\N	16053007	0412 9899672	\N	3	4	12	0418659d-ebe6-48b5-a5f8-1ab9ae66a192	f	2026-06-08 18:25:06.787831	2026-06-08 18:25:06.787837	\N
Willianys Nuñez	19	2007-02-05	32125778	0412 9899672	\N	1	4	13	ba331a91-b96d-4b93-a050-92e6d3294e3c	f	2026-06-08 18:25:54.457624	2026-06-08 18:25:54.457628	\N
Katherine Ariza	0	\N	24644990	0414 4268050	\N	3	4	14	a7531d37-1efb-4708-b0ab-d25549264b76	f	2026-06-08 18:26:32.746859	2026-06-08 18:26:32.746866	\N
Eidimar Nuñez	35	1991-03-26	22002458	0412 7430022	\N	3	4	15	0d0ebaf5-54f2-490f-b0f8-4c24aedee16d	f	2026-06-08 18:27:34.246205	2026-06-08 18:27:34.246209	\N
Dianis Vera	22	2004-04-21	30758060	0412 1432454	\N	1	15	16	a90cc8f2-2006-40c7-b605-ca9172d44d54	f	2026-06-08 18:38:09.303933	2026-06-08 18:38:09.30394	\N
Stefany Muro	31	1995-05-26	84558441	0414 5955436	\N	-2	15	17	4ddcba13-34f0-4995-b8c5-601ba9f7b5ee	f	2026-06-08 18:39:05.464906	2026-06-08 18:39:05.464909	\N
Dainielis Alcarra	22	2004-03-20	31932581	0412 8466374	\N	1	15	18	4640a0af-0629-46b4-8cb7-197c9bf65dd7	f	2026-06-08 18:44:01.734614	2026-06-08 18:44:01.734619	\N
Rosbelys Fabiany Tovar Acosta	24	2001-08-12	28299924	0424 4103690	\N	1	15	19	41c1999b-85b3-44b8-9162-67aeb954914d	f	2026-06-08 18:45:10.327931	2026-06-08 18:45:10.327934	\N
Franyelis Sinai  Villazana Brea	27	1998-12-18	26670956	0416 2448719	\N	1	15	20	574d2b73-a18a-4c17-999f-ee777e483b91	f	2026-06-08 18:45:41.663638	2026-06-08 18:45:41.663644	\N
Belkis Herrera	42	1983-08-03	17338173	0412 7174791	\N	1	15	21	9b46df9e-bd87-464b-88f3-0a1363c6727f	f	2026-06-08 18:46:13.086025	2026-06-08 18:46:13.086029	\N
Diosennys Annali Diaz Espejo	18	2008-04-23	33667219	0412 9063591	\N	1	15	22	6f625fff-96be-4b05-8d67-ecbf632804b5	f	2026-06-08 18:46:50.819246	2026-06-08 18:46:50.81925	\N
Roxana Alexandra Rodríguez	48	1977-12-26	14571617	0412 5064231	\N	3	6	23	fd29ac42-f7c5-4a8b-984f-aabac5ecec1b	f	2026-06-08 18:48:01.540285	2026-06-08 18:48:01.540289	\N
Alba Freites	60	1965-06-29	8671626	04244460729	\N	3	6	24	3a4b41f7-3f85-4024-9b7f-2dbf1b022c8d	f	2026-06-08 18:48:30.269073	2026-06-08 18:49:23.929022	\N
Felimar de Romero Hernández 	27	1998-11-11	26636188	04125188615	\N	3	6	25	458e58b3-87c2-49b7-84a5-361e85b5ab36	f	2026-06-08 18:50:09.327516	2026-06-08 18:50:09.327521	\N
María Porte 	50	1975-12-12	12772868	04120398558	\N	3	6	26	a7937cdf-9b6b-4fff-950c-82cbc15d4362	f	2026-06-08 18:50:39.481955	2026-06-08 18:50:39.481959	\N
Esquivel María	44	1981-06-19	15102954	04120381735	\N	3	6	27	9b810b5a-36ec-4df4-9948-0ba6304c7088	f	2026-06-08 18:51:24.134286	2026-06-08 18:51:24.13429	\N
Karem Cedeño	0	\N	30640668	04128473213	\N	-2	6	28	dedb4109-d010-448b-a065-bdd1eaffadc0	f	2026-06-08 18:52:00.146652	2026-06-08 18:52:00.146657	\N
\.


--
-- Data for Name: donaciones; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.donaciones (descripcion, cantidad, unidad, equipo, fecha, id, sync_id, is_deleted, created_at, updated_at, last_sync) FROM stdin;
Pastelitos 	252	Unidad(es)	N. 2	2026-05-03	1	b683153e-2ea3-4062-9afd-5bca2282ed5b	f	2026-05-10 19:26:01.084071	2026-05-10 19:26:01.084077	\N
Guayaba	3	Kilogramos	N. 2	2026-05-03	2	c2a3c89e-547f-4516-bcf5-fb75afba33fd	f	2026-05-10 19:27:16.975044	2026-05-10 19:27:16.975049	\N
Azúcar 	3	Kilogramos	N. 2	2026-05-10	3	753ed42f-5bcb-4cc0-a14b-c639ebde5eaa	f	2026-05-10 19:27:39.376762	2026-05-10 19:27:39.376767	\N
\.


--
-- Data for Name: ensenanzas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ensenanzas (capitan, subcapitan, fecha, id, sync_id, is_deleted, created_at, updated_at, last_sync) FROM stdin;
\.


--
-- Data for Name: lideres; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.lideres (nombre, edad, fecha_nacimiento, cedula, celular, correo, id_pastor, id, sync_id, is_deleted, created_at, updated_at, last_sync) FROM stdin;
Ludy	56	\N	1234567890	1234-5678901	nocorreo@correo.com	1	1	c9c627cb-40a1-4f0b-9888-f3253892800b	f	2026-05-13 19:14:41.805056	2026-05-13 19:14:41.805061	\N
\.


--
-- Data for Name: logisticas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.logisticas (almacen, capitan, distribucion, hidratacion, pasillo, secretaria, fecha, id, sync_id, is_deleted, created_at, updated_at, last_sync, id_capitan, observaciones) FROM stdin;
\.


--
-- Data for Name: otrasareas; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.otrasareas (alabanza, protocolo, semillitas, sonido, teatro, tv, ujier, seguridad, fecha, id, sync_id, is_deleted, created_at, updated_at, last_sync) FROM stdin;
\.


--
-- Data for Name: pastores; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.pastores (nombre, iglesia, id, sync_id, is_deleted, created_at, updated_at, last_sync) FROM stdin;
Francisco Barrios	Maranatha Venezuela sede San Diego	1	b3386bed-da9e-43bb-88ba-656957117023	f	2026-05-13 19:13:25.04304	2026-05-13 19:13:25.043046	\N
\.


--
-- Data for Name: permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.permissions (codigo, descripcion, id, sync_id, is_deleted, created_at, updated_at, last_sync) FROM stdin;
areas.view	Permiso areas.view	76	4a7c8a1f-0c06-4e4d-83cb-40b475df96a5	f	2026-05-07 02:34:14.563107	2026-05-07 02:34:14.563107	\N
areas.manage	Permiso areas.manage	77	deaf450c-a2a9-4109-a95c-82e3e1a7f26b	f	2026-05-07 02:34:15.487193	2026-05-07 02:34:15.487193	\N
salones.view	Permiso salones.view	78	c3e8f09f-e5eb-496d-b85a-8e45bbc017c9	f	2026-05-07 02:34:16.798078	2026-05-07 02:34:16.798078	\N
salones.manage	Permiso salones.manage	79	d27bbf69-a5dc-4519-9de2-331c0d2e21c6	f	2026-05-07 02:34:18.121693	2026-05-07 02:34:18.121693	\N
aulas.view	Permiso aulas.view	80	d35423b9-14e1-4a76-8726-eda8ba050572	f	2026-05-07 02:34:21.718228	2026-05-07 02:34:21.718228	\N
aulas.manage	Permiso aulas.manage	81	3470791a-9e69-419c-afa5-1e55e0539f3d	f	2026-05-07 02:34:26.153414	2026-05-07 02:34:26.153414	\N
estadistica.view	Permiso estadistica.view	82	b124faf7-95d5-4542-9dd8-eb1d65ff67a7	f	2026-05-07 02:34:27.467314	2026-05-07 02:34:27.467314	\N
donaciones.view	Permiso donaciones.view	83	1fb1c5bb-79da-4818-8653-8a4878face0c	f	2026-05-07 02:34:28.866472	2026-05-07 02:34:28.866472	\N
donaciones.manage	Permiso donaciones.manage	84	dd763ab5-1dc9-4a8f-9ca8-9dfc25c0c7d3	f	2026-05-07 02:34:31.657896	2026-05-07 02:34:31.657896	\N
preparados.view	Permiso preparados.view	85	392fb6a6-0057-440d-bf64-89b4cfef81c7	f	2026-05-07 02:34:33.824533	2026-05-07 02:34:33.824533	\N
preparados.manage	Permiso preparados.manage	86	5ed91b3b-434a-480a-bd19-fb22bc72f8c0	f	2026-05-07 02:34:36.859013	2026-05-07 02:34:36.859013	\N
distribuciones.view	Permiso distribuciones.view	87	90cf906d-d64a-44a7-80ad-60b6369bde24	f	2026-05-07 02:34:38.337399	2026-05-07 02:34:38.337399	\N
distribuciones.manage	Permiso distribuciones.manage	88	1ebc25f5-0fef-4800-8aaa-97658f264a83	f	2026-05-07 02:34:39.73482	2026-05-07 02:34:39.73482	\N
logistica.view	Permiso logistica.view	89	9248b852-4994-4d01-b83c-1b56481d9389	f	2026-05-07 02:34:41.22011	2026-05-07 02:34:41.22011	\N
logistica.manage	Permiso logistica.manage	90	a6e2c152-b8e4-491b-b23a-1e4f3bfbecb8	f	2026-05-07 02:34:43.918622	2026-05-07 02:34:43.918622	\N
otras_areas.view	Permiso otras_areas.view	91	ea60310d-2554-4696-97bd-40c97be98522	f	2026-05-07 02:34:45.81427	2026-05-07 02:34:45.81427	\N
otras_areas.manage	Permiso otras_areas.manage	92	dad2452b-1a15-44e8-a8d2-18839874687b	f	2026-05-07 02:34:48.074799	2026-05-07 02:34:48.074799	\N
ensenanza.view	Permiso ensenanza.view	93	d4f96164-adab-47d5-a3af-7db2498c61d6	f	2026-05-07 02:34:50.595613	2026-05-07 02:34:50.595613	\N
ensenanza.manage	Permiso ensenanza.manage	94	1006b482-3c1e-49de-b20d-1f7e34ef21f8	f	2026-05-07 02:34:53.652918	2026-05-07 02:34:53.652918	\N
recepcion.view	Permiso recepcion.view	95	62d65546-4292-4def-ab4c-58f2fd99e314	f	2026-05-07 02:34:55.182599	2026-05-07 02:34:55.182599	\N
recepcion.manage	Permiso recepcion.manage	96	857258c9-b070-481b-9037-c7c01b8a290b	f	2026-05-07 02:34:56.69203	2026-05-07 02:34:56.69203	\N
servidores.view	Permiso servidores.view	97	4a32acaa-6ecb-4b8f-b834-422d3bb2cdb3	f	2026-05-07 02:35:00.475911	2026-05-07 02:35:00.475911	\N
servidores.manage	Permiso servidores.manage	98	80c343b4-9c05-4716-ab6c-36daff3094c6	f	2026-05-07 02:35:06.88033	2026-05-07 02:35:06.88033	\N
reporte.view	Permiso reporte.view	99	93109aae-61b9-4673-b30d-b3fed9a9b7b5	f	2026-05-07 02:35:10.230442	2026-05-07 02:35:10.230442	\N
ayuda.view	Permiso ayuda.view	100	0e9526b2-2238-4530-acc8-97d2cfcf0d44	f	2026-05-07 02:35:16.276908	2026-05-07 02:35:16.276908	\N
pastores.view	Permiso pastores.view	101	222c5924-1db7-4ce6-9b55-08b1ea93244d	f	2026-05-19 13:08:33.864115	2026-05-19 13:08:33.86412	\N
pastores.manage	Permiso pastores.manage	102	9ce29b67-4f0c-4fa5-b811-c3a2a4ba7c51	f	2026-05-19 13:08:33.873743	2026-05-19 13:08:33.873749	\N
lideres.view	Permiso lideres.view	103	b72b056c-6984-4416-a872-828d576dd742	f	2026-05-19 13:08:33.886253	2026-05-19 13:08:33.886259	\N
lideres.manage	Permiso lideres.manage	104	64ede990-44ce-4d8f-aa05-040aa0fa6252	f	2026-05-19 13:08:33.897606	2026-05-19 13:08:33.897611	\N
capitanes.view	Permiso capitanes.view	105	e562e83c-5104-4c9c-90c1-09f700fcefa1	f	2026-05-19 13:08:33.908123	2026-05-19 13:08:33.908128	\N
capitanes.manage	Permiso capitanes.manage	106	0a6905bd-b472-4958-bbe0-bae5b2c58eac	f	2026-05-19 13:08:33.918799	2026-05-19 13:08:33.918805	\N
docentes.view	Permiso docentes.view	107	e05d93f3-b7ee-43b0-8442-57a0200bcdb5	f	2026-05-19 13:08:33.930435	2026-05-19 13:08:33.930441	\N
docentes.manage	Permiso docentes.manage	108	29da87a6-0f4b-4925-bf8c-4514c27720fa	f	2026-05-19 13:08:33.942265	2026-05-19 13:08:33.942269	\N
auxiliares.view	Permiso auxiliares.view	109	cfdc6817-8e8b-4adc-915b-0563c7c5cf15	f	2026-05-19 13:08:33.954321	2026-05-19 13:08:33.954326	\N
auxiliares.manage	Permiso auxiliares.manage	110	59823539-dd08-4ce3-aa6f-266577c083a9	f	2026-05-19 13:08:33.965532	2026-05-19 13:08:33.965538	\N
colaboradores.view	Permiso colaboradores.view	111	e7f9c076-b3ce-40ca-bc8b-72d7ad70d715	f	2026-05-19 13:08:33.976742	2026-05-19 13:08:33.976747	\N
colaboradores.manage	Permiso colaboradores.manage	112	993a1d85-be12-4a70-9171-469f48ecdbf9	f	2026-05-19 13:08:33.987363	2026-05-19 13:08:33.987369	\N
\.


--
-- Data for Name: recepciones; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.recepciones (nombre, fecha, id, sync_id, is_deleted, created_at, updated_at, last_sync) FROM stdin;
\.


--
-- Data for Name: role_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.role_permissions (role_id, permission_id) FROM stdin;
14	76
14	77
14	78
14	79
14	80
14	81
14	82
14	83
14	84
14	85
14	86
14	87
14	88
14	89
14	90
14	91
14	92
14	93
14	94
14	95
14	96
14	97
14	98
14	99
14	100
15	80
15	82
15	78
15	81
16	84
16	85
16	86
16	80
16	87
16	83
16	88
16	82
14	101
14	102
14	103
14	104
14	105
14	106
14	107
14	108
14	109
14	110
14	111
14	112
17	83
17	84
17	85
17	86
17	87
17	88
17	99
17	89
17	90
17	91
17	100
17	92
17	93
17	94
17	76
17	95
17	77
17	78
17	79
17	96
17	80
17	81
17	82
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.roles (nombre, descripcion, id, sync_id, is_deleted, created_at, updated_at, last_sync) FROM stdin;
root	Rol del sistema: root	13	3f2cafe5-cef8-4d96-a02f-723d2a28e2a6	f	2026-05-07 02:34:09.708778	2026-05-07 02:34:09.708778	\N
administrador	Rol del sistema: administrador	14	475e9027-8183-4967-b202-e8bbfb24bbfb	f	2026-05-07 02:34:12.848226	2026-05-07 02:34:12.848226	\N
maestro	Rol del sistema: maestro	15	149fc543-6df9-4f72-8f4e-8b909ce9ab03	f	2026-05-07 02:35:19.704892	2026-05-07 02:35:19.704892	\N
distribuidor	Rol del sistema: distribuidor	16	fe5225fa-3fd4-4fb2-a33d-9ae853667274	f	2026-05-07 02:35:34.0938	2026-05-07 02:35:34.0938	\N
secretaria	Rol del sistema: secretaria	17	eaf82c1e-ac43-40d6-b428-33014295b3bb	f	2026-05-19 13:27:19.06031	2026-05-19 13:27:19.060317	\N
\.


--
-- Data for Name: salones; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salones (salon, edad, id, sync_id, is_deleted, created_at, updated_at, last_sync, id_area) FROM stdin;
Sala 1 	1 año	2	f064fa37-639d-4dce-a006-e33439e601ef	f	2026-05-10 19:07:24.873925	2026-05-10 19:07:24.87397	\N	\N
Sala 2 	2 años	3	4aa1480a-5f76-41ac-816e-720a6e575ebd	f	2026-05-10 19:07:34.924991	2026-05-10 19:07:34.924997	\N	\N
Sala 3 	3 años	4	a3dde0eb-b014-4296-9880-16cb9c0fb2f0	f	2026-05-10 19:07:46.701155	2026-05-10 19:07:46.70116	\N	\N
A	3 años	5	bc306618-b5db-40e4-a2ee-3b19e28cc0d7	f	2026-05-10 19:09:01.258287	2026-05-10 19:09:01.258299	\N	\N
B	2 años	6	46d1ea2d-6056-4ca2-a752-2d16d4ee6a06	f	2026-05-10 19:09:22.002686	2026-05-10 19:09:22.002692	\N	\N
C	3 años	7	455e0cd0-e536-49c7-b6b4-674557422d6c	f	2026-05-10 19:09:38.902967	2026-05-10 19:09:38.902973	\N	\N
E	4 años	9	b0b3906c-e4fe-4435-8feb-8b1307d1f014	f	2026-05-10 19:09:52.911838	2026-05-10 19:09:52.911843	\N	\N
F	5 años	10	361047b5-bee6-4cc8-96be-43435c42a762	f	2026-05-10 19:09:59.807076	2026-05-10 19:09:59.807081	\N	\N
G	5 años	11	c4fe785f-0e66-44d9-a145-acb39f8ea3b2	f	2026-05-10 19:10:07.207829	2026-05-10 19:10:07.207835	\N	\N
H	6 años	12	741cdbfb-79f2-4097-8dbc-1b860d9f0298	f	2026-05-10 19:10:16.897096	2026-05-10 19:10:16.897101	\N	\N
I	6 años	13	fe9314e5-57f7-4074-97df-be2af7c9a5c2	f	2026-05-10 19:10:26.87231	2026-05-10 19:10:26.872315	\N	\N
J	7 años	14	9fac41ec-85f0-4f78-8a50-02d0cd554341	f	2026-05-10 19:10:49.475448	2026-05-10 19:10:49.475455	\N	\N
K	7 años	15	9aea54d8-8df1-4de2-aef8-8531a079490c	f	2026-05-10 19:10:57.535778	2026-05-10 19:10:57.535784	\N	\N
L	7 años	16	e091f154-a817-4f50-970e-343086343ddd	f	2026-05-10 19:11:03.939405	2026-05-10 19:11:03.939412	\N	\N
Comedor	8 a 11 años	17	571410af-c292-493a-a2ef-75fac7c5215a	f	2026-05-10 19:11:18.280569	2026-05-10 19:11:18.280574	\N	\N
D	4 años	8	a8d24439-1463-4326-808c-e7d9d60993e2	t	2026-05-10 19:09:45.604794	2026-05-11 22:10:30.242968	\N	\N
Cuna y gateo	1 mes a 11 meses	1	f96ca35c-bf98-4ffb-8f5c-9e4e1ebecb69	f	2026-05-10 19:07:14.180531	2026-05-19 02:29:51.370324	\N	5
Salón de usos múltiple 	12 años a 17 años	18	0480dd7e-1a46-4648-b6b4-dcb78fc6fb15	f	2026-05-10 19:11:44.432678	2026-05-19 02:30:23.946323	\N	7
\.


--
-- Data for Name: servidores; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.servidores (nombre, edad, cedula, celular, correo, numero_equipo, id, sync_id, is_deleted, created_at, updated_at, last_sync, fecha_nacimiento, id_capitan) FROM stdin;
Flavio Garcia	19	3411494	04243605084	flaviogarciaoriginal35@gmail.com	\N	1	01a6a302-6f65-4e64-8923-bee88bbe0536	f	2026-05-08 12:15:46.316708	2026-05-08 12:15:46.316714	\N	2007-03-02	\N
\.


--
-- Data for Name: sync_queue; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sync_queue (entity_name, entity_sync_id, operation, payload_json, status, attempts, last_error, processed_at, id, sync_id, is_deleted, created_at, updated_at, last_sync) FROM stdin;
usuarios	c38c7ec6-d7bb-4ab3-81a2-345e45c334ba	upsert	{"username": "root", "password": "$2b$12$BHvVfJEOiHt4UJekkU3QO.PiYuW9zV1DIa19cU05FBy21CfsyKugK", "activo": true, "reset_token": null, "reset_token_expiry": null, "rol_id": 13, "id": 1, "sync_id": "c38c7ec6-d7bb-4ab3-81a2-345e45c334ba", "is_deleted": false, "created_at": "2026-05-07T02:36:00.446834", "updated_at": "2026-05-07T02:36:00.446834", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "usuarios"}	pending	0	\N	\N	1	0603ff25-e09e-452c-8d2f-700f4c0b6b4b	f	2026-05-08 02:28:59.821629	2026-05-08 02:28:59.821634	\N
usuarios	fb8536e6-b056-434b-bf40-4e029095b3b7	upsert	{"username": "jeansiervodedios@gmail.com", "password": "$2b$12$CpAvk0NZDgorlmNTvjw9mO4d3q10ZkFKiO40TpTNyJ2maTf4y5x7S", "activo": true, "reset_token": null, "reset_token_expiry": null, "rol_id": 13, "id": 2, "sync_id": "fb8536e6-b056-434b-bf40-4e029095b3b7", "is_deleted": false, "created_at": "2026-05-08T02:18:11.069609", "updated_at": "2026-05-08T02:18:11.069614", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "usuarios"}	pending	0	\N	\N	2	82c7b88a-baf4-4dd6-adf4-c10843ab1c3a	f	2026-05-08 02:29:39.675372	2026-05-08 02:29:39.675376	\N
usuarios	cc4c425c-35ae-48a5-841d-b1197a8dbb92	upsert	{"username": "dina.m.c@hotmail.com", "password": "$2b$12$yCwF64SJEKfQufkZ7KwKIOh5lFIMEWDwJ8VpqkBMBNFxxu7GhnKCW", "activo": true, "reset_token": null, "reset_token_expiry": null, "rol_id": 14, "id": 3, "sync_id": "cc4c425c-35ae-48a5-841d-b1197a8dbb92", "is_deleted": false, "created_at": "2026-05-08T02:36:38.391185", "updated_at": "2026-05-08T02:36:38.391193", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "usuarios"}	pending	0	\N	\N	3	aa39e931-fc5b-49d7-99ee-f98d93e25edf	f	2026-05-08 02:36:38.405995	2026-05-08 02:36:38.406	\N
usuarios	fb8536e6-b056-434b-bf40-4e029095b3b7	upsert	{"username": "jeansiervodedios@gmail.com", "password": "$2b$12$CpAvk0NZDgorlmNTvjw9mO4d3q10ZkFKiO40TpTNyJ2maTf4y5x7S", "activo": false, "reset_token": "d3bf7ad8-f64b-4e30-8924-12a4e7fa9ae4", "reset_token_expiry": "2026-05-08T04:05:51.035446", "rol_id": 13, "id": 2, "sync_id": "fb8536e6-b056-434b-bf40-4e029095b3b7", "is_deleted": false, "created_at": "2026-05-08T02:18:11.069609", "updated_at": "2026-05-08T03:05:51.035905", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "usuarios"}	pending	0	\N	\N	4	76987879-4d98-4216-ad48-b03512460c8e	f	2026-05-08 03:32:27.411465	2026-05-08 03:32:27.411469	\N
usuarios	fb8536e6-b056-434b-bf40-4e029095b3b7	upsert	{"username": "jeansiervodedios@gmail.com", "password": "$2b$12$CpAvk0NZDgorlmNTvjw9mO4d3q10ZkFKiO40TpTNyJ2maTf4y5x7S", "activo": true, "reset_token": "d3bf7ad8-f64b-4e30-8924-12a4e7fa9ae4", "reset_token_expiry": "2026-05-08T04:05:51.035446", "rol_id": 13, "id": 2, "sync_id": "fb8536e6-b056-434b-bf40-4e029095b3b7", "is_deleted": false, "created_at": "2026-05-08T02:18:11.069609", "updated_at": "2026-05-08T03:32:27.405874", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "usuarios"}	pending	0	\N	\N	5	b43a9289-2e42-4f62-8d48-bb2d08e4c291	f	2026-05-08 03:34:03.439014	2026-05-08 03:34:03.439018	\N
servidores	01a6a302-6f65-4e64-8923-bee88bbe0536	upsert	{"nombre": "Flavio Garcia", "edad": 19, "fecha_nacimiento": "2007-03-02", "cedula": 3411494, "celular": "04243605084", "correo": "flaviogarciaoriginal35@gmail.com", "numero_equipo": null, "area_servicio": "Secretaria", "capitan": "Dina Carreño", "id": 1, "sync_id": "01a6a302-6f65-4e64-8923-bee88bbe0536", "is_deleted": false, "created_at": "2026-05-08T12:15:46.316708", "updated_at": "2026-05-08T12:15:46.316714", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "servidores"}	pending	0	\N	\N	6	06cf7a65-29fe-48ac-9672-c06055eb87a3	f	2026-05-08 12:15:46.322361	2026-05-08 12:15:46.322365	\N
areas	0f169ead-bb6a-44a9-9c91-63c37de3db0b	upsert	{"area": "Logistica", "id": 1, "sync_id": "0f169ead-bb6a-44a9-9c91-63c37de3db0b", "is_deleted": false, "created_at": "2026-05-10T19:04:09.641126", "updated_at": "2026-05-10T19:04:09.641135", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "areas"}	pending	0	\N	\N	7	0d050760-b2d6-490d-a097-62d1d9914f1a	f	2026-05-10 19:04:09.65671	2026-05-10 19:04:09.656716	\N
areas	dfdb89e7-4043-4002-b94c-59754dbc36ee	upsert	{"area": "Almacén", "id": 2, "sync_id": "dfdb89e7-4043-4002-b94c-59754dbc36ee", "is_deleted": false, "created_at": "2026-05-10T19:04:31.115682", "updated_at": "2026-05-10T19:04:31.115687", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "areas"}	pending	0	\N	\N	8	757df299-d29a-4513-943b-1f5db2f789c3	f	2026-05-10 19:04:31.130932	2026-05-10 19:04:31.130937	\N
areas	b36d362b-96b4-4f04-8040-3cf9ed1de78b	upsert	{"area": "Secretaría", "id": 3, "sync_id": "b36d362b-96b4-4f04-8040-3cf9ed1de78b", "is_deleted": false, "created_at": "2026-05-10T19:04:40.810793", "updated_at": "2026-05-10T19:04:40.810800", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "areas"}	pending	0	\N	\N	9	cca46126-efce-43ff-a545-409b8cb825ef	f	2026-05-10 19:04:40.822535	2026-05-10 19:04:40.822541	\N
areas	beb47f4f-756c-4259-b5ce-9c165ef2909e	upsert	{"area": "Distribución de Alimentos", "id": 4, "sync_id": "beb47f4f-756c-4259-b5ce-9c165ef2909e", "is_deleted": false, "created_at": "2026-05-10T19:04:58.415163", "updated_at": "2026-05-10T19:04:58.415169", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "areas"}	pending	0	\N	\N	10	206506ec-f00f-4f12-a612-6419affd23dc	f	2026-05-10 19:04:58.42687	2026-05-10 19:04:58.426875	\N
salones	f96ca35c-bf98-4ffb-8f5c-9e4e1ebecb69	upsert	{"salon": "Cuna y gateo", "edad": "1 mes a 11 meses", "id": 1, "sync_id": "f96ca35c-bf98-4ffb-8f5c-9e4e1ebecb69", "is_deleted": false, "created_at": "2026-05-10T19:07:14.180531", "updated_at": "2026-05-10T19:07:14.180537", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "salones"}	pending	0	\N	\N	11	72589a02-09ab-4534-b7ed-990162ddfaf1	f	2026-05-10 19:07:14.193186	2026-05-10 19:07:14.193192	\N
salones	f064fa37-639d-4dce-a006-e33439e601ef	upsert	{"salon": "Sala 1 ", "edad": "1 año", "id": 2, "sync_id": "f064fa37-639d-4dce-a006-e33439e601ef", "is_deleted": false, "created_at": "2026-05-10T19:07:24.873925", "updated_at": "2026-05-10T19:07:24.873970", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "salones"}	pending	0	\N	\N	12	d62cbe4b-5fec-4778-9f4b-fce64ab4c0a0	f	2026-05-10 19:07:24.886928	2026-05-10 19:07:24.886934	\N
salones	4aa1480a-5f76-41ac-816e-720a6e575ebd	upsert	{"salon": "Sala 2 ", "edad": "2 años", "id": 3, "sync_id": "4aa1480a-5f76-41ac-816e-720a6e575ebd", "is_deleted": false, "created_at": "2026-05-10T19:07:34.924991", "updated_at": "2026-05-10T19:07:34.924997", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "salones"}	pending	0	\N	\N	13	ecd0be3d-a348-42e9-bc86-c6ee5771bc9a	f	2026-05-10 19:07:34.938515	2026-05-10 19:07:34.93852	\N
salones	a3dde0eb-b014-4296-9880-16cb9c0fb2f0	upsert	{"salon": "Sala 3 ", "edad": "3 años", "id": 4, "sync_id": "a3dde0eb-b014-4296-9880-16cb9c0fb2f0", "is_deleted": false, "created_at": "2026-05-10T19:07:46.701155", "updated_at": "2026-05-10T19:07:46.701160", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "salones"}	pending	0	\N	\N	14	90cd3fbf-329f-4ab7-92db-83aafb0a4ee6	f	2026-05-10 19:07:46.715324	2026-05-10 19:07:46.71533	\N
salones	bc306618-b5db-40e4-a2ee-3b19e28cc0d7	upsert	{"salon": "A", "edad": "3 años", "id": 5, "sync_id": "bc306618-b5db-40e4-a2ee-3b19e28cc0d7", "is_deleted": false, "created_at": "2026-05-10T19:09:01.258287", "updated_at": "2026-05-10T19:09:01.258299", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "salones"}	pending	0	\N	\N	15	ba0686f2-0c2d-423a-af5d-7b3f25c3e5b3	f	2026-05-10 19:09:01.272953	2026-05-10 19:09:01.272959	\N
salones	46d1ea2d-6056-4ca2-a752-2d16d4ee6a06	upsert	{"salon": "B", "edad": "2 años", "id": 6, "sync_id": "46d1ea2d-6056-4ca2-a752-2d16d4ee6a06", "is_deleted": false, "created_at": "2026-05-10T19:09:22.002686", "updated_at": "2026-05-10T19:09:22.002692", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "salones"}	pending	0	\N	\N	16	155a3302-8b88-47d8-9231-404b0df34af5	f	2026-05-10 19:09:22.016329	2026-05-10 19:09:22.016334	\N
salones	455e0cd0-e536-49c7-b6b4-674557422d6c	upsert	{"salon": "C", "edad": "3 años", "id": 7, "sync_id": "455e0cd0-e536-49c7-b6b4-674557422d6c", "is_deleted": false, "created_at": "2026-05-10T19:09:38.902967", "updated_at": "2026-05-10T19:09:38.902973", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "salones"}	pending	0	\N	\N	17	caf5130e-4e05-40d0-8fa9-48121ec47f8d	f	2026-05-10 19:09:38.915999	2026-05-10 19:09:38.916006	\N
salones	a8d24439-1463-4326-808c-e7d9d60993e2	upsert	{"salon": "D", "edad": "4 años", "id": 8, "sync_id": "a8d24439-1463-4326-808c-e7d9d60993e2", "is_deleted": false, "created_at": "2026-05-10T19:09:45.604794", "updated_at": "2026-05-10T19:09:45.604799", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "salones"}	pending	0	\N	\N	18	578a6bc8-c74b-44d6-bbda-603015a058f8	f	2026-05-10 19:09:45.617105	2026-05-10 19:09:45.61711	\N
salones	b0b3906c-e4fe-4435-8feb-8b1307d1f014	upsert	{"salon": "E", "edad": "4 años", "id": 9, "sync_id": "b0b3906c-e4fe-4435-8feb-8b1307d1f014", "is_deleted": false, "created_at": "2026-05-10T19:09:52.911838", "updated_at": "2026-05-10T19:09:52.911843", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "salones"}	pending	0	\N	\N	19	2a80aec4-1249-4fa6-9861-e01b076c89bf	f	2026-05-10 19:09:52.925029	2026-05-10 19:09:52.925034	\N
salones	361047b5-bee6-4cc8-96be-43435c42a762	upsert	{"salon": "F", "edad": "5 años", "id": 10, "sync_id": "361047b5-bee6-4cc8-96be-43435c42a762", "is_deleted": false, "created_at": "2026-05-10T19:09:59.807076", "updated_at": "2026-05-10T19:09:59.807081", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "salones"}	pending	0	\N	\N	20	6a91adfa-ff92-41a6-87ff-7e440b238b23	f	2026-05-10 19:09:59.820915	2026-05-10 19:09:59.820922	\N
salones	c4fe785f-0e66-44d9-a145-acb39f8ea3b2	upsert	{"salon": "G", "edad": "5 años", "id": 11, "sync_id": "c4fe785f-0e66-44d9-a145-acb39f8ea3b2", "is_deleted": false, "created_at": "2026-05-10T19:10:07.207829", "updated_at": "2026-05-10T19:10:07.207835", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "salones"}	pending	0	\N	\N	21	2f148ccd-262d-47c7-9b52-2e4df5dd09ad	f	2026-05-10 19:10:07.220168	2026-05-10 19:10:07.220174	\N
salones	741cdbfb-79f2-4097-8dbc-1b860d9f0298	upsert	{"salon": "H", "edad": "6 años", "id": 12, "sync_id": "741cdbfb-79f2-4097-8dbc-1b860d9f0298", "is_deleted": false, "created_at": "2026-05-10T19:10:16.897096", "updated_at": "2026-05-10T19:10:16.897101", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "salones"}	pending	0	\N	\N	22	242fb929-dfbe-4d72-a794-19cd8723f7ef	f	2026-05-10 19:10:16.91127	2026-05-10 19:10:16.911276	\N
salones	fe9314e5-57f7-4074-97df-be2af7c9a5c2	upsert	{"salon": "I", "edad": "6 años", "id": 13, "sync_id": "fe9314e5-57f7-4074-97df-be2af7c9a5c2", "is_deleted": false, "created_at": "2026-05-10T19:10:26.872310", "updated_at": "2026-05-10T19:10:26.872315", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "salones"}	pending	0	\N	\N	23	3c1f2c18-bbbc-4bb9-b978-353de51ca9f7	f	2026-05-10 19:10:26.884918	2026-05-10 19:10:26.884923	\N
salones	9fac41ec-85f0-4f78-8a50-02d0cd554341	upsert	{"salon": "J", "edad": "7 años", "id": 14, "sync_id": "9fac41ec-85f0-4f78-8a50-02d0cd554341", "is_deleted": false, "created_at": "2026-05-10T19:10:49.475448", "updated_at": "2026-05-10T19:10:49.475455", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "salones"}	pending	0	\N	\N	24	dab06893-59c9-4ce5-b21a-2523029b8e37	f	2026-05-10 19:10:49.486519	2026-05-10 19:10:49.486525	\N
salones	9aea54d8-8df1-4de2-aef8-8531a079490c	upsert	{"salon": "K", "edad": "7 años", "id": 15, "sync_id": "9aea54d8-8df1-4de2-aef8-8531a079490c", "is_deleted": false, "created_at": "2026-05-10T19:10:57.535778", "updated_at": "2026-05-10T19:10:57.535784", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "salones"}	pending	0	\N	\N	25	193be0ad-05c7-4255-9ef6-a649fe0a6972	f	2026-05-10 19:10:57.548945	2026-05-10 19:10:57.548951	\N
salones	e091f154-a817-4f50-970e-343086343ddd	upsert	{"salon": "L", "edad": "7 años", "id": 16, "sync_id": "e091f154-a817-4f50-970e-343086343ddd", "is_deleted": false, "created_at": "2026-05-10T19:11:03.939405", "updated_at": "2026-05-10T19:11:03.939412", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "salones"}	pending	0	\N	\N	26	da0b0934-05fc-4b43-bf31-e9fab9505c54	f	2026-05-10 19:11:03.951153	2026-05-10 19:11:03.951158	\N
salones	571410af-c292-493a-a2ef-75fac7c5215a	upsert	{"salon": "Comedor", "edad": "8 a 11 años", "id": 17, "sync_id": "571410af-c292-493a-a2ef-75fac7c5215a", "is_deleted": false, "created_at": "2026-05-10T19:11:18.280569", "updated_at": "2026-05-10T19:11:18.280574", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "salones"}	pending	0	\N	\N	27	92f29e0a-cf6a-486b-8023-54058c76028e	f	2026-05-10 19:11:18.293608	2026-05-10 19:11:18.293615	\N
salones	0480dd7e-1a46-4648-b6b4-dcb78fc6fb15	upsert	{"salon": "Salón de usos múltiple ", "edad": "12 años a 17 años", "id": 18, "sync_id": "0480dd7e-1a46-4648-b6b4-dcb78fc6fb15", "is_deleted": false, "created_at": "2026-05-10T19:11:44.432678", "updated_at": "2026-05-10T19:11:44.432685", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "salones"}	pending	0	\N	\N	28	dd43616e-775f-49ad-a6fb-49bb77a8946f	f	2026-05-10 19:11:44.444207	2026-05-10 19:11:44.444213	\N
aulas	d27b0487-c559-4506-9ee7-44fe0f617046	upsert	{"auxiliar": 1, "capitan": 0, "colaborador": 1, "condicion": "Abierto", "maestra": 0, "ninos": 1, "ninas": 1, "subcapitan": 0, "fecha": "2026-05-03", "id_salon": 2, "id": 1, "sync_id": "d27b0487-c559-4506-9ee7-44fe0f617046", "is_deleted": false, "created_at": "2026-05-10T19:19:54.890844", "updated_at": "2026-05-10T19:19:54.890850", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "aulas"}	pending	0	\N	\N	29	e32c5f3f-37b7-4281-bd99-853f699740f5	f	2026-05-10 19:19:54.905205	2026-05-10 19:19:54.905211	\N
aulas	66777813-816b-4983-8d85-18d9e204d109	upsert	{"auxiliar": 1, "capitan": 0, "colaborador": 0, "condicion": "Abierto", "maestra": 1, "ninos": 3, "ninas": 1, "subcapitan": 0, "fecha": "2026-05-03", "id_salon": 3, "id": 2, "sync_id": "66777813-816b-4983-8d85-18d9e204d109", "is_deleted": false, "created_at": "2026-05-10T19:22:50.807202", "updated_at": "2026-05-10T19:22:50.807209", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "aulas"}	pending	0	\N	\N	30	011ed177-5ad6-4cd8-8f3f-0eb5bb666e6d	f	2026-05-10 19:22:50.819755	2026-05-10 19:22:50.81976	\N
donaciones	b683153e-2ea3-4062-9afd-5bca2282ed5b	upsert	{"descripcion": "Pastelitos ", "cantidad": 252.0, "unidad": "Unidad(es)", "equipo": "N. 2", "fecha": "2026-05-03", "id": 1, "sync_id": "b683153e-2ea3-4062-9afd-5bca2282ed5b", "is_deleted": false, "created_at": "2026-05-10T19:26:01.084071", "updated_at": "2026-05-10T19:26:01.084077", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "donaciones"}	pending	0	\N	\N	31	9307d1a5-804c-4aa8-88ed-bad2e73330b1	f	2026-05-10 19:26:01.097266	2026-05-10 19:26:01.097271	\N
donaciones	c2a3c89e-547f-4516-bcf5-fb75afba33fd	upsert	{"descripcion": "Guayaba", "cantidad": 3.0, "unidad": "Kilogramos", "equipo": "N. 2", "fecha": "2026-05-03", "id": 2, "sync_id": "c2a3c89e-547f-4516-bcf5-fb75afba33fd", "is_deleted": false, "created_at": "2026-05-10T19:27:16.975044", "updated_at": "2026-05-10T19:27:16.975049", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "donaciones"}	pending	0	\N	\N	32	d68896df-d0e5-4940-99b8-1ab2e5aae48c	f	2026-05-10 19:27:16.989308	2026-05-10 19:27:16.989314	\N
donaciones	753ed42f-5bcb-4cc0-a14b-c639ebde5eaa	upsert	{"descripcion": "Azúcar ", "cantidad": 3.0, "unidad": "Kilogramos", "equipo": "N. 2", "fecha": "2026-05-10", "id": 3, "sync_id": "753ed42f-5bcb-4cc0-a14b-c639ebde5eaa", "is_deleted": false, "created_at": "2026-05-10T19:27:39.376762", "updated_at": "2026-05-10T19:27:39.376767", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "donaciones"}	pending	0	\N	\N	33	3ead33b3-229c-44b7-984c-90ed0fd407e2	f	2026-05-10 19:27:39.392319	2026-05-10 19:27:39.392325	\N
alimentos_preparados	271bc578-5609-47c4-90da-af2edffb52f7	upsert	{"descripcion": "Jugo de guayaba", "cantidad": 237.0, "unidad": "Vaso(s)", "equipo": "N. 2", "fecha": "2026-05-03", "id": 1, "sync_id": "271bc578-5609-47c4-90da-af2edffb52f7", "is_deleted": false, "created_at": "2026-05-10T19:29:37.444635", "updated_at": "2026-05-10T19:29:37.444640", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "alimentos_preparados"}	pending	0	\N	\N	34	864a4cb6-16c9-4695-a21c-a7117d6e02e3	f	2026-05-10 19:29:37.494579	2026-05-10 19:29:37.494585	\N
distribuciones	515185c7-7062-4126-94b9-a2deeedba91a	upsert	{"donacion_id": null, "alimento_preparado_id": 1, "salon_id": 2, "area_id": null, "recepcion_id": null, "cantidad": 5.0, "unidad": "Vaso(s)", "fecha": "2026-05-03", "id": 1, "sync_id": "515185c7-7062-4126-94b9-a2deeedba91a", "is_deleted": false, "created_at": "2026-05-10T19:30:50.712220", "updated_at": "2026-05-10T19:30:50.712226", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "distribuciones"}	pending	0	\N	\N	35	884d4207-195a-4946-b33b-d8d6791d6d68	f	2026-05-10 19:30:50.722592	2026-05-10 19:30:50.722598	\N
usuarios	47a5e7a8-6790-4bb1-82b9-86828ed3e93c	upsert	{"username": "lol", "password": "$2b$12$AOtZvexOgAry1MT/uobEBOjw2z.yihuBVb/QSYof.5HOn/rcLKnku", "activo": true, "reset_token": null, "reset_token_expiry": null, "rol_id": 15, "id": 4, "sync_id": "47a5e7a8-6790-4bb1-82b9-86828ed3e93c", "is_deleted": false, "created_at": "2026-05-11T22:09:38.403710", "updated_at": "2026-05-11T22:09:38.403719", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "usuarios"}	pending	0	\N	\N	36	9ac2cfc8-f1b1-48a0-8790-d00cd822394e	f	2026-05-11 22:09:38.415948	2026-05-11 22:09:38.415955	\N
salones	a8d24439-1463-4326-808c-e7d9d60993e2	delete	{"salon": "D", "edad": "4 años", "id": 8, "sync_id": "a8d24439-1463-4326-808c-e7d9d60993e2", "is_deleted": true, "created_at": "2026-05-10T19:09:45.604794", "updated_at": "2026-05-11T22:10:30.242968", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "delete", "sync_entity_name": "salones"}	pending	0	\N	\N	37	068379e7-8084-4b1a-af1b-8edd1cea483e	f	2026-05-11 22:10:30.256846	2026-05-11 22:10:30.256853	\N
salones	f96ca35c-bf98-4ffb-8f5c-9e4e1ebecb69	upsert	{"salon": "Cuna y gateo", "edad": "1 mes a 11 meses", "id": 1, "sync_id": "f96ca35c-bf98-4ffb-8f5c-9e4e1ebecb69", "is_deleted": false, "created_at": "2026-05-10T19:07:14.180531", "updated_at": "2026-05-10T19:07:14.180537", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "salones"}	pending	0	\N	\N	38	58a6b3b4-69fd-44ee-a698-2746edcfb826	f	2026-05-11 22:11:11.744915	2026-05-11 22:11:11.74492	\N
usuarios	9abd47b8-fe09-42c7-af48-ad8337bbc2b8	upsert	{"username": "lol1", "password": "$2b$12$ei/9cW.z0dqrutOpWz/ecemPoFZUPR5A.kao3eapNITz5Uqv9IZi2", "activo": true, "reset_token": null, "reset_token_expiry": null, "rol_id": 16, "id": 5, "sync_id": "9abd47b8-fe09-42c7-af48-ad8337bbc2b8", "is_deleted": false, "created_at": "2026-05-11T22:17:56.622233", "updated_at": "2026-05-11T22:17:56.622240", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "usuarios"}	pending	0	\N	\N	39	b48df2e6-d167-49ab-933e-33b57515cb3b	f	2026-05-11 22:17:56.632028	2026-05-11 22:17:56.632035	\N
pastores	b3386bed-da9e-43bb-88ba-656957117023	upsert	{"nombre": "Francisco Barrios", "iglesia": "Maranatha Venezuela sede San Diego", "id": 1, "sync_id": "b3386bed-da9e-43bb-88ba-656957117023", "is_deleted": false, "created_at": "2026-05-13T19:13:25.043040", "updated_at": "2026-05-13T19:13:25.043046", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "pastores"}	pending	0	\N	\N	40	5ab78b53-40f6-4fb7-a86d-36a72b7762a5	f	2026-05-13 19:13:25.057413	2026-05-13 19:13:25.057419	\N
lideres	c9c627cb-40a1-4f0b-9888-f3253892800b	upsert	{"nombre": "Ludy", "edad": 56, "fecha_nacimiento": null, "cedula": 1234567890, "celular": "1234-5678901", "correo": "nocorreo@correo.com", "id_pastor": 1, "id": 1, "sync_id": "c9c627cb-40a1-4f0b-9888-f3253892800b", "is_deleted": false, "created_at": "2026-05-13T19:14:41.805056", "updated_at": "2026-05-13T19:14:41.805061", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "lideres"}	pending	0	\N	\N	41	95a31f60-26ee-48ec-9823-1000f5302889	f	2026-05-13 19:14:41.819239	2026-05-13 19:14:41.819245	\N
coordinadores	8bae3ac8-9814-45e5-91e8-dd2ffb877b55	upsert	{"nombre": "Dina Carreño", "edad": 50, "fecha_nacimiento": null, "cedula": 12354487, "celular": "0424-4370301", "correo": "dina.m.c@hotmail.com", "id_lider": 1, "id": 1, "sync_id": "8bae3ac8-9814-45e5-91e8-dd2ffb877b55", "is_deleted": false, "created_at": "2026-05-13T19:15:47.925392", "updated_at": "2026-05-13T19:15:47.925397", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "coordinadores"}	pending	0	\N	\N	42	43187616-838b-4b90-9426-8063908b8fa7	f	2026-05-13 19:15:47.937391	2026-05-13 19:15:47.937396	\N
areas	be378141-898b-49e6-a307-1b49612e0363	upsert	{"area": "Maternal", "id": 5, "sync_id": "be378141-898b-49e6-a307-1b49612e0363", "is_deleted": false, "created_at": "2026-05-14T14:56:43.761711", "updated_at": "2026-05-14T14:56:43.761716", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "areas"}	pending	0	\N	\N	43	9e38c565-adb2-485e-9e86-5ce7164d3f07	f	2026-05-14 14:56:43.769667	2026-05-14 14:56:43.769674	\N
areas	88243cda-291e-4651-b20e-79c9dc5a2e5b	upsert	{"area": "Infantil", "id": 6, "sync_id": "88243cda-291e-4651-b20e-79c9dc5a2e5b", "is_deleted": false, "created_at": "2026-05-14T14:56:49.421820", "updated_at": "2026-05-14T14:56:49.421825", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "areas"}	pending	0	\N	\N	44	7b649823-49e1-453b-9436-a526b4fd8fdf	f	2026-05-14 14:56:49.426292	2026-05-14 14:56:49.426296	\N
areas	a717ff7c-efa3-41d2-adf2-b8e6053a67a4	upsert	{"area": "Pre-Juvenil", "id": 7, "sync_id": "a717ff7c-efa3-41d2-adf2-b8e6053a67a4", "is_deleted": false, "created_at": "2026-05-14T14:56:54.880864", "updated_at": "2026-05-14T14:56:54.880869", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "areas"}	pending	0	\N	\N	45	3ef19353-a3d8-4a82-a54f-573fa446a203	f	2026-05-14 14:56:54.885266	2026-05-14 14:56:54.88527	\N
coordinadores	8bae3ac8-9814-45e5-91e8-dd2ffb877b55	upsert	{"nombre": "Dina Carreño", "edad": 50, "fecha_nacimiento": null, "cedula": 13254487, "celular": "0424-4370301", "correo": "dina.m.c@hotmail.com", "id_lider": 1, "id": 1, "sync_id": "8bae3ac8-9814-45e5-91e8-dd2ffb877b55", "is_deleted": false, "created_at": "2026-05-13T19:15:47.925392", "updated_at": "2026-05-13T19:15:47.925397", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "coordinadores"}	pending	0	\N	\N	46	344b6eb6-a418-41a5-a5df-1e252c4b0f05	f	2026-05-14 19:44:41.904298	2026-05-14 19:44:41.904303	\N
coordinadores	d7958258-4e2b-4d58-bbf2-4fc4abb1fef6	upsert	{"nombre": "Andrea González (md)", "edad": 29, "fecha_nacimiento": "1996-06-07", "cedula": 24458183, "celular": "0424-4965738", "correo": "nocorreo@correo.com", "id_lider": 1, "id": 3, "sync_id": "d7958258-4e2b-4d58-bbf2-4fc4abb1fef6", "is_deleted": false, "created_at": "2026-05-14T19:46:51.212916", "updated_at": "2026-05-14T19:46:51.212920", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "coordinadores"}	pending	0	\N	\N	47	ff2ad788-f448-4cc8-bf76-7965320c319c	f	2026-05-14 19:46:51.22931	2026-05-14 19:46:51.229315	\N
coordinadores	813a4009-bddd-45d2-90cb-92f6df72de52	upsert	{"nombre": "Sulma Ines Arango Loboa", "edad": 44, "fecha_nacimiento": "1981-09-28", "cedula": 22212426, "celular": "04244491781", "correo": null, "id_lider": 1, "id": 5, "sync_id": "813a4009-bddd-45d2-90cb-92f6df72de52", "is_deleted": false, "created_at": "2026-05-14T20:04:03.315374", "updated_at": "2026-05-14T20:04:03.315380", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "coordinadores"}	pending	0	\N	\N	48	90fdb619-8e61-43c2-bf91-580930712b7a	f	2026-05-14 20:04:03.326314	2026-05-14 20:04:03.326319	\N
coordinadores	d58cc795-0193-45a1-a9b4-e6f5878c457b	upsert	{"nombre": "Noreidis Rada ", "edad": 33, "fecha_nacimiento": "1992-11-24", "cedula": 21017972, "celular": "04262468973", "correo": null, "id_lider": 1, "id": 6, "sync_id": "d58cc795-0193-45a1-a9b4-e6f5878c457b", "is_deleted": false, "created_at": "2026-05-14T20:08:34.823654", "updated_at": "2026-05-14T20:08:34.823660", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "coordinadores"}	pending	0	\N	\N	49	5bf8cfdc-27b2-45ec-9506-bb8a3fcd4ad6	f	2026-05-14 20:08:34.836306	2026-05-14 20:08:34.836312	\N
coordinadores	8269663c-b3f6-4dab-9239-d851eb002e6a	upsert	{"nombre": "Vanessa Sánchez ", "edad": 35, "fecha_nacimiento": "1990-05-20", "cedula": 20180218, "celular": "04128664432", "correo": null, "id_lider": 1, "id": 7, "sync_id": "8269663c-b3f6-4dab-9239-d851eb002e6a", "is_deleted": false, "created_at": "2026-05-14T20:12:51.615495", "updated_at": "2026-05-14T20:12:51.615499", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "coordinadores"}	pending	0	\N	\N	50	129a872b-7ef9-4dfd-93bd-c95d4f453e15	f	2026-05-14 20:12:51.629696	2026-05-14 20:12:51.629702	\N
coordinadores	f15d3489-9a4f-4c37-b4df-f0350252c61c	upsert	{"nombre": "Dina Rodriguez ", "edad": 44, "fecha_nacimiento": "1981-06-22", "cedula": 15901226, "celular": "04128380443", "correo": null, "id_lider": 1, "id": 8, "sync_id": "f15d3489-9a4f-4c37-b4df-f0350252c61c", "is_deleted": false, "created_at": "2026-05-14T20:13:27.694090", "updated_at": "2026-05-14T20:13:27.694093", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "coordinadores"}	pending	0	\N	\N	51	d2b732b1-74c1-46a4-86d6-684d4a335da9	f	2026-05-14 20:13:27.705258	2026-05-14 20:13:27.705264	\N
coordinadores	84d66673-851d-4b60-84e2-4a64aae71461	upsert	{"nombre": "Elizabeth Solemni Pérez Padrón ", "edad": 36, "fecha_nacimiento": "1989-06-21", "cedula": 18973052, "celular": "04143492253", "correo": null, "id_lider": 1, "id": 9, "sync_id": "84d66673-851d-4b60-84e2-4a64aae71461", "is_deleted": false, "created_at": "2026-05-14T20:14:09.406260", "updated_at": "2026-05-14T20:14:09.406266", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "coordinadores"}	pending	0	\N	\N	52	cbb8e00d-2430-4c92-8716-bb2b8d1a8945	f	2026-05-14 20:14:09.420006	2026-05-14 20:14:09.420012	\N
coordinadores	70ab4c4d-cfc8-4170-a82a-27027c6fb479	upsert	{"nombre": "Rafael Garcia", "edad": 35, "fecha_nacimiento": "1990-08-14", "cedula": 20091488, "celular": "0412.1470380", "correo": null, "id_lider": 1, "id": 10, "sync_id": "70ab4c4d-cfc8-4170-a82a-27027c6fb479", "is_deleted": false, "created_at": "2026-05-14T20:14:54.082272", "updated_at": "2026-05-14T20:14:54.082276", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "coordinadores"}	pending	0	\N	\N	53	edb18307-0705-4001-a59e-7d754ed747a3	f	2026-05-14 20:14:54.095837	2026-05-14 20:14:54.095842	\N
capitanes	30213e04-ddc0-479a-bf11-c6db6f40593a	upsert	{"nombre": "Flavio García", "edad": 19, "fecha_nacimiento": "2007-03-02", "cedula": 33411494, "celular": "4244605084", "correo": "flaviogarciaoriginal35@gmail.com", "id_coordinador": 1, "id": 1, "sync_id": "30213e04-ddc0-479a-bf11-c6db6f40593a", "is_deleted": false, "created_at": "2026-05-14T20:16:29.383775", "updated_at": "2026-05-14T20:16:29.383779", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	54	9985f1aa-a4fa-4e21-8156-31646db67d6d	f	2026-05-14 20:16:29.397264	2026-05-14 20:16:29.397271	\N
capitanes	a600c738-f60b-409b-bb85-aaf5a3aef662	upsert	{"nombre": "Marcos Jimenez", "edad": 18, "fecha_nacimiento": "2007-08-22", "cedula": 32349262, "celular": "04144012640", "correo": null, "id_coordinador": 1, "id": 2, "sync_id": "a600c738-f60b-409b-bb85-aaf5a3aef662", "is_deleted": false, "created_at": "2026-05-14T20:17:12.047199", "updated_at": "2026-05-14T20:17:12.047203", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	55	745f3ab8-3327-4435-840d-b79cbc02ce07	f	2026-05-14 20:17:12.059483	2026-05-14 20:17:12.059489	\N
capitanes	69a397a8-37cd-4438-8d95-22bea36050b1	upsert	{"nombre": " Yohana González", "edad": 46, "fecha_nacimiento": "1979-12-01", "cedula": 15657098, "celular": "0412.755.4175", "correo": null, "id_coordinador": 6, "id": 3, "sync_id": "69a397a8-37cd-4438-8d95-22bea36050b1", "is_deleted": false, "created_at": "2026-05-14T20:18:38.232796", "updated_at": "2026-05-14T20:18:38.232800", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	56	68401d53-84ec-479a-887e-c719d5cfa019	f	2026-05-14 20:18:38.24466	2026-05-14 20:18:38.244665	\N
capitanes	200a5db3-1613-400c-92a5-8acd4798feeb	upsert	{"nombre": "Martha Navarro ", "edad": 52, "fecha_nacimiento": "1973-09-24", "cedula": 11354526, "celular": "0424-4560239", "correo": null, "id_coordinador": 6, "id": 4, "sync_id": "200a5db3-1613-400c-92a5-8acd4798feeb", "is_deleted": false, "created_at": "2026-05-14T20:19:40.501717", "updated_at": "2026-05-14T20:19:40.501724", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	57	d904a121-aa15-4d39-bd7e-a0d5ab015c18	f	2026-05-14 20:19:40.515221	2026-05-14 20:19:40.515242	\N
capitanes	594aa52f-d05d-405a-8e3f-6e69464e190b	upsert	{"nombre": "Rebeca Del Valle Valdespino", "edad": 40, "fecha_nacimiento": "1985-06-17", "cedula": 17513136, "celular": "414-5845023", "correo": null, "id_coordinador": 6, "id": 5, "sync_id": "594aa52f-d05d-405a-8e3f-6e69464e190b", "is_deleted": false, "created_at": "2026-05-14T20:20:20.569346", "updated_at": "2026-05-14T20:20:20.569350", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	58	7a9521e5-7c62-44ec-a149-a25f35eeda13	f	2026-05-14 20:20:20.585327	2026-05-14 20:20:20.585333	\N
capitanes	2483edf8-dbf6-4acd-a653-3a9e2a332152	upsert	{"nombre": "Reina Torres", "edad": 52, "fecha_nacimiento": "1974-03-09", "cedula": 12101243, "celular": "04244035469", "correo": null, "id_coordinador": 6, "id": 6, "sync_id": "2483edf8-dbf6-4acd-a653-3a9e2a332152", "is_deleted": false, "created_at": "2026-05-14T20:23:04.989606", "updated_at": "2026-05-14T20:23:04.989609", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	59	c53ccb7c-0128-4a39-bfc0-ac3cec015603	f	2026-05-14 20:23:05.001847	2026-05-14 20:23:05.001853	\N
capitanes	91142301-3ebf-4ffd-b586-6a5e545ce1cb	upsert	{"nombre": "Rosana Angélica Zumeta Viñas", "edad": 39, "fecha_nacimiento": "1986-11-23", "cedula": 17613359, "celular": "0414-4105673", "correo": null, "id_coordinador": 7, "id": 7, "sync_id": "91142301-3ebf-4ffd-b586-6a5e545ce1cb", "is_deleted": false, "created_at": "2026-05-14T20:23:59.362162", "updated_at": "2026-05-14T20:23:59.362165", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	60	c6490a28-3520-4721-95a8-d3c5afd8c0ac	f	2026-05-14 20:23:59.374211	2026-05-14 20:23:59.374215	\N
capitanes	2b56e3b2-f61f-4abe-a855-6c5fd57cefe7	upsert	{"nombre": "Orlairis del Valle Patti Rodriguez", "edad": 36, "fecha_nacimiento": "1990-03-10", "cedula": 20697541, "celular": "0424-4995846", "correo": null, "id_coordinador": 7, "id": 8, "sync_id": "2b56e3b2-f61f-4abe-a855-6c5fd57cefe7", "is_deleted": false, "created_at": "2026-05-14T20:24:45.236067", "updated_at": "2026-05-14T20:24:45.236074", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	61	20b5c4e7-4f63-4b91-8299-dd25cd01f63d	f	2026-05-14 20:24:45.248645	2026-05-14 20:24:45.248663	\N
capitanes	8c9b0bfd-b5f3-4341-9e87-61918c64a952	upsert	{"nombre": "Davis Jesús García Rodríguez ", "edad": 46, "fecha_nacimiento": "1979-05-17", "cedula": 13194143, "celular": "0424418118", "correo": null, "id_coordinador": 9, "id": 9, "sync_id": "8c9b0bfd-b5f3-4341-9e87-61918c64a952", "is_deleted": false, "created_at": "2026-05-14T20:25:23.522468", "updated_at": "2026-05-14T20:25:23.522472", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	62	dc2518aa-7c39-4aed-a7be-b8815dec09d0	f	2026-05-14 20:25:23.54019	2026-05-14 20:25:23.540196	\N
capitanes	91d7f153-4dbc-469f-bcd6-a62168b6f712	upsert	{"nombre": "María Carrillo", "edad": 41, "fecha_nacimiento": "1984-10-21", "cedula": 17257952, "celular": " 04144314626 ", "correo": null, "id_coordinador": 10, "id": 10, "sync_id": "91d7f153-4dbc-469f-bcd6-a62168b6f712", "is_deleted": false, "created_at": "2026-05-14T20:26:17.703728", "updated_at": "2026-05-14T20:26:17.703732", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	63	5b2b12a1-37f1-4091-8f5b-d7e0c1a55a2f	f	2026-05-14 20:26:17.715606	2026-05-14 20:26:17.715611	\N
capitanes	cec30d5a-b241-4a43-b165-769aa968862d	upsert	{"nombre": "Richard José Giménez Meléndez ", "edad": 41, "fecha_nacimiento": "1984-11-12", "cedula": 17613006, "celular": "0412-4107719", "correo": null, "id_coordinador": 10, "id": 11, "sync_id": "cec30d5a-b241-4a43-b165-769aa968862d", "is_deleted": false, "created_at": "2026-05-14T20:27:03.677150", "updated_at": "2026-05-14T20:27:03.677154", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	64	6e2a1a2e-09b2-4f28-8f5a-ec0fa207010d	f	2026-05-14 20:27:03.688114	2026-05-14 20:27:03.688118	\N
capitanes	0b1e9196-5b82-4995-a1e2-56c4eaefc602	upsert	{"nombre": "Alicia García ", "edad": 60, "fecha_nacimiento": "1966-04-07", "cedula": 9525964, "celular": "04244298347", "correo": null, "id_coordinador": 10, "id": 12, "sync_id": "0b1e9196-5b82-4995-a1e2-56c4eaefc602", "is_deleted": false, "created_at": "2026-05-14T20:28:35.716678", "updated_at": "2026-05-14T20:28:35.716681", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	65	91c7e6e8-9f45-4cb7-8702-3abf83f0fa53	f	2026-05-14 20:28:35.72812	2026-05-14 20:28:35.728126	\N
capitanes	a58ac00b-db58-4d0c-8e9f-905c846d8655	upsert	{"nombre": "Crisálida Rojas", "edad": 58, "fecha_nacimiento": "1967-05-21", "cedula": 8668243, "celular": "04128864207", "correo": null, "id_coordinador": 10, "id": 13, "sync_id": "a58ac00b-db58-4d0c-8e9f-905c846d8655", "is_deleted": false, "created_at": "2026-05-14T20:29:23.600222", "updated_at": "2026-05-14T20:29:23.600227", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	66	bd869859-f7fe-492b-9c76-22f67689e91c	f	2026-05-14 20:29:23.613377	2026-05-14 20:29:23.613383	\N
capitanes	f9e8cd0a-5a76-468c-8bc7-40b4be9b296f	upsert	{"nombre": "Liyeira Ochoa ", "edad": 52, "fecha_nacimiento": "1974-03-07", "cedula": 11526448, "celular": "04165406041 ", "correo": null, "id_coordinador": 1, "id": 14, "sync_id": "f9e8cd0a-5a76-468c-8bc7-40b4be9b296f", "is_deleted": false, "created_at": "2026-05-14T20:30:09.881666", "updated_at": "2026-05-14T20:30:09.881671", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	67	09a54d54-2bfe-4f10-b8d4-656d317271ca	f	2026-05-14 20:30:09.892788	2026-05-14 20:30:09.892793	\N
capitanes	69a397a8-37cd-4438-8d95-22bea36050b1	upsert	{"nombre": " Yohana González", "edad": 46, "fecha_nacimiento": null, "cedula": 15657098, "celular": "0412.755.4175", "correo": null, "id_coordinador": 5, "id": 3, "sync_id": "69a397a8-37cd-4438-8d95-22bea36050b1", "is_deleted": false, "created_at": "2026-05-14T20:18:38.232796", "updated_at": "2026-05-14T20:18:38.232800", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	68	96f3781f-66d0-49c3-aba7-05ea7fedc4ec	f	2026-05-14 20:47:39.849511	2026-05-14 20:47:39.849516	\N
capitanes	200a5db3-1613-400c-92a5-8acd4798feeb	upsert	{"nombre": "Martha Navarro ", "edad": 52, "fecha_nacimiento": null, "cedula": 11354526, "celular": "0424-4560239", "correo": null, "id_coordinador": 5, "id": 4, "sync_id": "200a5db3-1613-400c-92a5-8acd4798feeb", "is_deleted": false, "created_at": "2026-05-14T20:19:40.501717", "updated_at": "2026-05-14T20:19:40.501724", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	69	faabc8f9-f12b-4021-bed1-f63b3d649e74	f	2026-05-14 20:48:06.942727	2026-05-14 20:48:06.942731	\N
capitanes	594aa52f-d05d-405a-8e3f-6e69464e190b	upsert	{"nombre": "Rebeca Del Valle Valdespino", "edad": 40, "fecha_nacimiento": null, "cedula": 17513136, "celular": "414-5845023", "correo": null, "id_coordinador": 5, "id": 5, "sync_id": "594aa52f-d05d-405a-8e3f-6e69464e190b", "is_deleted": false, "created_at": "2026-05-14T20:20:20.569346", "updated_at": "2026-05-14T20:20:20.569350", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	70	2937b56d-4bf7-4626-a1c2-37f5b2236052	f	2026-05-14 20:48:23.216546	2026-05-14 20:48:23.216551	\N
capitanes	91142301-3ebf-4ffd-b586-6a5e545ce1cb	upsert	{"nombre": "Rosana Angélica Zumeta Viñas", "edad": 39, "fecha_nacimiento": null, "cedula": 17613359, "celular": "0414-4105673", "correo": null, "id_coordinador": 8, "id": 7, "sync_id": "91142301-3ebf-4ffd-b586-6a5e545ce1cb", "is_deleted": false, "created_at": "2026-05-14T20:23:59.362162", "updated_at": "2026-05-14T20:23:59.362165", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	71	8c8aef5f-c73c-466f-ad5c-954bd4ee1f8d	f	2026-05-14 20:49:16.828104	2026-05-14 20:49:16.828109	\N
capitanes	2b56e3b2-f61f-4abe-a855-6c5fd57cefe7	upsert	{"nombre": "Orlairis del Valle Patti Rodriguez", "edad": 36, "fecha_nacimiento": null, "cedula": 20697541, "celular": "0424-4995846", "correo": null, "id_coordinador": 8, "id": 8, "sync_id": "2b56e3b2-f61f-4abe-a855-6c5fd57cefe7", "is_deleted": false, "created_at": "2026-05-14T20:24:45.236067", "updated_at": "2026-05-14T20:24:45.236074", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	72	15028ac3-ba1d-4b5c-ba60-8ccfc28a2e02	f	2026-05-14 20:49:34.13127	2026-05-14 20:49:34.131275	\N
capitanes	d02592f9-c18d-44b6-9b5e-29cc18836073	upsert	{"nombre": "Yorkhatreen Yanez", "edad": 27, "fecha_nacimiento": "1998-06-01", "cedula": 27925147, "celular": "424-4095793", "correo": null, "id_coordinador": 6, "id": 15, "sync_id": "d02592f9-c18d-44b6-9b5e-29cc18836073", "is_deleted": false, "created_at": "2026-05-14T20:56:22.652276", "updated_at": "2026-05-14T20:56:22.652280", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	73	3490aa8a-4e26-4c46-ad29-bcae24697911	f	2026-05-14 20:56:22.6642	2026-05-14 20:56:22.664205	\N
coordinadores	3cc2f257-edd8-4c5d-bee8-5833bb45e2bb	upsert	{"nombre": "Mariana Alcalá de Malavé", "edad": 37, "fecha_nacimiento": "1988-12-26", "cedula": 18781089, "celular": "0412413000", "correo": null, "id_lider": 1, "id": 11, "sync_id": "3cc2f257-edd8-4c5d-bee8-5833bb45e2bb", "is_deleted": false, "created_at": "2026-05-14T20:58:26.084420", "updated_at": "2026-05-14T20:58:26.084424", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "coordinadores"}	pending	0	\N	\N	74	e8596b3a-30fe-4809-b416-e202907d23b6	f	2026-05-14 20:58:26.09521	2026-05-14 20:58:26.095216	\N
coordinadores	0e92faf0-7d2c-4b61-be4e-40e59dd8f59c	upsert	{"nombre": "Carlos Enrique Malavé", "edad": 44, "fecha_nacimiento": "1981-07-17", "cedula": 15824189, "celular": "04244494489", "correo": null, "id_lider": 1, "id": 12, "sync_id": "0e92faf0-7d2c-4b61-be4e-40e59dd8f59c", "is_deleted": false, "created_at": "2026-05-14T20:59:10.681315", "updated_at": "2026-05-14T20:59:10.681319", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "coordinadores"}	pending	0	\N	\N	75	c77e3c64-0d17-4812-8dbc-5cefd05b7a87	f	2026-05-14 20:59:10.693426	2026-05-14 20:59:10.693432	\N
coordinadores	ce761b99-567e-4923-8d37-1f2677c4a3fe	upsert	{"nombre": "Jesús María Silva Terán", "edad": 54, "fecha_nacimiento": "1971-12-02", "cedula": 11155867, "celular": "04128861314", "correo": null, "id_lider": 1, "id": 13, "sync_id": "ce761b99-567e-4923-8d37-1f2677c4a3fe", "is_deleted": false, "created_at": "2026-05-14T20:59:45.480812", "updated_at": "2026-05-14T20:59:45.480816", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "coordinadores"}	pending	0	\N	\N	76	7b278a87-46b1-4dca-9381-c896c827be11	f	2026-05-14 20:59:45.49104	2026-05-14 20:59:45.491044	\N
capitanes	91d7f153-4dbc-469f-bcd6-a62168b6f712	upsert	{"nombre": "María Carrillo", "edad": 41, "fecha_nacimiento": null, "cedula": 17257952, "celular": " 04144314626 ", "correo": null, "id_coordinador": 13, "id": 10, "sync_id": "91d7f153-4dbc-469f-bcd6-a62168b6f712", "is_deleted": false, "created_at": "2026-05-14T20:26:17.703728", "updated_at": "2026-05-14T20:26:17.703732", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	77	708cd7a8-bd24-42df-8df4-db8827b343c7	f	2026-05-14 21:00:21.455677	2026-05-14 21:00:21.455684	\N
capitanes	0b1e9196-5b82-4995-a1e2-56c4eaefc602	upsert	{"nombre": "Alicia García ", "edad": 60, "fecha_nacimiento": null, "cedula": 9525964, "celular": "04244298347", "correo": null, "id_coordinador": 13, "id": 12, "sync_id": "0b1e9196-5b82-4995-a1e2-56c4eaefc602", "is_deleted": false, "created_at": "2026-05-14T20:28:35.716678", "updated_at": "2026-05-14T20:28:35.716681", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	78	52e792ff-8830-4917-bb70-ff2dc3c3b099	f	2026-05-14 21:00:32.814049	2026-05-14 21:00:32.814055	\N
capitanes	cec30d5a-b241-4a43-b165-769aa968862d	upsert	{"nombre": "Richard José Giménez Meléndez ", "edad": 41, "fecha_nacimiento": null, "cedula": 17613006, "celular": "0412-4107719", "correo": null, "id_coordinador": 13, "id": 11, "sync_id": "cec30d5a-b241-4a43-b165-769aa968862d", "is_deleted": false, "created_at": "2026-05-14T20:27:03.677150", "updated_at": "2026-05-14T20:27:03.677154", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "capitanes"}	pending	0	\N	\N	79	e94a0b6b-d061-42be-b8cd-dd280a943fb2	f	2026-05-14 21:00:48.999151	2026-05-14 21:00:48.999155	\N
coordinadores	d7958258-4e2b-4d58-bbf2-4fc4abb1fef6	upsert	{"nombre": "Andrea González (md)", "edad": 29, "fecha_nacimiento": null, "cedula": 24458183, "celular": "0424-4965738", "correo": null, "id_lider": 1, "id": 3, "sync_id": "d7958258-4e2b-4d58-bbf2-4fc4abb1fef6", "is_deleted": false, "created_at": "2026-05-14T19:46:51.212916", "updated_at": "2026-05-14T19:46:51.212920", "last_sync": null, "sync_device_id": "WEB_APP_SERVER", "sync_operation": "upsert", "sync_entity_name": "coordinadores"}	pending	0	\N	\N	80	9f5f0437-acd9-4db9-a383-d8d14612183b	f	2026-05-15 03:21:20.354343	2026-05-15 03:21:20.354348	\N
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.usuarios (username, password, activo, reset_token, reset_token_expiry, rol_id, id, sync_id, is_deleted, created_at, updated_at, last_sync) FROM stdin;
root	$2b$12$BHvVfJEOiHt4UJekkU3QO.PiYuW9zV1DIa19cU05FBy21CfsyKugK	t	\N	\N	13	1	c38c7ec6-d7bb-4ab3-81a2-345e45c334ba	f	2026-05-07 02:36:00.446834	2026-05-08 02:28:59.816975	\N
dina.m.c@hotmail.com	$2b$12$yCwF64SJEKfQufkZ7KwKIOh5lFIMEWDwJ8VpqkBMBNFxxu7GhnKCW	t	\N	\N	14	3	cc4c425c-35ae-48a5-841d-b1197a8dbb92	f	2026-05-08 02:36:38.391185	2026-05-08 02:36:38.391193	\N
jeansiervodedios@gmail.com	$2b$12$CpAvk0NZDgorlmNTvjw9mO4d3q10ZkFKiO40TpTNyJ2maTf4y5x7S	t	d3bf7ad8-f64b-4e30-8924-12a4e7fa9ae4	2026-05-08 04:05:51.035446	13	2	fb8536e6-b056-434b-bf40-4e029095b3b7	f	2026-05-08 02:18:11.069609	2026-05-08 03:34:03.436308	\N
lol	$2b$12$AOtZvexOgAry1MT/uobEBOjw2z.yihuBVb/QSYof.5HOn/rcLKnku	t	\N	\N	15	4	47a5e7a8-6790-4bb1-82b9-86828ed3e93c	f	2026-05-11 22:09:38.40371	2026-05-11 22:09:38.403719	\N
lol1	$2b$12$ei/9cW.z0dqrutOpWz/ecemPoFZUPR5A.kao3eapNITz5Uqv9IZi2	t	76e26cea-74c5-4968-ad29-355c34152619	2026-05-11 23:26:32.856096	16	5	9abd47b8-fe09-42c7-af48-ad8337bbc2b8	f	2026-05-11 22:17:56.622233	2026-05-11 22:26:32.858052	\N
flaviogarciaoriginal35@gmail.com	$2b$12$RYzfoke.ovXwmzlR1cXj8e1qVrEMAU4fAwoJPSEaXVBDwGLhYj4nm	t	\N	\N	13	6	b68f1802-d063-452a-a359-a80ef5e2183c	f	2026-05-17 23:03:48.799188	2026-05-17 23:03:48.799188	\N
\.


--
-- Name: alimentos_preparados_componentes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.alimentos_preparados_componentes_id_seq', 2, true);


--
-- Name: alimentos_preparados_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.alimentos_preparados_id_seq', 1, true);


--
-- Name: areas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.areas_id_seq', 9, true);


--
-- Name: asistencia_servidores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.asistencia_servidores_id_seq', 1, false);


--
-- Name: aulas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.aulas_id_seq', 2, true);


--
-- Name: auxiliares_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auxiliares_id_seq', 1, false);


--
-- Name: capitanes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.capitanes_id_seq', 15, true);


--
-- Name: colaboradores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.colaboradores_id_seq', 1, false);


--
-- Name: coordinadores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.coordinadores_id_seq', 13, true);


--
-- Name: distribuciones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.distribuciones_id_seq', 1, true);


--
-- Name: docentes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.docentes_id_seq', 28, true);


--
-- Name: donaciones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.donaciones_id_seq', 3, true);


--
-- Name: ensenanzas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ensenanzas_id_seq', 1, false);


--
-- Name: lideres_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.lideres_id_seq', 1, true);


--
-- Name: logisticas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.logisticas_id_seq', 1, false);


--
-- Name: otrasareas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.otrasareas_id_seq', 1, false);


--
-- Name: pastores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.pastores_id_seq', 1, true);


--
-- Name: permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.permissions_id_seq', 112, true);


--
-- Name: recepciones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.recepciones_id_seq', 1, false);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.roles_id_seq', 17, true);


--
-- Name: salones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salones_id_seq', 18, true);


--
-- Name: servidores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.servidores_id_seq', 3, true);


--
-- Name: sync_queue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sync_queue_id_seq', 80, true);


--
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 6, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: alimentos_preparados_componentes alimentos_preparados_componentes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alimentos_preparados_componentes
    ADD CONSTRAINT alimentos_preparados_componentes_pkey PRIMARY KEY (id);


--
-- Name: alimentos_preparados alimentos_preparados_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alimentos_preparados
    ADD CONSTRAINT alimentos_preparados_pkey PRIMARY KEY (id);


--
-- Name: areas areas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.areas
    ADD CONSTRAINT areas_pkey PRIMARY KEY (id);


--
-- Name: asistencia_servidores asistencia_servidores_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asistencia_servidores
    ADD CONSTRAINT asistencia_servidores_pkey PRIMARY KEY (id);


--
-- Name: aulas aulas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aulas
    ADD CONSTRAINT aulas_pkey PRIMARY KEY (id);


--
-- Name: auxiliares auxiliares_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auxiliares
    ADD CONSTRAINT auxiliares_pkey PRIMARY KEY (id);


--
-- Name: capitanes capitanes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.capitanes
    ADD CONSTRAINT capitanes_pkey PRIMARY KEY (id);


--
-- Name: colaboradores colaboradores_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.colaboradores
    ADD CONSTRAINT colaboradores_pkey PRIMARY KEY (id);


--
-- Name: coordinadores coordinadores_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.coordinadores
    ADD CONSTRAINT coordinadores_pkey PRIMARY KEY (id);


--
-- Name: distribuciones distribuciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.distribuciones
    ADD CONSTRAINT distribuciones_pkey PRIMARY KEY (id);


--
-- Name: docentes docentes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.docentes
    ADD CONSTRAINT docentes_pkey PRIMARY KEY (id);


--
-- Name: donaciones donaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.donaciones
    ADD CONSTRAINT donaciones_pkey PRIMARY KEY (id);


--
-- Name: ensenanzas ensenanzas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ensenanzas
    ADD CONSTRAINT ensenanzas_pkey PRIMARY KEY (id);


--
-- Name: lideres lideres_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lideres
    ADD CONSTRAINT lideres_pkey PRIMARY KEY (id);


--
-- Name: logisticas logisticas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.logisticas
    ADD CONSTRAINT logisticas_pkey PRIMARY KEY (id);


--
-- Name: otrasareas otrasareas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.otrasareas
    ADD CONSTRAINT otrasareas_pkey PRIMARY KEY (id);


--
-- Name: pastores pastores_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pastores
    ADD CONSTRAINT pastores_pkey PRIMARY KEY (id);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);


--
-- Name: recepciones recepciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recepciones
    ADD CONSTRAINT recepciones_pkey PRIMARY KEY (id);


--
-- Name: role_permissions role_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_pkey PRIMARY KEY (role_id, permission_id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: salones salones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salones
    ADD CONSTRAINT salones_pkey PRIMARY KEY (id);


--
-- Name: servidores servidores_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.servidores
    ADD CONSTRAINT servidores_pkey PRIMARY KEY (id);


--
-- Name: sync_queue sync_queue_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sync_queue
    ADD CONSTRAINT sync_queue_pkey PRIMARY KEY (id);


--
-- Name: areas uq_areas_area; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.areas
    ADD CONSTRAINT uq_areas_area UNIQUE (area);


--
-- Name: auxiliares uq_auxiliares_cedula; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auxiliares
    ADD CONSTRAINT uq_auxiliares_cedula UNIQUE (cedula);


--
-- Name: auxiliares uq_auxiliares_correo; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auxiliares
    ADD CONSTRAINT uq_auxiliares_correo UNIQUE (correo);


--
-- Name: capitanes uq_capitanes_cedula; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.capitanes
    ADD CONSTRAINT uq_capitanes_cedula UNIQUE (cedula);


--
-- Name: capitanes uq_capitanes_correo; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.capitanes
    ADD CONSTRAINT uq_capitanes_correo UNIQUE (correo);


--
-- Name: colaboradores uq_colaboradores_cedula; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.colaboradores
    ADD CONSTRAINT uq_colaboradores_cedula UNIQUE (cedula);


--
-- Name: colaboradores uq_colaboradores_correo; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.colaboradores
    ADD CONSTRAINT uq_colaboradores_correo UNIQUE (correo);


--
-- Name: coordinadores uq_coordinadores_cedula; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.coordinadores
    ADD CONSTRAINT uq_coordinadores_cedula UNIQUE (cedula);


--
-- Name: coordinadores uq_coordinadores_correo; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.coordinadores
    ADD CONSTRAINT uq_coordinadores_correo UNIQUE (correo);


--
-- Name: docentes uq_docentes_cedula; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.docentes
    ADD CONSTRAINT uq_docentes_cedula UNIQUE (cedula);


--
-- Name: docentes uq_docentes_correo; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.docentes
    ADD CONSTRAINT uq_docentes_correo UNIQUE (correo);


--
-- Name: lideres uq_lideres_cedula; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lideres
    ADD CONSTRAINT uq_lideres_cedula UNIQUE (cedula);


--
-- Name: lideres uq_lideres_correo; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lideres
    ADD CONSTRAINT uq_lideres_correo UNIQUE (correo);


--
-- Name: salones uq_salones_salon; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salones
    ADD CONSTRAINT uq_salones_salon UNIQUE (salon);


--
-- Name: servidores uq_servidores_cedula; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.servidores
    ADD CONSTRAINT uq_servidores_cedula UNIQUE (cedula);


--
-- Name: servidores uq_servidores_correo; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.servidores
    ADD CONSTRAINT uq_servidores_correo UNIQUE (correo);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- Name: ix_alimentos_preparados_componentes_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_alimentos_preparados_componentes_id ON public.alimentos_preparados_componentes USING btree (id);


--
-- Name: ix_alimentos_preparados_componentes_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_alimentos_preparados_componentes_sync_id ON public.alimentos_preparados_componentes USING btree (sync_id);


--
-- Name: ix_alimentos_preparados_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_alimentos_preparados_id ON public.alimentos_preparados USING btree (id);


--
-- Name: ix_alimentos_preparados_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_alimentos_preparados_sync_id ON public.alimentos_preparados USING btree (sync_id);


--
-- Name: ix_areas_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_areas_id ON public.areas USING btree (id);


--
-- Name: ix_areas_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_areas_sync_id ON public.areas USING btree (sync_id);


--
-- Name: ix_asistencia_servidores_categoria_contexto; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_asistencia_servidores_categoria_contexto ON public.asistencia_servidores USING btree (categoria_contexto);


--
-- Name: ix_asistencia_servidores_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_asistencia_servidores_fecha ON public.asistencia_servidores USING btree (fecha);


--
-- Name: ix_asistencia_servidores_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_asistencia_servidores_id ON public.asistencia_servidores USING btree (id);


--
-- Name: ix_asistencia_servidores_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_asistencia_servidores_sync_id ON public.asistencia_servidores USING btree (sync_id);


--
-- Name: ix_aulas_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_aulas_id ON public.aulas USING btree (id);


--
-- Name: ix_aulas_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_aulas_sync_id ON public.aulas USING btree (sync_id);


--
-- Name: ix_auxiliares_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_auxiliares_id ON public.auxiliares USING btree (id);


--
-- Name: ix_auxiliares_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_auxiliares_sync_id ON public.auxiliares USING btree (sync_id);


--
-- Name: ix_capitanes_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_capitanes_id ON public.capitanes USING btree (id);


--
-- Name: ix_capitanes_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_capitanes_sync_id ON public.capitanes USING btree (sync_id);


--
-- Name: ix_colaboradores_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_colaboradores_id ON public.colaboradores USING btree (id);


--
-- Name: ix_colaboradores_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_colaboradores_sync_id ON public.colaboradores USING btree (sync_id);


--
-- Name: ix_coordinadores_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_coordinadores_id ON public.coordinadores USING btree (id);


--
-- Name: ix_coordinadores_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_coordinadores_sync_id ON public.coordinadores USING btree (sync_id);


--
-- Name: ix_distribuciones_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_distribuciones_id ON public.distribuciones USING btree (id);


--
-- Name: ix_distribuciones_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_distribuciones_sync_id ON public.distribuciones USING btree (sync_id);


--
-- Name: ix_docentes_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_docentes_id ON public.docentes USING btree (id);


--
-- Name: ix_docentes_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_docentes_sync_id ON public.docentes USING btree (sync_id);


--
-- Name: ix_donaciones_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_donaciones_id ON public.donaciones USING btree (id);


--
-- Name: ix_donaciones_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_donaciones_sync_id ON public.donaciones USING btree (sync_id);


--
-- Name: ix_ensenanzas_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_ensenanzas_id ON public.ensenanzas USING btree (id);


--
-- Name: ix_ensenanzas_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_ensenanzas_sync_id ON public.ensenanzas USING btree (sync_id);


--
-- Name: ix_lideres_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_lideres_id ON public.lideres USING btree (id);


--
-- Name: ix_lideres_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_lideres_sync_id ON public.lideres USING btree (sync_id);


--
-- Name: ix_logisticas_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_logisticas_fecha ON public.logisticas USING btree (fecha);


--
-- Name: ix_logisticas_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_logisticas_id ON public.logisticas USING btree (id);


--
-- Name: ix_logisticas_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_logisticas_sync_id ON public.logisticas USING btree (sync_id);


--
-- Name: ix_otrasareas_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_otrasareas_id ON public.otrasareas USING btree (id);


--
-- Name: ix_otrasareas_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_otrasareas_sync_id ON public.otrasareas USING btree (sync_id);


--
-- Name: ix_pastores_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_pastores_id ON public.pastores USING btree (id);


--
-- Name: ix_pastores_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_pastores_sync_id ON public.pastores USING btree (sync_id);


--
-- Name: ix_permissions_codigo; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_permissions_codigo ON public.permissions USING btree (codigo);


--
-- Name: ix_permissions_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_permissions_id ON public.permissions USING btree (id);


--
-- Name: ix_permissions_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_permissions_sync_id ON public.permissions USING btree (sync_id);


--
-- Name: ix_recepciones_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_recepciones_id ON public.recepciones USING btree (id);


--
-- Name: ix_recepciones_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_recepciones_sync_id ON public.recepciones USING btree (sync_id);


--
-- Name: ix_roles_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_roles_id ON public.roles USING btree (id);


--
-- Name: ix_roles_nombre; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_roles_nombre ON public.roles USING btree (nombre);


--
-- Name: ix_roles_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_roles_sync_id ON public.roles USING btree (sync_id);


--
-- Name: ix_salones_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_salones_id ON public.salones USING btree (id);


--
-- Name: ix_salones_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_salones_sync_id ON public.salones USING btree (sync_id);


--
-- Name: ix_servidores_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_servidores_id ON public.servidores USING btree (id);


--
-- Name: ix_servidores_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_servidores_sync_id ON public.servidores USING btree (sync_id);


--
-- Name: ix_sync_queue_entity_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_sync_queue_entity_name ON public.sync_queue USING btree (entity_name);


--
-- Name: ix_sync_queue_entity_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_sync_queue_entity_sync_id ON public.sync_queue USING btree (entity_sync_id);


--
-- Name: ix_sync_queue_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_sync_queue_id ON public.sync_queue USING btree (id);


--
-- Name: ix_sync_queue_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_sync_queue_sync_id ON public.sync_queue USING btree (sync_id);


--
-- Name: ix_usuarios_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_usuarios_id ON public.usuarios USING btree (id);


--
-- Name: ix_usuarios_reset_token; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_usuarios_reset_token ON public.usuarios USING btree (reset_token);


--
-- Name: ix_usuarios_rol_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_usuarios_rol_id ON public.usuarios USING btree (rol_id);


--
-- Name: ix_usuarios_sync_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_usuarios_sync_id ON public.usuarios USING btree (sync_id);


--
-- Name: ix_usuarios_username; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_usuarios_username ON public.usuarios USING btree (username);


--
-- Name: alimentos_preparados_componentes alimentos_preparados_componentes_alimento_preparado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alimentos_preparados_componentes
    ADD CONSTRAINT alimentos_preparados_componentes_alimento_preparado_id_fkey FOREIGN KEY (alimento_preparado_id) REFERENCES public.alimentos_preparados(id);


--
-- Name: alimentos_preparados_componentes alimentos_preparados_componentes_donacion_materia_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alimentos_preparados_componentes
    ADD CONSTRAINT alimentos_preparados_componentes_donacion_materia_id_fkey FOREIGN KEY (donacion_materia_id) REFERENCES public.donaciones(id);


--
-- Name: asistencia_servidores asistencia_servidores_id_servidor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asistencia_servidores
    ADD CONSTRAINT asistencia_servidores_id_servidor_fkey FOREIGN KEY (id_persona) REFERENCES public.servidores(id);


--
-- Name: aulas aulas_id_salon_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aulas
    ADD CONSTRAINT aulas_id_salon_fkey FOREIGN KEY (id_salon) REFERENCES public.salones(id);


--
-- Name: auxiliares auxiliares_id_capitan_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auxiliares
    ADD CONSTRAINT auxiliares_id_capitan_fkey FOREIGN KEY (id_capitan) REFERENCES public.capitanes(id);


--
-- Name: capitanes capitanes_id_coordinador_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.capitanes
    ADD CONSTRAINT capitanes_id_coordinador_fkey FOREIGN KEY (id_coordinador) REFERENCES public.coordinadores(id);


--
-- Name: colaboradores colaboradores_id_capitan_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.colaboradores
    ADD CONSTRAINT colaboradores_id_capitan_fkey FOREIGN KEY (id_capitan) REFERENCES public.capitanes(id);


--
-- Name: coordinadores coordinadores_id_area_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.coordinadores
    ADD CONSTRAINT coordinadores_id_area_fkey FOREIGN KEY (id_area) REFERENCES public.areas(id);


--
-- Name: coordinadores coordinadores_id_lider_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.coordinadores
    ADD CONSTRAINT coordinadores_id_lider_fkey FOREIGN KEY (id_lider) REFERENCES public.lideres(id);


--
-- Name: distribuciones distribuciones_alimento_preparado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.distribuciones
    ADD CONSTRAINT distribuciones_alimento_preparado_id_fkey FOREIGN KEY (alimento_preparado_id) REFERENCES public.alimentos_preparados(id);


--
-- Name: distribuciones distribuciones_area_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.distribuciones
    ADD CONSTRAINT distribuciones_area_id_fkey FOREIGN KEY (area_id) REFERENCES public.areas(id);


--
-- Name: distribuciones distribuciones_donacion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.distribuciones
    ADD CONSTRAINT distribuciones_donacion_id_fkey FOREIGN KEY (donacion_id) REFERENCES public.donaciones(id);


--
-- Name: distribuciones distribuciones_recepcion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.distribuciones
    ADD CONSTRAINT distribuciones_recepcion_id_fkey FOREIGN KEY (recepcion_id) REFERENCES public.recepciones(id);


--
-- Name: distribuciones distribuciones_salon_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.distribuciones
    ADD CONSTRAINT distribuciones_salon_id_fkey FOREIGN KEY (salon_id) REFERENCES public.salones(id);


--
-- Name: docentes docentes_id_capitan_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.docentes
    ADD CONSTRAINT docentes_id_capitan_fkey FOREIGN KEY (id_capitan) REFERENCES public.capitanes(id);


--
-- Name: aulas fk_aulas_id_auxiliar_auxiliares; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aulas
    ADD CONSTRAINT fk_aulas_id_auxiliar_auxiliares FOREIGN KEY (id_auxiliar) REFERENCES public.auxiliares(id);


--
-- Name: aulas fk_aulas_id_maestra_docentes; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aulas
    ADD CONSTRAINT fk_aulas_id_maestra_docentes FOREIGN KEY (id_maestra) REFERENCES public.docentes(id);


--
-- Name: salones fk_salones_id_area_areas; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salones
    ADD CONSTRAINT fk_salones_id_area_areas FOREIGN KEY (id_area) REFERENCES public.areas(id);


--
-- Name: lideres lideres_id_pastor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lideres
    ADD CONSTRAINT lideres_id_pastor_fkey FOREIGN KEY (id_pastor) REFERENCES public.pastores(id);


--
-- Name: logisticas logisticas_id_capitan_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.logisticas
    ADD CONSTRAINT logisticas_id_capitan_fkey FOREIGN KEY (id_capitan) REFERENCES public.servidores(id);


--
-- Name: role_permissions role_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(id) ON DELETE CASCADE;


--
-- Name: role_permissions role_permissions_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE CASCADE;


--
-- Name: servidores servidores_id_capitan_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.servidores
    ADD CONSTRAINT servidores_id_capitan_fkey FOREIGN KEY (id_capitan) REFERENCES public.capitanes(id);


--
-- Name: usuarios usuarios_rol_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_rol_id_fkey FOREIGN KEY (rol_id) REFERENCES public.roles(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: -
--

GRANT ALL ON SCHEMA public TO postgres;


--
-- PostgreSQL database dump complete
--

\unrestrict hWn8X2m287poF0rDj2vZr8au6DhJ2Kb9X2mnq9iln6zqCrVIDgcJ80dZ6IfjeFg

