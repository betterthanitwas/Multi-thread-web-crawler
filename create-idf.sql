USE WEBCRAWL;

DROP TABLE IF EXISTS WORD_IDF;

CREATE TABLE WORD_IDF (
PRIMARY KEY (WORD_ID),
FOREIGN KEY (WORD_ID) REFERENCES WORD(WORD_ID))
AS
SELECT WORD_ID, LOG(
		(SELECT COUNT(*) FROM SITE)
			/ (SELECT COUNT(*) FROM EXCERPT WHERE EXCERPT.WORD_ID = WORD.WORD_ID)
			) AS WORD_IDF
		FROM WORD;
