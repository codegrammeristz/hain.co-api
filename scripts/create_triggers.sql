-- PROCEDURE CREATION

-- -- EXECUTED ALREADY
CREATE OR REPLACE FUNCTION log_add_admin()
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
        CONCAT('Added new admin: ', NEW.admin_full_name),
        3,
        current_timestamp,
        'ADD RECORD'
    );
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

-- -- EXECUTED ALREADY
CREATE OR REPLACE FUNCTION log_add_product()
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
        'ADMIN/STAFF',
        CONCAT('Added new product: ', NEW.product_name, ' with code: ', NEW.product_code),
        3,
        current_timestamp,
        'ADD RECORD'
    );
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

-- -- EXECUTED ALREADY
CREATE OR REPLACE FUNCTION log_add_customer()
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
        'ADMIN/CUSTOMER',
        CONCAT('Added new customer with email: ', NEW.customer_email),
        3,
        current_timestamp,
        'ADD RECORD'
    );
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

-- -- EXECUTED ALREADY
CREATE OR REPLACE FUNCTION log_add_staff()
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
        CONCAT('Added new staff with username: ', NEW.staff_username),
        3,
        current_timestamp,
        'ADD RECORD'
    );
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

-- -- EXECUTED ALREADY
CREATE OR REPLACE FUNCTION log_add_order()
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
        'STAFF/CUSTOMER',
        CONCAT('New Order by: ', NEW.order_customer_email, ' ordering: ', NEW.order_product_code),
        3,
        current_timestamp,
        'ADD RECORD'
    );
    RETURN NEW;
END
$$
LANGUAGE 'plpgsql';

-- TRIGGER CREATION

-- -- EXECUTED ALREADY
CREATE TRIGGER log_new_admin
    AFTER INSERT
    ON hainco_admin
    FOR EACH ROW
    EXECUTE PROCEDURE log_add_admin();

-- -- EXECUTED ALREADY
CREATE TRIGGER log_new_product
    AFTER INSERT
    ON hainco_product
    FOR EACH ROW
    EXECUTE PROCEDURE log_add_product();

-- -- EXECUTED ALREADY
CREATE TRIGGER log_new_customer
    AFTER INSERT
    ON hainco_customer
    FOR EACH ROW
    EXECUTE PROCEDURE log_add_customer();

-- -- EXECUTED ALREADY
CREATE TRIGGER log_new_staff
    AFTER INSERT
    ON hainco_staff
    FOR EACH ROW
    EXECUTE PROCEDURE log_add_staff();

-- -- EXECUTED ALREADY
CREATE TRIGGER log_new_order
    AFTER INSERT
    ON hainco_order
    FOR EACH ROW
    EXECUTE PROCEDURE log_add_order();