GRANT USAGE ON SCHEMA {db.schema.authorisation.name} TO {secrets.api.username};
GRANT SELECT ON ALL TABLES IN SCHEMA {db.schema.authorisation.name} TO {secrets.api.username};
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA {db.schema.authorisation.name} TO {secrets.api.username};

GRANT USAGE ON SCHEMA {db.schema.iot.name} TO {secrets.api.username};
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA {db.schema.iot.name} TO {secrets.api.username};
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA {db.schema.iot.name} TO {secrets.api.username};

GRANT USAGE ON SCHEMA {db.schema.authorisation.name} TO {secrets.authorisation.username};
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA {db.schema.authorisation.name} TO {secrets.authorisation.username};
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA {db.schema.authorisation.name} TO {secrets.authorisation.username};