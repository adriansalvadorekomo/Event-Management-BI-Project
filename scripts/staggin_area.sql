CREATE TABLE stg_beneficiary (
    id_beneficiary VARCHAR(50),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50)
);
CREATE TABLE stg_category (
    id_category VARCHAR(50),
    name VARCHAR(100)
);
CREATE TABLE stg_subcategory (
    id_subcategory VARCHAR(50),
    name VARCHAR(100),
    id_category VARCHAR(50)
);
CREATE TABLE stg_provider (
    id_provider VARCHAR(50),
    name VARCHAR(255),
    service_type VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    city VARCHAR(100)
);

CREATE TABLE stg_service (
    id_service VARCHAR(50),
    title VARCHAR(255),
    price VARCHAR(50),
    description TEXT,
    id_provider VARCHAR(50),
    id_subcategory VARCHAR(50)
);


CREATE TABLE stg_event (
    id_event VARCHAR(50),
    title VARCHAR(255),
    event_date VARCHAR(50),
    budget VARCHAR(50),
    type VARCHAR(100),
    id_beneficiary VARCHAR(50)
);

CREATE TABLE stg_reservation (
    id_reservation VARCHAR(50),
    id_service VARCHAR(50),
    id_event VARCHAR(50),
    reservation_date VARCHAR(50),
    status VARCHAR(50),
    final_price VARCHAR(50)
);

CREATE TABLE stg_evaluation (
    id_evaluation VARCHAR(50),
    id_reservation VARCHAR(50),
    rating VARCHAR(10),
    comment TEXT
);

CREATE TABLE stg_complaint (
    id_complaint VARCHAR(50),
    subject VARCHAR(100),
    description TEXT,
    status VARCHAR(50),
    id_beneficiary VARCHAR(50),
    id_provider VARCHAR(50)
);

CREATE TABLE stg_marketing_spend (
    id VARCHAR(50),
    month VARCHAR(20),
    marketing_spend VARCHAR(50),
    new_beneficiaries VARCHAR(50)
);

CREATE TABLE stg_visitors (
    id VARCHAR(50),
    date VARCHAR(50),
    visitors VARCHAR(50),
    reservations VARCHAR(50)
);
