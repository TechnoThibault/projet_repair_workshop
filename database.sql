-- clients  customers	Informations relatives aux clients
-- appareils devices	Informations sur les appareils déposés
-- techniciens technicians	Informations sur les techniciens
-- reparations repairs	Fiches de réparation
-- pieces parts	Catalogue des pièces détachées
-- pieces_reparation repair_parts	Pièces utilisées lors des réparations
-- Delete existing tables if needed
DROP TABLE IF EXISTS customers,
devices,
technicians,
repairs,
repair_comments,
parts,
repair_parts;

-- Create enum for repair status
DROP TYPE if EXISTS repair_status;

CREATE TYPE repair_status AS ENUM(
    'pending',
    'in_progress',
    'waiting_for_parts',
    'completed',
    'cancelled'
);

-- Create trigger to change latest update of a row
CREATE OR REPLACE FUNCTION update_updated_at () returns trigger AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language plpgsql;

-- Tables creation
CREATE TABLE customers (
    id serial,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    email VARCHAR(320) NOT NULL,
    address VARCHAR(200) NOT NULL,
    birth_date date NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    CONSTRAINT customers_pk PRIMARY KEY (id),
    CONSTRAINT customers_uk_phone_number UNIQUE (phone_number),
    CONSTRAINT customers_uk_email UNIQUE (email),
    CONSTRAINT customers_ck_first_name_length CHECK (CHAR_LENGTH(first_name) > 0),
    CONSTRAINT customers_ck_last_name_length CHECK (CHAR_LENGTH(last_name) > 0),
    CONSTRAINT customers_ck_email_valid_format CHECK (email ~* '^[A-Z0-9._+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$'),
    CONSTRAINT customers_ck_birth_date_before_today CHECK (birth_date < current_date)
);

CREATE TABLE devices (
    id serial,
    customer_id INT NOT NULL,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    serial_number VARCHAR(20) NOT NULL, -- Serial numbers can start with zeros
    device_type VARCHAR(30) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    CONSTRAINT devices_pk PRIMARY KEY (id),
    CONSTRAINT devices_fk_devices_subscriptions FOREIGN key (customer_id) REFERENCES customers (id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT devices_uk_serial_number UNIQUE (serial_number),
    CONSTRAINT devices_ck_brand_length CHECK (CHAR_LENGTH(brand) > 0),
    CONSTRAINT devices_ck_model_length CHECK (CHAR_LENGTH(model) > 0),
    CONSTRAINT devices_ck_serial_number CHECK (CHAR_LENGTH(serial_number) > 0),
    CONSTRAINT devices_ck_device_type CHECK (CHAR_LENGTH(device_type) > 0)
);

CREATE TABLE technicians (
    id serial,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    email VARCHAR(320) NOT NULL,
    address VARCHAR(200) NOT NULL,
    birth_date date NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    CONSTRAINT technicians_pk PRIMARY KEY (id),
    CONSTRAINT technicians_uk_phone_number UNIQUE (phone_number),
    CONSTRAINT technicians_uk_email UNIQUE (email),
    CONSTRAINT technicians_ck_first_name_length CHECK (CHAR_LENGTH(first_name) > 0),
    CONSTRAINT technicians_ck_last_name_length CHECK (CHAR_LENGTH(last_name) > 0),
    CONSTRAINT technicians_ck_email_valid_format CHECK (email ~* '^[A-Z0-9._+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$'),
    CONSTRAINT technicians_ck_birth_date_before_today CHECK (birth_date < current_date)
);

CREATE TABLE repairs (
    id serial,
    device_id INT NOT NULL,
    technician_id INT,
    description TEXT NOT NULL,
    status repair_status NOT NULL DEFAULT 'pending',
    labor_cost NUMERIC(7, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    updated_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    CONSTRAINT repairs_pk PRIMARY KEY (id),
    CONSTRAINT repairs_fk_repairs_devices FOREIGN key (device_id) REFERENCES devices (id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT repairs_fk_repairs_technicians FOREIGN key (technician_id) REFERENCES technicians (id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT repairs_ck_description_length CHECK (CHAR_LENGTH(description) > 0),
    CONSTRAINT repairs_ck_labor_cost_not_negative CHECK (labor_cost >= 0.00)
);

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON repairs FOR EACH ROW
EXECUTE FUNCTION update_updated_at ();

CREATE TABLE repair_comments (
    id serial,
    repair_id INT NOT NULL,
    technician_id INT,
    comment TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    updated_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    CONSTRAINT repair_comments_pk PRIMARY KEY (id),
    CONSTRAINT repair_comments_fk_repair_comments_repairs FOREIGN key (repair_id) REFERENCES repairs (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT repair_comments_fk_repair_comments_technicians FOREIGN key (technician_id) REFERENCES technicians (id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT repair_comments_ck_comment_length CHECK (CHAR_LENGTH(comment) > 0)
);

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON repair_comments FOR EACH ROW
EXECUTE FUNCTION update_updated_at ();

CREATE TABLE parts (
    id serial,
    name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    unit_price NUMERIC(7, 2) NOT NULL DEFAULT 0.00,
    stock_quantity INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    updated_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    CONSTRAINT parts_pk PRIMARY KEY (id),
    CONSTRAINT parts_ck_name_length CHECK (CHAR_LENGTH(name) > 0),
    CONSTRAINT parts_ck_description_length CHECK (CHAR_LENGTH(description) > 0),
    CONSTRAINT parts_ck_unit_price_not_negative CHECK (unit_price >= 0.00),
    CONSTRAINT parts_ck_stock_quantity_not_negative CHECK (stock_quantity >= 0)
);

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON parts FOR EACH ROW
EXECUTE FUNCTION update_updated_at ();

CREATE TABLE repair_parts (
    id serial,
    repair_id INT NOT NULL,
    part_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price NUMERIC(7, 2) NOT NULL DEFAULT 0.00,
    CONSTRAINT repair_parts_pk PRIMARY KEY (id),
    CONSTRAINT repair_parts_fk_repair_parts_repairs FOREIGN key (repair_id) REFERENCES repairs (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT repair_parts_fk_repair_parts_parts FOREIGN key (part_id) REFERENCES parts (id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT repair_parts_ck_quantity_positive CHECK (quantity >= 1),
    CONSTRAINT repair_parts_ck_unit_price_not_negative CHECK (unit_price >= 0.00)
);