INSERT INTO
    persons (
        id,
        first_name,
        last_name,
        phone_number,
        email,
        address,
        birth_date
    )
VALUES
    (
        1,
        'Thomas',
        'Martin',
        '+32470100001',
        'thomas.martin@example.com',
        '12 Rue Royale, Brussels',
        '1990-04-15'
    ),
    (
        2,
        'Emma',
        'Dubois',
        '+32470100002',
        'emma.dubois@example.com',
        '25 Avenue Louise, Brussels',
        '1995-08-21'
    ),
    (
        3,
        'Lucas',
        'Bernard',
        '+32470100003',
        'lucas.bernard@example.com',
        '8 Rue Neuve, Brussels',
        '1988-02-10'
    ),
    (
        4,
        'Sarah',
        'Petit',
        '+32470100004',
        'sarah.petit@example.com',
        '14 Rue du Midi, Brussels',
        '1992-11-05'
    ),
    (
        5,
        'Nathan',
        'Robert',
        '+32470100005',
        'nathan.robert@example.com',
        '30 Avenue de Tervueren, Brussels',
        '1985-06-18'
    ),
    (
        6,
        'Julie',
        'Richard',
        '+32470100006',
        'julie.richard@example.com',
        '5 Place Flagey, Brussels',
        '1998-01-25'
    ),
    (
        7,
        'Gabriel',
        'Durand',
        '+32470100007',
        'gabriel.durand@example.com',
        '19 Rue Belliard, Brussels',
        '1991-09-12'
    ),
    (
        8,
        'Alice',
        'Moreau',
        '+32470100008',
        'alice.moreau@example.com',
        '42 Rue de la Loi, Brussels',
        '1996-03-30'
    ),
    (
        9,
        'Louis',
        'Simon',
        '+32470100009',
        'louis.simon@example.com',
        '7 Boulevard Anspach, Brussels',
        '1987-12-08'
    ),
    (
        10,
        'Chloe',
        'Laurent',
        '+32470100010',
        'chloe.laurent@example.com',
        '16 Rue des Colonies, Brussels',
        '1993-07-14'
    ),
    (
        11,
        'Marc',
        'Lefevre',
        '+32470200001',
        'marc.lefevre@repairshop.be',
        '10 Rue de la Paix, Brussels',
        '1980-05-20'
    ),
    (
        12,
        'Sophie',
        'Garcia',
        '+32470200002',
        'sophie.garcia@repairshop.be',
        '20 Avenue Louise, Brussels',
        '1987-10-11'
    ),
    (
        13,
        'Antoine',
        'Roux',
        '+32470200003',
        'antoine.roux@repairshop.be',
        '15 Rue Royale, Brussels',
        '1983-03-17'
    ),
    (
        14,
        'Laura',
        'Vincent',
        '+32470200004',
        'laura.vincent@repairshop.be',
        '9 Place Jourdan, Brussels',
        '1990-12-02'
    ),
    (
        15,
        'Pierre',
        'Michel',
        '+32470200005',
        'pierre.michel@repairshop.be',
        '3 Rue de Namur, Brussels',
        '1985-07-22'
    );

INSERT INTO
    customers (id, person_id)
VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10);

INSERT INTO
    technicians (id, person_id)
VALUES
    (1, 11),
    (2, 12),
    (3, 13),
    (4, 14),
    (5, 15);

INSERT INTO
    devices (
        id,
        customer_id,
        brand,
        model,
        serial_number,
        device_type
    )
