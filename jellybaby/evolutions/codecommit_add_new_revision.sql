ALTER TABLE jellybaby_codecommit ADD COLUMN new_revision VARCHAR(200) DEFAULT '';
UPDATE jellybaby_codecommit SET new_revision = revision::text;