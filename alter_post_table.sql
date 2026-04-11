ALTER TABLE post
    ADD COLUMN IF NOT EXISTS content           TEXT,
    ADD COLUMN IF NOT EXISTS content_anonymise TEXT,
    ADD COLUMN IF NOT EXISTS topic             VARCHAR(50),
    ADD COLUMN IF NOT EXISTS hashtags          TEXT,
    ADD COLUMN IF NOT EXISTS language          VARCHAR(5)  DEFAULT 'fr',
    ADD COLUMN IF NOT EXISTS status            VARCHAR(20) DEFAULT 'brouillon'
                                               CHECK (status IN ('brouillon', 'en_validation', 'publie', 'archive')),
    ADD COLUMN IF NOT EXISTS published_at      TIMESTAMP,
    ADD COLUMN IF NOT EXISTS updated_at        TIMESTAMP   DEFAULT NOW(),
    ADD COLUMN IF NOT EXISTS score_useful      INTEGER     DEFAULT 0,
    ADD COLUMN IF NOT EXISTS score_very_useful INTEGER     DEFAULT 0,
    ADD COLUMN IF NOT EXISTS completude        BOOLEAN     DEFAULT FALSE;

CREATE INDEX IF NOT EXISTS idx_post_content  ON post USING gin(to_tsvector('french', coalesce(content, '')));
CREATE INDEX IF NOT EXISTS idx_post_topic    ON post(topic);
CREATE INDEX IF NOT EXISTS idx_post_status   ON post(status);
CREATE INDEX IF NOT EXISTS idx_post_language ON post(language);

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_post_updated_at
BEFORE UPDATE ON post
FOR EACH ROW EXECUTE FUNCTION update_updated_at();
