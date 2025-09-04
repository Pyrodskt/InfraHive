Table PLATFORM.ENTITY {
    id integer [pk, unique, not null, increment]
    name varchar [not null]
    parent_id integer [null]
    comment text [null]
    level integer [not null]
    localisation_id integer [null]
    createdAt datetime [not null]
    updatedAt datetime [not null]

    indexes {
        (name, parent_id) [unique]
    }
}
Table GENERAL.LOCALISATION {
    id integer [pk, unique, not null, increment]
    name varchar [unique, not null]
    parent_id integer [null]
    comment text [null]
    level integer [not null]
    address varchar [null]
    postcode varchar [null]
    town varchar [null]
    state varchar [null]
    country varchar [null]
    createdAt datetime [not null]
    updatedAt datetime [not null]
}

Table INVENTORY.COMPUTER {
    id integer [pk, unique, not null, increment]
    name varchar [unique, not null]
    hostname varchar [not null]
    computer_type_id integer [not null]
    operating_system_id integer [not null]
    entity_id integer [null]
    createdAt datetime [not null]
    updatedAt datetime [not null]
}

Table INVENTORY.COMPUTER_TYPE {
    id integer [pk, unique, not null, increment]
    name varchar [unique, not null]
    description text [null]
    createdAt datetime [not null]
    updatedAt datetime [not null]
}

Table INVENTORY.OPERATING_SYSTEM {
    id integer [pk, unique, not null, increment]
    family varchar [not null]
    product varchar [null]
    version varchar [null]
    createdAt datetime [not null]
    updatedAt datetime [not null]
}

Ref: GENERAL.LOCALISATION.parent_id > GENERAL.LOCALISATION.id [delete: set null, update: no action]

Ref: PLATFORM.ENTITY.parent_id > PLATFORM.ENTITY.id [delete: set null, update: no action]
Ref: PLATFORM.ENTITY.localisation_id > GENERAL.LOCALISATION.id [delete: set null, update: no action]

Ref: INVENTORY.OPERATING_SYSTEM.id > INVENTORY.COMPUTER.operating_system.id [delete: set null, update: no action]
Ref: PLATFORM.ENTITY.id > INVENTORY.COMPUTER.entity_id [delete: set null, update: no action]