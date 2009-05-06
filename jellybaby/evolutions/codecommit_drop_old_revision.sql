ALTER TABLE jellybaby_codecommit DROP COLUMN revision;
ALTER TABLE jellybaby_codecommit RENAME COLUMN new_revision TO revision;
ALTER TABLE jellybaby_codecommit ALTER COLUMN revision DROP DEFAULT;