VALUES
    (
        1,
        1,
        'Apple',
        'iPhone 14',
        'IPH14-00001',
        'Smartphone'
    ),
    (
        2,
        1,
        'Apple',
        'MacBook Pro 14',
        'MBP14-00001',
        'Laptop'
    ),
    (
        3,
        2,
        'Samsung',
        'Galaxy S23',
        'SGS23-00002',
        'Smartphone'
    ),
    (
        4,
        3,
        'Apple',
        'iPad Air 5',
        'IPAD-00003',
        'Tablet'
    ),
    (5, 4, 'Dell', 'XPS 15', 'XPS15-00004', 'Laptop'),
    (
        6,
        5,
        'Google',
        'Pixel 8',
        'PIX8-00005',
        'Smartphone'
    ),
    (
        7,
        6,
        'Samsung',
        'Galaxy Tab S8',
        'TAB8-00006',
        'Tablet'
    ),
    (
        8,
        7,
        'Lenovo',
        'ThinkPad T14',
        'T14-00007',
        'Laptop'
    ),
    (
        9,
        8,
        'Apple',
        'iPhone 13',
        'IPH13-00008',
        'Smartphone'
    ),
    (
        10,
        9,
        'HP',
        'Pavilion 15',
        'HP15-00009',
        'Laptop'
    ),
    (
        11,
        10,
        'Apple',
        'iPhone 15 Pro',
        'IPH15-00010',
        'Smartphone'
    ),
    (
        12,
        3,
        'Sony',
        'WH-1000XM5',
        'SONY-00011',
        'Headphones'
    );

INSERT INTO
    repairs (
        id,
        device_id,
        technician_id,
        description,
        status,
        labor_cost,
        created_at,
        updated_at
    )
VALUES
    (
        1,
        1,
        1,
        'Screen replacement due to accidental fall.',
        'completed',
        80.00,
        '2026-10-01 09:00',
        '2026-10-03 15:00'
    ),
    (
        2,
        2,
        2,
        'Battery drains very quickly. Battery diagnosis and replacement required.',
        'completed',
        65.00,
        '2026-10-02 10:00',
        '2026-10-05 14:00'
    ),
    (
        3,
        3,
        1,
        'Charging port is damaged and device does not charge properly.',
        'in_progress',
        45.00,
        '2026-10-15 11:00',
        '2026-10-20 13:00'
    ),
    (
        4,
        4,
        3,
        'Tablet screen is cracked and touch functionality is partially unavailable.',
        'waiting_for_parts',
        90.00,
        '2026-10-18 09:30',
        '2026-10-22 16:00'
    ),
    (
        5,
        5,
        2,
        'Laptop overheats and shuts down unexpectedly.',
        'in_progress',
        55.00,
        '2026-10-20 14:00',
        '2026-10-23 10:00'
    ),
    (
        6,
        6,
        NULL,
        'Phone does not turn on. Requires initial diagnosis.',
        'pending',
        0.00,
        '2026-10-25 09:00',
        '2026-10-25 09:00'
    ),
    (
        7,
        7,
        4,
        'Tablet battery replacement.',
        'completed',
        50.00,
        '2026-10-10 10:00',
        '2026-10-12 17:00'
    ),
    (
        8,
        8,
        5,
        'Keyboard keys are not responding.',
        'waiting_for_parts',
        40.00,
        '2026-10-21 11:00',
        '2026-10-24 12:00'
    ),
    (
        9,
        9,
        1,
        'Camera glass is broken and needs replacement.',
        'completed',
        35.00,
        '2026-10-05 13:00',
        '2026-10-07 16:00'
    ),
    (
        10,
        10,
        NULL,
        'Laptop is slow and requires hardware diagnostics.',
        'pending',
        0.00,
        '2026-10-26 10:00',
        '2026-10-26 10:00'
    ),
    (
        11,
        11,
        3,
        'Back glass is damaged. Replacement requested.',
        'cancelled',
        0.00,
        '2026-10-12 09:00',
        '2026-10-13 11:00'
    ),
    (
        12,
        1,
        2,
        'Speaker produces distorted sound during calls.',
        'completed',
        30.00,
        '2026-10-28 09:00',
        '2026-10-30 15:00'
    ),
    (
        13,
        12,
        4,
        'Headphones have intermittent Bluetooth connectivity.',
        'in_progress',
        25.00,
        '2026-11-01 10:00',
        '2026-11-02 14:00'
    ),
    (
        14,
        3,
        5,
        'Screen occasionally flickers. Requires display diagnostics.',
        'pending',
        0.00,
        '2026-11-02 11:00',
        '2026-11-02 11:00'
    ),
    (
        15,
        5,
        2,
        'Laptop fan makes unusual noises.',
        'waiting_for_parts',
        35.00,
        '2026-11-03 09:00',
        '2026-11-04 16:00'
    );

