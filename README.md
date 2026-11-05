# Project Description

Develop a console-based application that allows a repair workshop to manage its customers, deposited devices, repairs performed, and spare parts used.

## Features

- Register new customers.
- Register devices dropped off by customers.
- Create repair records.
- Assign repairs to technicians.
- Update the status of a repair.
- Add the spare parts used during a repair.
- Automatically calculate the total cost of a repair.
- View completed or pending repairs.

## Database Structure

| Table | Purpose |
|---|---|
| customers | Customer information |
| devices | Information about deposited devices |
| technicians | Technician information |
| repairs | Repair records |
| repair_comments | Comments related to a repair |
| parts | Spare parts catalogue |
| repair_parts | Parts used during repairs |

---

## repairs Table

This table contains general information about each repair.

It represents the repair record created when a customer drops off a device.

### Example

| id | device_id | technician_id | description | status | labor_cost | created_at | updated_at |
|---|---|---|---|---|---|---|---|
| 1 | 3 | 2 | Screen replacement | In Progress | €45 | 05-11-26 00:00:00 | 05-11-26 00:00:00 |
| 2 | 5 | 1 | Battery issue | Completed | €30 | 05-11-26 00:00:00 | 05-11-26 00:00:00 |

- Which device needs to be repaired.
- Which technician is responsible for the repair.
- What problem has been reported.
- The current status of the repair.
- How much the labour costs.

---

## parts Table

This table contains the catalogue of spare parts available in the workshop.

### Example

| id | name | unit_price | stock_quantity | created_at | updated_at |
|---|---|---|---|---|---|
| 1 | 15-inch Computer Screen | 120 | 5 | 05-11-26 00:00:00 | 05-11-26 00:00:00 |
| 2 | Computer Battery | 65 | 10 | 05-11-26 00:00:00 | 05-11-26 00:00:00 |
| 3 | 500 GB SSD Drive | 55 | 8 | 05-11-26 00:00:00 | 05-11-26 00:00:00 |
| 4 | Computer Keyboard | 40 | 3 | 05-11-26 00:00:00 | 05-11-26 00:00:00 |

- Keep track of available spare parts.
- Know the price of each part.
- Check the quantities available in stock.
- Update spare part information.

---

## repair_parts Table

It is used to create a link between repairs and the spare parts used.

The `repair_tables` table records which parts were used for each repair and in what quantities.

### Example

| id | repair_id | part_id | quantity | unit_price |
|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 120 |
| 2 | 1 | 4 | 1 | 40 |
| 3 | 2 | 2 | 1 | 65 |
| 4 | 2 | 3 | 1 | 55 |

- Repair 1: one screen and one keyboard were used.
- Repair 2: one battery and one SSD drive were used.

Note: It also keeps the unit price at the moment of adding it to the repair in case the price of the part changes after adding it.

---

## Example of a Repair Cost Calculation

Let's take repair number 1:

| Item | Price |
|---|---:|
| Labour | €45 |
| Screen | €120 |
| Keyboard | €40 |
| **Total** | **€205** |

The total cost is calculated automatically by adding:

- The labour cost.
- The price of each spare part used, multiplied by its quantity.

**Formula:**

```text
Total Cost = Labour Cost + Sum(Part Prices × Quantities Used)

Total Cost = 45 + (120 × 1) + (40 × 1)
Total Cost = €205
```