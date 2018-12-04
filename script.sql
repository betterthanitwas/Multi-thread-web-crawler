# create logical group of DB objects in DB (pg 241), also change char set
CREATE SCHEMA WEBCRAWL CHARACTER SET UTF8MB4 COLLATE UTF8MB4_BIN;
SET AUTOCOMMIT = 0;
SET GLOBAL TRANSACTION ISOLATION LEVEL SERIALIZABLE;
# tell mysql which db to use
USE WEBCRAWL;

CREATE TABLE SITE (
SITE_ID		BIGINT UNSIGNED		NOT NULL	UNIQUE	AUTO_INCREMENT,
SITE_URL	VARCHAR(255)		UNIQUE,	# make sure the URL is unique
SITE_TITLE	VARCHAR(100),
PRIMARY KEY (SITE_ID))
ENGINE = INNODB; # produces transaction - safe tables (pg. 247)

CREATE TABLE WORD (
WORD_ID		BIGINT UNSIGNED		NOT NULL	UNIQUE	AUTO_INCREMENT,
WORD_WORD	VARCHAR(45)			UNIQUE,
PRIMARY KEY (WORD_ID))
ENGINE = INNODB;

CREATE TABLE EXCERPT (
EXCERPT_ID				BIGINT UNSIGNED		UNIQUE	AUTO_INCREMENT, #test
SITE_ID					BIGINT UNSIGNED,
WORD_ID					BIGINT UNSIGNED, # try adding index here to see if its faster on return...
EXCERPT_WRD_AMT_SITE	INT,
EXCERPT_PHRASE			VARCHAR(150),
EXCERPT_WORD			VARCHAR(45),	#test
PRIMARY KEY (EXCERPT_ID),
FOREIGN KEY	(SITE_ID) REFERENCES SITE(SITE_ID),
FOREIGN KEY (WORD_ID) REFERENCES WORD(WORD_ID))
ENGINE = INNODB;


# store URL
delimiter |

CREATE PROCEDURE PRC_STORE_URL_TTL (IN URL VARCHAR(255), IN TTL VARCHAR(100), OUT UID BIGINT UNSIGNED)
    BEGIN 
        START TRANSACTION;
		INSERT INTO SITE (SITE_URL, SITE_TITLE)
			VALUES(URL, TTL);
        SET UID = LAST_INSERT_ID();
        COMMIT;
	END |

delimiter ;


# store word
delimiter |

CREATE PROCEDURE PRC_STORE_WORD (IN WORD_S VARCHAR(45), IN UID BIGINT UNSIGNED, IN WCOUNT INT, IN PHRASE VARCHAR(150))
    BEGIN
		DECLARE WID BIGINT UNSIGNED;
		DECLARE W_EXISTS INT;  
		SET W_EXISTS = 0;  
        
        START TRANSACTION;
		SELECT COUNT(*) INTO @W_EXISTS FROM WORD WHERE WORD_WORD = WORD_S;   
		
		IF (@W_EXISTS > 0) THEN 
			SELECT WORD_ID INTO @WID FROM WORD WHERE WORD_WORD = WORD_S;  
		ELSE 
			INSERT INTO WORD (WORD_WORD) VALUES(WORD_S);  
			SET @WID = LAST_INSERT_ID();  
		END IF;
        INSERT INTO EXCERPT (SITE_ID, WORD_ID, EXCERPT_WRD_AMT_SITE, EXCERPT_PHRASE, EXCERPT_WORD) 
			VALUES(UID, @WID, WCOUNT, PHRASE, WORD_S);
		COMMIT;
	END |
    
delimiter ;


# return url title and excerpt of a word
delimiter |

CREATE PROCEDURE PRC_FIND_WRD (IN WORD_W VARCHAR(45))
    BEGIN 
		SELECT 	SITE_URL, SITE_TITLE, EXCERPT_PHRASE
        FROM	WORD JOIN EXCERPT USING (WORD_ID) JOIN SITE USING (SITE_ID)
        WHERE	WORD_W = WORD_WORD;
	END |

delimiter ;