INSERT INTO
    repair_comments (id, repair_id, technician_id, comment, created_at)
VALUES
    (
        1,
        1,
        1,
        'Initial inspection completed. Screen damage confirmed.',
        '2026-10-01 10:00'
    ),
    (
        2,
        1,
        1,
        'Replacement screen installed successfully.',
        '2026-10-03 14:00'
    ),
    (
        3,
        2,
        2,
        'Battery health measured at 58%. Replacement recommended.',
        '2026-10-02 11:00'
    ),
    (
        4,
        2,
        2,
        'New battery installed and tested.',
        '2026-10-05 13:00'
    ),
    (
        5,
        3,
        1,
        'Charging port inspection completed.',
        '2026-10-15 12:00'
    ),
    (
        6,
        3,
        1,
        'Replacement port ordered.',
        '2026-10-20 13:00'
    ),
    (
        7,
        4,
        3,
        'Screen replacement required. Part currently unavailable.',
        '2026-10-18 11:00'
    ),
    (
        8,
        4,
        3,
        'Waiting for delivery of replacement display.',
        '2026-10-22 16:00'
    ),
    (
        9,
        5,
        2,
        'Dust accumulation found inside cooling system.',
        '2026-10-20 15:00'
    ),
    (
        10,
        5,
        2,
        'Thermal paste replaced. Additional testing ongoing.',
        '2026-10-23 10:00'
    ),
    (
        11,
        6,
        NULL,
        'Device received. Awaiting technician assignment.',
        '2026-10-25 09:00'
    ),
    (
        12,
        7,
        4,
        'Battery replacement completed.',
        '2026-10-12 16:00'
    ),
    (
        13,
        8,
        5,
        'Keyboard replacement required.',
        '2026-10-21 14:00'
    ),
    (
        14,
        8,
        5,
        'New keyboard ordered.',
        '2026-10-24 12:00'
    ),
    (
        15,
        9,
        1,
        'Camera glass replaced and camera tested successfully.',
        '2026-10-07 15:00'
    ),
    (
        16,
        10,
        NULL,
        'Device received for diagnostic testing.',
        '2026-10-26 10:00'
    ),
    (
        17,
        11,
        3,
        'Customer requested cancellation before repair started.',
        '2026-10-13 11:00'
    ),
    (
        18,
        12,
        2,
        'Speaker module replaced and audio tested.',
        '2026-10-30 14:00'
    ),
    (
        19,
        13,
        4,
        'Bluetooth module under investigation.',
        '2026-11-02 14:00'
    ),
    (
        20,
        15,
        2,
        'Replacement cooling fan ordered.',
        '2026-11-04 16:00'
    );

INSERT INTO
    parts (id, name, description, unit_price, stock_quantity)
