-- PROCEDURE CREATION

CREATE OR REPLACE FUNCTION log_update_admin()
    RETURNS trigger AS
$$
BEGIN
    INSERT INTO hainco_transaction(
        transaction_agent,
        transaction_description,
        transaction_type,
        transaction_date,
        transaction_state
    ) VALUES (
        'ADMIN',
        CONCAT('Updated admin information of: ', NEW.admin_full_name),
        3,
        current_timestamp,
        'UPDATE RECORD'
    );
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';


CREATE OR REPLACE FUNCTION log_update_staff()
    RETURNS trigger AS
$$
BEGIN
    INSERT INTO hainco_transaction(
        transaction_agent,
        transaction_description,
        transaction_type,
        transaction_date,
        transaction_state
    ) VALUES (
        'ADMIN',
        CONCAT('Updated staff information of: ', NEW.staff_username),
        3,
        current_timestamp,
        'UPDATE RECORD'
    );
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';


CREATE OR REPLACE FUNCTION log_update_product()
    RETURNS trigger AS
$$
BEGIN
    INSERT INTO hainco_transaction(
        transaction_agent,
        transaction_description,
        transaction_type,
        transaction_date,
        transaction_state
    ) VALUES (
        'ADMIN',
        CONCAT('Updated product information of: ', NEW.product_code),
        3,
        current_timestamp,
        'UPDATE RECORD'
    );
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION log_update_customer()
    RETURNS trigger AS
$$
BEGIN
    INSERT INTO hainco_transaction(
        transaction_agent,
        transaction_description,
        transaction_type,
        transaction_date,
        transaction_state
    ) VALUES (
        'ADMIN',
        CONCAT('Updated customer information of: ', NEW.customer_email),
        3,
        current_timestamp,
        'UPDATE RECORD'
    );
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION log_update_order()
    RETURNS trigger AS
$$
BEGIN
    INSERT INTO hainco_transaction(
        transaction_agent,
        transaction_description,
        transaction_type,
        transaction_date,
        transaction_state
    ) VALUES (
        'STAFF',
        CONCAT('Updated Order by: ', NEW.order_customer_email, ' ordering: ', NEW.order_product_code, ' from status code: ', OLD.order_status, ' to status code: ', NEW.order_status),
        3,
        current_timestamp,
        'UPDATE RECORD'
    );
    RETURN NEW;
END
$$
LANGUAGE 'plpgsql';

-- TRIGGER CREATION

CREATE TRIGGER log_updated_admin
    AFTER UPDATE
    ON hainco_admin
    FOR EACH ROW
    EXECUTE PROCEDURE log_update_admin();

CREATE TRIGGER log_updated_staff
    AFTER UPDATE
    ON hainco_staff
    FOR EACH ROW
    EXECUTE PROCEDURE log_update_staff();

CREATE TRIGGER log_updated_order
    AFTER UPDATE
    ON hainco_order
    FOR EACH ROW
    EXECUTE PROCEDURE log_update_order();

CREATE TRIGGER log_updated_customer
    AFTER UPDATE
    ON hainco_customer
    FOR EACH ROW
    EXECUTE PROCEDURE log_update_customer();

CREATE TRIGGER log_updated_product
    AFTER UPDATE
    ON hainco_product
    FOR EACH ROW
    EXECUTE PROCEDURE log_update_product();