VALUES
    (
        1,
        'iPhone 14 Screen',
        'Original quality replacement display for iPhone 14.',
        120.00,
        8
    ),
    (
        2,
        'MacBook Battery',
        'Replacement battery compatible with MacBook Pro 14.',
        150.00,
        5
    ),
    (
        3,
        'Samsung Charging Port',
        'Charging connector replacement for Galaxy S23.',
        25.00,
        12
    ),
    (
        4,
        'iPad Air Display',
        'Replacement display for iPad Air 5.',
        135.00,
        0
    ),
    (
        5,
        'Laptop Thermal Paste',
        'High-performance thermal compound.',
        8.00,
        30
    ),
    (
        6,
        'Pixel 8 Battery',
        'Replacement battery for Google Pixel 8.',
        45.00,
        4
    ),
    (
        7,
        'Tablet Battery',
        'Replacement battery for Galaxy Tab S8.',
        55.00,
        6
    ),
    (
        8,
        'ThinkPad Keyboard',
        'Replacement keyboard for ThinkPad T14.',
        65.00,
        0
    ),
    (
        9,
        'iPhone 13 Camera Glass',
        'Replacement rear camera glass.',
        12.00,
        15
    ),
    (
        10,
        'Laptop SSD 1TB',
        'NVMe SSD storage upgrade, 1TB.',
        85.00,
        10
    ),
    (
        11,
        'iPhone 15 Pro Back Glass',
        'Replacement rear glass panel.',
        75.00,
        3
    ),
    (
        12,
        'iPhone Speaker Module',
        'Replacement internal speaker module.',
        20.00,
        7
    ),
    (
        13,
        'Bluetooth Module',
        'Bluetooth replacement module for compatible headphones.',
        35.00,
        2
    ),
    (
        14,
        'Laptop Cooling Fan',
        'Replacement cooling fan for Dell XPS 15.',
        40.00,
        0
    ),
    (
        15,
        'Universal Charging Cable',
        'USB-C charging cable for compatible devices.',
        10.00,
        50
    );

INSERT INTO
    repair_parts (id, repair_id, part_id, quantity, unit_price)
VALUES
    (1, 1, 1, 1, 120.00),
    (2, 2, 2, 1, 150.00),
    (3, 3, 3, 1, 25.00),
    (4, 4, 4, 1, 135.00),
    (5, 5, 5, 2, 8.00),
    (6, 7, 7, 1, 55.00),
    (7, 8, 8, 1, 65.00),
    (8, 9, 9, 1, 12.00),
    (9, 10, 10, 1, 85.00),
    (10, 11, 11, 1, 75.00),
    (11, 12, 12, 1, 20.00),
    (12, 13, 13, 1, 35.00),
    (13, 15, 14, 1, 40.00),
    (14, 3, 15, 1, 10.00),
    (15, 5, 10, 1, 85.00),
    (16, 7, 15, 2, 10.00),
    (17, 1, 15, 1, 10.00),
    (18, 12, 15, 1, 10.00);

SELECT
    SETVAL(
        PG_GET_SERIAL_SEQUENCE('persons', 'id'),
        (
            SELECT
                MAX(id)
            FROM
                persons
        )
    );

SELECT
    SETVAL(
        PG_GET_SERIAL_SEQUENCE('customers', 'id'),
        (
            SELECT
                MAX(id)
            FROM
                customers
        )
    );

SELECT
    SETVAL(
        PG_GET_SERIAL_SEQUENCE('technicians', 'id'),
        (
            SELECT
                MAX(id)
            FROM
                technicians
        )
    );

SELECT
    SETVAL(
        PG_GET_SERIAL_SEQUENCE('devices', 'id'),
        (
            SELECT
                MAX(id)
            FROM
                devices
        )
    );

SELECT
    SETVAL(
        PG_GET_SERIAL_SEQUENCE('repairs', 'id'),
        (
            SELECT
                MAX(id)
            FROM
                repairs
        )
    );

SELECT
    SETVAL(
        PG_GET_SERIAL_SEQUENCE('repair_comments', 'id'),
        (
            SELECT
                MAX(id)
            FROM
                repair_comments
        )
    );

SELECT
    SETVAL(
        PG_GET_SERIAL_SEQUENCE('parts', 'id'),
        (
            SELECT
                MAX(id)
            FROM
                parts
        )
    );

SELECT
    SETVAL(
        PG_GET_SERIAL_SEQUENCE('repair_parts', 'id'),
        (
            SELECT
                MAX(id)
            FROM
                repair_parts
        )
    );